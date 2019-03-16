import xml.etree.ElementTree as ET
import re
import json
from  datetime import datetime
import zipfile, io, gzip, os, shutil, glob



#1. Load Dictionary
class Dictionary(object):
    def __init__(self, directory):
        self.dictionary = {}
        with open(os.path.join(directory,'s.json')) as f:
            self.dictionary = json.load(f)
        self.dict_mashup = {}
        for i in self.dictionary:
            for j in self.dictionary[i]:
                idx = j.strip().split(',')
                self.dict_mashup[idx[0]] = [i] + idx
        self.tverbs = {}
        self.build_verb_map()

    def do_sort_byname(self, name_to_sort):
        names = sorted(set(name_to_sort))
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

    def build_verb_map(self):
        with open(os.path.join('omsdktest', 'verbs.json'), 'r') as f:
            verbs = json.load(f)
            self.verbs = self.do_sort_byname(verbs['verbs'])
            for i in self.verbs:
                self.tverbs[i] = ".".join([j[0].upper()+j[1:] for j in i.split()])

#2. Device Load
class DeviceMapper(object):
    def __init__(self, directory, dictionary):
        self.directory = directory
        self.ipaddr = re.sub('\\\\.*$', '', re.sub('.*Master/Server.', '', directory))
        self.dictionary = dictionary
        self.devicejson = {}
        self.tnames = {}
        self.fqdds = {}
        self.verbs = dictionary.verbs
        self.tverbs = dictionary.tverbs

    def get_json_device(self):
        with open(os.path.join(directory, 'Key_Inventory_ConfigState.json'), 'r') as f:
            self.devicejson = json.load(f)


    def build_name_map(self):
        self.get_json_device()
        for comp in self.devicejson:
            if comp in ['System']: continue
            for ent in self.devicejson[comp]:
                for n in ['DeviceDescription', 'ElementName',
                          'LicenseDescription', 'Key']:
                    if n in ent:
                        self.update_lookup(ent['Key'], ent[n])
                        break

        for (ent_n,ent_key) in  [
                ('system board intrusion cable or interconnect', 'Cable.Internal.Intrusion'),
                ('power supply 1', 'PSU.Slot.1'),
                ('power supply 2', 'PSU.Slot.2'),
                ('power control', 'iDRAC.Embedded.1#HostPowerCtrl'),
                ('iDRAC-Embedded', 'iDRAC.Embedded.1'),
                ('system-server', 'System.Embedded.1'),
                ('system cpu', 'System.CPU'),
                ('system is', 'System.1'),
                ('disk-direct-ahci', 'Disk.Direct.1-1:AHCI.Slot.7-1'),
                ('cpu 1', 'CPU.Socket.1'),
                ('cpu 2', 'CPU.Socket.2'),
                ('disk drive bay 1', 'Disk.Bay.1-0'),
                ('%na%', 'N/A'),
                ]:
            self.update_lookup(ent_key, ent_n)
        for (ent_n) in  [
                'foreign configuration',
                'chassis',
                'previous configuration',
                'virtual console session',
                'virtual media session',
                'process of installing an operating system or hypervisor',
                'background initialization',
                'auto discovery',
                'configuration',
                'configuration profile',
                'system configuration profile',
                'configuration profile xml file',
                'system configuration profile xml file',
                'patrol read operation',
                'firmware update',
                "bios watchdog timer",
                "os watchdog timer",
                "watchdog timer",
                "system board battery",
                "storage battery",
                "export system profile",
                "vflash backup partition",
                "hardware inventory",
                "lifecycle controller data",
                "backup file",
                "backup file passphrase",
                "system performance",
                "enhanced cooling mode",
                "storage adapter",
                "usb cable",
                "power supplies",
                "processing of update packages"
                ]:
            c = ".".join([i[0].upper()+i[1:] for i in ent_n.split()])
            self.update_lookup(c, ent_n)
        self.names = self.do_sort_byname(self.tnames.keys())

    def sp_clean(self, msg):
        return msg

    def do_sort_byname(self, name_to_sort):
        names = sorted(name_to_sort)
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

    def update_lookup(self, ent_key, ent_n):
        if ent_key not in self.fqdds:
            #TODO: Assumption 1 entry is fqdd!
            if type(ent_n) == list:
                ent_n = ent_n[0] if len(ent_n) else ent_key
            ent_n = ent_n.lower()
            if ent_n in ['ac', 'system', 'license']:
                return False
            self.fqdds[ent_key] = ent_n
            self.tnames[ent_n] = ent_key
            return True
        return False

    def discover_comps(self, msg):
        msg = msg.lower()
        updated = False
        for pattern in [
            '(power|processor|system|memory|disk|cpu)[^.()]*redundancy',
            '(power|processor|system|memory|disk|cpu)[^.()]*module.*temperature',
            '(power|processor|system|memory|disk|cpu)[^.()]*module',
            '(power|processor|system|control|chassis|peripheral|battery|memory|disk|cpu)[^.()]*(voltage|temperature|current)'
        ]:
            rc = re.compile(pattern)
            match = rc.search(msg)
            if not match: continue
            c = ".".join([i[0].upper()+i[1:] for i in match.group(0).split()])
            if self.update_lookup(c, match.group(0)):
                updated = True
        return updated

    def lookup_collect_and_replace(self, msg, fqdd, msgarg, m=None):
        if self.discover_comps(msg) or self.update_lookup(fqdd, msgarg):
            self.names = self.do_sort_byname(self.tnames.keys())
        comps = []
        for k in self.names:
            if k in msg:
                if self.tnames[k] not in comps and self.tnames[k] != 'NotFound.1':
                    comps.append(self.tnames[k])
                msg = msg.replace(k, self.tnames[k])
        if fqdd not in comps and fqdd != 'NotFound.1':
            comps.append(fqdd)
        state = []
        for k in self.verbs:
            if k in msg:
                if k not in state: state.append(k)
                msg = msg.replace(k, self.tverbs[k])
        return comps, state, msg

    def get_log(self):
        logfiles = glob.glob(os.path.join(directory, '*.xml'))
        if len(logfiles) == 0:
            logfiles = [os.path.join(directory, 'dummy.log.xml')]
            with open(logfiles[0], 'w') as f:
                f.write('<LCLogEvents></LCLogEvents>\n')
                f.flush()
        return logfiles[0]


class LogStream(object):
    ignore_msgids = [
        'USR0030', 'LOG007',
        'USR0031', 'USR0034', 'USR0032', 'RAC1195',
        'USR0002', 'USR0005', 'USR0007', 'USR107',
    ]
    maplist = [
    #    ('created', 'deleted'),
        ('started', 'completed'),
        ('created', 'exited'),
        ('is low', 'is operating normally'), #2
        ('returned to a ready state', 'is online'),
        ('is down', 'started'),
        ('turning off', 'turning on'),
        # completed | abruptly stopped'
    ]
    
    # version change detected is bad!
    # [ (detected),
    #    (is lost)
    #    ('auto discovery', disabled) ]
    #    ('was changed')
    # version change detected is good
    # [ (disabled) ]
    #
    # counters:
    #   powerdown,hardreset,powerup,shutdown => requests | frequency
    #   is lost | frequency

    def __init__(self, filename, dictionary):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        self.dictionary = dictionary
        self.comps = { '_un' : [] }
        self.datasets = {}

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

    def sp_cleanse(self, msg):
        msg = re.sub('nic embedded ([^\s]+) port ([^\s]+)',
                     'embedded nic \\1 port \\2 partition 1', msg)
        msg = re.sub('nic mezzanine ([^\s]+) port ([^\s]+)',
                     'nic in mezzanine \\1a port \\2 partition 1', msg)
        return msg


    def parse(self, dmap):
        for i in self.root:
            # Flatten entry
            msg = self.build_entry(i, [], {})

            if type(msg['Message']) == list:
                msg['Message'] = "::".join(msg['Message'])

            if 'MessageArgs.Arg' not in msg:
                msg['MessageArgs.Arg'] = []

            if 'FQDD' not in msg:
                args = msg['MessageArgs.Arg']
                if len(args):
                    msg['FQDD'] = args[0] if type(args) == list else args
                else:
                    msg['FQDD'] = 'NotFound.1'

            msg['Subsystem'] = re.sub('[0-9]+', '', msg['MessageID'])

            if msg['MessageID'] in self.ignore_msgids:
                continue

            msg['Message'] = msg['Message'].lower()

            msg['Message'] = self.sp_cleanse(msg['Message'])
            # enrich

            msg['Components'], msg['State'], msg['Message'] = \
                dmap.lookup_collect_and_replace(msg['Message'],
                    msg['FQDD'], msg['MessageArgs.Arg'], msg)

            if str(msg['Components']) not in self.comps:
                self.comps[str(msg['Components'])] = []

            self.comps[str(msg['Components'])].insert(0, [msg['State'],
                    msg['MessageID'], msg['Timestamp'],
                    msg['Severity'], msg['Components'], msg['Message'],
                    msg['MessageArgs.Arg']])

    def compute_days_since(self, start, end=None):
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
            if end and 'Z' in end:
                end = end[0:end.rindex('Z')]
            if end and 'z' in end:
                end = end[0:end.rindex('z')]
            start = datetime.fromtimestamp(
                    datetime.strptime(start, date_format).timestamp())

        if end is None:
            end = datetime.now()
        else:
            end = datetime.fromtimestamp(
                datetime.strptime(end, date_format).timestamp())
        return int((end-start).seconds)

    def process(self):
        oldrec = {}
        for i in self.comps:
            for tupl in self.maplist:
                for l in tupl:
                    oldrec[l] = None
        
            for j in self.comps[i]:
                sec = 0
                for tupl in self.maplist:
                    done = False
                    for l in tupl:
                        if l in j[0]:
                            oldrec[l] = j
                            done = True
                            break
                    if done: break
        
                for tupl in self.maplist:
                    if not len(set([l for l in tupl if not oldrec[l]])):
                        sec = self.compute_days_since(oldrec[tupl[0]][3],
                                            oldrec[tupl[1]][3])
                        oldrec[tupl[0]] = None
                        oldrec[tupl[1]] = None
                        s = str(i) + "/" + str(j[5])
                        if s not in self.datasets:
                            self.datasets[s] = []
                        self.datasets[s].append(sec)
                    if tupl[0] in j[0]:
                        oldrec[tupl[0]] = None
                        oldrec[tupl[1]] = None
        
                #print(str(j) + "," + str(i) + "," + str(sec))


dictionary = Dictionary('.')
print(",".join(['ipaddr', 'state', 'msgid', 'date', 'sev', 'comps','msg', 'args']))
for i in glob.glob('./log.xml'):
#for i in glob.glob('../omdata/Store/Master/Server/*/*log.xml')[0:2]:
    #directory = '../omdata/Store/Master/Server/DVRBR42'
    directory = os.path.split(i)[0]
    dmap = DeviceMapper(directory, dictionary)
    dmap.build_name_map()
    stream = LogStream(dmap.get_log(), dictionary)
    stream.parse(dmap)
    for j in stream.comps:
        for k in stream.comps[j]:
            print(",".join([str(a).replace(',',';') for a in [dmap.ipaddr]+k]))
    #print(json.dumps(stream.comps, sort_keys=True, indent=4, \
    #      separators=(',', ': ')))
    #stream.process()
    #print(json.dumps(stream.datasets, sort_keys=True, indent=4, \
    #      separators=(',', ': ')))
    #print(json.dumps(dmap.tnames, sort_keys=True, indent=4, \
    #      separators=(',', ': ')))
