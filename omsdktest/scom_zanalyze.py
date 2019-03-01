import sys
import os
import json
sys.path.append(os.getcwd())
from datetime import datetime
from datetime import date, timedelta

from sys import stdout, path

import glob
import json
import re

class Enumerator(object):
    def __init__(self):
        self.names = []

    def get_enum(self, name):
        if name not in self.names:
            self.names.append(name)
        return self.names.index(name)+1

class Indexer(object):
    def __init__(self, entity):
        self.indexes = {}
        for i in entity:
            self.indexes[i] = len(entity[i])
        self.names = [i for i in self.indexes]
        self.iterator = {}
        self.initialize()

    def initialize(self):
        for i in self.names:
            self.iterator[i] = 0
        self.iterator[self.names[len(self.names)-1]] = -1

    def nexti(self):
        for i in range(len(self.names)-1,-1,-1):
            self.iterator[self.names[i]] = self.iterator[self.names[i]]+1
            if self.iterator[self.names[i]] < self.indexes[self.names[i]]:
                return True
            self.iterator[self.names[i]] = 0
        return False

    def printx(self):
        print(",".join(["{0}={1}".format(i, self.iterator[i]) for i in self.names]))


class Base(object):
    pass

class FieldCollector(Base):
    def __init__(self, name):
        self.fields = []
        self.name = name

    def op(self, entity, sp_fields=None, scope_fields=None):
        if sp_fields and len(sp_fields) == 0: sp_fields = None
        if scope_fields and len(scope_fields) == 0: scope_fields = None
        for parts in entity:
            if not scope_fields or parts in scope_fields:
                self._op(entity[parts], sp_fields)

    def _op(self, entity, sp_fields):
        for parts in entity:
            if type(parts) is dict:
                self._op(parts, sp_fields)
            elif type(entity[parts]) is dict:
                self._op(entity[parts], sp_fields)
            elif type(entity[parts]) is list:
                for ent in entity[parts]:
                    self._op(ent, sp_fields)
            elif parts not in self.fields:
                self._append(parts, sp_fields)

    def _append(self, field, sp_fields):
        self.fields.append(field)
        if field in sp_fields:
            self.fields.append(field + "_orig")

    @property
    def Fields(self):
        return self.fields

    @property
    def PersistentObject(self):
        return "../omdata/__data/" + self.name + "_fields.txt"

    def serialize(self):
        with open(self.PersistentObject, "w") as f:
            f.write(json.dumps(self.fields, sort_keys=True, indent=4, \
              separators=(',', ': ')))

    def load(self):
        if os.path.exists(self.PersistentObject):
            with open(self.PersistentObject, "r") as f:
                self.fields = json.load(f)


class DataCollector(Base):
    def __init__(self, name, oc):
        self.ipaddr = None
        self.sp_fields = []
        self.entity = {}
        self.enums = oc

    def op(self, join_entries, filter_fields, spec):
        final_it = self.entity

        if join_entries and len(join_entries) > 0:
            final_it = {} 
            for i in join_entries:
                if (i in self.entity):
                    final_it[i] = self.entity[i]

        ix = Indexer(final_it)
        records = []
        while ix.nexti():
            rec = self.collect_row(ix, filter_fields, spec)
            if rec: records.append(rec)
        return records

    def collect_row(self, ix, fields, spec):
        myrec = {}
        origrec = {}
        for t in ix.iterator:
            myrec.update(self.entity[t][ix.iterator[t]])
            origrec.update(self.entity[t][ix.iterator[t]])

        for field in fields:
            value = ""
            if (field.endswith('_orig')):
                field = field.replace('_orig','')
                if (field in origrec and origrec[field]):
                    myrec[field + "_orig"] = str(origrec[field])
                else:
                    myrec[field + "_orig"] = ""
            elif (field in origrec and origrec[field]):
                myrec[field] = self.beautify_field(field, origrec[field])
            elif field == "SREC":
                myrec[field] = "-".join([myrec['DeviceID'],
                            myrec['SubDeviceID'], myrec['VendorID'],
                            myrec['SubVendorID']])
            else:
                myrec[field] = ""

        return myrec if not spec or spec(myrec) else None

    def beautify_field(self, fname, value):
        if value == "Not Available":
            value = "0"
        return self.my_beautify_field(fname, value)

    def my_beautify_field(self, fname, value):
        return str(value)

class DeviceCollector(DataCollector):
    def __init__(self, fname, oc):
        super().__init__('DeviceCollector', oc)
        self.sp_fields = ["FQDD", "Model", "SystemID"]
        ipaddr = re.sub('.*\\\\', '', fname)
        pathdir = re.sub(ipaddr + '$', '', fname)
        self.entity.update({ 'doc.props' : [ { 'IPAddress' : ipaddr } ] })
        for parts in ['Firmware.json', 'Key_Inventory_ConfigState.json']:
            json_path = os.path.join(pathdir, parts)
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    self.entity.update(json.load(f))

    def my_beautify_field(self, fname, value):
        if fname in ['SystemID']:
            value = "000{0:X}".format(int(value))[-4:]
        elif fname in ['FQDD']:
            value = self.enums[fname].get_enum(value.split('.')[0])
        elif fname in ['HostName']:
            if value.lower().startswith('win'):
                value='win'
            elif value.lower().startswith('localhost') or \
                 value.lower().startswith('esx') or \
                 value.lower().startswith('ubuntu'):
                value = 'linux/esx'
            elif value in [ "Not Available", "0"]:
                value = 'bare-metal'
            else:
                value = 'Unknown'
        elif fname in ['VersionString','ComponentID' 'DeviceID',
                       'SubDeviceID', 'SubVendorID', 'VendorID']:
            if value is None: value = ""
            if value == "NULL" : value = ""
        return value

class Objects(object):

    def __init__(self, directory, typeo, join_entries=None, filter_fields=None):
        self.enums = { 'FQDD' : Enumerator() }
        self.objects = []
        for i in glob.glob(directory):
            self.objects.append(typeo(i, self.enums))
        fields = FieldCollector(typeo.__name__)
        for i in self.objects:
            fields.op(i.entity, i.sp_fields, join_entries)
        fields.serialize()

        if not filter_fields:
            filter_fields = fields.Fields
        self.filter_fields = filter_fields

        self.processed = []
        for i in self.objects:
            self.processed.extend(i.op(join_entries, filter_fields, spec))

    def printx(self):
        print(",".join(self.filter_fields))
        for entry in self.processed:
            print(",".join([entry[i] for i in self.filter_fields]))

def spec(obj):
        return True

#store_loc = '../omdata/Store'
store_loc = 'Store.100'
dev = Objects(store_loc + '/Master/*/*/100*', DeviceCollector,
        join_entries = ['Firmware', 'System', 'doc.props'],
        filter_fields = [ 'IPAddress',
            'LifecycleControllerVersion',

            'Model',
            'FQDD_orig',
            'HostName',

            'FQDD',
            'SystemID',
            'ComponentID',
            'DeviceID',
            'SubDeviceID',
            'VendorID',
            'SubVendorID',
            'SREC',

            'VersionString',
            'InstallationDate',
       ])

fnames = []
fnames.extend(dev.filter_fields)
#fnames.extend(['dd','max_id', 'max_vs', 'prev_id','prev_vs','eql_id', 'eql_vs',
#               'eql>max', 'eql<min', 'min<max'])
fnames.extend(['max_id', 'max_vs', 'max_id_min', 'dt_base_i', 'FWIndicator'])
fnames.extend(['attributes','Vulnerability','Security','Availability','Performance','Reliability','dt_base', 'diff_eql_max' ])

fw_fields = {}
fw_anal_fields = {}
with open('../omdata/SDKRepo/PDK.json', "r") as f:
    fw_fields = json.load(f)

with open('../omdata/SDKRepo/T.json', "r") as f:
    fw_anal_fields = json.load(f)

def cmpx(i, j):
    if (i == j):
        return "equal"
    elif i < j:
        return "less"
    else:
        return "great"

def cmp_vers(device, catalog, msg):
    i_vers = device
    i_vers1 = None
    if i_vers.startswith('OSC_'):
        i_vers = re.sub('OSC_', '', i_vers)
    if re.match('^[0-9.-]+$', i_vers):
        i_vers1 = [int(i) for i in i_vers.replace('-','.').split('.')]

    j_vers = catalog
    j_vers1 = None
    if j_vers.startswith('OSC_'):
        j_vers = re.sub('OSC_', '', j_vers)
    if re.match('^[0-9.-]+$', j_vers):
        j_vers1 = [int(i) for i in j_vers.replace('-','.').split('.')]

    if not i_vers1 or not j_vers1:
        i_vers1 = device
        j_vers1 = catalog
    
    if msg == "<":
        return i_vers1 < j_vers1
    elif msg == ">":
        return i_vers1 > j_vers1
    elif msg == "<=":
        return i_vers1 <= j_vers1
    elif msg == ">=":
        return i_vers1 >= j_vers1
    elif msg == "==":
        return i_vers1 == j_vers1
    else:
        print(">>>>>>")

def doprint(data):
    print(data)

def difference(d1, d2 = None):
    if d1 == "99.99.99":
        return 999999
    if d2 is None:
        return 400

    today = date.today()
    t = [int(j) for j in d1.split('.')]
    catd1 = today.replace(2000+t[0], t[1], t[2]+15)
    t = [int(j) for j in d2.split('.')]
    catd2 = today.replace(2000+t[0], t[1], t[2]+15)
    return (catd1-catd2).days

doprint(",".join(fnames))
for dev_fw in dev.processed:
    for d in ['ComponentID', 'DeviceID', 'SubDeviceID',
            'SubVendorID', 'VendorID']:
        if d not in dev_fw or not dev_fw[d]: dev_fw[d] = ""
        if dev_fw[d] == '0': dev_fw[d] = ""
        if dev_fw[d] == 'NULL': dev_fw[d] = ""

    t1 = "{0}-{1}".format(dev_fw['SystemID'], dev_fw['ComponentID'])
    if t1 not in fw_fields:
        t1 = "{0}-{1}-{2}-{3}-{4}-{5}".format(
            dev_fw['SystemID'], dev_fw['ComponentID'],
            dev_fw['DeviceID'], dev_fw['SubDeviceID'],
            dev_fw['VendorID'], dev_fw['SubVendorID'])
    if t1 not in fw_fields:
        t1 = "-{0}".format(dev_fw['ComponentID'])

    if t1 not in fw_fields:
        t1 = "-{0}-{1}-{2}-{3}-{4}".format(
            dev_fw['ComponentID'],
            dev_fw['DeviceID'], dev_fw['SubDeviceID'],
            dev_fw['VendorID'], dev_fw['SubVendorID'])

    if t1 not in fw_fields:
        t1 = "--{0}-{1}-{2}-{3}".format(
            dev_fw['DeviceID'], dev_fw['SubDeviceID'],
            dev_fw['VendorID'], dev_fw['SubVendorID'])
    if t1 not in fw_fields:
        t1 = "?"

    dev_fw['FWIndicator'] = t1

    if t1 not in fw_fields:
        dev_fw['diff_eql_max'] = 'No-Update-Found'
        dev_fw['dt_base_i'] = -999999
        dev_fw['dt_base'] = -999999
        doprint(",".join([str(dev_fw[k]) if k in dev_fw else "" for k in fnames]))
        continue

    imin = None
    imax = None
    exact = None

    for (k, v) in [ ('VersionString', 'vendorVersion')]:
      imin = None
      imax = None
      exact = None
      dev_fw['attributes'] = ""
      for ent in fw_fields[t1]['_plist']:
        cat_fw = fw_fields[t1][ent]
        isequal = False
        if (cmp_vers(dev_fw[k], cat_fw[v], "==")):
            if not exact or cmp_vers(exact['catalog_version'], cat_fw['catalog_version'], "<"):
                exact = cat_fw
                isequal = True
        if (cmp_vers(dev_fw[k], cat_fw[v], "<=")):
            if not isequal:
                dev_fw['attributes']+=","+fw_anal_fields[ent]['Attributes']
            if not isequal and 'Vulnerability' in fw_anal_fields[ent]:
                dev_fw['attributes']+=",[0]" + fw_anal_fields[ent]['Vulnerability']
            if not imax or cmp_vers(imax['catalog_version'], cat_fw['catalog_version'], "<"):
                imax = cat_fw
        if (cmp_vers(dev_fw[k], cat_fw[v], ">=")):
            if not imin or cmp_vers(imin['catalog_version'], cat_fw['catalog_version'], "<"):
                imin = cat_fw

    # 4: 063A--165F-0639-14E4-1028 : 7.10 in 2018-07; 20.6.52 in 18.03
    # max version=GA6E; installed GA6C
    dev_fw['attributes'] = list(set(dev_fw['attributes'].split(',')))
    for at in dev_fw['attributes']:
        if at[3:] == '': continue
        if at[3:].startswith('CVE-'):
            at = "[0]Vulnerability"
        if at[3:] not in dev_fw:
            dev_fw[at[3:]] = 0
        dev_fw[at[3:]] += 1

    dev_fw['attributes'].sort()
    dev_fw['attributes'] = ":".join(dev_fw['attributes'])


    dev_fw['max_id'] = imax['max_cat'] if imax else "99.99.99"
    dev_fw['max_id_min'] = imax['min_cat'] if imax else "99.99.99"
    dev_fw['max_vs'] = imax['vendorVersion'] if imax else "99.99.99"
    dev_fw['eql_id'] = exact['max_cat'] if exact else "00.00.00"
    dev_fw['eql_vs'] = exact['vendorVersion'] if exact else "00.00.00"
    dev_fw['prev_id'] = imin['max_cat'] if imin else "00.00.00"
    dev_fw['prev_vs'] = imin['vendorVersion'] if imin else "00.00.00"
    min_catalog = "18.03.00"

    # X-Rev was applied
    if dev_fw['max_id'] == "99.99.99":
        # eql_id will always be 00.00.00
        # prev_id == 00.00.00 => is it not_found?
        #        update present, it will always be < max_id
        dev_fw['diff_eql_max'] = 'X-Rev'
        dev_fw['dt_base_i'] = 999999
        dev_fw['dt_base'] = difference(dev_fw['max_id'])

    # At the latest!
    elif dev_fw['max_id'] == dev_fw['eql_id']:
        dev_fw['diff_eql_max'] = 'At-Latest'
        dev_fw['dt_base_i'] = 888888
        dev_fw['dt_base'] = 0
    # Update released after a year!!!
    elif dev_fw['eql_id'] == "00.00.00" and dev_fw['prev_id'] == "00.00.00":
        value = dev_fw['InstallationDate']
        # Baseline to start of century
        if value.startswith("19"): value="2000-01-01T01:00:00Z"
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        value = datetime.strptime(value, date_format).strftime('%y.%m.00')
        # if not_updated_since == 0 & version != latest | hidden IPS version
        if (min_catalog > value):
            dev_fw['diff_eql_max'] = 'Update-After-Multiple-Years'
        else:
            dev_fw['diff_eql_max'] = 'Update-After-Single-Year'
        dev_fw['dt_base_i'] = int(dev_fw['max_id'].replace('.',''))
        dev_fw['dt_base'] = difference(dev_fw['max_id'])

    # IPS Patch in between catalogs
    elif dev_fw['eql_id'] == "00.00.00" and dev_fw['prev_id'] != "00.00.00":
        dev_fw['diff_eql_max'] = 'IPS/Demoted-Update'
        #dev_fw['prev_id'] = imin['min_cat']
        dev_fw['dt_base_i'] = int(dev_fw['max_id'].replace('.','')) - \
                            int(dev_fw['prev_id'].replace('.',''))
        dev_fw['dt_base'] = difference(dev_fw['max_id'], dev_fw['prev_id'])

    # One Update inside year applied!!!
    # will never happen, since prev_id <= eql_id
    elif dev_fw['eql_id'] != "00.00.00" and dev_fw['prev_id'] == "00.00.00":
        dev_fw['diff_eql_max'] = 'Rare-Update-One-Applied'
        dev_fw['dt_base_i'] = int(dev_fw['max_id'].replace('.','')) - \
                            int(dev_fw['eql_id'].replace('.',''))
        dev_fw['dt_base'] = difference(dev_fw['max_id'], dev_fw['eql_id'])

    # Multiple Updates inside year, at least one applied!!!
    elif dev_fw['eql_id'] != "00.00.00" and dev_fw['prev_id'] != "00.00.00":
        dev_fw['diff_eql_max'] = 'Multiple-Updates-One-Applied'
        dev_fw['dt_base_i'] = int(dev_fw['max_id'].replace('.','')) - \
                            int(dev_fw['eql_id'].replace('.',''))
        dev_fw['dt_base'] = difference(dev_fw['max_id'], dev_fw['eql_id'])

    dev_fw['eql>max'] = dev_fw['eql_id'] <= dev_fw['max_id']
    dev_fw['eql<min'] = dev_fw['eql_id'] >= dev_fw['prev_id']
    dev_fw['min<max'] = dev_fw['prev_id'] <= dev_fw['max_id']

    doprint(",".join([str(dev_fw[i]) if i in dev_fw else "" for i in fnames]))
