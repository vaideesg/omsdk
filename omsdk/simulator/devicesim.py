import sys
import logging
import os
from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
from omsdk.sdkcenum import TypeHelper
import re
import json

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class Simulation:
    def __init__(self):
        self.record = False
        self.simulate = False
    def start_recording(self):
        self.record = True
        self.simulate = False
    def end_recording(self):
        self.record = False
        self.simulate = False
    def start_simulating(self):
        self.simulate = True
        self.record = False
    def end_simulating(self):
        self.record = False
        self.simulate = False
    def is_recording(self):
        return self.record
    def is_simulating(self):
        return self.simulate

    def simulate_config(self, ipaddr):
        mypath = "."
        for i in ["simulator", ipaddr, 'config']:
            mypath = os.path.join(mypath, i)
        mypath = os.path.join(mypath, "config.xml")
        retval = None
        if os.path.exists(mypath) and not os.path.isdir(mypath):
            with open(mypath) as enum_data:
                retval = json.load(enum_data)
        return retval

    def record_config(self, ipaddr, config):
        mypath = "."
        for i in ["simulator", ipaddr, 'config']:
            mypath = os.path.join(mypath, i)
            if not os.path.exists(mypath):
                os.mkdir(mypath)
        mypath = os.path.join(mypath, "config.xml")
        with open(mypath, 'w') as myconfig:
                myconfig.write(config)
        return retval

    def simulate_proto(self, ipaddr, enumid, clsName):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
        mypath = os.path.join(mypath, clsName + ".json")
        retval = {'Data' : {}, 'Status' : 'Failed', 'Message' : 'No file found'}
        if os.path.exists(mypath) and not os.path.isdir(mypath):
            with open(mypath) as enum_data:
                retval = json.load(enum_data)
        return retval

    def record_proto(self, ipaddr, enumid, clsName, retval):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
            if not os.path.exists(mypath):
                os.mkdir(mypath)
        with open(os.path.join(mypath, clsName + ".json"), "w") as f:
            json.dump(retval, f, sort_keys=True, indent=4, \
                 separators=(',', ': '))

    def simulator_connect(self, ipaddr, enumid, protoobj):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
        if os.path.exists(mypath) and os.path.isdir(mypath):
            if enumid != ProtocolEnum.WSMAN:
                return protobj
            sjson = os.path.join(mypath, 'System.json')
            simspec = None
            for i in protoobj.views:
                if TypeHelper.resolve(i) == 'System':
                    simspec = re.sub(".*/", '', protoobj.views[i])
                    break
            if os.path.exists(sjson) and simspec:
                with open(sjson, 'r') as endata:
                    _s = json.load(endata)
                    if _s and 'Data' in _s and \
                       _s['Data'] and simspec in _s['Data']:
                        return protoobj
        return None

Simulator = Simulation()

