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
import logging


logger = logging.getLogger(__name__)

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


class Prettifyer:
    def prettify_json(self, json_object):
        return "<empty json>" if json_object is None else json.dumps(json_object, sort_keys=True, indent=4, \
              separators=(',', ': '), cls=MyEncoder)

PrettyPrint = Prettifyer()