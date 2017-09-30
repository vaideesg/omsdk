from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType, FQDDHelper
from omsdk.typemgr.BuiltinTypes import RootClassType
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.BIOS import *
from omdrivers.types.iDRAC.NIC import *
from omdrivers.types.iDRAC.FCHBA import *
from omdrivers.types.iDRAC.RAID import *
import sys
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class SystemConfiguration(RootClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        if PY2:
            super(SystemConfiguration, self).__init__("SystemConfiguration", None, parent)
        else:
            super().__init__("SystemConfiguration", None, parent)
        self.LifecycleController = LifecycleController(parent=self, loading_from_scp=loading_from_scp)
        self.System = System(parent=self, loading_from_scp=loading_from_scp)
        self.iDRAC = iDRAC(parent=self, loading_from_scp=loading_from_scp)
        self.FCHBA = ArrayType(FCHBA, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self.NIC = ArrayType(NetworkInterface, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self.BIOS = BIOS(parent=self, loading_from_scp=loading_from_scp)
        self.Controller = ArrayType(Controller, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self._ignore_attribs('ServiceTag', 'Model', 'TimeStamp')
        self.commit(loading_from_scp)

