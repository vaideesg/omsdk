from omsdk.version.sdkversion import OverrideCompatibleEnumPyVersion
OverrideCompatibleEnumPyVersion = (3, 0, 0)

from enum import Enum
import sys

if OverrideCompatibleEnumPyVersion:
    PY2 = (sys.version_info < OverrideCompatibleEnumPyVersion)
    PY3 = (sys.version_info >= OverrideCompatibleEnumPyVersion)

if PY2:
    from enum import EnumValue

class TypeHelper:
    @staticmethod
    def belongs_to(entype, value):
        if PY2:
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
        if PY2 and isinstance(enval, EnumValue):
            return (enval.key)
        elif PY3 and isinstance(enval, Enum):
            return (enval.value)
        else:
            return enval

    @staticmethod
    def get_name(enval, mymap):
        if PY2 or not isinstance(enval, Enum) :
            for i in mymap:
                if mymap[i] == TypeHelper.resolve(enval):
                    return i
        elif PY3 and isinstance(enval, Enum):
            return (enval.name)
        else:
            return enval

class EnumWrapper(object):
    enum_entries = {}
    enum_name = None
    def __init__(self, name, entries):
        EnumWrapper.enum_entries[name] = entries
        if PY2:
            EnumWrapper.enum_name = name
            ent = EnumWrapper.enum_entries[name].keys()
            self.enum_type = Enum(*ent, value_type = EnumWrapper.mapvalue)
        else:
            self.enum_type  = Enum(name, EnumWrapper.enum_entries[name])


    @staticmethod
    def mapvalue(self, i, value):
        if PY2:
            return EnumValue(self, i, EnumWrapper.enum_entries[EnumWrapper.enum_name][value])
        else:
            pass

    @staticmethod
    def resolve(enval):
        if PY2:
            return (enval.key)
        else:
            return (enval.value)
