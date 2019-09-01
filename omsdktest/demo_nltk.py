import nltk
import xml.etree.ElementTree as ET
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re

def jprint(msg):
    print(json.dumps(msg, sort_keys=True, indent=4, \
            separators=(',', ': ')))

class EEMI(object):

    def extract_string(self, ent, doprint_attributes):
        tmsg = ""
        comma = ""
        if doprint_attributes:
            for i in ent.attrib:
                #tmsg += i + "=" + ent.attrib[i] + comma
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
        pp = Parser()
        self.counts = { 'Total' : { "MessageCount" : 0,
                                    "ComponentCount" : 0,
                                    "UnparseCount" : 0} }
        for ent in self.root.findall('.//reg:MESSAGE', ns):
            self.messages[counter] = {}
            self.collect_info(ent, self.messages[counter])
            self.messages[counter]['PHRASES'] = pp.parse_message(
                self.messages[counter]['MESSAGE_COMPONENTS'],
                self.messages[counter]['PREFIX'])
            #if self.messages[counter]['PREFIX'] not in [
            #    'VLT', 'TEMP', 'PDR', 'VDR', 'CTL' ]:
            #    continue

            prefix = self.messages[counter]['PREFIX']
            if prefix not in self.counts:
                self.counts[prefix] = { "MessageCount" : 0,
                                        "ComponentCount" : 0,
                                        "UnparseCount" : 0}

            noun_phrase = self.messages[counter]['PHRASES'][0]
            self.counts[prefix]['MessageCount'] += 1
            self.counts['Total']['MessageCount'] += 1
            if "<UNPARSEABLE>" in noun_phrase:
                self.counts['Total']['UnparseCount'] += 1
                self.counts[prefix]['UnparseCount'] += 1
            if noun_phrase not in self.doit:
                self.doit[noun_phrase] = []
                self.counts[prefix]['ComponentCount'] += 1
                self.counts['Total']['ComponentCount'] += 1
            self.doit[noun_phrase].append(self.messages[counter]['PHRASES'][1])
            counter = counter + 1
        self.output = {}
        for i in self.doit:
            self.output[i] = { "states" : [], "init" : [],
                               "end" : [],
                               "terminal" : [], "transitions" : {} }
            for s in self.doit[i]:
                self.output[i]['states'].append(s)

                isTerminal = False
                isEndState = False
                isInitState = False
                if 'init' in s or 'create' in s or \
                   'start' in s or 'resume' in s:
                   isInitState = True

                for verbs in [ 'restarted', 'restored',
                    'turning on', 'completed']:
                    if verbs in s:
                        isTerminal = True
                        isEndState = True

                for verbs in [ 'failed', 'cancel']:
                    if verbs in s:
                        isEndState = True

                for vblist in [
                    [ 'success', [ 'unsuccess' ] ],
                    [ 'enabled', [ 'not' ] ],
                    [ 'normal', [ 'above', 'below' ] ]
                ]:
                    if vblist[0] not in s:
                        continue
                    isEndState = True
                    for vbs in vblist[1]:
                        if vbs in s:
                            isEndState = False
                    if isEndState:
                        isTerminal = True

                if isTerminal:
                    self.output[i]["terminal"].append(s)
                if isEndState:
                    self.output[i]["end"].append(s)
                if isInitState:
                    self.output[i]["init"].append(s)


            for s in self.output[i]['states']:
                if s in self.output[i]['end']:
                    continue
                self.output[i]['transitions'][s] = []
                for s1 in self.output[i]['states']:
                    if s1 == s: continue
                    self.output[i]['transitions'][s].append(s1)

class Parser(object):

    def __init__(self):
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
            "system graceful shutdown",
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

    def parse_message(self, message, msg_type):
        text = re.sub('[(][^[)]*[)]', '', message.lower())
        text = re.sub('(-[a-zA-Z0-9]) option', 'option \\1', text)
        text = re.sub('\\.$', '', text)
        text = text.replace('hot-spare', 'hot spare')
        text = text.replace("physical_drive_name", "pd_name")
        text = text.replace("virtual_disk", "vd_name")
        text = text.replace("over voltage fault", "voltage fault over")
        text = text.replace("under voltage fault", "voltage fault under")
        text = text.replace("controller cache is preserved", "controller preserved cache")
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

class StreamProcessor(object):
    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.comps = {}
        self.datasets = {}
        self.counts = {
            'total' : 0,
            'white_noise' : 0,
            'reduced' : 0,
            'actionable' : 0
        }
        self.blackboard = {}
        self.statistics = {}

    def build_entry(self, entry, prefix, json_obj):
        for i in entry:
            json_obj.update(entry.attrib)
            if len(i): self.build_entry(i, prefix + [i.tag], json_obj)
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

    def check_state(self, s):
        isTerminal = False
        isEndState = False
        isInitState = False
        if 'init' in s or 'create' in s or \
           'start' in s or 'resume' in s:
           isInitState = True

        for verbs in [ 'restarted', 'restored',
            'turning on', 'completed',
            
            'detected', 'created', 'changed',
            'started', 'exported', 'imported', 'exited',
            'not licensed'
            ]:
            if verbs in s:
                isTerminal = True
                isEndState = True

        for verbs in [ 'failed', 'cancel']:
            if verbs in s:
                isEndState = True

        for vblist in [
            [ 'success', [ 'unsuccess' ] ],
            [ 'enabled', [ 'not' ] ],
            [ 'normal', [ 'above', 'below' ] ]
        ]:
            if vblist[0] not in s:
                continue
            isEndState = True
            for vbs in vblist[1]:
                if vbs in s:
                    isEndState = False
            if isEndState:
                isTerminal = True
        return isTerminal

    def parse(self):
        pp = Parser()
        for i in self.root:
            # Flatten entry
            msg = self.build_entry(i, [], {})
            self.counts['total'] += 1 

            if msg['MessageID'] in self.ignore_msgids:
                self.counts['white_noise'] += 1
                continue

            print(":::::" + msg['Message'])
            msg1 = pp.parse_message(msg['Message'], 'XYZ')
            if self.check_state(msg1[1]):
                print(">>>>> is Terminal")
            else:
                jprint(msg1)


myd=3

if myd == 1:
    eemi = EEMI()
    #jprint(eemi.output)
    jprint(eemi.doit)
if myd == 2:
    msg = "an under voltage fault detected power supply number"
    pp = Parser()
    print(pp.parse_message(msg))
if myd == 3:
    s =StreamProcessor('../omdata/Store/Master/Server/100.96.24.187/log.xml')
    s.parse()
