from omdrivers.enums.iDRAC.PCIeSSD import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import logging

logger = logging.getLogger(__name__)

class PCIeSSD(ClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        super().__init__("Component", None, parent)
        # readonly attribute populated by iDRAC
        self.BusProtocol = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BusProtocolVersion = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CapableSpeed = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CryptographicErase = EnumTypeField(None,CryptographicEraseTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DeviceProtocol = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FailurePredicted = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ModelNumber = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PcieMaxLinkWidth = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PcieNegotiatedLinkSpeed = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PcieNegotiatedLinkWidth = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RemainingRatedWriteEndurance = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SecureErase = EnumTypeField(None,SecureEraseTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SerialNumber = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Size = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SmartStatus = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.State = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        if not loading_from_scp: self.commit()

