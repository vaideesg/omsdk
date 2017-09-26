from omsdk.typemgr.BuiltinTypes import RootClassType
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.BIOS import *
from omdrivers.types.iDRAC.RAID import *
from omdrivers.types.iDRAC.NIC import *
from omdrivers.types.iDRAC.FCHBA import *


class SystemConfiguration(RootClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        super().__init__("SystemConfiguration", None, parent)
        self.System = System(parent=self, loading_from_scp=loading_from_scp)
        #self.iDRAC = iDRAC(parent=self, loading_from_scp=loading_from_scp)
        #self.LifecycleController = LifecycleController(parent=self, loading_from_scp=loading_from_scp)
        #self.BIOS = BIOS(parent=self, loading_from_scp=loading_from_scp)
        #self.NIC = ArrayType(NIC, parent=self, loading_from_scp=loading_from_scp)
        #self.FCHBA = ArrayType(NIC, parent=self, loading_from_scp=loading_from_scp)
        #self.Controller = ArrayType(RAID, parent=self, loading_from_scp=loading_from_scp)
        self.commit(loading_from_scp)
