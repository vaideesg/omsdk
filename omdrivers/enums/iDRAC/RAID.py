from omsdk.sdkcenum import EnumWrapper
import logging

logger = logging.getLogger(__name__)

BackplaneTypeTypes = EnumWrapper("BackplaneTypeTypes", {
    "Not_Shared" : "Not Shared",
    "Shared" : "Shared",
}).enum_type

CachecadeTypes = EnumWrapper("CachecadeTypes", {
    "Cachecade_Virtual_Disk" : "Cachecade Virtual Disk",
    "Not_a_Cachecade_Virtual_Disk" : "Not a Cachecade Virtual Disk",
}).enum_type

CurrentControllerModeTypes = EnumWrapper("CurrentControllerModeTypes", {
    "HBA" : "HBA",
    "RAID" : "RAID",
}).enum_type

DiskCachePolicyTypes = EnumWrapper("DiskCachePolicyTypes", {
    "Default" : "Default",
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

EncryptionModeTypes = EnumWrapper("EncryptionModeTypes", {
    "Dell_Key_Management" : "Dell Key Management",
    "Local_Key_Management" : "Local Key Management",
    "T_None" : "None",
}).enum_type

LockStatusTypes = EnumWrapper("LockStatusTypes", {
    "Locked" : "Locked",
    "Unlocked" : "Unlocked",
}).enum_type

PCIeSSDSecureEraseTypes = EnumWrapper("PCIeSSDSecureEraseTypes", {
    "T_False" : "False",
    "T_True" : "True",
}).enum_type

RAIDControllerBootModeTypes = EnumWrapper("RAIDControllerBootModeTypes", {
    "Continue_Boot_On_Error" : "Continue Boot On Error",
    "Headless_Mode_Continue_On_Error" : "Headless Mode Continue On Error",
    "Headless_Safe_Mode" : "Headless Safe Mode",
    "User_Mode" : "User Mode",
}).enum_type

RAIDEnclosureCurrentCfgModeTypes = EnumWrapper("RAIDEnclosureCurrentCfgModeTypes", {
    "Split_Mode" : "Split Mode",
    "Unified_Mode" : "Unified Mode",
}).enum_type

RAIDEnclosureRequestedCfgModeTypes = EnumWrapper("RAIDEnclosureRequestedCfgModeTypes", {
    "Split_Mode" : "Split Mode",
    "T_None" : "None",
    "Unified_Mode" : "Unified Mode",
}).enum_type

RAIDEnhancedAutoImportForeignConfigTypes = EnumWrapper("RAIDEnhancedAutoImportForeignConfigTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

RAIDHotSpareStatusTypes = EnumWrapper("RAIDHotSpareStatusTypes", {
    "Dedicated" : "Dedicated",
    "Global" : "Global",
    "No" : "No",
}).enum_type

RAIDMaxCapableSpeedTypes = EnumWrapper("RAIDMaxCapableSpeedTypes", {
    "T_12_GBS" : "12_GBS",
    "T_1_5_GBS" : "1_5_GBS",
    "T_3_GBS" : "3_GBS",
    "T_6_GBS" : "6_GBS",
}).enum_type

RAIDNegotiatedSpeedTypes = EnumWrapper("RAIDNegotiatedSpeedTypes", {
    "T_12_GBS" : "12_GBS",
    "T_1_5_GBS" : "1_5_GBS",
    "T_3_GBS" : "3_GBS",
    "T_6_GBS" : "6_GBS",
}).enum_type

RAIDPDStateTypes = EnumWrapper("RAIDPDStateTypes", {
    "Blocked" : "Blocked",
    "Failed" : "Failed",
    "Foreign" : "Foreign",
    "Missing" : "Missing",
    "Non_RAID" : "Non-RAID",
    "Online" : "Online",
    "Ready" : "Ready",
    "Unknown" : "Unknown",
}).enum_type

RAIDSupportedRAIDLevelsTypes = EnumWrapper("RAIDSupportedRAIDLevelsTypes", {
    "RAID_0" : "RAID-0",
    "RAID_1" : "RAID-1",
    "RAID_10" : "RAID-10",
    "RAID_5" : "RAID-5",
    "RAID_50" : "RAID-50",
    "RAID_60" : "RAID-60",
}).enum_type

RAIDTypesTypes = EnumWrapper("RAIDTypesTypes", {
    "RAID_0" : "RAID 0",
    "RAID_1" : "RAID 1",
    "RAID_10" : "RAID 10",
    "RAID_5" : "RAID 5",
    "RAID_50" : "RAID 50",
    "RAID_6" : "RAID 6",
    "RAID_60" : "RAID 60",
}).enum_type

RAIDactionTypes = EnumWrapper("RAIDactionTypes", {
    "Create" : "Create",
    "CreateAuto" : "CreateAuto",
    "Delete" : "Delete",
    "Update" : "Update",
}).enum_type

RAIDbatteryLearnModeTypes = EnumWrapper("RAIDbatteryLearnModeTypes", {
    "Automatic" : "Automatic",
    "Disabled" : "Disabled",
    "Warn_only" : "Warn only",
}).enum_type

RAIDccModeTypes = EnumWrapper("RAIDccModeTypes", {
    "Normal" : "Normal",
    "StopOnError" : "StopOnError",
}).enum_type

RAIDcopybackModeTypes = EnumWrapper("RAIDcopybackModeTypes", {
    "Off" : "Off",
    "On" : "On",
    "On_with_SMART" : "On with SMART",
}).enum_type

RAIDdedicatedSpareTypes = EnumWrapper("RAIDdedicatedSpareTypes", {
    "autoselect" : "autoselect",
}).enum_type

RAIDdefaultReadPolicyTypes = EnumWrapper("RAIDdefaultReadPolicyTypes", {
    "Adaptive" : "Adaptive",
    "NoReadAhead" : "NoReadAhead",
    "ReadAhead" : "ReadAhead",
}).enum_type

RAIDdefaultWritePolicyTypes = EnumWrapper("RAIDdefaultWritePolicyTypes", {
    "WriteBack" : "WriteBack",
    "WriteBackForce" : "WriteBackForce",
    "WriteThrough" : "WriteThrough",
}).enum_type

RAIDforeignConfigTypes = EnumWrapper("RAIDforeignConfigTypes", {
    "Clear" : "Clear",
    "Ignore" : "Ignore",
    "Import" : "Import",
}).enum_type

RAIDinitOperationTypes = EnumWrapper("RAIDinitOperationTypes", {
    "Fast" : "Fast",
    "T_None" : "None",
}).enum_type

RAIDloadBalancedModeTypes = EnumWrapper("RAIDloadBalancedModeTypes", {
    "Automatic" : "Automatic",
    "Disabled" : "Disabled",
}).enum_type

RAIDprModeTypes = EnumWrapper("RAIDprModeTypes", {
    "Automatic" : "Automatic",
    "Disabled" : "Disabled",
    "Manual" : "Manual",
}).enum_type

RAIDrekeyTypes = EnumWrapper("RAIDrekeyTypes", {
    "T_False" : "False",
    "T_True" : "True",
}).enum_type

RAIDremovecontrollerKeyTypes = EnumWrapper("RAIDremovecontrollerKeyTypes", {
    "T_False" : "False",
    "T_True" : "True",
}).enum_type

RAIDresetConfigTypes = EnumWrapper("RAIDresetConfigTypes", {
    "T_False" : "False",
    "T_True" : "True",
}).enum_type

RAIDsupportedDiskProtTypes = EnumWrapper("RAIDsupportedDiskProtTypes", {
    "SAS" : "SAS",
    "SATA" : "SATA",
}).enum_type

T10PIStatusTypes = EnumWrapper("T10PIStatusTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

StripeSizeTypes = EnumWrapper('StripeSizeTypes', {
     'S_Default' : 'Default',
     'S_512'   : 512,
     'S_1KB'   : 1*1024,
     'S_2KB'   : 2*1024,
     'S_4KB'   : 4*1024,
     'S_8KB'   : 8*1024,
     'S_16KB'  : 16*1024,
     'S_32KB'  : 32*1024,
     'S_64KB'  : 64*1024,
     'S_128KB' : 128*1024,
     'S_256KB' : 256*1024,
     'S_512KB' : 512*1024,
     'S_1MB'   : 1*1024*1024,
     'S_2MB'   : 2*1024*1024,
     'S_4MB'   : 4*1024*1024,
     'S_8MB'   : 8*1024*1024,
     'S_16MB'  : 16*1024*1024,
}).enum_type
