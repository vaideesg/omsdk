import sys
import os
import json
sys.path.append(os.getcwd())

from sys import stdout, path

import glob
import json
import re

lc_versions = {
     "2.1.0"      : "0100",
     "2.30.30.30" : "3030.30",
     "2.40.40.40" : "4040.40",
     "2.50.50.50" : "5050.50",
     "2.52.52.52" : "5252.52",
     "2.60.60.60" : "6060.60",
     "3.00.00.00" : "0000.00",
     "3.15.15.15" : "1515.15",
     "3.17.17.17" : "1717.17",
     "3.18.18.18" : "1818.18",
     "3.19.19.19" : "1919.19",
     "3.20.20.20" : "2020.20",
     "3.21.21.21" : "2121.21",
     "3.22.22.22" : "2222.22",
     "3.23.23.23" : "2323.23",
     "3.30.30.30" : "3030.30",
     "3.40.40.40" : "4040.40"
}

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
        comma = ""
        for i in self.names:
            sys.stdout.write(comma+'"' + i + '=' + str(self.iterator[i]) + '"')
            comma = ","
        sys.stdout.write('\n')


class Base(object):
    pass

class FieldCollector(Base):
    def __init__(self, join_fields=None):
        self.fields = []
        self.join_fields = join_fields

    def op(self, entity):
        for parts in entity:
            if not join_fields or parts in join_fields:
                self._op(entity[parts])

    def _op(self, entity):
        for parts in entity:
            if type(parts) is dict:
                self._op(parts)
            elif type(entity[parts]) is dict:
                self._op(entity[parts])
            elif type(entity[parts]) is list:
                for ent in entity[parts]:
                    self._op(ent)
            elif parts not in self.fields:
                self._append(parts)

    def _append(self, field):
        self.fields.append(field)
        if field in ["BIOSVersionString",
                     "LifecycleControllerVersion",
                     "CPLDVersion",
                     "VersionString",
                     "InstallationDate",
                     "FQDD", "Model"]:
            self.fields.append(field + "_orig")

    def summary(self):
        comma = ""
        for field in self.fields:
            sys.stdout.write(comma + '"' + field + '"')
            comma = ","
        sys.stdout.write('\n')

    @property
    def Fields(self):
        return self.fields

    @property
    def PersistentObject(self):
        return "./__data/fields.txt"

    def serialize(self):
        with open(self.PersistentObject, "w") as f:
            f.write(json.dumps(self.fields, sort_keys=True, indent=4, \
              separators=(',', ': ')))

    def load(self):
        if os.path.exists(self.PersistentObject):
            with open(self.PersistentObject, "r") as f:
                self.fields = json.load(f)

class DataCollector(Base):
    def __init__(self, fields, filter_fields = None, spec = None):
        self.fields = fields
        self.ipaddr = None
        self.filter_fields = filter_fields
        if not self.filter_fields:
            self.filter_fields = self.fields.Fields
        self.spec = spec
        self.enumerator = {}

    def _op(self, entity):
        if 'doc.props' in entity and 'IPAddress' in entity['doc.props']:
            self.ipaddr = entity['doc.props']['IPAddress']
        join_fields = ['Firmware', 'System', 'doc.props']
        if 'Firmware' in entity:
            for fwent in entity['Firmware']:
                self.write_row(fwent)

    def op(self, entity):
        final_it = entity

        if self.fields.join_fields:
            final_it = {} 
            for i in self.fields.join_fields:
                if (i in entity):
                    final_it[i] = entity[i]

        ix = Indexer(final_it)
        while ix.nexti():
            self.write_row(ix, entity)

    def write_header(self):
        comma = ""
        for field in self.filter_fields:
            sys.stdout.write(comma + '"' + field + '"')
            comma = ","
        sys.stdout.write('\n')

    def write_row(self, ix, entity):
        return self._write_row(ix, entity, self.filter_fields)

    def _write_row(self, ix, entity, fields):
        myrec = {}
        origrec = {}
        for t in ix.iterator:
            myrec.update(entity[t][ix.iterator[t]])
            origrec.update(entity[t][ix.iterator[t]])

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

        if not self.spec or self.spec(myrec):
            comma = ""
            for field in fields:
                sys.stdout.write(comma+'"' + myrec[field] + '"')
                comma = ","
            sys.stdout.write('\n')
        return True

    def beautify_field(self, fname, value):
        if fname in ['FQDD']:
            value = value.split('.')[0]
        if fname in ['Model', 'FQDD']:
            if fname not in self.enumerator:
                self.enumerator[fname] = []
            if value not in self.enumerator[fname]:
                self.enumerator[fname].append(value)
            value = str(self.enumerator[fname].index(value))
        elif value == "Not Available":
            return "0"
        elif fname in ["BIOSVersionString", "CPLDVersion", "VersionString"]:
            value = re.sub('[^0-9.]+', '', value + ".0.0.0.0")
            value = re.sub('^\\.', '', value)
            value = re.sub('^([0-9]+).([0-9]+).([0-9]+).([0-9]+).*',
                   '\\1.\\2.\\3.\\4', value)
            val = 0
            for i in [int(i) for i in value.split('.')]:
                val = val * 100 + (i%100)
            value = str(val)
        elif fname in ["LifecycleControllerVersion"]:
            value = re.sub('[^0-9.]+', '', value + ".0.0.0.0")
            value = re.sub('^\\.', '', value)
            value = re.sub('^([0-9]+).([0-9]+).([0-9]+).([0-9]+).*',
                   '\\2.\\3.\\4.0', value)
            val = 0
            for i in [int(i) for i in value.split('.')]:
                val = val * 100 + (i%100)
            while val > 10000:
                val = val/10
            value = str(val)
        elif fname in ['InstallationDate']:
            from datetime import datetime
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            value = datetime.strptime(value, date_format).strftime('%y%m')
        elif fname in ['FQDD']:
            value = value.split('.')[0]
        else:
            value = str(value)
        return value

    def summary(self):
        pass


def processor(func):
    for i in glob.glob('./Store/Master/*/*/100*'):
        ipaddr = re.sub('.*\\\\', '', i)
        pathdir = re.sub(ipaddr + '$', '', i)

        entity = { 
            'doc.props' : [ { 'IPAddress' : ipaddr } ],
        }
        for parts in ['Firmware.json', 'Key_Inventory_ConfigState.json']:
            json_path = os.path.join(pathdir, parts)
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    entity.update(json.load(f))
        func.op(entity)

class FieldModifier(object):
    pass

from datetime import datetime
class DateModifier(FieldModifier):
    def __init__(self, name):
        self.name = name
        self.date_format = "%Y-%m-%dT%H:%M:%SZ"

    def beautify(self, value):
        return datetime.strptime(value, self.date_format).strftime('%y%m')

join_fields = ['Firmware', 'System', 'doc.props']
fields = FieldCollector(join_fields)
processor(fields)
fields.serialize()

filter_fields = [
    'IPAddress',
    'LifecycleControllerVersion',
    'FQDD',
    'Model',
    'InstallationDate',
    'VersionString_orig',
    'InstallationDate_orig',
    'FQDD_orig',
    'Model_orig'
]

def spec(obj):
    return True

dc = DataCollector(fields, filter_fields, spec)
dc.write_header()
processor(dc)
dc.summary()
#print(json.dumps(dc.enumerator, sort_keys=True, indent=4, separators=(',', ': ')))
