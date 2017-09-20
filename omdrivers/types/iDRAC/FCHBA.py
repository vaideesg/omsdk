from omsdk.sdkcenum import EnumWrapper
from omdrivers.types.iDRAC.BaseARType import *
from omdrivers.enums.iDRAC.FCHBA import *
import logging

logger = logging.getLogger(__name__)

class FCHBA(BaseARType):

    def my_create(self):
        self.BootScanSelection = BootScanSelectionTypes.Disabled
        self.FCTape = FCTapeTypes.Disabled
        self.FabricLoginRetryCount = "3"
        self.FabricLoginTimeout = "3000"
        self.FirstFCTargetLUN = None
        self.FirstFCTargetWWPN = None
        self.FramePayloadSize = FramePayloadSizeTypes.Auto
        self.HardZone = HardZoneTypes.Disabled
        self.HardZoneAddress = "0"
        self.LinkDownTimeout = "3000"
        self.LoopResetDelay = "5"
        self.PortDownRetryCount = None
        self.PortDownTimeout = "3000"
        self.PortLoginRetryCount = "3"
        self.PortLoginTimeout = "3000"
        self.PortSpeed = PortSpeedTypes.Auto
        self.SecondFCTargetLUN = None
        self.SecondFCTargetWWPN = None
        self.VirtualWWN = None
        self.VirtualWWPN = None
        return self

    def my_modify(self):
        self.BootScanSelection = BootScanSelectionTypes.Disabled
        self.FCTape = FCTapeTypes.Disabled
        self.FabricLoginRetryCount = "3"
        self.FabricLoginTimeout = "3000"
        self.FirstFCTargetLUN = None
        self.FirstFCTargetWWPN = None
        self.FramePayloadSize = FramePayloadSizeTypes.Auto
        self.HardZone = HardZoneTypes.Disabled
        self.HardZoneAddress = "0"
        self.LinkDownTimeout = "3000"
        self.LoopResetDelay = "5"
        self.PortDownRetryCount = None
        self.PortDownTimeout = "3000"
        self.PortLoginRetryCount = "3"
        self.PortLoginTimeout = "3000"
        self.PortSpeed = PortSpeedTypes.Auto
        self.SecondFCTargetLUN = None
        self.SecondFCTargetWWPN = None
        self.VirtualWWN = None
        self.VirtualWWPN = None
        return self

    def my_delete(self):
        self.BootScanSelection = BootScanSelectionTypes.Disabled
        self.FCTape = FCTapeTypes.Disabled
        self.FabricLoginRetryCount = "3"
        self.FabricLoginTimeout = "3000"
        self.FirstFCTargetLUN = None
        self.FirstFCTargetWWPN = None
        self.FramePayloadSize = FramePayloadSizeTypes.Auto
        self.HardZone = HardZoneTypes.Disabled
        self.HardZoneAddress = "0"
        self.LinkDownTimeout = "3000"
        self.LoopResetDelay = "5"
        self.PortDownRetryCount = None
        self.PortDownTimeout = "3000"
        self.PortLoginRetryCount = "3"
        self.PortLoginTimeout = "3000"
        self.PortSpeed = PortSpeedTypes.Auto
        self.SecondFCTargetLUN = None
        self.SecondFCTargetWWPN = None
        self.VirtualWWN = None
        self.VirtualWWPN = None
        return self

