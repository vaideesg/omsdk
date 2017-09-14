import json
import glob
import re
import os
from enum import Enum
from sys import stdout
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkcunicode import UnicodeWriter
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
import logging

logger = logging.getLogger(__name__)

class Update(object):

    def __init__(self, entity, firmware_enum):
        self.entity = entity
        self.firmware_enum = firmware_enum

