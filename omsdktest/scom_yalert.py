
import xml.etree.ElementTree as ET
import re
import json
from  datetime import datetime

dictionary = {}
with open('s.json') as f:
    dictionary = json.load(f)
tree = ET.parse('log.xml/log.xml')
#tree = ET.parse('t.xml')

names = [
    ("Virtual Disk 0 on Integrated RAID Controller 1", "Disk.Virtual.0:RAID.Integrated.1-1"),
    ("Disk 0 in Backplane 1 of Integrated RAID Controller 1", "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1"),
    ("Disk 1 in Backplane 1 of Integrated RAID Controller 1", "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1"),
    ("Backplane 1 of Integrated RAID Controller 1", "Enclosure.Internal.0-1:RAID.Integrated.1-1"),
    ("Integrated RAID Controller 1", "RAID.Integrated.1-1"),
    ('power supply 2', 'PSU.Slot.2'),
    ('power supply 1', 'PSU.Slot.1'),
    ('process of installing an operating system or hypervisor', 'Install.OS'),
    ('virtual console session', 'vcs')
]

dict_mashup = {}
count = 0
for i in dictionary:
    for j in dictionary[i]:
        idx = j.strip().split(',')
        dict_mashup[idx[0]] = [i] + idx
        if '$' not in idx[0]:
            count = count + 1
            names.append( (idx[0], "{0}-{1}".format("".join([y[0:1] for y in idx[0].split()]),count)) )

# dict_mashup: noun | MsgId | verbs | string

root = tree.getroot()

def build_entry(entry, json_obj):
    for i in entry:
        json_obj.update(entry.attrib)
        if len(i): build_entry(i, json_obj)
        elif i.text:
            if i.tag in json_obj:
                if type(json_obj[i.tag]) != list:
                    json_obj[i.tag] = [json_obj[i.tag]]
                else:
                    json_obj[i.tag].append(i.text.strip())
            else:
                json_obj[i.tag] = i.text.strip()
    return json_obj

ignore_msgids = [
    'USR0030', 'LOG007',

    'USR0031', 'USR0034', 'USR0032', 'RAC1195',
    'USR0002', 'USR0005', 'USR0007', 'USR107',
]
comps = { '_un' : [] }
for i in range(0,len(names)):
    names[i] = (names[i][0].lower(), names[i][1])

for i in root:
    # Build entry
    msg = build_entry(i, {})
    if msg['MessageID'] in ignore_msgids:
        continue

    # enrich
    msg['Components'] = []
    msg['Message'] = msg['Message'].lower()
    for (k,v) in names:
        if k in msg['Message']:
            msg['Components'].append(v)
            msg['Message'] = msg['Message'].replace(k, v)

    argument = '_un:' + msg['MessageID']
    lookup = ''
    if msg['MessageID'] in dict_mashup:
        msgid = re.sub('[0-9]+', '', msg['MessageID'])
        argument = '[^\s]+'
        if '$' in dict_mashup[msg['MessageID']][0]:
            if 'Arg' in msg and type(msg['Arg']) != list:
                argument = msg['Arg'].lower()
        compiler = re.compile(re.sub('\${[^}]+}',
                    argument, dict_mashup[msg['MessageID']][0]))
        match = compiler.search(msg['Message'])
        argument = match.group(0) if match else \
                dict_mashup[msg['MessageID']][0] \
                if dict_mashup[msg['MessageID']][0] != "" else ('_op:' + msgid)
        lookup = dict_mashup[msg['MessageID']][2]
    if argument not in comps:
        comps[argument] = []
    summary = dict_mashup[msg['MessageID']][2] \
            if msg['MessageID'] in dict_mashup else ""

    comps[argument].insert(0, [lookup, summary,
            msg['MessageID'], msg['Timestamp'],
            msg['Severity'], msg['Components'], msg['Message']])

def compute_days_since(start, end=None):
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    start = datetime.fromtimestamp(
            datetime.strptime(start, date_format).timestamp())
    if end is None:
        end = datetime.now()
    else:
        end = datetime.fromtimestamp(
            datetime.strptime(end, date_format).timestamp())
    return int((end-start).seconds)

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

oldrec = {}
datasets = {}
for i in comps:
    for tupl in maplist:
        for l in tupl:
            oldrec[l] = None

    for j in comps[i]:
        sec = 0
        for tupl in maplist:
            done = False
            for l in tupl:
                if l in j[0]:
                    oldrec[l] = j
                    done = True
                    break
            if done: break

        for tupl in maplist:
            if not len(set([l for l in tupl if not oldrec[l]])):
                sec = compute_days_since(oldrec[tupl[0]][3],
                                     oldrec[tupl[1]][3])
                oldrec[tupl[0]] = None
                oldrec[tupl[1]] = None
                s = str(i) + "/" + str(j[5])
                if s not in datasets:
                    datasets[s] = []
                datasets[s].append(sec)
            if tupl[0] in j[0]:
                oldrec[tupl[0]] = None
                oldrec[tupl[1]] = None

        #print("{0},{1},{2} days,{3},{4},{5},{6},{7},{8},{9}".format(
        #        j[0],j[1],j[2],j[3], j[4], j[5], j[6], i,sec))
        print(str(j) + "," + str(i) + "," + str(sec))

print(json.dumps(datasets, sort_keys=True, indent=4, \
          separators=(',', ': ')))
