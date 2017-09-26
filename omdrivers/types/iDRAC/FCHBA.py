from omdrivers.enums.iDRAC.FCHBA import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import logging

logger = logging.getLogger(__name__)

class FCHBA(ClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        super().__init__("Component", None, parent)
        self.BootScanSelection = EnumTypeField(BootScanSelectionTypes.Disabled,BootScanSelectionTypes, parent=self)
        # readonly attribute
        self.BusDeviceFunction = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChipMdl = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceName = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.EFIVersion = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FCTape = EnumTypeField(FCTapeTypes.Disabled,FCTapeTypes, parent=self)
        self.FabricLoginRetryCount = IntField("3", parent=self)
        self.FabricLoginTimeout = IntField("3000", parent=self)
        # readonly attribute
        self.FamilyVersion = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FirstFCTargetLUN = IntField(None, parent=self)
        self.FirstFCTargetWWPN = IntField(None, parent=self)
        self.FramePayloadSize = EnumTypeField(FramePayloadSizeTypes.Auto,FramePayloadSizeTypes, parent=self)
        self.HardZone = EnumTypeField(HardZoneTypes.Disabled,HardZoneTypes, parent=self)
        self.HardZoneAddress = IntField("0", parent=self)
        self.LinkDownTimeout = IntField("3000", parent=self)
        self.LoopResetDelay = IntField("5", parent=self)
        # readonly attribute
        self.PCIDeviceID = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PortDownRetryCount = IntField(None, parent=self)
        self.PortDownTimeout = IntField("3000", parent=self)
        self.PortLoginRetryCount = IntField("3", parent=self)
        self.PortLoginTimeout = IntField("3000", parent=self)
        # readonly attribute populated by iDRAC
        self.PortNumber = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PortSpeed = EnumTypeField(PortSpeedTypes.Auto,PortSpeedTypes, parent=self)
        self.SecondFCTargetLUN = IntField(None, parent=self)
        self.SecondFCTargetWWPN = IntField(None, parent=self)
        self.VirtualWWN = IntField(None, parent=self)
        self.VirtualWWPN = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.WWN = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.WWPN = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        if not loading_from_scp: self.commit()

