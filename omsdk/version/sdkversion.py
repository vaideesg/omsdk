import sys

OMSDKVersion = (0, 5, 0)

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