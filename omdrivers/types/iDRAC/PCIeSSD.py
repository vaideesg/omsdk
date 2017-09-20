from omsdk.sdkcenum import EnumWrapper
from omdrivers.types.iDRAC.BaseARType import *
from omdrivers.enums.iDRAC.PCIeSSD import *
import logging

logger = logging.getLogger(__name__)

class PCIeSSD(BaseARType):

    def my_create(self):
        self.CryptographicErase = None
        self.SecureErase = None
        return self

    def my_modify(self):
        self.CryptographicErase = None
        self.SecureErase = None
        return self

    def my_delete(self):
        self.CryptographicErase = None
        self.SecureErase = None
        return self

