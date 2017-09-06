import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

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
