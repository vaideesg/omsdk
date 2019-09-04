import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import xml.etree.ElementTree as ET
import json
import re
from  datetime import datetime
import zipfile, io, gzip, os, shutil, glob

#from nltk.corpus import nltk_words
#EnglishDict = dict.fromkeys(nltk_words.words(), None)

def dprint(msg):
    pass

def jprint(msg):
    print(json.dumps(msg, sort_keys=True, indent=4, \
            separators=(',', ': ')))

class DeviceMapper(object):
    def __init__(self, directory, srvname = ""):
        self.directory = directory
        self.ipaddr = re.sub('\\\\.*$', '', re.sub('.*Master/Server.', '', directory))
        self.devicejson = {}
        self.tnames = {}
        self.server_name = srvname


    def build_name_map(self):
        with open(os.path.join(directory, 'Key_Inventory_ConfigState.json'), 'r') as f:
            self.devicejson = json.load(f)

        for comp in self.devicejson:
            if comp in ['System', 'Subsystem']: continue
            for ent in self.devicejson[comp]:
                for name in ['DeviceDescription', 'ElementName',
                          'LicenseDescription']:
                    if name in ent:
                        if type(ent[name]) != list:
                            self.tnames[ent[name].lower()] = ent['Key']
                        elif len(ent[n]) > 0:
                            self.tnames[ent[name][0].lower()] = ent['Key']

        for (ent_n,ent_key) in  [
                ('power supply 1', 'PSU.Slot.1'),
                ('power supply 2', 'PSU.Slot.2'),
                ('power control', 'iDRAC.Embedded.1#HostPowerCtrl'),
                ('cpu 1', 'CPU.Socket.1'),
                ('cpu 2', 'CPU.Socket.2') ]:
            if ent_n not in self.tnames:
                self.tnames[ent_n.lower()] = ent_key

    def get_log(self):
        logfiles = glob.glob(os.path.join(directory, '*.xml'))
        if len(logfiles) == 0:
            logfiles = [os.path.join(directory, 'dummy.log.xml')]
            with open(logfiles[0], 'w') as f:
                f.write('<LCLogEvents></LCLogEvents>\n')
                f.flush()
        return logfiles[0]


class EEMI(object):

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

    def __init__(self):
        self.filename = 'omsdktest/iDRAC_MsgReg_15G_Halo_2019Q4.xml'
        self.tree = ET.parse(self.filename)
        reg = "http://schemas.dmtf.org/wbem/messageregistry/1"
        ns = { 'reg' : reg }
        self.root = self.tree.getroot()
        counter = 1
        self.messages = {}
        self.doit = {}
        self.actions = {}
        pp = Parser({})
        self.counts = { 'Total' : { "MessageCount" : 0,
                                    "ComponentCount" : 0,
                                    "UnparseCount" : 0} }
        self.act_words = set()
        for ent in self.root.findall('.//reg:MESSAGE', ns):
            self.messages[counter] = {}
            self.collect_info(ent, self.messages[counter])
            self.messages[counter]['PHRASES'] = pp.parse_message(
                self.messages[counter]['MESSAGE_COMPONENTS'],
                self.messages[counter]['PREFIX'])

            mm = self.messages[counter]['RECOMMENDED_ACTION'].lower()
            types = {
                'review system' : 'CHECK',
                'check system logs' : 'LOGS',
                'No response' : 'IGNORE',
                'reseat' : 'H&E',
                'reinstall' : 'H&E',
                'reset'  : 'RESET',
                'turn off'  : 'RESET',
                'retry'  : 'RETRY',
                'remove'  : 'H&E',
                're-apply'  : 'H&E',
                'latest' : 'UPGRADE',
                'contact your' : 'SOS',
                'contact techincal' : 'SOS'
            }

            mm_msg = []
            for tt in types:
                if tt in mm: mm_msg.append(types[tt])

            for mmword in set(mm.split()):
                #if mmword in EnglishDict:
                if wordnet.synsets(mmword):
                    self.act_words |= set([mmword])

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
        if False:
            self.output = {}
            for i in self.doit:
                self.output[i] = { "states" : [], "init" : [],
                                "end" : [],
                                "terminal" : [], "transitions" : {} }
                for s in self.doit[i]:
                    self.output[i]['states'].append(s)
                    isTerminal, isEnd, isInit = pp.check_state(s)
    
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

    def __init__(self, tnames):
        self.ignore_swords = set(['not','under', 'over']) 
        self.swords = set(stopwords.words('english'))
        self.swords = set(['is', 'the', 'a', 'an', 'for', 'you', 'your', 'was', 'has', 'been',
            'this', 'these', 'there', 'some',])
        self.stopWords = self.swords - self.ignore_swords
        self.components = [
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
        self.comp_names2fqdd = tnames
        self.comp_names = self._do_sort_byname(tnames)

    def check_state(self, verb_phrase):

        init_classifier = [
            [ 'init',    None, None ],
            [ 'create',     None, None ],
            [ 'start',   None, None ],
            [ 'resume',    None, None ],
        ]

        terminal_classifier = [
            [ 'restarted',         None, None ],
            [ 'inserted',          None, None ],
            [ 'restored',          None, None ],
            [ 'turning on',        None, None ],
            [ 'turning off',       None, None ],
            [ 'complete',          None, None ],
            [ 'detected',          None, None ],
            [ 'changed',           None, None ],
            [ 'exported',          None, None ],
            [ 'imported',          None, None ],
            [ 'exited',            None, None ],
            [ 'requested powerup', None, None ],
            [ 'not licensed',      None, None ],
            [ 'success',           'unsuccess',   None ],
            [ 'enabled',           'not',         None ],
            [ 'normal',            'above|below', None ],
        ]

        end_classifier = [
            [ 'failed',    None, None ],
            [ 'cancel',     None, None ],
        ]

        isInitState = False
        for vb_class in init_classifier:
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
        for vb_class in terminal_classifier:
            if vb_class[0] not in verb_phrase:
                continue
            # primary verb matches
            # check if others match
            if vb_class[1] is not None and \
               re.search(vb_class[1], verb_phrase):
               continue
            isTerminal = True
            isEndState = True

        for vb_class in end_classifier:
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
        text = re.sub('[(][^[)]*[)]', '', message.lower())
        text = re.sub('(-[a-zA-Z0-9]) option', 'option \\1', text)
        text = re.sub('\\.$', '', text)
        text = text.replace('hot-spare', 'hot spare')
        text = text.replace("physical_drive_name", "pd_name")
        text = text.replace("virtual_disk", "vd_name")
        text = text.replace("over voltage fault", "voltage fault over")
        text = text.replace("under voltage fault", "voltage fault under")
        text = text.replace("controller cache is preserved",
                            "controller preserved cache")
        text = text.replace('on device idrac',
                            'assigned to device idrac')
        if 'partition' not in text:
            text = re.sub('nic embedded ([^\s]+) port ([^\s]+)',
                     'embedded nic \\1 port \\2 partition 1', text)
            text = re.sub('nic mezzanine ([^\s]+) port ([^\s]+)',
                     'nic in mezzanine \\1a port \\2 partition 1', text)

        dprint(">1:::" + text)
        for k in self.comp_names:
            if k not in text: continue
            if comps: comps.append(self.comp_names2fqdd[k])
            text = text.replace(k, self.comp_names2fqdd[k])
        dprint(">2:::" + text)

        text = nltk.word_tokenize(text)
        phrase = [ [], [] ]
        counter = 0
        for i in ["unable", "invalid"]:
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
            if word in ['collecting', 'restoring', 'validating',
                        'performing', 'starting', 'initializing',
                        'initiated', 'staged', 'completed', 'requested',
                        'verifying',  'preparing', 'changing',
                        'unsupported', 'valid',
                        'finalizing'] and len(phrase[0]) == 0:
                counter = 0
        if len(phrase[0]) == 0:
            return [msg_type + "<UNPARSEABLE>", " ".join(text)]
        return [" ".join(phrase[0]), " ".join(phrase[1])]

class PDF(object):
    def __init__(self, entries):
        self.entries = entries
        self.count = 10
        self.max_ent = max(entries)
        self.min_ent = min(entries)
        self.interval = round((self.max_ent-self.min_ent)/self.count)
        if self.interval == 0:
            self.count = 0
            self.pdf = [1.0]
        else:
            frequencies=[0 for i in range(0,self.count+1)]
            for i in entries:
                frequencies[int((i-self.min_ent)/self.interval)] += 1
            sum_ent = sum(frequencies)
            self.pdf = [i/sum_ent for i in frequencies]

    def to_json(self):
        return {
            'Min' : self.min_ent,
            'Max' : self.max_ent,
            'Interval' : self.interval,
            'Function' : self.pdf

        }

    def predict(self, at_least = 0.5):
        values = 0
        for i in range(0,self.count+1):
            values += self.pdf[i]
            if values > at_least:
                return [ ((i+0) * self.interval + self.min_ent),
                         ((i+1) * self.interval + self.min_ent) ]
        return [ ((self.count+0) * self.interval + self.min_ent),
                 ((self.count+1) * self.interval + self.min_ent) ]

class Blackboard(object):

    @staticmethod
    def _compute_since(start, end=None):
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        try:
            start = datetime.fromtimestamp(
                    datetime.strptime(start, date_format).timestamp())
        except ValueError:
            date_format = "%Y-%m-%dT%H:%M:%S"
            if 'Z' in start:
                start = start[0:start.rindex('Z')]
            elif 'z' in start:
                start = start[0:start.rindex('z')]
            start = datetime.fromtimestamp(
                    datetime.strptime(start, date_format).timestamp())

        if end is None:
            end = datetime.now()
        else:
            try:
                end = datetime.fromtimestamp(
                    datetime.strptime(end, date_format).timestamp())
            except ValueError:
                date_format = "%Y-%m-%dT%H:%M:%S"
                #if end and 'Z' in end:
                #    end = end[0:end.rindex('Z')]
                #if end and 'z' in end:
                #    end = end[0:end.rindex('z')]
                end=end[0:19]
                end = datetime.fromtimestamp(
                        datetime.strptime(end, date_format).timestamp())
        return int((end-start).total_seconds())

    def __init__(self, comp, sysblackboard):
        self.comp = comp
        self.prev_state = None
        self.cur_state = None
        self.cur_tstamp = None
        self.transition_times = {}
        self.transition_counts = {}
        self.transition_state = {}
        self.sysblackboard = sysblackboard

    def to_json(self):
        pdf = {}
        for i in self.transition_times:
            pdf[i] = {}
            for j in self.transition_times[i]:
                pdf[i][j] = PDF(self.transition_times[i][j]).to_json()

        return {
            'cur_state' : self.cur_state,
            'cur_tstamp' : self.cur_tstamp,
            #'transition_times' : self.transition_times,
            #'transition_counts' : self.transition_counts,
            #'transition_state' : self.transition_state,
            'pdf' : pdf
        }

    def update_state(self, state, tstamp, isTerminal):
        printMsg = True
        if state == "<SYS_TURN_OFF>":
            printMsg = False

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
                print("{0}: Move from an state({1}) to same state({2}): {3}".format(
                    self.comp, self.cur_state, state,
                    self.transition_counts[self.cur_state][state][-1]))
                print("------ {0} => {1} | {2}".format(self.cur_tstamp, tstamp,
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
                print("{0}: Move from a state({1}) to another state({2})".format(
                    self.comp, self.cur_state, state))
                if isTerminal:
                    print("Reached terminal state. Removing from backboard")
                print("------ {0} => {1} | {2}".format(self.cur_tstamp, tstamp,
                    self.transition_times[self.cur_state][state][-1]))

        self.prev_state = self.cur_state
        self.cur_state = None if isTerminal else state
        self.cur_tstamp = tstamp
        return True

class SystemBlackboard(object):
    def __init__(self):
        self.blackboard = {}
        self.reset_times = []
        self.reset_acts = []
        self.cur_tstamp = None

    def update_state_all(self, state, tstamp, isTerminal):
        self._update_time('system', state, tstamp)
        for i in self.blackboard:
            self.blackboard[i].update_state(state, tstamp, isTerminal)
        return True

    def update_state(self, comp, state, tstamp, isTerminal):
        self._update_time(comp, state, tstamp)
        if comp not in self.blackboard:
            self.blackboard[comp] = Blackboard(comp, self)
        return self.blackboard[comp].update_state(state,
            tstamp, isTerminal)

    def _update_time(self, comp, state, tstamp):
        if not self.cur_tstamp:
            self.cur_tstamp = tstamp
        if Blackboard._compute_since(self.cur_tstamp, tstamp) < 0:
            self.reset_times.append([self.cur_tstamp, tstamp])
            self.reset_acts.append([comp, state])
        self.cur_tstamp = tstamp

    def to_json(self):
        myjson = {}
        for i in self.blackboard:
            if self.blackboard[i].cur_state:
                myjson[i] = self.blackboard[i].cur_state
        return myjson

    def details(self):
        myjson = {}
        for i in self.blackboard:
            myjson[i] = self.blackboard[i].to_json()
        myjson['_reset_times'] = self.reset_times
        myjson['_reset_acts'] = self.reset_acts
        return myjson


class StreamProcessor(object):
    ignore_msgids = [
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

    def __init__(self, dmap):
        self.dmap = dmap
        self.filename = dmap.get_log()
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        self.comps = {}
        self.datasets = {}
        self.counts = {
            'total' : 0,
            'white_noise' : 0,
            'reduced' : 0,
            'actionable' : 0
        }
        self.blackboard = SystemBlackboard()
        self.parser = Parser(dmap.tnames)

    def _build_msg(self, entry, prefix, json_obj):
        for i in entry:
            json_obj.update(entry.attrib)
            if len(i): self._build_msg(i, prefix + [i.tag], json_obj)
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

    def parse(self):
        for i in self.root:
            # Flatten entry
            msg = self._build_msg(i, [], {})
            self.counts['total'] += 1 

            # Ignore Messages 
            if msg['MessageID'] in self.ignore_msgids:
                self.counts['white_noise'] += 1
                continue

            # Normalize Message
            if type(msg['Message']) == list:
                msg['Message'] = "::".join(msg['Message'])

            if 'MessageArgs.Arg' not in msg:
                msg['MessageArgs.Arg'] = []
            elif type(msg['MessageArgs.Arg']) != list:
                msg['MessageArgs.Arg'] = [msg['MessageArgs.Arg']]

            dprint("{0}:{1}::{2}".format(msg['Sequence'], msg['Timestamp'], msg['Message']))

            parsed_msg = self.parser.parse_message(msg['Message'], 'XYZ', msg['MessageArgs.Arg'])
            msg['Components'] = list(set(msg['MessageArgs.Arg']))
            # parsed_msg[0] => noun phrase, parsed_msg[1] => verb_phrase

            isTerminal, isEnd, isInit = self.parser.check_state(parsed_msg[1])

            # Handle Reboot scenarios. This will reset all the state machines!
            # Need to handle this, otherwise, there will be spurious transitions
            if parsed_msg[0] == "system" and isTerminal:
                self.blackboard.update_state_all('<SYS_TURN_OFF>', 
                    msg['Timestamp'], isTerminal)
                print("===== updated blackboard")
                jprint(self.blackboard.to_json())
                print("===== updated blackboard ends")
            else:
                if self.blackboard.update_state(parsed_msg[0],parsed_msg[1],
                        msg['Timestamp'], isTerminal):
                    print("===== updated blackboard")
                    jprint(self.blackboard.to_json())
                    print("===== updated blackboard ends")

        print("===== final blackboard")
        jprint(self.blackboard.to_json())
        jprint(self.blackboard.details())
        print("===== final blackboard ends")

myd=3

if myd == 1:
    eemi = EEMI()
    #jprint(eemi.output)
    jprint(list(eemi.act_words))
if myd == 2:
    msg = "an under voltage fault detected power supply number"
    pp = Parser()
    print(pp.parse_message(msg))
if myd == 3:
#for i in glob.glob('../omdata/Store/Master/Server/*/*log.xml')[0:3]:
    logfile ='../omdata/Store/Master/Server/100.96.24.187/log.xml'
    logfile ='../omdata/Store/Master/Server/100.96.45.225/SRVTAG-log.xml'
    #logfile ='./187/log.xml'
    print(logfile)
    directory = os.path.split(logfile)[0]
    server_name = os.path.split(directory)[1]
    dmap = DeviceMapper(directory, server_name)
    dmap.build_name_map()
    s = StreamProcessor(dmap)
    s.parse()
