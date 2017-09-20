from omsdk.sdkcenum import EnumWrapper
from omdrivers.types.iDRAC.BaseARType import *
from omdrivers.enums.iDRAC.RAID import *
import logging

logger = logging.getLogger(__name__)

class RAID(BaseARType):

    def my_create(self):
        self.Cachecade = None
        self.DiskCachePolicy = DiskCachePolicyTypes.Default
        self.CurrentControllerMode = CurrentControllerModeTypes.RAID
        self.EncryptionMode = None
        self.KeyID = None
        self.LockStatus = None
        self.NewControllerKey = None
        self.OldControllerKey = None
        self.PCIeSSDSecureErase = PCIeSSDSecureEraseTypes.T_False
        self.RAIDControllerBootMode = None
        self.RAIDEnclosureRequestedCfgMode = RAIDEnclosureRequestedCfgModeTypes.T_None
        self.RAIDHotSpareStatus = RAIDHotSpareStatusTypes.No
        self.RAIDTypes = None
        self.RAIDaction = RAIDactionTypes.Create
        self.RAIDbatteryLearnMode = None
        self.RAIDbgiRate = "100"
        self.RAIDccMode = RAIDccModeTypes.Normal
        self.RAIDccRate = "100"
        self.RAIDcopybackMode = RAIDcopybackModeTypes.On
        self.RAIDdedicatedSpare = None
        self.RAIDinitOperation = RAIDinitOperationTypes.T_None
        self.RAIDloadBalancedMode = RAIDloadBalancedModeTypes.Automatic
        self.RAIDprMode = RAIDprModeTypes.Automatic
        self.RAIDrebuildRate = "100"
        self.RAIDreconstructRate = "100"
        self.RAIDrekey = RAIDrekeyTypes.T_False
        self.RAIDremovecontrollerKey = RAIDremovecontrollerKeyTypes.T_False
        self.RAIDresetConfig = RAIDresetConfigTypes.T_False
        self.T10PIStatus = None
        self.RAIDforeignConfig = RAIDforeignConfigTypes.Clear
        self.RAIDdefaultWritePolicy = RAIDdefaultWritePolicyTypes.WriteThrough
        self.RAIDdefaultReadPolicy = RAIDdefaultReadPolicyTypes.Adaptive
        self.RAIDEnhancedAutoImportForeignConfig = RAIDEnhancedAutoImportForeignConfigTypes.Disabled
        self.StripeSize = StripeSizeTypes.S_512
        return self

    def my_modify(self):
        self.DiskCachePolicy = DiskCachePolicyTypes.Default
        #self.PCIeSSDSecureErase = PCIeSSDSecureEraseTypes.T_False
        self.RAIDEnclosureRequestedCfgMode = RAIDEnclosureRequestedCfgModeTypes.T_None
        self.RAIDaction = RAIDactionTypes.Update
        self.RAIDbatteryLearnMode = None
        self.RAIDbgiRate = "100"
        self.RAIDccMode = RAIDccModeTypes.Normal
        self.RAIDccRate = "100"
        self.RAIDcopybackMode = RAIDcopybackModeTypes.On
        self.RAIDdefaultReadPolicy = RAIDdefaultReadPolicyTypes.Adaptive
        self.RAIDdefaultWritePolicy = RAIDdefaultWritePolicyTypes.WriteBack
        self.RAIDforeignConfig = RAIDforeignConfigTypes.Ignore
        self.RAIDloadBalancedMode = RAIDloadBalancedModeTypes.Automatic
        self.RAIDprMode = RAIDprModeTypes.Automatic
        self.RAIDrebuildRate = "100"
        self.RAIDreconstructRate = "100"
        self.RAIDrekey = RAIDrekeyTypes.T_False
        self.RAIDremovecontrollerKey = RAIDremovecontrollerKeyTypes.T_False
        self.RAIDresetConfig = RAIDresetConfigTypes.T_False
        self.T10PIStatus = None
        return self

    def my_delete(self):
        self.RAIDaction = RAIDactionTypes.Delete
        return self

