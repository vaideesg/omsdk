import xml.etree.ElementTree as ET
import re
import json
from  datetime import datetime
import zipfile, io, gzip, os, shutil, glob



#1. Load Dictionary
class Dictionary(object):
    def __init__(self, directory):
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
                #('host system is', 'Host.System.1'),
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
                "fans",
                "processing of update packages",
                "factory default settings",
                "network link",
                "license"
                ]:
            c = ".".join([i[0].upper()+i[1:] for i in ent_n.split()])
            self.update_lookup(c, ent_n)
        self.do_sort_byname()

    def sp_clean(self, msg):
        return msg

    def do_sort_byname(self):
        self.names = sorted(set(list(self.tnames.keys()) + self.verbs))
        i = 0
        while i < len(self.names):
            for j in range(i+1, len(self.names)):
                if self.names[i] in self.names[j]:
                    # move to end!
                    self.names.append(self.names[i])
                    del self.names[i]
                    i = i - 1
                    break
            i = i+1

    def update_lookup(self, ent_key, ent_n):
        if ent_key not in self.fqdds:
            #TODO: Assumption 1 entry is fqdd!
            if type(ent_n) == list:
                ent_n = ent_n[0] if len(ent_n) else ent_key
            ent_n = ent_n.lower()
            if ent_n in ['ac', 'system']:
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

    def _replace(self, final_msg, names, tnames, comps, tverbs, state):
        for k in names:
            end_count = len(final_msg)
            midx = 0
            while midx < end_count:
                if k in final_msg[midx]:
                    if k in tnames:
                        if tnames[k] not in comps and tnames[k] != 'NotFound.1':
                            comps.append(tnames[k])
                    elif k in tverbs:
                        if tverbs[k] not in comps and tverbs[k] != 'NotFound.1':
                            state.append(tverbs[k])

                    prev_part = final_msg[midx][0:final_msg[midx].index(k)].strip()
                    end_part = final_msg[midx][final_msg[midx].index(k)+len(k):].strip()
                    if prev_part != "":
                        final_msg[midx] = prev_part
                    else:
                        del final_msg[midx]
                        midx -= 1
                    if end_part != "":
                        final_msg.insert(midx+1, end_part)
                    end_count = len(final_msg)
                midx += 1
        return True

    def lookup_collect_and_replace(self, msg, fqdd, msgarg, m=None):
        if self.discover_comps(msg) or self.update_lookup(fqdd, msgarg):
            self.do_sort_byname()
        comps = []
        state = []
        final_msg = [msg]
        self._replace(final_msg, self.names, self.tnames, comps, self.tverbs, state)

        if fqdd not in comps and fqdd != 'NotFound.1':
            comps.append(fqdd)

        stop_words = ['.', 'the', 'requested', 'was', 'were', 'on', 'from', 'to', 'feature', 'for']
        msg = "/".join([i for i in final_msg if i not in stop_words])
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
        'USR0030', 'LOG007', 'LOG203',
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

    def __init__(self, filename, comps = {}):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        self.comps = comps
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
            if type(msg['MessageArgs.Arg']) != list:
                msg['MessageArgs.Arg'] = [msg['MessageArgs.Arg']]

            if 'FQDD' not in msg:
                args = msg['MessageArgs.Arg']
                if len(args):
                    msg['FQDD'] = args[0]
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

            comp = "//".join(msg['Components'])
            if comp not in self.comps:
                self.comps[comp] = {
                    #State, MessageID, TS  Sev M   MA
                    'State' : [],
                    'MessageID' : [],
                    "Timestamp" : [],
                    "Severity" : [],
                    "Message" : [],
                    "MessageArgs.Arg" : []
                }
            self.comps[comp]['State'].append("-".join(msg['State']))
            self.comps[comp]['MessageID'].append(msg['MessageID'])
            self.comps[comp]['Timestamp'].append(msg['Timestamp'])
            self.comps[comp]['Severity'].append(msg['Severity'])
            self.comps[comp]['MessageArgs.Arg'].append("-".join(msg['MessageArgs.Arg']))
            self.comps[comp]['Message'].append(msg['Message'])

            #if str(msg['Components']) not in self.comps:
            #    self.comps[str(msg['Components'])] = []
            #self.comps[str(msg['Components'])].insert(0, [msg['State'],
            #        msg['MessageID'], msg['Timestamp'],
            #        msg['Severity'], msg['Components'], msg['Message'],
            #        msg['MessageArgs.Arg']])

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
                if end and 'Z' in end:
                    end = end[0:end.rindex('Z')]
                if end and 'z' in end:
                    end = end[0:end.rindex('z')]
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
comps = {}
for i in glob.glob('../omdata/Store/Master/Server/*/*log.xml')[4:6]:
    print(i)
    directory = os.path.split(i)[0]
    dmap = DeviceMapper(directory, dictionary)
    dmap.build_name_map()
    stream = LogStream(dmap.get_log(), comps)
    stream.parse(dmap)

Transitions = {

    'iDRAC.Embedded.1' : {
        "states" : [
            "System.Hardreset",
            "System.Powercycle",
            "System.Powerdown",
            "System.Powerup",
            "System.Graceful.Shutdown",
        ],
        "init" : [
            "System.Hardreset",
            "System.Powercycle",
            "System.Powerdown",
            "System.Powerup",
            "System.Graceful.Shutdown",
            ],
        "terminal" : [
            "System.Powerup",
        ],
        "transitions" : {
            "System.Hardreset" : ['System.Powerup'],
            "System.Powercycle" : ['System.Powerup'],
            "System.Powerdown" : ['System.Powerup'],
            "System.Powerup" : ['System.Powerup'],
            "System.Graceful.Shutdown" : ['System.Powerup'],
        }
    },
    'Background.Initialization' : {
        "states" : [ 'Has.Started', 'Has.Completed', 'Was.Cancelled'],
        "init" : [ 'Has.Started' ],
        "terminal" : [ 'Has.Completed', 'Was.Cancelled'],
        "transitions" : {
            "Has.Started" : [ "Has.Completed", "Was.Cancelled" ],
        }
    },
    'System.1//' : {
        "states" : [
            'Turning.On',
            'Turning.Off',
            'Performing.A.Lpc.Reset',
            'Powering.On',
            'Powering.Off'
        ],
        "init" : [
            'Turning.Off',
            'Performing.A.Lpc.Reset',
            'Powering.Off'
            ],
        "terminal" : [
            'Turning.On',
            'Performing.A.Lpc.Reset',
            'Powering.On'
        ],
        "transitions" : {
            'Turning.Off' : [ 'Turning.On'],
            'Powering.Off' : [ 'Powering.On' ],
        }
    },
    'Auto.Discovery//' : {
        "states" : [ 'Licensed', 'Disabled', 'Enabled'],
        "init" : [ 'Licensed', 'Enabled' ,'Disabled'],
        "terminal" : [ 'Licensed', 'Enabled' ],
        "transitions" : {
            'Licensed' : [ 'Disabled', 'Enabled'],
            'Disabled' : [ 'Disabled', 'Enabled' ]
        }
    },
    "Chassis//": {
        "states" : [ 
            "Is.Open.While.The.Power.Is.On",
            "Is.Closed.While.The.Power.Is.Off",
            "Is.Closed.While.The.Power.Is.On",
            "Is.Open.While.The.Power.Is.Off"
        ],
        "init" : [ 
            "Is.Open.While.The.Power.Is.On",
            "Is.Open.While.The.Power.Is.Off"
        ],
        "terminal" : [ 
            "Is.Closed.While.The.Power.Is.Off",
            "Is.Closed.While.The.Power.Is.On",
        ],
        "transitions" : {
            "Is.Open.While.The.Power.Is.On" : [
                "Is.Closed.While.The.Power.Is.Off",
                "Is.Closed.While.The.Power.Is.On",
                "Is.Open.While.The.Power.Is.Off"
            ],
            "Is.Open.While.The.Power.Is.Off" : [
                "Is.Open.While.The.Power.Is.On",
                "Is.Closed.While.The.Power.Is.Off",
                "Is.Closed.While.The.Power.Is.On",
            ]
        }
    }
}

c_stats = { }
for i in comps:
    found = None
    for abc in Transitions:
        if ('/' in abc and abc in i) or abc == i: 
            found = abc
            break
    if not found: continue
    print("********** {0} ************".format(found))

    if found not in c_stats:
        c_stats[found] = {
            'found' : found,
            'state' : None,
            'time' : None,
            's1' : 0, 's2' :0, 's3' : 0, 's4' : 0, 's5' : 0, 's6' : 0, 's7' : 0,
            'times' : []
        }
    for j in range(0, len(comps[i]['State'])):
        # none => init
        if c_stats[found]['state'] is None:
            if comps[i]['State'][j] not in Transitions[found]['init']:
                c_stats[found]['s1'] += 1
                print('{0}> is not an init state! Ignoring!'.format(
                       comps[i]['State'][j]))
            elif comps[i]['State'][j] not in Transitions[found]['transitions']:
                if comps[i]['State'][j] not in Transitions[found]['terminal']:
                    c_stats[found]['s2'] += 1
                    print('no transition from {0} is found! Ignoring!'.format(
                       comps[i]['State'][j]))
                else:
                    c_stats[found]['s3'] += 1
                    print("==== self-terminal-state:" + comps[i]['State'][j])
            else:
                print("==== started")
                c_stats[found]['state'] = comps[i]['State'][j]
                c_stats[found]['time'] = comps[i]['Timestamp'][j]
                print(" Entering " + c_stats[found]['state'])
            continue
            # what to do?
        if comps[i]['State'][j] not in Transitions[found]['transitions'][c_stats[found]['state']]:
            c_stats[found]['s4'] += 1
            print('no transition from {0} to {1} is found! Ignoring!'.format(
                       c_stats[found]['state'], comps[i]['State'][j]))
            continue
        # no transitions out of that state and also not terminal state! Ignore
        if comps[i]['State'][j] not in Transitions[found]['transitions'] and \
            comps[i]['State'][j] not in Transitions[found]['terminal']:
            c_stats[found]['s5'] += 1
            print('no transition from {0}! Ignoring!'.format(
                       comps[i]['State'][j]))
            continue
        # valid transition found!
        sec = stream.compute_days_since(comps[i]['Timestamp'][j], c_stats[found]['time'])
        c_stats[found]['times'].append(
            [c_stats[found]['state'], comps[i]['State'][j], sec]
        )
        c_stats[found]['state'] = comps[i]['State'][j]
        c_stats[found]['time'] = comps[i]['Timestamp'][j]
        print('moving to ' + c_stats[found]['state'] + " in " + str(sec) + " seconds")
        if c_stats[found]['state'] in Transitions[found]['terminal']:
            c_stats[found]['s6'] += 1
            # if reached the terminal state switch to None
            c_stats[found]['state'] = None
            c_stats[found]['time'] = None
            print("==== closed")
        c_stats[found]['s7'] += 1
    print("**************************************************")

#print(json.dumps(comps, sort_keys=True, indent=4, \
#        separators=(',', ': ')))
for found in c_stats:
    if c_stats[found]['state'] is None: continue
    for state in Transitions[c_stats[found]['found']]['transitions'][c_stats[found]['state']]:
        if state in Transitions[c_stats[found]['found']]['terminal']:
            print("{0} Current={1}, Proposed={2}".format(found, c_stats[found]['state'],state))

print(json.dumps(c_stats, sort_keys=True, indent=4, \
        separators=(',', ': ')))

def _summary(comps):
    states = {}
    for i in comps:
        states[i] = {
            'State' : list(set(comps[i]['State'])),
            'MessageID' : list(set(comps[i]['MessageID']))
        }

    print(json.dumps(states, sort_keys=True, indent=4, \
        separators=(',', ': ')))
