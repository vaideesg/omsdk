from __future__ import print_function
import io
import logging
import threading
import time
import json
from enum import Enum
from json import JSONEncoder
from omsdk.sdkcenum import EnumWrapper,TypeHelper
from pprint import pprint
from datetime import datetime
import xml.etree.ElementTree as ET
import traceback

import sys

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto import rfc1902
    from pysnmp import debug
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

LOG_LEVEL = EnumWrapper("logLevel", {
        'FATAL' : 1,
        'ERROR' : 2,
        'WARN' : 3,
        'INFO' : 4,
        'DEBUG': 5
    }).enum_type

CurrentLogLevel = LOG_LEVEL.ERROR

class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, str):
            return o
        if PySnmpPresent:
            if isinstance(o, rfc1902.Integer):
                return str(o)
            if isinstance(o, rfc1902.OctetString):
                return str(o)
        if isinstance(o, type):
            return str(type)
        if PY2 and isinstance(o, EnumValue):
            return o.key
        if isinstance(o, datetime):
            return str(datetime)
        return o.json_encode()

class pretty:
    def printx(self, json_object):
        if json_object is None:
            print("<empty json>")
            return False
        print(json.dumps(json_object, sort_keys=True, indent=4, \
              separators=(',', ': '), cls=MyEncoder))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class myprint:
    def checklevel(self, lvl):
        return TypeHelper.resolve(CurrentLogLevel) >= TypeHelper.resolve(lvl)

    def debug(self, msg):
        if self.checklevel(LOG_LEVEL.DEBUG):
            print(msg)

    def debugxml(self, obj):
        pass

    def debugdict(self, obj):
        if self.checklevel(LOG_LEVEL.DEBUG):
            pprint(obj)

    def debugloc(self, msg = "test"):
        if self.checklevel(LOG_LEVEL.DEBUG):
            eprint("Start <<<<<<<<<<<" + msg)
            traceback.print_stack()
            eprint("End <<<<<<<<<<<" + msg)

    def loc(self, msg = "test"):
        if self.checklevel(LOG_LEVEL.INFO):
            eprint("Start <<<<<<<<<<<" + msg)
            traceback.print_stack()
            eprint("End <<<<<<<<<<<" + msg)

    def info(self, msg):
        if self.checklevel(LOG_LEVEL.INFO):
            print(msg)

    def debugjson(self, json_object):
        if self.checklevel(LOG_LEVEL.DEBUG):
            if json_object is None:
                print("<empty json>")
                return False
            print(json.dumps(json_object, sort_keys=True, indent=4, \
              separators=(',', ': '), cls=MyEncoder))
        return True

LogMan = myprint()
