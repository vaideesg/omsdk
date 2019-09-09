import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import xml.etree.ElementTree as ET
import json
import re
from  datetime import datetime
import zipfile, io, gzip, os, shutil, glob
from datetime import datetime, timedelta
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from flask import Flask, render_template, request, url_for
import threading

def dprint(msg):
    pass

def jprint(msg):
    print(json.dumps(msg, sort_keys=True, indent=4, \
            separators=(',', ': ')))

class EEMI(object):
    action_types = {
                'CANCEL' : 'cancel',
                'CHANGE' : 'change',
                'CHECK' : 'review\s|settings|configuration|ensure\s|enter\s|make sure|view\s',
                'DISABLE' : 'disable\s',
                'WAIT' : 'wait\s',
                'ENABLE' : 'enable\s',
                'CLEAR' : 'clear',
                'CORRECT' : 'correct',
                'CONNECT' : 'connected|disconnect\s|reconnect\s',
                'CONFIGURE' : 'configure|reconfigure\s',
                'CREATE' : 'cannot be created|create\s|recreate\s',
                'DELETE' : 'delete\s',
                'DESTINATION' : 'destination\s',
                'EXISTS' : 'exists',
                'IGNORE' : 'no response|is not required|not be required',
                'LOGS'  : 'check system logs',
                'RETRY' : 'retry|select|change|click',
                'RESTART' : 'restart\s|power\s|reboot|turn on\s',
                'RESET' : 'reset\s|turn off',
                'SOS' : 'contact\s.*(technical support|administrator|service provider|customer service|vendor|technical service)',
                'UPGRADE' : 'latest|upgrade|acquire|update\s|download|reacquire',

                # should be last
                'H&E' : 'reseat|connect\s|check|reinstall|reinsert|close|replace|remove|add\s|adjust',
            }

    def extract_string(self, ent, doprint_attributes):
        tmsg = ""
        comma = ""
        if doprint_attributes:
            for i in ent.attrib:
                tmsg += ent.attrib[i] + comma
                comma = " "
        nchild = 0
        for sub in ent:
            if doprint_attributes:
                for i in sub.attrib:
                    #tmsg += i + "=" + sub.attrib[i] + comma
                    tmsg += sub.attrib[i] + comma
                    comma = " "
            name = re.sub('{[^}]+}', '', sub.tag)
            if sub.text is None:
                if 'NAME' in sub.attrib:
                    tmsg += comma + sub.attrib['SOURCE_PROPERTY'].replace(' ', '_')
            else:
                tmsg += comma + sub.text
            comma = " "
            nchild += 1
        if nchild == 0 and ent.text:
            tmsg += ent.text
        tmsg = re.sub('\s+', ' ', tmsg)
        tmsg = re.sub('^\s+|\s+$', ' ', tmsg)
        return tmsg

    def collect_info(self, ent, collector):
        for i in ent.attrib:
            collector[i] = ent.attrib[i]
        for sub in ent:
            name = re.sub('{[^}]+}', '', sub.tag)
            doprint = name not in ['MESSAGE_COMPONENTS']
            if name in [ "TEST_ARGUMENTS" ]:
                pass
            elif name in [
                "MESSAGE_COMPONENTS",
                "PERCEIVED_SEVERITY",
                "RECOMMENDED_ACTION",
                "CIMSTATUSCODE",
                "ERROR_SOURCE",
                "ERROR_TYPE",
                "OTHER_ERROR_TYPE",
                "MESSAGE_DESCRIPTION",
            ]:
                collector[name] = self.extract_string(sub, doprint)
            elif name in [
                "FIXED_MESSAGE_INSTANCE_VALUES",
                "MESSAGE_ID",
            ]:
                self.collect_info(sub, collector)
            else:
                collector[name] = {}
                self.collect_info(sub, collector[name])
        return collector

    def create_message_record(self, msg):
        if msg['MessageID'] not in self.messages:
            self.messages[msg['MessageID']] = {
                    'ACTIONS' : 'Not found',
                    'PREFIX' : re.sub('[0-9]+', '', msg['MessageID'])
            }

    def __init__(self, device_spec):
        self.filename = device_spec.get_message_catalog()
        self.tree = ET.parse(self.filename)
        reg = "http://schemas.dmtf.org/wbem/messageregistry/1"
        self.ns = { 'reg' : reg }
        self.root = self.tree.getroot()
        self.messages = {}
        self.act_phrase = {}

        replaces = {
            'end user license agreement' : 'eula',
            'yyyy-mm-ddthh:mm:ss' : '',
            '&(apos|gt|lt);' : '',
            '(idrac) ([0-9])' : '\\1\\2',
            '[(]([^)]+)[)]' : '\\1'
        }
        racadms = [
            'racadm help NIC.VndrConfigGroup.1.VirtWWPN',
            'racadm set idrac.os-bmc.PTMode usb-p2p',
            'racadm set idrac.os-bmc.UsbNicIpAddress ip address',
            'racadm set idrac.os-bmc.adminstate enabled',
        ]
        for i in range(0,len(racadms)):
            racadms[i] = racadms[i].lower()

        for ent in self.root.findall('.//reg:MESSAGE', self.ns):
            collect = {}
            self.collect_info(ent, collect)
            counter = collect['NAME']
            self.messages[counter] = collect
            action = self.messages[counter]['RECOMMENDED_ACTION'].lower()

            action = action.replace('(s)', '')
            action = re.sub('"([^\s]+)"', '\\1', action)
            action = re.sub('[<>]', '', action)
            for rac in racadms:
                action = action.replace(rac, '"{0}"'.format(rac))
            
            joined_actions = []
            for fld in ['"', "'"]:
                if fld in action:
                    act_string = []
                    for p in action.split(fld):
                        p1 = p.strip()
                        if p1 != '' and not p1.startswith('racadm'):
                            act_string.append(p1)
                    action = " ".join(act_string)

            for act_phrase in replaces:
                action = re.sub(act_phrase, replaces[act_phrase], action)
            for act_phrase in re.split('[^-/a-zA-Z0-9_,\s]', action):
                act_phrase = act_phrase.strip()
                if act_phrase == '': continue

                if act_phrase not in self.act_phrase:
                    self.act_phrase[act_phrase] =0
                self.act_phrase[act_phrase] += 1

                for act in self.action_types:
                    if re.search(self.action_types[act], act_phrase) and \
                        act not in joined_actions:
                        joined_actions.append(act)
            self.messages[counter]['ACTIONS'] = ";".join(joined_actions)

    def _do_load_messages(self):
        counter = 1
        self.doit = {}
        self.actions = {}
        pp = Parser({}, iDRAC())
        self.counts = { 'Total' : { "MessageCount" : 0,
                                    "ComponentCount" : 0,
                                    "UnparseCount" : 0} }
        self.act_words = {}
        self.act_phrase = {}
        for ent in self.root.findall('.//reg:MESSAGE', self.ns):
            self.messages[counter] = {}
            self.collect_info(ent, self.messages[counter])
            self.messages[counter]['PHRASES'] = pp.parse_message(
                self.messages[counter]['MESSAGE_COMPONENTS'],
                self.messages[counter]['PREFIX'])

        if False:
            prefix = self.messages[counter]['PREFIX']
            if prefix not in self.counts:
                self.counts[prefix] = { "MessageCount" : 0,
                                        "ComponentCount" : 0,
                                        "UnparseCount" : 0}

            noun_phrase = self.messages[counter]['PHRASES'][0]
            verb_phrase = self.messages[counter]['PHRASES'][1]
            self.counts[prefix]['MessageCount'] += 1
            self.counts['Total']['MessageCount'] += 1
            if "<UNPARSEABLE>" in noun_phrase:
                self.counts['Total']['UnparseCount'] += 1
                self.counts[prefix]['UnparseCount'] += 1
            if noun_phrase not in self.doit:
                self.doit[noun_phrase] = []
                self.actions[noun_phrase] = {}
                self.counts[prefix]['ComponentCount'] += 1
                self.counts['Total']['ComponentCount'] += 1
            self.doit[noun_phrase].append(verb_phrase)
            self.actions[noun_phrase][verb_phrase] = ",".join(mm_msg)
            counter = counter + 1
            self.output = {}
            for i in self.doit:
                self.output[i] = { "states" : [], "init" : [],
                                "end" : [],
                                "terminal" : [], "transitions" : {} }
                for s in self.doit[i]:
                    self.output[i]['states'].append(s)
                    isTerminal, isEnd, isInit = pp.check_state(s, i)

                    if isTerminal:
                        self.output[i]["terminal"].append(s)
                    if isEnd:
                        self.output[i]["end"].append(s)
                    if isInit:
                        self.output[i]["init"].append(s)


                for s in self.output[i]['states']:
                    if s in self.output[i]['end']:
                        continue
                    self.output[i]['transitions'][s] = []
                    for s1 in self.output[i]['states']:
                        if s1 == s: continue
                        self.output[i]['transitions'][s].append(s1)

class Parser(object):

    def _do_sort_byname(self, tnames):
        names = sorted(set(list(tnames.keys())))
        i = 0
        while i < len(names):
            for j in range(i+1, len(names)):
                if names[i] in names[j]:
                    # move to end!
                    names.append(names[i])
                    del names[i]
                    i = i - 1
                    break
            i = i+1
        return names

    def __init__(self, tnames, device_spec):
        self.ignore_swords = set(['not','under', 'over']) 
        self.swords = set(['is', 'the', 'a', 'an', 'for', 'you', 'your', 'was', 'has', 'been',
            'this', 'these', 'there', 'some',])
        self.stopWords = self.swords - self.ignore_swords
        self.components = device_spec.get_component_names()
        self.device_spec = device_spec
        self.comp_names2fqdd = tnames
        self.comp_names = self._do_sort_byname(tnames)
        self.init_classifier = device_spec.get_init_classifier()
        self.terminal_classifier = device_spec.get_terminal_classifier()
        self.end_classifier = device_spec.get_end_classifier()
        self.init_verbs = self.device_spec.get_init_verb_words()
        self.init_unparseable = self.device_spec.get_init_unparseable_words()

    def check_state(self, verb_phrase, noun_phrase):

        isInitState = False
        for vb_class in self.init_classifier:
            if vb_class[0] not in verb_phrase:
                continue
            # primary verb matches
            # check if others match
            if vb_class[1] is not None and \
               re.search(vb_class[1], verb_phrase):
               continue
            isInitState = True

        isTerminal = False
        isEndState = False
        for vb_class in self.terminal_classifier:
            if vb_class[0] not in verb_phrase:
                continue
            # primary verb matches
            # check if others match
            if vb_class[1] is not None and \
               re.search(vb_class[1], verb_phrase):
               continue

            if vb_class[2] is not None and \
               not re.search(vb_class[2], noun_phrase):
               continue
            isTerminal = True
            isEndState = True

        for vb_class in self.end_classifier:
            if vb_class[0] not in verb_phrase:
                continue
            # primary verb matches
            # check if others match
            if vb_class[1] is not None and \
               re.search(vb_class[1], verb_phrase):
               continue
            isEndState = True

        return isTerminal, isEndState, isInitState

    def parse_message(self, message, msg_type, comps = None):
        dprint(">0:::" + message)

        text = self.device_spec.cleanse_message(message.lower())

        dprint(">1:::" + text)
        for k in self.comp_names:
            if k not in text: continue
            if comps: comps.append(self.comp_names2fqdd[k])
            text = text.replace(k, self.comp_names2fqdd[k])
        dprint(">2:::" + text)

        text = nltk.word_tokenize(text)
        phrase = [ [], [] ]
        counter = 0
        for i in self.init_unparseable:
            for j in text:
                if j in self.stopWords:
                    continue
                if j == i:
                    return [msg_type + "<UNPARSEABLE>", " ".join(text)]
                break

        for (word, tag) in nltk.pos_tag(text):
            if tag.startswith('VB'):
                if word not in [ 'smi' ]:
                    counter = 1 
            if word in self.stopWords:
                continue
            if counter == 0:
                myname = " ".join(phrase[0])
                nname = myname + " " + word

                found_equal = False
                found_future = False
                for nword in self.components:
                    if myname == nword: found_equal = True
                    if nname in nword: found_future = True

                if found_equal and not found_future:
                    counter = 1
                elif found_future:
                    counter = 0
            if counter == 0 and \
                (word in self.ignore_swords or word.startswith('-')):
                counter = 1

            phrase[counter].append(word)
            if word in self.init_verbs and len(phrase[0]) == 0:
                counter = 0
        if len(phrase[0]) == 0:
            return [msg_type + "<UNPARSEABLE>", " ".join(text)]
        return [" ".join(phrase[0]), " ".join(phrase[1])]

class PDF(object):
    def __init__(self, entries):
        self.entries = entries
        count = 10
        newcount = self._do_init(count)
        if newcount != count:
            count = newcount
            newcount = self._do_init(count)
        if newcount != count:
            count = newcount
            newcount = self._do_init(count)

    def _do_init(self, count):
        self.count = count 
        self.max_ent = max(self.entries)
        self.min_ent = min(self.entries)
        self.interval = round((self.max_ent-self.min_ent)/self.count)
        if self.interval == 0:
            self.count = 0
            self.pdf = [1.0]
        else:
            frequencies=[0 for i in range(0,self.count+1)]
            for i in self.entries:
                frequencies[int((i-self.min_ent)/self.interval)] += 1
            sum_ent = sum(frequencies)
            self.pdf = [i/sum_ent for i in frequencies]
        return len([1 for i in self.pdf if i != 0.0])

    def to_json(self):
        return {
            'Min' : self.min_ent,
            'Max' : self.max_ent,
            'Interval' : self.interval,
            'Function' : self.pdf
        }

    def predict(self, at_least = 0.5):
        compute = lambda val, idx: timedelta(seconds=((val+idx) * self.interval + self.min_ent))

        values = 0
        for i in range(0,self.count+1):
            values += self.pdf[i]
            if values > at_least:
                return compute(i, 1)
        return compute(self.count, 1)

class Blackboard(object):

    @staticmethod
    def _tstamp_to_datetime(time):
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        try:
            time = datetime.fromtimestamp(
                    datetime.strptime(time, date_format).timestamp())
        except ValueError:
            date_format = "%Y-%m-%dT%H:%M:%S"
            #if 'Z' in time:
            #    time = time[0:time.rindex('Z')]
            #elif 'z' in time:
            #    time = time[0:time.rindex('z')]
            time=time[0:19]
            time = datetime.fromtimestamp(
                    datetime.strptime(time, date_format).timestamp())
        return time

    @staticmethod
    def _compute_since(start, end=None):
        start = Blackboard._tstamp_to_datetime(start)
        end = Blackboard._tstamp_to_datetime(end) if end else datetime.now()
        return int((end-start).total_seconds())

    def __init__(self, comp, sysblackboard):
        self.comp = comp
        self.prev_state = None
        self.cur_state = None
        self.cur_tstamp = None
        self.cur_action = None
        self.transition_times = {}
        self.transition_counts = {}
        self.transition_state = {}
        self.sysblackboard = sysblackboard
        self.history = []
        self._lock = threading.Lock()

    def prepare(self):
        with self._lock:
            self.pdf = {}
            for i in self.transition_times:
                self.pdf[i] = {}
                for j in self.transition_times[i]:
                    self.pdf[i][j] = PDF(self.transition_times[i][j])

    def predict(self, i, j, at_least = 0.5):
        ptime = timedelta(0)
        with self._lock:
            #jprint(self.transition_times[i][j])
            ptime = self.pdf[i][j].predict(at_least)
        return ptime

    #def to_json(self):
    #    pdf_json = {}
    #    for i in self.transition_times:
    #        pdf_json[i] = {}
    #        for j in self.transition_times[i]:
    #            pdf_json[i][j] = self.pdf[i][j].to_json()
    #
    #    return {
    #       'cur_state' : self.cur_state,
    #       'cur_tstamp' : self.cur_tstamp,
    #       'pdf' : pdf_json,
    #       'cur_action' : self.cur_action
    #   }

    def update_state(self, state, tstamp, isTerminal, action, prefix):
        printMsg = True
        if state == "<SYS_TURN_OFF>":
            printMsg = False
        self.cur_action = action

        old_state = state

        if isTerminal:
            state = "<TERMINAL>"

        if self.cur_state is None:
            self.cur_state = "<init>"
            self.prev_state = None

        if self.cur_tstamp is None:
            self.cur_tstamp = tstamp

        if self.cur_state not in self.transition_times:
            self.transition_times[self.cur_state] = {}
            self.transition_counts[self.cur_state] = {}
            self.transition_state[self.cur_state] = {}

        if state not in self.transition_times[self.cur_state]:
            self.transition_times[self.cur_state][state] = []
            self.transition_counts[self.cur_state][state] = []
            self.transition_state[self.cur_state][state] = []

        tsecs = self._compute_since(self.cur_tstamp, tstamp)
        if tsecs < 0: tsecs = 0
        self.transition_times[self.cur_state][state].append(tsecs)

        self.transition_state[self.cur_state][state].append(old_state)

        # asking for moving to same state.  Is this allowed?

        if self.cur_state == state:

            if self.prev_state != self.cur_state:
                self.transition_counts[self.cur_state][state].append(1)
            else:
                self.transition_counts[self.cur_state][state][-1] += 1

            if printMsg:
                dprint("{0}: Move from an state({1}) to same state({2}): {3}".format(
                    self.comp, self.cur_state, state,
                    self.transition_counts[self.cur_state][state][-1]))
                dprint("------ {0} => {1} | {2}".format(self.cur_tstamp, tstamp,
                    self.transition_times[self.cur_state][state][-1]))

        # is this a valid transition?, need transition table!
        #elif not is_valid(self.cur_state, state):
        #
        #    return False
        #
        # Valid transition to Terminal State
        else:

            self.transition_counts[self.cur_state][state].append(1)

            if printMsg:
                dprint("{0}: Move from a state({1}) to another state({2})".format(
                    self.comp, self.cur_state, state))
                if isTerminal:
                    dprint("Reached terminal state. Removing from backboard")
                dprint("------ {0} => {1} | {2}".format(self.cur_tstamp, tstamp,
                    self.transition_times[self.cur_state][state][-1]))
        self.history.append([tstamp,
                    self.cur_state, old_state,
                    str(isTerminal),
                    str(self.transition_counts[self.cur_state][state][-1])])

        self.prev_state = self.cur_state
        self.cur_state = None if isTerminal else state
        self.cur_tstamp = tstamp
        return True

class SystemBlackboard(object):
    def __init__(self, host, parent=None):
        self.blackboard = {}
        self.reset_times = []
        self.reset_acts = []
        self.cur_tstamp = None
        self.host = host
        self.parent = parent
        self.online = False

    def update_state_all(self, comp, state, tstamp, isTerminal, action, prefix):
        self._update_time(comp, state, tstamp)
        for i in self.blackboard:
            self.blackboard[i].update_state(state, tstamp, isTerminal, action, prefix)
        self.parent.update(self, comp, state, prefix)
        return True

    def update_state(self, comp, state, tstamp, isTerminal, action, prefix):
        self._update_time(comp, state, tstamp)
        if comp not in self.blackboard:
            self.blackboard[comp] = Blackboard(comp, self)
        self.parent.update(self, comp, state, prefix)
        return self.blackboard[comp].update_state(state,
            tstamp, isTerminal, action, prefix)

    def _update_time(self, comp, state, tstamp):
        if not self.cur_tstamp:
            self.cur_tstamp = tstamp
        if Blackboard._compute_since(self.cur_tstamp, tstamp) < 0:
            self.reset_times.append([self.cur_tstamp, tstamp])
            self.reset_acts.append([comp, state])
        self.cur_tstamp = tstamp

    def to_json(self):
        myjson = []
        for comp in self.blackboard:
            if self.blackboard[comp].cur_state:
                cstate = self.blackboard[comp].cur_state
                ctstamp = self.blackboard[comp].cur_tstamp
                self.blackboard[comp].prepare()
                spdf = self.blackboard[comp].pdf
                predict_it = "<>"
                if cstate not in spdf:
                    predict_it = "not_found<{0}>".format(cstate)
                elif '<TERMINAL>' not in spdf[cstate]:
                    predict_it = "not_found<{0}->TERMINAL>".format(cstate)
                else:
                    #predict_it = Blackboard._tstamp_to_datetime(ctstamp) + \
                    #        spdf[cstate]['<TERMINAL>'].predict(0.8)
                    #predict_it = predict_it.strftime("%Y-%m-%dT%H:%M:%S")
                    predict_it = str(self.blackboard[comp].predict(cstate, '<TERMINAL>', 0.8))
                myjson.append([
                    self.blackboard[comp].cur_tstamp,
                    self.host,
                    comp,
                    self.blackboard[comp].cur_state,
                    self.blackboard[comp].cur_action,
                    predict_it])
        return myjson

    def jprint(self, name):
        printer = print if self.online else dprint
        printer("======= {0} blackboard".format(name))
        for i in self.to_json():
            printer(", ".join(i))
        printer("======= {0} blackboard ends".format(name))

    def jhistory(self, name):
        printer = print if self.online else dprint
        printer("======= {0}::{1} history".format(self.host,name))
        for comp in self.blackboard:
            printer("  ------- {0}::{1} --------".format(self.host, comp))
            for hist in self.blackboard[comp].history:
                printer("   " + ", ".join(hist))
        printer("======= {0} history ends".format(name))

    def jdetails(self, name):
        myjson = {}
        for i in self.blackboard:
            myjson[i] = self.blackboard[i].to_json()
        myjson['_reset_times'] = self.reset_times
        myjson['_reset_acts'] = self.reset_acts
        printer = print if self.online else dprint
        printer("======= {0}::{1} details".format(self.host,name))
        print(json.dumps(myjson, sort_keys=True, indent=4, \
            separators=(',', ': ')))
        printer("======= {0} details ends".format(name))

class UberBlackboard(object):

    def __init__(self):
        self.counts = {}
        self.counts['Total'] = {"MessageCount" : 0, "UnparseCount" : 0 }
        self.counts['Components'] = {}
        self.counts['Categories'] = {}

    def update(self, host, comp, state, prefix):
        self.counts['Total']['MessageCount'] += 1

        if comp not in self.counts['Components']:
            self.counts['Components'][comp] = {"MessageCount" : 0, "UnparseCount" : 0 }
        self.counts['Components'][comp]['MessageCount'] += 1

        if prefix not in self.counts['Categories']:
            self.counts['Categories'][prefix] = {"MessageCount" : 0, "UnparseCount" : 0 }
        self.counts['Categories'][prefix]["MessageCount"] += 1

        if "<UNPARSEABLE>" in comp:
            print(comp + "//" + state)
            self.counts['Categories'][prefix]["MessageCount"] += 1
            self.counts['Total']['UnparseCount'] += 1

    def details(self):
        return self.counts


class DeviceLogAnalyzer(object):

    def build_name_map(self):
        self.devicejson = self.device_sdk.get_device_json()

        for comp in self.devicejson:
            if comp in self.device_spec.get_ignore_components():
                continue
            for ent in self.devicejson[comp]:
                for name in self.device_spec.get_name_fields():
                    if name in ent:
                        if type(ent[name]) != list:
                            self.tnames[ent[name].lower()] = ent['Key']
                        elif len(ent[n]) > 0:
                            self.tnames[ent[name][0].lower()] = ent['Key']

        for (ent_n,ent_key) in  self.device_spec.get_init_name_key_map():
            if ent_n not in self.tnames:
                self.tnames[ent_n.lower()] = ent_key

    def __init__(self, device_sdk, device_spec, eemi, uber):

        self.device_sdk = device_sdk
        self.tnames = {}
        self.comps = {}
        self.datasets = {}

        self.eemi = eemi
        self.uber = uber

        self.tree = ET.parse(self.device_sdk.get_log())
        self.root = self.tree.getroot()

        self.device_spec = device_spec
        self.build_name_map()
        self.blackboard = SystemBlackboard(self.device_sdk.ipaddr, uber)
        self.parser = Parser(self.tnames, device_spec)
        self.ignore_msgids = device_spec.get_white_noise()

    def _build_msg_from_xml(self, entry, prefix, json_obj):
        for i in entry:
            json_obj.update(entry.attrib)
            if len(i): self._build_msg_from_xml(i, prefix + [i.tag], json_obj)
            elif i.text:
                i_tag = ".".join(prefix + [i.tag])
                if i_tag in json_obj:
                    if type(json_obj[i_tag]) != list:
                        json_obj[i_tag] = [json_obj[i_tag]]
                    else:
                        json_obj[i_tag].append(i.text.strip())
                else:
                    json_obj[i_tag] = i.text.strip()
        return json_obj

    def load_log(self):
        self.blackboard.online = False
        for i in self.root:
            # Flatten entry
            msg = self._build_msg_from_xml(i, [], {})
            self.parse(msg)

        self.blackboard.online = True
        self.blackboard.jprint('final')

    def parse(self, msg):
        if True:
            if msg['MessageID'] not in self.eemi.messages:
                print(msg['MessageID'] + "is not found")
                self.eemi.create_message_record(msg)

            # Ignore Messages 
            if msg['MessageID'] in self.ignore_msgids:
                self.uber.update(self.device_sdk.ipaddr, 'WhiteNoise', '<>',
                    self.eemi.messages[msg['MessageID']]['PREFIX'])
                return False

            if msg['Timestamp'].startswith('19') or \
               msg['Timestamp'].startswith('200'):
                self.uber.update(self.device_sdk.ipaddr, 'LostTime', '<>',
                    self.eemi.messages[msg['MessageID']]['PREFIX'])
                return False

            # Normalize Message
            if type(msg['Message']) == list:
                msg['Message'] = "::".join(msg['Message'])

            if 'MessageArgs.Arg' not in msg:
                msg['MessageArgs.Arg'] = []
            elif type(msg['MessageArgs.Arg']) != list:
                msg['MessageArgs.Arg'] = [msg['MessageArgs.Arg']]

            dprint("{0}:{1}::{2}".format(msg['Sequence'], msg['Timestamp'],
                    msg['Message']))


            parsed_msg = self.parser.parse_message(msg['Message'],
                self.eemi.messages[msg['MessageID']]['PREFIX'],
                msg['MessageArgs.Arg'])
            msg['Components'] = list(set(msg['MessageArgs.Arg']))
            action = self.eemi.messages[msg['MessageID']]['ACTIONS']
            prefix = self.eemi.messages[msg['MessageID']]['PREFIX']

            if '<UNPARSEABLE>' in parsed_msg[0]:
                self.uber.update(self.device_sdk.ipaddr, 'Unparse', '<>',
                    self.eemi.messages[msg['MessageID']]['PREFIX'])
                return False

            # parsed_msg[0] => noun phrase, parsed_msg[1] => verb_phrase

            isTerminal, isEnd, isInit = self.parser.check_state(parsed_msg[1],
                parsed_msg[0])

            # Handle Reboot scenarios. This will reset all the state machines!
            # Need to handle this, otherwise, there will be spurious transitions
            if parsed_msg[0] == "system" and isTerminal:
                self.blackboard.update_state_all(parsed_msg[0],
                    '<SYS_TURN_OFF>', msg['Timestamp'], isTerminal,
                    action, prefix)
                self.blackboard.jprint('updated')
            elif self.blackboard.update_state(parsed_msg[0],parsed_msg[1],
                        msg['Timestamp'], isTerminal, action, prefix):
                self.blackboard.jprint('updated')

        return True

myd=3

class iDRAC(object):

    def get_message_catalog(self):
        return 'omsdktest/iDRAC_MsgReg_15G_Halo_2019Q4.xml'

    def get_init_classifier(self):
        return [
            [ 'init',    None, None ],
            [ 'create',     None, None ],
            [ 'start',   None, None ],
            [ 'resume',    None, None ],
        ]

    def get_terminal_classifier(self):
        return [
            [ 'restarted',         None, None ],
            [ 'inserted',          None, None ],
            [ 'restored',          None, None ],
            [ 'turning on',        None, None ],
            [ 'turning off',       None, None ],
            [ 'complete',          None, None ],
            [ 'detected',          None, None ],
            [ 'changed',           None, None ],
            [ 'started',           None, 'link' ],
            [ 'downloading',       None, 'update package' ],
            [ 'exported',          None, None ],
            [ 'imported',          None, None ],
            [ 'exited',            None, None ],
            [ 'are redundant',     None, None ],
            [ 'online',            None, None ],
            [ 'installed',         None, None ],
            [ 'requested powerup', None, None ],
            [ 'not licensed',      None, None ],
            [ 'success',           'unsuccess',   None ],
            [ 'enabled',           'not',         None ],
            [ 'ready',             'not',         None ],
            [ 'normal',            'above|below', None ],
        ]

    def get_end_classifier(self):
        return [
            [ 'failed',    None, None ],
            [ 'cancel',     None, None ],
        ]

    def get_init_verb_words(self):
        return ['collecting', 'restoring', 'validating',
                        'performing', 'starting', 'initializing',
                        'initiated', 'staged', 'completed', 'requested',
                        'verifying',  'preparing', 'changing',
                        'unsupported', 'valid',
                        'finalizing']

    def get_init_unparseable_words(self):
        return ["unable", "invalid"]

    def cleanse_message(self, message):
        text = re.sub('[(][^[)]*[)]', '', message)
        text = re.sub('(-[a-zA-Z0-9]) option', 'option \\1', text)
        text = re.sub('\\.$', '', text)
        text = re.sub('(downloading)\s(.*)\s(update package)', '\\3 \\1 \\2', text)
        text = text.replace('hot-spare', 'hot spare')
        text = text.replace("physical_drive_name", "pd_name")
        text = text.replace("virtual_disk", "vd_name")
        text = text.replace("over voltage fault", "voltage fault over")
        text = text.replace("under voltage fault", "voltage fault under")
        text = text.replace("controller cache is preserved",
                            "controller preserved cache")
        text = text.replace("preserved cache",
                            "controller preserved cache")
        text = text.replace('on device idrac',
                            'assigned to device idrac')
        if 'partition' not in text:
            text = re.sub('nic embedded ([^\s]+) port ([^\s]+)',
                     'embedded nic \\1 port \\2 partition 1', text)
            text = re.sub('nic mezzanine ([^\s]+) port ([^\s]+)',
                     'nic in mezzanine \\1a port \\2 partition 1', text)
        return text

    def get_component_names(self):
        return [
            "os watchdog timer",
            "os to idrac pass-through",
            "watchdog timer",
            "cpu number voltage regulator module",
            "cpu number terminator",
            "cpu number",
            "cpu bus",
            "memory",
            "low memory",
            "memory device",
            "memory device location",
            "memory interconnect",
            "memory mirror"
            "memory mirror redundancy"
            "memory raid"
            "memory raid redundancy"
            "memory spare"
            "memory spare redundancy"
            "memory redundancy"
            "memory riser",
            "persistent correctable memory error",
            "abort cc error",
            "background initialization",
            "background initialization rate",
            "bad block table",
            "bad block",
            "bad disk block",
            "check consistency",
            "clear operation",
            "consistency check",
            "copyback",
            "disk media error",
            "global hot spare",
            "initialization",
            "key exchange",
            "microcode",
            "patrol read",
            "patrol read rate",
            "patrol read operation",
            "pd_name initialization",
            "pd_name",
            "rebuild operation virtual drive",
            "rebuild",
            "reconfiguration",
            "redundancy",
            "security",
            "security key",
            "smart",
            "bus",
            "certificate validation",
            "certificate signing request",
            "certificate",
            "certificate upload",
            "bmc watchdog",
            "character",
            "firmware file",
            "firmware image",
            "firmware rollback",
            "firmware software incompatibility",
            "firmware update",
            "firmware update operation",
            "firmware version",
            "front panel usb",
            "front usb port",
            "group job task_id",
            "hardware cache",
            "hardware identity certificate",
            "hardware incompatibility",
            "hardware inventory",
            "hardware",
            "preserved cache",
            "dedicated hot spare",
            "enhanced dynamic power supply engagement",
            "integrated data center",
            "integrated data center public ip",
            "virtual media image server",
            "virtual disk",
            "vflash",
            "vflash backup partition",
            "vflash erase operation",
            "vflash media",
            "vflash media partition",
            "vflash media reader license",
            "vflash sd card",
            "vflash sd card",
            "version",
            "vd_name rebuild",
            "vd_name read policy",
            "vd_name initialization",
            "vd_name blink",
            "vd_name consistency check",
            "username",
            "update package",
            "supportassist collection",
            "supportassist collection operation",
            "system returned",
            "system in",
            "system halted",
            "system",
            "system bios",
            "system board battery",
            "system board name cable or interconnect",
            "system board name current",
            "system board name temperature",
            "system board name voltage",
            "system configuration check operation",
            "system configuration config_id",
            "system configuration lockdown mode",
            "server configuration profile",
            "system controller",
            "system cooling",
            "system erase",
            "system error",
            "system event log",
            "system fault event",
            "system health",
            "system id",
            "system information",
            "system inlet temperature",
            "system input power cap",
            "system inventory",
            "system level current",
            "system lockdown",
            "system management interrupt",
            "system management mode",
            "system memory",
            "system nmi",
            "system performance",
            "system profile backup",
            "system profile operation",
            "system reboot",
            "system service tag",
            "system services",
            "system software event",
            "system time and date",
        ]

    def get_white_noise(self):
        return [
            'USR0030', 'LOG007', 'LOG203',
            'USR0031', 'USR0034', 'USR0032', 'RAC1195',
            'USR0002', 'USR0005', 'USR0007', 'USR107',
    
            # Dummy ids
            "PSU0800","PSU0003", "VLT0304",
    
            # Need to find state machine
            "UEFI0116","UEFI0033",
            "LIC211", "LIC208",
            "JCP027", "JCP057", "JCP037",
            "SYS057",
            "RAC0182", "UEFI0323", "UEFI0324",
            "RED052", "RED054", "RED063", "RED002", "RED055",
            "SUP0516", "SUP0518",
            "HWC2014",
        ]

    def get_ignore_components(self):
        return ['System', 'Subsystem']

    def get_name_fields(self):
        return ['DeviceDescription', 'ElementName',
                          'LicenseDescription']

    def get_init_name_key_map(self):
       return [ 
                ('power supply 1', 'PSU.Slot.1'),
                ('power supply 2', 'PSU.Slot.2'),
                ('power control', 'iDRAC.Embedded.1#HostPowerCtrl'),
                ('cpu 1', 'CPU.Socket.1'),
                ('cpu 2', 'CPU.Socket.2') ]

class DeviceSDK(object):
    def __init__(self, directory, ipaddr):
        self.directory = directory
        self.ipaddr = ipaddr
        self.devicejson = None

    def get_device_json(self):
        if not self.devicejson:
            with open(os.path.join(self.directory,
               'Key_Inventory_ConfigState.json'), 'r') as f:
                self.devicejson = json.load(f)
        return self.devicejson

    def get_log(self):
        logfiles = glob.glob(os.path.join(self.directory, '*.xml'))
        if len(logfiles) == 0:
            logfiles = [os.path.join(directory, 'dummy.log.xml')]
            with open(logfiles[0], 'w') as f:
                f.write('<LCLogEvents></LCLogEvents>\n')
                f.flush()
        return logfiles[0]


class Caller(object):

    doit = 1
    def __init__(self):
        print (Caller.doit)
        Caller.doit += 1
        self.count = 1
        self.devices = {}

    def add_device(self, device):
        self.devices[device.device_sdk.ipaddr] = device
        return self

    def message_handler(self, message):
        if message['Host'] not in self.devices:
            print(message['Host'] + " not found! Ignoring Message!")
            return False
        return self.devices[message['Host']].parse(message)

    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
      while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            message = {
                'Sequence' : self.count + 1,
                'Timestamp' : datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            }
            self.count+=1
            maps = {
                '1.3.6.1.4.1.674.10892.5.3.1.1.0': 'MessageID',
                '1.3.6.1.4.1.674.10892.5.3.1.2.0': 'Message',
                '1.3.6.1.4.1.674.10892.5.3.1.6.0': 'FQDD',
                '1.3.6.1.4.1.674.10892.5.3.1.8.0': 'MessageArgs.Arg',
                '1.3.6.1.4.1.674.10892.5.3.1.9.0': 'Host',

            }
            for oid, val in varBinds:
                oid_pretty = oid.prettyPrint()
                if oid_pretty in maps:
                    message[maps[oid_pretty]] = str(val.
                        getComponent().getComponent())
            self.message_handler(message)
      return wholeMsg

    def start_process(self):
        transportDispatcher = AsynsockDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbFun)
        transportDispatcher.registerTransport(
            udp.domainName,
            udp.UdpSocketTransport().openServerMode(('localhost', 162))
        )

        transportDispatcher.jobStarted(1)
        try:
            print("Starting dispatcher")
            # Dispatcher will never finish as job#1 never reaches zero
            transportDispatcher.runDispatcher()
        except:
            transportDispatcher.closeDispatcher()
            raise

class Enigma(object):

    def __init__(self):
        device_spec = iDRAC()
        eemi = EEMI(device_spec)
        uber = UberBlackboard()
        device = None
        self.caller = Caller()

        for lfile in glob.glob('../omdata/Store/Master/Server/*/*log.xml')[2:3]:
            directory = os.path.split(lfile)[0]
            server_name = os.path.split(directory)[1]
            print(server_name)
            print(directory)
            device_sdk = DeviceSDK(directory, server_name)
            device = DeviceLogAnalyzer(device_sdk, device_spec, eemi, uber)
            self.caller.add_device(device)
            device.load_log()
            print("======= here =====")
            threading.Thread(target=self.thread_function, args=(1,)).start()

    def thread_function(self, name):
        print(name)
        self.caller.start_process()


app = Flask(__name__, template_folder='templates')
enigma = Enigma()

@app.route("/", methods = ['POST','GET'])
def table():
    if request.method == 'GET':
        mlist = []
        for i in enigma.caller.devices:
            mlist.extend(enigma.caller.devices[i].blackboard.to_json())
        return render_template('blackboard.html', json_table=mlist)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
