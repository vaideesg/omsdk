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
# Authors: Vaideeswaran Ganesan
#
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY2UC = (sys.version_info < (3,0,0))

OMSDKVersion = (0, 9, 1002)

APIVersions = {
    'ConfigFactory' : (1, 0, 0),
    'DeviceDriver'  : (1, 0, 0),
    'ConsoleDriver' : (0, 1, 0),
    'SNMPListener'  : (0, 0, 1)
}

OverrideCompatibleEnumPyVersion = None
class Compatibility:
    def __init__(self):
        self.compat_enum_version = None

    def set_compat_enum_version(self, version):
        self.compat_enum_version = version

class CompatibilityFactory:
    compat = Compatibility()
    @staticmethod
    def get_compat():
       return CompatibilityFactory.compat

cc = CompatibilityFactory()

if PY3:
    _EnumStyle = 'V3'
else:
    _EnumStyle = 'NotPresent'
    try :
        import enum
        if hasattr(enum, 'version'):
            _EnumStyle = 'V3'
        elif hasattr(enum, '__version__'):
            _EnumStyle = 'V2'
    except ImportError:
        pass
if _EnumStyle == 'V3':
    OverrideCompatibleEnumPyVersion = sys.version_info
else:
    OverrideCompatibleEnumPyVersion = (3, 0, 0)
