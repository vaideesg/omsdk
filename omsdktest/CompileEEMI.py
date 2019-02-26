import pandas as pd
import math
import json
import re

# complementary | resolution!

ss = {
    # different
    'watchdog timer' : 'UEFI',
    'vflash' : 'OSD',

}

# redundancy | spover power redundancy
# memory mirror => redundancy

dictionary = None
with open('../omdata/MsgReg/defn.json') as f:
    dictionary = json.load(f)


cntr = {}
flds = {}
new_recs = {}
f = pd.read_csv('../omdata/MsgRegistry.csv')
for nrec in f.index:
    if type(f['Message'][nrec]) == float and math.isnan(f['Message'][nrec]):
        continue
    msgrec = f['Message'][nrec].lower()
    dorem_start = False
    msgrec = re.sub('[ \t]+', ' ', msgrec.strip())
    nouns = []
    for i in dictionary['nouns']:
        if i in msgrec:
            msgrec = msgrec.replace(i, '')
            nouns.append(i)

    verbs = []
    for i in dictionary['verbs']:
        if i in msgrec:
            msgrec = msgrec.replace(i, '')
            verbs.append(i)

    ops = []
    for i in dictionary['ops']:
        if i in msgrec:
            msgrec = msgrec.replace(i, '')
            ops.append(i)

    subject = "/".join(nouns)
    if len(ops):
        subject = "Operation:" + subject
    if subject not in new_recs:
        new_recs[subject] = []

    new_recs[subject].append(
        '{0},{1},{2},{3}'.\
            format(f['Name'][nrec], "/".join(verbs),
                   "/".join(ops), f['Message'][nrec]))

print(json.dumps(new_recs, sort_keys=True, indent=4, \
          separators=(',', ': ')))
#'"{0}","{1}","{2}","{3}","{4}","{5}","{6}"'.\
#   format(f['Name'][nrec],f['Severity'][nrec],f['Message'][nrec],
#   s, "/".join(verbs), "/".join(ops), "")) ]
