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
from omsdk.version.sdkversion import OverrideCompatibleEnumPyVersion

from enum import Enum
import sys

if OverrideCompatibleEnumPyVersion:
    PY2Enum = (sys.version_info < OverrideCompatibleEnumPyVersion)
    PY3Enum = (sys.version_info >= OverrideCompatibleEnumPyVersion)

if PY2Enum:
    from enum import EnumValue

# 
#  If you create a enumeration as:
#      TestOptions_Map = { 'VAL_1' : 'Value 1', 'VAL_2' : 'Value 2' }
#      TestOptionsEnum = EnumWrapper("Test",  TestOptions_Map).enum_type
#
#  TypeHelper.resolve('VAL_1') ==> 'Value 1'
#  TypeHelper.resolve(TestOptionsEnum.VAL_1) ==> 'Value 1'
#
#  TypeHelper.belongs_to(TestOptionsEnum, TestOptionsEnum.VAL_1) ==> True
#  TypeHelper.belongs_to(TestOptionsEnum, OtherEnum.VAL_1) ==> False
#  TypeHelper.belongs_to(TestOptionsEnum, 'VAL_1') ==> False
#
#  TypeHelper.get_name('Value 1', TestOptions_Map) ==> 'VAL_1'
#  TypeHelper.get_name('Value N', TestOptions_Map) ==> None
#
#  TypeHelper.convert_to_enum('Value 1', TestOptions) => TestOptionsEnum.VAL_1
#  TypeHelper.convert_to_enum('Value 2', TestOptions) => TestOptionsEnum.VAL_2
#  TypeHelper.convert_to_enum('Value N', TestOptions) => None
#

class TypeHelper:
    @staticmethod
    def belongs_to(entype, value):
        if PY2Enum:
            if  (type(entype) is Enum):
                return (isinstance(value, EnumValue) and \
                        value.enumtype == entype)
            elif entype == type(value):
                return True
            else:
                return False
        else:
            return entype.__name__ == type(value).__name__
            #if not isinstance(value, argtype) and \
            #   argtype.__name__ != type(value).__name__:

    @staticmethod
    def resolve(enval):
        if PY2Enum and isinstance(enval, EnumValue):
            return (enval.key)
        elif PY3Enum and isinstance(enval, Enum):
            return (enval.value)
        else:
            return enval

    @staticmethod
    def get_name(enval, mymap):
        if PY2Enum or not isinstance(enval, Enum) :
            for i in mymap:
                if mymap[i] == TypeHelper.resolve(enval):
                    return i
        elif PY3Enum and isinstance(enval, Enum):
            return (enval.name)
        else:
            return enval

    @staticmethod
    def convert_to_enum(enval, entype, defval = None):
        for i in entype:
            if enval == TypeHelper.resolve(i):
                return i
        return defval

    @staticmethod
    def is_enum(entype):

        if PY3Enum and isinstance(entype, type(Enum)):
            return True
        elif PY2Enum and isinstance(entype, Enum):
            return True
        return False

class EnumWrapper(object):
    enum_entries = {}
    enum_name = None
    def __init__(self, name, entries):
        EnumWrapper.enum_entries[name] = entries
        if PY2Enum:
            EnumWrapper.enum_name = name
            ent = EnumWrapper.enum_entries[name].keys()
            self.enum_type = Enum(*ent, value_type = EnumWrapper.mapvalue)
        else:
            self.enum_type  = Enum(name, EnumWrapper.enum_entries[name])


    @staticmethod
    def mapvalue(self, i, value):
        if PY2Enum:
            return EnumValue(self, i, EnumWrapper.enum_entries[EnumWrapper.enum_name][value])
        else:
            pass

    @staticmethod
    def resolve(enval):
        if PY2Enum:
            return (enval.key)
        else:
            return (enval.value)
