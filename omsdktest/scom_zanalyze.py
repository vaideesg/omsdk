import sys
import os
import json
sys.path.append(os.getcwd())

from sys import stdout, path

import glob
import json
import re

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
        return "./__data/" + self.name + "_fields.txt"

    def serialize(self):
        with open(self.PersistentObject, "w") as f:
            f.write(json.dumps(self.fields, sort_keys=True, indent=4, \
              separators=(',', ': ')))

    def load(self):
        if os.path.exists(self.PersistentObject):
            with open(self.PersistentObject, "r") as f:
                self.fields = json.load(f)


class EnumHelper(object):
    def __init__(self):
        self.enumerator = {}

    def todo(self):
        if fname in ['Model', 'FQDD']:
            if fname not in self.enumerator:
                self.enumerator[fname] = []
            if value not in self.enumerator[fname]:
                self.enumerator[fname].append(value)
            value = str(self.enumerator[fname].index(value))

class DataCollector(Base):
    def __init__(self, fields):
        self.ipaddr = None
        self.sp_fields = []
        self.entity = {}

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
            else:
                myrec[field] = "0"

        return myrec if not spec or spec(myrec) else None

    def beautify_field(self, fname, value):
        if value == "Not Available":
            value = "0"
        return self.my_beautify_field(fname, value)

    def my_beautify_field(self, fname, value):
        return str(value)

class DeviceCollector(DataCollector):
    def __init__(self, fname):
        super().__init__('DeviceCollector')
        self.sp_fields = [
            "InstallationDate",
            "FQDD", "Model", "SystemID"]
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
        elif fname in ['InstallationDate']:
            from datetime import datetime
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            value = datetime.strptime(value, date_format).strftime('%y%m')
        elif fname in ['FQDD']:
            value = value.split('.')[0]
        elif fname in ['VersionString','ComponentID' 'DeviceID',
                       'SubDeviceID', 'SubVendorID', 'VendorID']:
            if value is None: value = ""
        return value

class Objects(object):

    def __init__(self, directory, typeo, join_entries=None, filter_fields=None):
        self.objects = []
        for i in glob.glob(directory):
            self.objects.append(typeo(i))
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

class FieldModifier(object):
    pass

from datetime import datetime
class DateModifier(FieldModifier):
    def __init__(self, name):
        self.name = name
        self.date_format = "%Y-%m-%dT%H:%M:%SZ"

    def beautify(self, value):
        return datetime.strptime(value, self.date_format).strftime('%y%m')

dev = Objects('./Store/Master/*/*/100*', DeviceCollector,
        join_entries = ['Firmware', 'System', 'doc.props'],
        filter_fields = [ 'IPAddress',
            'LifecycleControllerVersion',
            'FQDD',
            'Model',
            'SystemID',
            'VersionString',
            'ComponentID',
            'InstallationDate',
            'InstallationDate_orig',
            'FQDD_orig',
            'Model_orig' ])

fnames = []
fnames.extend(dev.filter_fields)
fnames.extend(['max_id', 'max_vs', 'min_id','min_vs','eql_id', 'eql_vs']) 

fw_fields = {}
with open('./SDKRepo/PDK.json', "r") as f:
    fw_fields = json.load(f)

def cmpx(i, j):
    if (i == j):
        return "equal"
    elif i < j:
        return "less"
    else:
        return "great"

print(",".join(fnames))
for dev_fw in dev.processed:
    for d in ['ComponentID', 'DeviceID', 'SubDeviceID',
            'SubVendorID', 'VendorID']:
        if d not in dev_fw or not dev_fw[d]: dev_fw[d] = ""
        if dev_fw[d] == '0': dev_fw[d] = ""

    t1 = "{0}-{1}".format(dev_fw['SystemID'], dev_fw['ComponentID'])
    if t1 not in fw_fields:
        t1 = "{0}-{1}-{2}-{3}-{4}".format(
            dev_fw['SystemID'], dev_fw['ComponentID'],
            dev_fw['DeviceID'], dev_fw['SubDeviceID'],
            dev_fw['SubVendorID'], dev_fw['VendorID'])

    if t1 not in fw_fields:
        print(",".join([str(dev_fw[k]) if k in dev_fw else "" for k in fnames]))
        continue

    imin = None
    imax = None
    exact = None

    for (k, v) in [ ('VersionString', 'vendorVersion')]:
      imin = None
      imax = None
      exact = None
      for ent in fw_fields[t1]['_plist']:
        cat_fw = fw_fields[t1][ent]
        if (dev_fw[k] == cat_fw[v]):
            if not exact or exact['catalog_version']<cat_fw['catalog_version']:
                exact = cat_fw
        if (dev_fw[k] <= cat_fw[v]):
            if not imax or imax['catalog_version'] < cat_fw['catalog_version']:
                imax = cat_fw
        if (dev_fw[k] >= cat_fw[v]):
            if not imin or imin['catalog_version'] > cat_fw['catalog_version']:
                imin = cat_fw

    dev_fw['max_id'] = imax['catalog_version'] if imax else "99.99.99"
    dev_fw['min_id'] = imin['catalog_version'] if imin else "00.00.00"
    dev_fw['eql_id'] = exact['catalog_version'] if exact else "00.00.00"
    dev_fw['max_vs'] = imax['vendorVersion'] if imax else "99.99.99"
    dev_fw['min_vs'] = imin['vendorVersion'] if imin else "00.00.00"
    dev_fw['eql_vs'] = exact['vendorVersion'] if exact else "00.00.00"
    print(",".join([str(dev_fw[i]) if i in dev_fw else "" for i in fnames]))

# fix systemID => Model_Hex
# select catalog_version, dateTime where:
#     VersionString == vendorVersion
#     SystemID = model_systemID
#     component_componentID == 107142
