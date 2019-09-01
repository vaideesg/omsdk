import xml.etree.ElementTree as ET
import re
import json
from  datetime import datetime
import zipfile, io, gzip, os, shutil, glob


def dprint(msg):
    pass
def jprint(msg):
    print(json.dumps(msg, sort_keys=True, indent=4, \
            separators=(',', ': ')))

#1. Load Dictionary
class Dictionary(object):
    def __init__(self, directory):
        self.tverbs = {}
        self.build_verb_map()
        self.build_transition_map()

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

    def build_transition_map(self):
        with open(os.path.join('omsdktest', 'transitions.json'), 'r') as f:
            self.transitions = json.load(f)

#2. Device Load
class DeviceMapper(object):
    def __init__(self, directory, dictionary, srvname = ""):
        self.directory = directory
        self.ipaddr = re.sub('\\\\.*$', '', re.sub('.*Master/Server.', '', directory))
        self.devicejson = {}
        self.tnames = {}
        self.fqdds = {}
        self.verbs = dictionary.verbs
        self.tverbs = dictionary.tverbs
        self.transitions = dictionary.transitions
        self.server_name = srvname

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



    def process(self):
        oldrec = {}
        for i in self.comps:
            for tupl in self.maplist:
                for l in tupl:
                    oldrec[l] = None

            self.counts['reduced'] += 1
        
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


class StreamProcessor(object):
    DEF_S = {
        "P_1" : {
            "states" : [ "New.Device.Detected",
                "Not.Detected", 
                "Has.A.Thermal.Trip.(over-temperature).Event",
                "Is.Inserted",
                "Has.Encountered.An.Error",
                "Were.Restored",
                "Is.Removed",
                "Is.Installed",
                "Predictive.Failure.Reported.For",
                "Expires.In",
                "Expired",
                "Are.Redundant",
                "Detected",
                "Is.Offline",
                "Is.Online",
                "Created",
                "Deleted",
                "Was.Reset",
                "Has.Started-Initializing",
                ],
            "init" : [  ],
            "terminal" : [
                "New.Device.Detected",
                "Is.Inserted",
                "Is.Installed",
                "Detected",
                "Were.Restored",
                "Expires.In",
                "Expired",
                "Predictive.Failure.Reported.For",
                "Are.Redundant",
                "Is.Offline",
                "Is.Online",
                "Created",
                "Deleted",
                "Was.Reset",
                "Has.Started-Initializing",
           ],
            "info" : [  "New.Device.Detected" ],
            "transitions" : {
            }
        },
        "P_Fan"  : {
            "states" : [
                "Not.Present",
                ],
            "init" : [  ],
            "terminal" : [
            ],
            "info" : [  ],
            "transitions" : {
            }

        },
        "BGI_Op"  : {
            "states" : [
                "Has.Started",
                "Has.Completed",
                "Completed",
                "Started",
                "Completed.A.Charge.Cycle",
                "Is.Operating.Normally",
                ],
            "init" : [  ],
            "terminal" : [
                "Has.Completed",
                "Completed",
                "Completed.A.Charge.Cycle",
                "Is.Operating.Normally",
            ],
            "info" : [  ],
            "transitions" : {
                "Has.Started" : [ "Has.Completed", "Completed" ],
                "Started" : [ "Has.Completed", "Completed" ],
            }

        },
        "P_Threshold"  : {
            "states" : [
                "Is.Less.Than-Lower.Warning-Threshold",
                "Is.Less.Than-Lower.Critical-Threshold",
                "Is.Greater.Than-Higher.Warning-Threshold",
                "Is.Greater.Than-Higher.Critical-Threshold",
                "Is.Within-Normal",
                "Normal"
                ],
            "init" : [  ],
            "terminal" : [
                "Is.Within-Normal",
                "Normal",
            ],
            "info" : [  ],
            "transitions" : {
                "Is.Less.Than-Lower.Warning-Threshold" : [ "Normal", "Is.Within-Normal" ],
            }

        },
        "P_KK_T" : {
            "states" : [
                "Is.Lost",
                "Restored",
                ],
            "init" : [  ],
            "terminal" : [
                "Restored",
           ],
            "info" : [  ],
            "transitions" : {
                "Is.Lost" : [ "Restored" ],
            }
        },
        "__Network.Link" : {
            "states" : [ "Is.Down", "Is.Started", "Is.Up" ],
            "init" : [ "Is.Down", "Is.Started" ],
            "terminal" : [  ],
            "transitions" : {
                "Is.Down" : [ "Is.Up", "Is.Started" ],
                "Is.Started" : [ "Is.Up", "Is.Down" ]
            }
        },
        "P_SS" : {
            "states" : [ "Ip.Address.Changed.From" ],
            "init" : [  ],
            "terminal" : [  "Ip.Address.Changed.From" ],
            "info" : [  "Ip.Address.Changed.From" ],
            "transitions" : { }
        },
        "P_5" : {
            "states" : [ "Is.Not.Connected,.Or.Is.Improperly.Connected" ],
            "init" : [ "Is.Not.Connected,.Or.Is.Improperly.Connected" ],
            "terminal" : [   ],
            "transitions" : { }
        },
        "iDRAC.Embedded.1//rac_active_directory_authentication" : {
            "states" : [ "Disabled" ],
            "init" : [  ],
            "terminal" : [  "Disabled" ],
            "info" : [  "Disabled" ],
            "transitions" : { }
        },
        "P_2" : {
            "states" : [
                "Deleted-Successfully",
                "Exported-Successfully",
                "Completed-Successfully"
            ],
            "init" : [  ],
            "terminal" : [
                "Deleted-Successfully",
                "Exported-Successfully",
                "Completed-Successfully"
            ],
            "info" : [  ],
            "transitions" : { }
        }
    }
    s_comps = [
        'RAC Active Directory authentication',
        'power management firmware'
    ]

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
        self.blackboard = {}
        self.statistics = {}

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
                #if end and 'Z' in end:
                #    end = end[0:end.rindex('Z')]
                #if end and 'z' in end:
                #    end = end[0:end.rindex('z')]
                end=end[0:19]
                end = datetime.fromtimestamp(
                        datetime.strptime(end, date_format).timestamp())
        return int((end-start).seconds)

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

    def _dprint(self, perror, msg):
        if perror: print(msg)

    def reset_blackboard(self, record):
        k = [i for i in self.blackboard]
        print("Resetting blackboard. Faking as if it has reached final state!!!")
        for comp in self.blackboard:
            self.statistics[comp][self.blackboard[comp]]['t'].append(record['Timestamp'])
            if len(self.statistics[comp][self.blackboard[comp]]['t']) >= 2:
                nlist = self.statistics[comp][self.blackboard[comp]]['t'][-2:]
                self.statistics[comp][self.blackboard[comp]]['s'].append(self.compute_days_since(nlist[0], nlist[1]))
        for comp in k:
            del self.blackboard[comp]

    def build_blackboard(self, trans, comp, record, perror=True):
        if comp not in self.statistics:
            self.statistics[comp] = { }
        if record['StateX'] in trans['terminal']:
            if comp in self.blackboard:
                print("Reached terminal state. Removing from backboard")
                self.statistics[comp][self.blackboard[comp]]['t'].append(record['Timestamp'])
                if len(self.statistics[comp][self.blackboard[comp]]['t']) >= 2:
                    nlist = self.statistics[comp][self.blackboard[comp]]['t'][-2:]
                    self.statistics[comp][self.blackboard[comp]]['s'].append(self.compute_days_since(nlist[0], nlist[1]))
                del self.blackboard[comp]
                return True
            else:
                self._dprint(False, "Already in terminal state. No action")
                return False
        # what to do with this state?
        #print(record['StateX'] in trans['init'])
        if comp not in self.blackboard:
            print("Entering " + comp + " into blackboard")
            self.blackboard[comp] = record['StateX']
            if record['StateX'] not in self.statistics[comp]:
                self.statistics[comp][record['StateX']] = { 't' : [], 's' : [] }
            self.statistics[comp][record['StateX']]['t'].append(record['Timestamp'])
            return True

        #if record['StateX'] in trans['transitions']:
        if self.blackboard[comp] in trans['transitions']:
            to_states = trans['transitions'][self.blackboard[comp]]
            if record['StateX'] in to_states:
                print("Moving " + comp + " to new state " + record['StateX'])
                if record['StateX'] not in self.statistics[comp]:
                    self.statistics[comp][record['StateX']] = { 't' : [], 's' : [] }
                self.statistics[comp][record['StateX']]['t'].append(record['Timestamp'])
                self.statistics[comp][self.blackboard[comp]]['t'].append(record['Timestamp'])
                if len(self.statistics[comp][self.blackboard[comp]]['t']) >= 2:
                    nlist = self.statistics[comp][self.blackboard[comp]]['t'][-2:]
                    self.statistics[comp][self.blackboard[comp]]['s'].append(self.compute_days_since(nlist[0], nlist[1]))
                self.blackboard[comp] = record['StateX']
                return True
            else:
                self._dprint(perror, "ERROR: " + comp + " invalid new state : " + self.blackboard[comp] + ", " + record['StateX'] + " cannot be performed")
                # TODO Don't update. Ask for state transitions update
        else:
            self._dprint(perror, "ERROR: " + comp + " No transitions out of blackboard state: " + self.blackboard[comp] + ", " + record['StateX'] + " cannot be performed")
            # TODO Don't update. Ask for state transitions update
        return False


    def parse(self):
        for i in self.root:
            # Flatten entry
            msg = self.build_entry(i, [], {})
            self.counts['total'] += 1 

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
                self.counts['white_noise'] += 1
                continue
            print(":::::" + msg['MessageID'] + "::"+ msg['Message'])

            msg['Message'] = msg['Message'].lower()

            msg['Message'] = self.sp_cleanse(msg['Message'])
            # enrich

            msg['Components'], msg['State'], msg['Message'] = \
                self.dmap.lookup_collect_and_replace(msg['Message'],
                    msg['FQDD'], msg['MessageArgs.Arg'], msg)


            for scomp in self.s_comps:
                if scomp.lower() in msg['Message']:
                    msg['Components'].append(scomp.lower().replace(' ', '_'))

            comp = "//".join(msg['Components'])
            msg['StateX'] = "-".join(msg['State'])

            if msg['MessageID'] in [ 'SYS1001']: #, 'SYS1003'] :
                print("==== resetting blackboard")
                self.reset_blackboard(msg);
                continue

            if msg['StateX'] == "" or comp == "":
                jprint(msg)
                self._dprint(True, "ERROR: Empty state: {1} for {0}".format(comp, msg['StateX']))
                continue

            #if msg['MessageID'] in ['PWR2403']:
            #    jprint(msg)

            found_default = False
            for p_ex in self.DEF_S:
                if msg['StateX'] not in self.DEF_S[p_ex]['states']:
                    continue
                if self.build_blackboard(self.DEF_S[p_ex], comp, msg, False):
                    print("===== updated blackboard")
                    jprint(self.blackboard)
                    print("===== updated blackboard ends")
                found_default = True
                break

            if not found_default:
                if comp not in self.dmap.transitions or 'states' not in self.dmap.transitions[comp]:
                    jprint(msg)
                if msg['StateX'] not in self.dmap.transitions[comp]['states']:
                    self._dprint(True, "ERROR: Invalid state: {1} for {0}".format(comp, msg['StateX']))
                    continue
                if self.build_blackboard(self.dmap.transitions[comp], comp, msg, True):
                    print("===== updated blackboard")
                    jprint(self.blackboard)
                    print("===== updated blackboard ends")

        print("===== final blackboard")
        jprint(self.blackboard)
        print("===== final blackboard ends")

dictionary = Dictionary('.')
dprint(",".join(['ipaddr', 'state', 'msgid', 'date', 'sev', 'comps','msg', 'args']))
comps = {}
rcounts = { 'total' : 0, 'white_noise' : 0,
            'reduced' : 0, 'actionable' : 0 }

for i in glob.glob('../omdata/Store/Master/Server/*/*log.xml')[0:3]:
    print("Loading log ..." + i)
    directory = os.path.split(i)[0]
    server_name = os.path.split(directory)[1]
    dmap = DeviceMapper(directory, dictionary, server_name)
    dmap.build_name_map()
    stream = StreamProcessor(dmap)
    print(stream.dmap.server_name)
    stream.parse()
    jprint(stream.statistics)

print("Log loading complete ======")
