#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan, Karthik Prabu
#
from __future__ import print_function
import io
import logging
import threading
import time
import json
from enum import Enum
from json import JSONEncoder
from omsdk.sdkcenum import EnumWrapper,TypeHelper,PY2Enum
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

if PY2Enum:
    from enum import EnumValue


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
        if PY2Enum and isinstance(o, EnumValue):
            return o.key
        if isinstance(o, datetime):
            return str(datetime)
        return o.json_encode()


class Prettifyer:
    def prettify_json(self, json_object):
        return "<empty json>" if json_object is None else json.dumps(json_object, sort_keys=True, indent=4, \
              separators=(',', ': '), cls=MyEncoder)

PrettyPrint = Prettifyer()
