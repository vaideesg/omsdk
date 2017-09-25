from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import logging

logger = logging.getLogger(__name__)

class iDRAC(ClassType):

    def __init__(self, parent = None):
        super().__init__("Component", None, parent)

        # readonly attribute populated by iDRAC
        self.E_12GBackplaneon13GCapable_PlatformCapability = EnumTypeField(None,E_12GBackplaneon13GCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.E_3rdPartyCard_PCIeSlotLFM = EnumTypeField(None,E_3rdPartyCard_PCIeSlotLFMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Destination_SNMPAlert = StringField(None, parent=self)
        self.Description_ChassisInfo = StringField(None, parent=self)
        self.ACRestoreState_PrivateStore = EnumTypeField(None,ACRestoreState_PrivateStoreTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AESKey_SecureDefaultPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AESiv_SecureDefaultPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AcSysRecovery_SysInfo = StringField(None, parent=self)
        self.AccessPrivilege_VirtualConsole = EnumTypeField(None,AccessPrivilege_VirtualConsoleTypes, parent=self)
        self.AccessType_vFlashPartition = EnumTypeField(None,AccessType_vFlashPartitionTypes, parent=self)
        self.Access_QuickSync = EnumTypeField(None,Access_QuickSyncTypes, parent=self)
        self.AccumulateInterval_IPMISOL = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.AccumulativePower_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AccumulativeStartEnergy_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Action_SupportAssist = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ActiveNIC_CurrentNIC = EnumTypeField(None,ActiveNIC_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ActivePolicyName_ServerPwr = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ActivePowerCapVal_ChassisPower = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ActivePowerCapVal_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ActiveSATACount_PrivateStore = IntField(None, parent=self)
        self.ActiveSessions_Racadm = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ActiveSessions_VNCServer = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ActiveSessions_VirtualMedia = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ActiveSharedLOM_CurrentNIC = EnumTypeField(None,ActiveSharedLOM_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address10_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address10_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address11_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address11_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address12_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address12_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address13_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address13_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address14_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address14_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address15_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address15_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address1_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Address1_IPv6 = StringField(None, parent=self)
        self.Address1_IPv6Static = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Address2_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address2_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address3_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address3_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address4_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address4_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address5_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address5_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address6_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address6_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address7_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address7_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address8_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address8_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address9_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address9_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AddressState_IPv6 = EnumTypeField(None,AddressState_IPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Address_EmailAlert = StringField(None, parent=self)
        self.Address_IPv4 = StringField(None, parent=self)
        self.Address_IPv4Static = StringField(None, parent=self)
        self.Address_IPv6 = StringField(None, parent=self)
        self.Address_IPv6Static = StringField(None, parent=self)
        self.AdminState_OS_MC = EnumTypeField(None,AdminState_OS_MCTypes, parent=self)
        self.AgentCommunity_SNMP = StringField(None, parent=self)
        self.AgentEnable_SNMP = EnumTypeField(None,AgentEnable_SNMPTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AirExhaustTempSupport_ThermalSettings = EnumTypeField(None,AirExhaustTempSupport_ThermalSettingsTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AirExhaustTempValueSet_ThermalSettings = StringField(None, parent=self)
        self.AirExhaustTemp_ThermalSettings = EnumTypeField(None,AirExhaustTemp_ThermalSettingsTypes, parent=self)
        self.AisleName_ChassisTopology = StringField(None, parent=self)
        self.AisleName_ServerTopology = StringField(None, parent=self)
        self.AlertAckInterval_SNMPAlert = IntField(None, parent=self)
        self.AlertAddrMigration_PrivateStore = EnumTypeField(None,AlertAddrMigration_PrivateStoreTypes, parent=self)
        self.AlertEnable_IPMILan = EnumTypeField(None,AlertEnable_IPMILanTypes, parent=self)
        self.AlertEntry_IPMIPefSeldomAlerts = StringField(None, parent=self)
        self.AlertPort_CMCSNMPAlert = IntField(None, parent=self)
        self.AlertPort_SNMP = IntField(None, parent=self)
        self.AlertStartupDelay_IPMIPefSeldom = StringField(None, parent=self)
        self.AlertStringEntry_IPMIPefSeldomAlerts = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.AllowableLicenses_PlatformLicense = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ApplyNICSelection_NIC = EnumTypeField(None,ApplyNICSelection_NICTypes, parent=self)
        self.ApplyReboot_AutoUpdate = IntField(None, parent=self)
        self.ArpControl_IPMIIPConfig = StringField(None, parent=self)
        self.ArpInterval_IPMIIPConfig = StringField(None, parent=self)
        self.AssetTagSetByDCMI_ServerInfo = EnumTypeField(None,AssetTagSetByDCMI_ServerInfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AssetTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AssetTag_ServerInfo = StringField(None, parent=self)
        self.AttachMode_RFS = EnumTypeField(None,AttachMode_RFSTypes, parent=self)
        self.AttachState_VirtualConsole = EnumTypeField(None,AttachState_VirtualConsoleTypes, parent=self)
        self.AttachState_vFlashPartition = EnumTypeField(None,AttachState_vFlashPartitionTypes, parent=self)
        self.Attached_VirtualMedia = EnumTypeField(None,Attached_VirtualMediaTypes, parent=self)
        self.AuthFailureCount_QuickSync = IntField(None, parent=self)
        self.AuthFailureTime_QuickSync = StringField(None, parent=self)
        self.AuthTimeout_ActiveDirectory = IntField(None, parent=self)
        self.AuthenticationEnables_IPMILANConfig = StringField(None, parent=self)
        self.AuthenticationProtocol_Users = EnumTypeField(None,AuthenticationProtocol_UsersTypes, parent=self)
        self.AuthenticationTypeEnables_IPMISerial = StringField(None, parent=self)
        self.Authentication_IPMISOL = EnumTypeField(None,Authentication_IPMISOLTypes, parent=self)
        self.AutoBackup_LCAttributes = EnumTypeField(None,AutoBackup_LCAttributesTypes, parent=self)
        self.AutoConfigIPV6_NIC = EnumTypeField(None,AutoConfigIPV6_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AutoConfig_CurrentIPv6 = EnumTypeField(None,AutoConfig_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AutoConfig_IPv6 = EnumTypeField(None,AutoConfig_IPv6Types, parent=self)
        self.AutoConfig_NIC = EnumTypeField(None,AutoConfig_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AutoDetect_CurrentNIC = EnumTypeField(None,AutoDetect_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AutoDetect_NIC = EnumTypeField(None,AutoDetect_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AutoDiscovery_LCAttributes = EnumTypeField(None,AutoDiscovery_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AutoEnable_SerialRedirection = EnumTypeField(None,AutoEnable_SerialRedirectionTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AutoNegotiate_SECONDARYNIC = EnumTypeField(None,AutoNegotiate_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AutoOSLockState_AutoOSLockGroup = EnumTypeField(None,AutoOSLockState_AutoOSLockGroupTypes, parent=self)
        self.AutoRestore_LCAttributes = EnumTypeField(None,AutoRestore_LCAttributesTypes, parent=self)
        self.AutoUpdate_LCAttributes = EnumTypeField(None,AutoUpdate_LCAttributesTypes, parent=self)
        self.Autoduplex_NIC = EnumTypeField(None,Autoduplex_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Autoneg_CurrentNIC = EnumTypeField(None,Autoneg_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Autoneg_NIC = EnumTypeField(None,Autoneg_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AvailableSize_vFlashSD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AvailableSpareAlertThreshold_Storage = IntField(None, parent=self)
        self.BIOSFeature_SysInfo = StringField(None, parent=self)
        self.BIOSRTDRequested_LCAttributes = EnumTypeField(None,BIOSRTDRequested_LCAttributesTypes, parent=self)
        self.BIOSStatus_SysInfo = StringField(None, parent=self)
        self.BMCRecordID_IPMIPefOften = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BSODBootCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BSODBootCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BackplaneBusMode_Backplane = EnumTypeField(None,BackplaneBusMode_BackplaneTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BackplaneCable0ErrorMask_DCSCustom = IntField(None, parent=self)
        self.BackplaneCable1ErrorMask_DCSCustom = IntField(None, parent=self)
        self.BackplaneCable2ErrorMask_DCSCustom = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BackplaneCapable_PlatformCapability = EnumTypeField(None,BackplaneCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BackplaneSplitMode_Backplane = IntField(None, parent=self)
        self.BackupGatewayIP_IPMIIPConfig = StringField(None, parent=self)
        self.BackupGatewayMac_IPMIIPConfig = StringField(None, parent=self)
        self.BaseDN_LDAP = StringField(None, parent=self)
        self.BaudRate_IPMISOL = EnumTypeField(None,BaudRate_IPMISOLTypes, parent=self)
        self.BaudRate_IPMISerial = EnumTypeField(None,BaudRate_IPMISerialTypes, parent=self)
        self.BaudRate_Serial = EnumTypeField(None,BaudRate_SerialTypes, parent=self)
        self.Begin_Update = EnumTypeField(None,Begin_UpdateTypes, parent=self)
        self.BindDN_LDAP = StringField(None, parent=self)
        self.BindPassword_LDAP = StringField(None, parent=self)
        self.Bitmap_vFlashSD = StringField(None, parent=self)
        self.BladeAllocatedPwr_PrivateStore = IntField(None, parent=self)
        self.BladeBIOSBudgetMax_PrivateStore = IntField(None, parent=self)
        self.BladeBIOSBudgetMin_PrivateStore = IntField(None, parent=self)
        self.BladeBIOSRuntimeMax_PrivateStore = IntField(None, parent=self)
        self.BladeBIOSRuntimeMin_PrivateStore = IntField(None, parent=self)
        self.BladeCPUNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeCPUThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BladeFabricMismatch_PrivateStore = IntField(None, parent=self)
        self.BladeHDDPwr_PrivateStore = IntField(None, parent=self)
        self.BladeHDDThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BladeInsertionPrompt_LCD = EnumTypeField(None,BladeInsertionPrompt_LCDTypes, parent=self)
        self.BladeMemNThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BladeMemNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeMezzNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeMezzThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BladeNDCNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeNDCThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BladePlatformLimit_PrivateStore = IntField(None, parent=self)
        self.BladePreBudgetMax_PrivateStore = IntField(None, parent=self)
        self.BladePreBudgetMin_PrivateStore = IntField(None, parent=self)
        self.BladeSeamlessMethod_PrivateStore = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BladeSlotInfo_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BladeSlotNumInChassis_ServerTopology = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BladeStorNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeStorThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.BlinkPattern_IndicatorLCP = EnumTypeField(None,BlinkPattern_IndicatorLCPTypes, parent=self)
        self.BlockEnable_IPBlocking = EnumTypeField(None,BlockEnable_IPBlockingTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.BluetoothCapable_PlatformCapability = EnumTypeField(None,BluetoothCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BootCaptureFileCount_VirtualConsole = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BootCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BootCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BootCaptureSequence_VirtualConsole = IntField(None, parent=self)
        self.BootOnce_ServerBoot = EnumTypeField(None,BootOnce_ServerBootTypes, parent=self)
        self.BootOnce_VirtualMedia = EnumTypeField(None,BootOnce_VirtualMediaTypes, parent=self)
        self.BootToMaser_LCAttributes = EnumTypeField(None,BootToMaser_LCAttributesTypes, parent=self)
        self.BrdRevision_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Build_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ButtonDisable_FrontPanel = EnumTypeField(None,ButtonDisable_FrontPanelTypes, parent=self)
        self.CACertificate_SecuritySSL = StringField(None, parent=self)
        self.CIPHERSuiteDisable_PrivateStore = EnumTypeField(None,CIPHERSuiteDisable_PrivateStoreTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CMCIP_LCAttributes = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCIPv6Info_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCIPv6Url_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCInfo_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CMCResetState_NIC = EnumTypeField(None,CMCResetState_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CMCUrl_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CPLDVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CPUInfos_SysInfo = StringField(None, parent=self)
        self.CSCCsrBusiness_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCityName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCommonName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCountryCode_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrDeptName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrEmailAddr_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrStateName_SecurityCSC = StringField(None, parent=self)
        self.CSIORLaunched_LCAttributes = EnumTypeField(None,CSIORLaunched_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CUPSCapable_PlatformCapability = EnumTypeField(None,CUPSCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CaCertPath_Security = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Capacity_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CardType_GpGPUTable = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CardType_PCIeSlotLFM = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CatalogID_AutoUpdate = StringField(None, parent=self)
        self.CatalogName_AutoUpdate = StringField(None, parent=self)
        self.CertValidationEnable_ActiveDirectory = EnumTypeField(None,CertValidationEnable_ActiveDirectoryTypes, parent=self)
        self.CertValidationEnable_LDAP = EnumTypeField(None,CertValidationEnable_LDAPTypes, parent=self)
        self.Certificate_SecuritySSL = StringField(None, parent=self)
        self.ChanPrivLimit_IPMISerial = EnumTypeField(None,ChanPrivLimit_IPMISerialTypes, parent=self)
        self.ChannelAccess_IPMILANConfig = StringField(None, parent=self)
        self.ChannelAccess_IPMISerial = IntField(None, parent=self)
        self.ChannelEnableCommand_IPMIFireWallChannel = StringField(None, parent=self)
        self.ChannelHeader_IPMIFireWallChannel = StringField(None, parent=self)
        self.ChannelOffset_IPMIFireWall = StringField(None, parent=self)
        self.ChannelSubFunctionSetting_IPMIFireWallChannel = StringField(None, parent=self)
        self.ChassisData_IPMIChassisData = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisHeight_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisIdentifyDuration_LCD = IntField(None, parent=self)
        self.ChassisIdentifyEnable_LCD = EnumTypeField(None,ChassisIdentifyEnable_LCDTypes, parent=self)
        self.ChassisInfraPower_SC_MC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisIntrusionCapable_PlatformCapability = EnumTypeField(None,ChassisIntrusionCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisLEDState_ChassisPwrState = EnumTypeField(None,ChassisLEDState_ChassisPwrStateTypes, parent=self)
        self.ChassisManagementMonitoring_ChassisControl = EnumTypeField(None,ChassisManagementMonitoring_ChassisControlTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisManagementatServer_ChassisControl = EnumTypeField(None,ChassisManagementatServer_ChassisControlTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChassisModel_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisModel_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChassisName_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisName_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisName_Info = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisName_ServerTopology = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisPSUInfoCapability_RSM = EnumTypeField(None,ChassisPSUInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisPowerCap_SC_MC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisPowerInfoCapability_RSM = EnumTypeField(None,ChassisPowerInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisPowerPolicy_Info = EnumTypeField(None,ChassisPowerPolicy_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisPowerStatus_Info = EnumTypeField(None,ChassisPowerStatus_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisResetOperation_Info = EnumTypeField(None,ChassisResetOperation_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisServiceTagCRC_SC_MC = IntField(None, parent=self)
        self.ChassisServiceTagLen_SC_MC = IntField(None, parent=self)
        self.ChassisServiceTagSet_SC_MC = IntField(None, parent=self)
        # readonly attribute
        self.ChassisServiceTag_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisServiceTag_SC_MC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisSubType_Info = EnumTypeField(None,ChassisSubType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisSystemInfoCapability_RSM = EnumTypeField(None,ChassisSystemInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisType_ChassisInfo = EnumTypeField(None,ChassisType_ChassisInfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisType_Info = EnumTypeField(None,ChassisType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CipherSuitePrivilege_IPMILANConfig = StringField(None, parent=self)
        self.CloneStatus_GroupManager = EnumTypeField(None,CloneStatus_GroupManagerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ClusterState_EC = EnumTypeField(None,ClusterState_ECTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ClusterState_MSM = EnumTypeField(None,ClusterState_MSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CollectSystemInventoryOnRestart_LCAttributes = EnumTypeField(None,CollectSystemInventoryOnRestart_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Columns_SlotConfig = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Command_Serial = StringField(None, parent=self)
        self.CommunityName_CMCSNMPAlert = StringField(None, parent=self)
        self.CommunityName_IPMILan = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CompDisplayName_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ConfigCertStatus_Security = IntField(None, parent=self)
        self.ConfigChangedByUser_NIC = EnumTypeField(None,ConfigChangedByUser_NICTypes, parent=self)
        self.ConfigMaxDelay_NIC = IntField(None, parent=self)
        self.Config_CMCSlot = StringField(None, parent=self)
        self.Config_FanSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Config_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Config_IOMSlot = StringField(None, parent=self)
        self.Config_PSUSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Config_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Config_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ConfigurationUpdateTimeStamp_GroupManager = StringField(None, parent=self)
        self.ConfigurationXML_USB = EnumTypeField(None,ConfigurationXML_USBTypes, parent=self)
        self.Configuration_LCD = EnumTypeField(None,Configuration_LCDTypes, parent=self)
        self.ConnectionMode_IPMISerial = EnumTypeField(None,ConnectionMode_IPMISerialTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ContainedIn_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Contains_CMCSlot = StringField(None, parent=self)
        self.Contains_FanSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Contains_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Contains_IOMSlot = StringField(None, parent=self)
        self.Contains_PSUSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Contains_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Contains_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ControlCollaboration_WebServer = IntField(None, parent=self)
        self.ControlVFLoder_WebServer = IntField(None, parent=self)
        self.Control_IPMIPefSeldom = StringField(None, parent=self)
        self.ControllerIPMBAddress_IPMISystemParameter = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CrashVideoCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CrashVideoCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CreatingUser_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CriticalEventGenerationInterval_ThermalConfig = IntField(None, parent=self)
        self.CsrCommonName_Security = StringField(None, parent=self)
        self.CsrCountryCode_Security = StringField(None, parent=self)
        self.CsrEmailAddr_Security = StringField(None, parent=self)
        self.CsrKeySize_Security = EnumTypeField(None,CsrKeySize_SecurityTypes, parent=self)
        self.CsrLocalityName_Security = StringField(None, parent=self)
        self.CsrOrganizationName_Security = StringField(None, parent=self)
        self.CsrOrganizationUnit_Security = StringField(None, parent=self)
        self.CsrStateName_Security = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CumulativePowerStartTime_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CurrentDisplay_LCD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CurrentFPStates_LCD = IntField(None, parent=self)
        self.CustomLFM_PCIeSlotLFM = IntField(None, parent=self)
        self.CustomMsg_EmailAlert = StringField(None, parent=self)
        self.CustomUI_DCSCustom = EnumTypeField(None,CustomUI_DCSCustomTypes, parent=self)
        self.DCLookupByUserDomain_ActiveDirectory = EnumTypeField(None,DCLookupByUserDomain_ActiveDirectoryTypes, parent=self)
        self.DCLookupDomainName_ActiveDirectory = StringField(None, parent=self)
        self.DCLookupEnable_ActiveDirectory = EnumTypeField(None,DCLookupEnable_ActiveDirectoryTypes, parent=self)
        self.DCMIControl_DCMIThermal = IntField(None, parent=self)
        self.DCMIDHCPmgmtstring_NIC = StringField(None, parent=self)
        self.DCMIDHCPopt12_NIC = EnumTypeField(None,DCMIDHCPopt12_NICTypes, parent=self)
        self.DCMIDHCPopt60opt43_NIC = EnumTypeField(None,DCMIDHCPopt60opt43_NICTypes, parent=self)
        self.DCMIDHCPpkttimeout_NIC = IntField(None, parent=self)
        self.DCMIDHCPrandombackoff_NIC = EnumTypeField(None,DCMIDHCPrandombackoff_NICTypes, parent=self)
        self.DCMIDHCPretrytimeout_NIC = IntField(None, parent=self)
        self.DCMIDHCPwaitinterval_NIC = IntField(None, parent=self)
        self.DCSCtlr1Reset_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr1Status_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr2Reset_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr2Status_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlrSync_DCSResetCtlr = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DHCPEnable_CurrentIPv4 = EnumTypeField(None,DHCPEnable_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DHCPEnable_IPv4 = EnumTypeField(None,DHCPEnable_IPv4Types, parent=self)
        self.DHCPEnable_SECONDARYNIC = EnumTypeField(None,DHCPEnable_SECONDARYNICTypes, parent=self)
        self.DN.1_LDAPRoleGroup = StringField(None, parent=self)
        self.DN.2_LDAPRoleGroup = StringField(None, parent=self)
        self.DN.3_LDAPRoleGroup = StringField(None, parent=self)
        self.DN.4_LDAPRoleGroup = StringField(None, parent=self)
        self.DN.5_LDAPRoleGroup = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DNS1_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS1_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNS1_IPv4 = StringField(None, parent=self)
        self.DNS1_IPv4Static = StringField(None, parent=self)
        self.DNS1_IPv6 = StringField(None, parent=self)
        self.DNS1_IPv6Static = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DNS2_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS2_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNS2_IPv4 = StringField(None, parent=self)
        self.DNS2_IPv4Static = StringField(None, parent=self)
        self.DNS2_IPv6 = StringField(None, parent=self)
        self.DNS2_IPv6Static = StringField(None, parent=self)
        self.DNSDRACName_SECONDARYNIC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSDomainFromDHCP_CurrentNIC = EnumTypeField(None,DNSDomainFromDHCP_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSDomainFromDHCP_NIC = EnumTypeField(None,DNSDomainFromDHCP_NICTypes, parent=self)
        self.DNSDomainFromDHCP_NICStatic = EnumTypeField(None,DNSDomainFromDHCP_NICStaticTypes, parent=self)
        self.DNSDomainNameFromDHCP_NIC = EnumTypeField(None,DNSDomainNameFromDHCP_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSDomainName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSDomainName_NIC = StringField(None, parent=self)
        self.DNSDomainName_NICStatic = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSFromDHCP6_CurrentIPv6 = EnumTypeField(None,DNSFromDHCP6_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSFromDHCP6_IPv6 = EnumTypeField(None,DNSFromDHCP6_IPv6Types, parent=self)
        self.DNSFromDHCP6_IPv6Static = EnumTypeField(None,DNSFromDHCP6_IPv6StaticTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSFromDHCP_CurrentIPv4 = EnumTypeField(None,DNSFromDHCP_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSFromDHCP_IPv4 = EnumTypeField(None,DNSFromDHCP_IPv4Types, parent=self)
        self.DNSFromDHCP_IPv4Static = EnumTypeField(None,DNSFromDHCP_IPv4StaticTypes, parent=self)
        self.DNSFromDHCP_SECONDARYNIC = EnumTypeField(None,DNSFromDHCP_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSRacName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSRacName_NIC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DNSRegister_CurrentNIC = EnumTypeField(None,DNSRegister_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DNSRegister_NIC = EnumTypeField(None,DNSRegister_NICTypes, parent=self)
        self.DNSServer1_SECONDARYNIC = StringField(None, parent=self)
        self.DNSServer2_SECONDARYNIC = StringField(None, parent=self)
        self.DN_LDAPRoleGroup = StringField(None, parent=self)
        self.DPCapable_PlatformCapability = EnumTypeField(None,DPCapable_PlatformCapabilityTypes, parent=self)
        self.DataCenterName_ChassisTopology = StringField(None, parent=self)
        self.DataCenterName_ServerTopology = StringField(None, parent=self)
        self.DataVersion_PMLicensing = StringField(None, parent=self)
        self.DayLightOffset_Time = IntField(None, parent=self)
        self.DayofMonth_AutoBackup = StringField(None, parent=self)
        self.DayofMonth_AutoUpdate = StringField(None, parent=self)
        self.DayofWeek_AutoBackup = StringField(None, parent=self)
        self.DayofWeek_AutoUpdate = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DedicatedNICCapable_PlatformCapability = EnumTypeField(None,DedicatedNICCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DedicatedNICScanTime_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DedicatedNICScanTime_NIC = IntField(None, parent=self)
        self.DefaultCredentialMitigation_DefaultCredentialMitigationConfigGroup = EnumTypeField(None,DefaultCredentialMitigation_DefaultCredentialMitigationConfigGroupTypes, parent=self)
        self.DefaultGatewayMAC_IPMIIPConfig = StringField(None, parent=self)
        self.DefaultIPAddress_SupportAssist = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DefaultLicenseFeatures_PlatformLicense = EnumTypeField(None,DefaultLicenseFeatures_PlatformLicenseTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DefaultLocalPathName_SupportAssist = StringField(None, parent=self)
        self.DefaultPassword_SupportAssist = StringField(None, parent=self)
        self.DefaultProtocol_SupportAssist = EnumTypeField(None,DefaultProtocol_SupportAssistTypes, parent=self)
        self.DefaultScreen_LCD = EnumTypeField(None,DefaultScreen_LCDTypes, parent=self)
        self.DefaultShareName_SupportAssist = StringField(None, parent=self)
        self.DefaultUserCreated_SecureDefaultPassword = EnumTypeField(None,DefaultUserCreated_SecureDefaultPasswordTypes, parent=self)
        self.DefaultUserName_SupportAssist = StringField(None, parent=self)
        self.DefaultWorkgroupName_SupportAssist = StringField(None, parent=self)
        self.DeleteControl_IPMISerial = EnumTypeField(None,DeleteControl_IPMISerialTypes, parent=self)
        self.DeliveryRetryAttempts_RedfishEventing = IntField(None, parent=self)
        self.DeliveryRetryIntervalInSeconds_RedfishEventing = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Description_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Description_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Description_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Description_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DestIPv4Addr_SNMPTrapIPv4 = StringField(None, parent=self)
        self.DestIPv4Address_MSMSNMPTrapIPv4 = StringField(None, parent=self)
        self.DestIPv6Addr_LDAPRoleGroup = StringField(None, parent=self)
        self.DestIPv6Addr_SNMPTrapIPv6 = StringField(None, parent=self)
        self.DestIPv6Address_CMCSNMPTrapIPv6 = StringField(None, parent=self)
        self.DestIPv6Address_MSMSNMPTrapIPv6 = StringField(None, parent=self)
        self.DestinationMACAddress_IPMILANPEFConfig = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DestinationNum_LDAPRoleGroup = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.DestinationNum_SNMPTrapIPv4 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.DestinationNum_SNMPTrapIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DestinationType_SNMPAlert = IntField(None, parent=self)
        self.Destination_SNMPAlert = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DeviceGUID_IPMISystemParameter = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DeviceProp_SATAInventory = StringField(None, parent=self)
        self.DiagsJobScheduled_LCAttributes = EnumTypeField(None,DiagsJobScheduled_LCAttributesTypes, parent=self)
        self.Did_GpGPUTable = IntField(None, parent=self)
        self.DisablePowerButton_ChassisPower = EnumTypeField(None,DisablePowerButton_ChassisPowerTypes, parent=self)
        self.DiscoveryEnable_IntegratedDatacenter = EnumTypeField(None,DiscoveryEnable_IntegratedDatacenterTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DiscoveryFactoryDefaults_LCAttributes = EnumTypeField(None,DiscoveryFactoryDefaults_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DiscoveryPort_SNMP = IntField(None, parent=self)
        self.DisplayToeTagError_SecureDefaultPassword = EnumTypeField(None,DisplayToeTagError_SecureDefaultPasswordTypes, parent=self)
        self.DomainController1_ActiveDirectory = StringField(None, parent=self)
        self.DomainController2_ActiveDirectory = StringField(None, parent=self)
        self.DomainController3_ActiveDirectory = StringField(None, parent=self)
        self.DomainNameDHCP_SECONDARYNIC = EnumTypeField(None,DomainNameDHCP_SECONDARYNICTypes, parent=self)
        self.Domain_ADGroup = StringField(None, parent=self)
        self.Domain_AutoBackup = StringField(None, parent=self)
        self.Domain_AutoUpdate = StringField(None, parent=self)
        self.DummySwitchConnection_NIC = StringField(None, parent=self)
        self.DummySwitchPortConnection_NIC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Duplex_CurrentNIC = EnumTypeField(None,Duplex_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Duplex_NIC = EnumTypeField(None,Duplex_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Duplex_SECONDARYNIC = EnumTypeField(None,Duplex_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DynamicStepUp_ServerPwr = EnumTypeField(None,DynamicStepUp_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ECComponentID_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ECStartTime_ChassisPower = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ETAG_Users = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.EchoControl_IPMISerial = EnumTypeField(None,EchoControl_IPMISerialTypes, parent=self)
        self.Eject_IntegratedDatacenter = EnumTypeField(None,Eject_IntegratedDatacenterTypes, parent=self)
        self.EmailOptIn_SupportAssist = EnumTypeField(None,EmailOptIn_SupportAssistTypes, parent=self)
        self.EmbeddedNICBIBInfo_NIC = StringField(None, parent=self)
        self.EmbeddedNICMAC_SysInfo = StringField(None, parent=self)
        self.EmulationType_vFlashPartition = EnumTypeField(None,EmulationType_vFlashPartitionTypes, parent=self)
        self.EnableChassisConsoleAccess_VirtualConsole = EnumTypeField(None,EnableChassisConsoleAccess_VirtualConsoleTypes, parent=self)
        self.EnableSCAttributes_SC_MC = IntField(None, parent=self)
        self.EnableSharedCompUpdate_Update = EnumTypeField(None,EnableSharedCompUpdate_UpdateTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.EnableStatus_MgmtNetworkInterface = EnumTypeField(None,EnableStatus_MgmtNetworkInterfaceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Enable_ASRConfig = EnumTypeField(None,Enable_ASRConfigTypes, parent=self)
        self.Enable_ActiveDirectory = EnumTypeField(None,Enable_ActiveDirectoryTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentIPv4 = EnumTypeField(None,Enable_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentIPv6 = EnumTypeField(None,Enable_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentNIC = EnumTypeField(None,Enable_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Enable_EmailAlert = EnumTypeField(None,Enable_EmailAlertTypes, parent=self)
        self.Enable_IPMILan = EnumTypeField(None,Enable_IPMILanTypes, parent=self)
        self.Enable_IPMISOL = EnumTypeField(None,Enable_IPMISOLTypes, parent=self)
        self.Enable_IPv4 = EnumTypeField(None,Enable_IPv4Types, parent=self)
        self.Enable_IPv6 = EnumTypeField(None,Enable_IPv6Types, parent=self)
        self.Enable_LDAP = EnumTypeField(None,Enable_LDAPTypes, parent=self)
        self.Enable_NIC = EnumTypeField(None,Enable_NICTypes, parent=self)
        self.Enable_RFS = EnumTypeField(None,Enable_RFSTypes, parent=self)
        self.Enable_Racadm = EnumTypeField(None,Enable_RacadmTypes, parent=self)
        self.Enable_Racadm = EnumTypeField(None,Enable_RacadmTypes, parent=self)
        self.Enable_Redfish = EnumTypeField(None,Enable_RedfishTypes, parent=self)
        self.Enable_SNMPAlert = EnumTypeField(None,Enable_SNMPAlertTypes, parent=self)
        self.Enable_SSH = EnumTypeField(None,Enable_SSHTypes, parent=self)
        self.Enable_Serial = EnumTypeField(None,Enable_SerialTypes, parent=self)
        self.Enable_SerialRedirection = EnumTypeField(None,Enable_SerialRedirectionTypes, parent=self)
        self.Enable_SwitchConnectionView = EnumTypeField(None,Enable_SwitchConnectionViewTypes, parent=self)
        self.Enable_Telnet = EnumTypeField(None,Enable_TelnetTypes, parent=self)
        self.Enable_Users = EnumTypeField(None,Enable_UsersTypes, parent=self)
        self.Enable_VNCServer = EnumTypeField(None,Enable_VNCServerTypes, parent=self)
        self.Enable_VirtualConsole = EnumTypeField(None,Enable_VirtualConsoleTypes, parent=self)
        self.Enable_WebServer = EnumTypeField(None,Enable_WebServerTypes, parent=self)
        self.Enable_vFlashSD = EnumTypeField(None,Enable_vFlashSDTypes, parent=self)
        self.EnabledOnFrontPanel_VirtualConsole = EnumTypeField(None,EnabledOnFrontPanel_VirtualConsoleTypes, parent=self)
        self.Enabled_STP = EnumTypeField(None,Enabled_STPTypes, parent=self)
        self.EncryptEnable_VirtualConsole = EnumTypeField(None,EncryptEnable_VirtualConsoleTypes, parent=self)
        self.EncryptEnable_VirtualMedia = EnumTypeField(None,EncryptEnable_VirtualMediaTypes, parent=self)
        self.EncryptionKey_IPMILan = StringField(None, parent=self)
        self.EncryptionStatus_GroupManager = EnumTypeField(None,EncryptionStatus_GroupManagerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.EndTime_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EndTime_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EngineID_SNMP = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ErrorCode_SupportAssist = StringField(None, parent=self)
        self.ErrorDisplayMode_LCD = EnumTypeField(None,ErrorDisplayMode_LCDTypes, parent=self)
        self.EventBasedAutoCollection_SupportAssist = EnumTypeField(None,EventBasedAutoCollection_SupportAssistTypes, parent=self)
        self.EventGenerationInterval_ThermalConfig = IntField(None, parent=self)
        self.ExceptionAction_DCMIThermal = IntField(None, parent=self)
        self.ExceptionTime_DCMIThermal = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ExpressServiceCode_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FIPSMode_Security = EnumTypeField(None,FIPSMode_SecurityTypes, parent=self)
        self.FPConfig_SysInfo = StringField(None, parent=self)
        self.FPStatus_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.FQDD_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FQDD_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FQDD_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FReDFWVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FTRCapable_PlatformCapability = EnumTypeField(None,FTRCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FWVersion_SysInfo = StringField(None, parent=self)
        self.FaceplatePowerWatts_ChassisPower = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.FactoryMAC_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FailCount_IPBlocking = IntField(None, parent=self)
        self.FailWindow_IPBlocking = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Failover_CurrentNIC = EnumTypeField(None,Failover_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Failover_NIC = EnumTypeField(None,Failover_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FanHealth_Info = EnumTypeField(None,FanHealth_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanName_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FanRedundancy_Info = EnumTypeField(None,FanRedundancy_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FanSpeedHighOffsetVal_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanSpeedLowOffsetVal_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanSpeedMaxOffsetVal_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanSpeedMediumOffsetVal_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanSpeedOffsetValueSet_ThermalSettings = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FanSpeedOffset_ThermalSettings = EnumTypeField(None,FanSpeedOffset_ThermalSettingsTypes, parent=self)
        self.FieldSupportDebugAESIV_Security = StringField(None, parent=self)
        self.FilePath_SupportAssist = StringField(None, parent=self)
        self.FilterAutoCollections_SupportAssist = EnumTypeField(None,FilterAutoCollections_SupportAssistTypes, parent=self)
        self.FilterEntry_IPMIPEFSeldomFilter = StringField(None, parent=self)
        self.FirmwareVersion_CMC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.FirmwareVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FirstBootDevice_ServerBoot = EnumTypeField(None,FirstBootDevice_ServerBootTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FlexMacCompleted_NIC = EnumTypeField(None,FlexMacCompleted_NICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Flexmacaddress_NIC = StringField(None, parent=self)
        self.FloppyEmulation_VirtualMedia = EnumTypeField(None,FloppyEmulation_VirtualMediaTypes, parent=self)
        self.FlowControl_IPMISerial = EnumTypeField(None,FlowControl_IPMISerialTypes, parent=self)
        self.FormatType_vFlashPartition = EnumTypeField(None,FormatType_vFlashPartitionTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FreshAirCapable_PlatformCapability = EnumTypeField(None,FreshAirCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FreshAirCompliantConfiguration_ThermalConfig = EnumTypeField(None,FreshAirCompliantConfiguration_ThermalConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FrontPanelCapable_PlatformCapability = EnumTypeField(None,FrontPanelCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FrontPanelLocking_LCD = EnumTypeField(None,FrontPanelLocking_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FrontPanelUSBCapable_PlatformCapability = EnumTypeField(None,FrontPanelUSBCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FwUpdateIPAddr_Update = StringField(None, parent=self)
        self.FwUpdatePath_Update = StringField(None, parent=self)
        self.FwUpdateTFTPEnable_Update = EnumTypeField(None,FwUpdateTFTPEnable_UpdateTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FwupdatePart_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.G5KxcablePresence_NIC = EnumTypeField(None,G5KxcablePresence_NICTypes, parent=self)
        self.GCLookupEnable_ActiveDirectory = EnumTypeField(None,GCLookupEnable_ActiveDirectoryTypes, parent=self)
        self.GCRootDomain_ActiveDirectory = StringField(None, parent=self)
        self.GUID_SysInfo = StringField(None, parent=self)
        self.GatewaySelector_IPMILANPEFConfig = EnumTypeField(None,GatewaySelector_IPMILANPEFConfigTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Gateway_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Gateway_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Gateway_IPv4 = StringField(None, parent=self)
        self.Gateway_IPv4Static = StringField(None, parent=self)
        self.Gateway_IPv6 = StringField(None, parent=self)
        self.Gateway_IPv6Static = StringField(None, parent=self)
        self.Gen_GpGPUTable = IntField(None, parent=self)
        self.GlobalCatalog1_ActiveDirectory = StringField(None, parent=self)
        self.GlobalCatalog2_ActiveDirectory = StringField(None, parent=self)
        self.GlobalCatalog3_ActiveDirectory = StringField(None, parent=self)
        self.GlobalControl_IPMIPefSeldom = StringField(None, parent=self)
        self.GpGPUActiveEntries_ServerPwr = IntField(None, parent=self)
        self.GpuDCT_GpGPUTable = IntField(None, parent=self)
        self.GpuHotSup_GpGPUTable = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.GraphicsURI_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.GroupAttributeIsDN_LDAP = EnumTypeField(None,GroupAttributeIsDN_LDAPTypes, parent=self)
        self.GroupAttribute_LDAP = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.GroupCreateTimestamp_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.GroupMasterElectionWaitTime_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.GroupName_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.GroupPasscode_GroupManager = StringField(None, parent=self)
        self.GroupPingerInterval_GroupManager = IntField(None, parent=self)
        self.GroupPublishInterval_GroupManager = IntField(None, parent=self)
        self.GroupTaskAutoRetryCount_GroupManager = IntField(None, parent=self)
        self.GroupTaskAutoRetryInterval_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.GroupUUID_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.GroupingTimestamp_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.GroupingUser_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.HWRev_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HandshakeControl_IPMISerial = EnumTypeField(None,HandshakeControl_IPMISerialTypes, parent=self)
        self.HardwareIdentityCertStatus_Certificate = EnumTypeField(None,HardwareIdentityCertStatus_CertificateTypes, parent=self)
        self.HardwareVersion_Info = StringField(None, parent=self)
        self.Header_IPMIFireWall = StringField(None, parent=self)
        self.HealthStatus_MSM = EnumTypeField(None,HealthStatus_MSMTypes, parent=self)
        self.Health_vFlashSD = EnumTypeField(None,Health_vFlashSDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.HelpURL_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HideErrs_LCD = EnumTypeField(None,HideErrs_LCDTypes, parent=self)
        self.HistorySize_Serial = IntField(None, parent=self)
        self.HostFrontPortStatus_USB = EnumTypeField(None,HostFrontPortStatus_USBTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.HostFrontPortsDynamicMode_USB = EnumTypeField(None,HostFrontPortsDynamicMode_USBTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HostNameBinary_SysInfo = StringField(None, parent=self)
        self.HostName_SECONDARYNIC = StringField(None, parent=self)
        self.HostName_ServerOS = StringField(None, parent=self)
        self.HostOSProxyAddress_SupportAssist = StringField(None, parent=self)
        self.HostOSProxyConfigured_SupportAssist = EnumTypeField(None,HostOSProxyConfigured_SupportAssistTypes, parent=self)
        self.HostOSProxyPassword_SupportAssist = StringField(None, parent=self)
        self.HostOSProxyPort_SupportAssist = IntField(None, parent=self)
        self.HostOSProxyUserName_SupportAssist = StringField(None, parent=self)
        self.HostSNMPAlert_ServiceModule = EnumTypeField(None,HostSNMPAlert_ServiceModuleTypes, parent=self)
        self.HttpPort_WebServer = IntField(None, parent=self)
        self.HttpsPort_WebServer = IntField(None, parent=self)
        self.HttpsRedirection_WebServer = EnumTypeField(None,HttpsRedirection_WebServerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.IDSDMCapable_PlatformCapability = EnumTypeField(None,IDSDMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IDSDMState_PrivateStore = EnumTypeField(None,IDSDMState_PrivateStoreTypes, parent=self)
        self.ID_ChassisHealthIndicator = StringField(None, parent=self)
        self.ID_IdentifyButton = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ID_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ID_PowerButton = StringField(None, parent=self)
        self.ID_PowerHealthIndicator = StringField(None, parent=self)
        self.ID_ThermalHealthIndicator = StringField(None, parent=self)
        self.IOIDOptEnable_IOIDOpt = EnumTypeField(None,IOIDOptEnable_IOIDOptTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.IOM1i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOM2i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOM3i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOM4i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOM5i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOM6i2cBusNo_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOMFWVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOMType_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IPAddress_AutoBackup = StringField(None, parent=self)
        self.IPAddress_AutoUpdate = StringField(None, parent=self)
        self.IPAddress_LCAttributes = StringField(None, parent=self)
        self.IPChangeNotifyPS_LCAttributes = EnumTypeField(None,IPChangeNotifyPS_LCAttributesTypes, parent=self)
        self.IPHeader_IPMIIPConfig = StringField(None, parent=self)
        self.IPMIKey_Users = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IPMIVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IPV4Address_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4Gateway_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4NetMask_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4StaticDomainName_SECONDARYNIC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IPV6NumOfExtAddress_CurrentIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IPV6NumOfExtAddress_IPv6 = IntField(None, parent=self)
        self.IPv4Enable_SECONDARYNIC = EnumTypeField(None,IPv4Enable_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.IPv4_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ISInfos_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Id_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Id_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IdleTimeout_Serial = IntField(None, parent=self)
        self.IdracPTEpIpAddr_OS_MC = StringField(None, parent=self)
        self.IgnoreCertWarning_LCAttributes = EnumTypeField(None,IgnoreCertWarning_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.IgnoreCertificateErrors_RedfishEventing = EnumTypeField(None,IgnoreCertificateErrors_RedfishEventingTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ImageFileName_VirtualMedia = StringField(None, parent=self)
        self.ImageName_AutoBackup = StringField(None, parent=self)
        self.ImagePath_VirtualMedia = StringField(None, parent=self)
        self.ImageType_VirtualMedia = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Image_RFS = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.InactivityTimeoutDuration_VirtualConsole = IntField(None, parent=self)
        self.InactivityTimeoutEnable_VirtualConsole = EnumTypeField(None,InactivityTimeoutEnable_VirtualConsoleTypes, parent=self)
        self.InactivityTimeout_QuickSync = IntField(None, parent=self)
        self.InactivityTimerEnable_QuickSync = EnumTypeField(None,InactivityTimerEnable_QuickSyncTypes, parent=self)
        self.IndicatorColor_ChassisHealthIndicator = EnumTypeField(None,IndicatorColor_ChassisHealthIndicatorTypes, parent=self)
        self.IndicatorColor_IdentifyButton = EnumTypeField(None,IndicatorColor_IdentifyButtonTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.IndicatorColor_PowerButton = EnumTypeField(None,IndicatorColor_PowerButtonTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IndicatorColor_PowerHealthIndicator = EnumTypeField(None,IndicatorColor_PowerHealthIndicatorTypes, parent=self)
        self.IndicatorColor_ThermalHealthIndicator = EnumTypeField(None,IndicatorColor_ThermalHealthIndicatorTypes, parent=self)
        self.IndicatorLED_Info = EnumTypeField(None,IndicatorLED_InfoTypes, parent=self)
        self.IndicatorState_ChassisHealthIndicator = EnumTypeField(None,IndicatorState_ChassisHealthIndicatorTypes, parent=self)
        self.IndicatorState_IdentifyButton = EnumTypeField(None,IndicatorState_IdentifyButtonTypes, parent=self)
        self.IndicatorState_PowerButton = EnumTypeField(None,IndicatorState_PowerButtonTypes, parent=self)
        self.IndicatorState_PowerHealthIndicator = EnumTypeField(None,IndicatorState_PowerHealthIndicatorTypes, parent=self)
        self.IndicatorState_ThermalHealthIndicator = EnumTypeField(None,IndicatorState_ThermalHealthIndicatorTypes, parent=self)
        self.Initialized_vFlashSD = EnumTypeField(None,Initialized_vFlashSDTypes, parent=self)
        self.InitiatorPersistencePolicy_IOIDOpt = EnumTypeField(None,InitiatorPersistencePolicy_IOIDOptTypes, parent=self)
        self.InputNewLineSeq_IPMISerial = EnumTypeField(None,InputNewLineSeq_IPMISerialTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.InputVoltageType_Info = EnumTypeField(None,InputVoltageType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IntervalInSeconds_PowerHistorical = IntField(None, parent=self)
        self.IntervalInSeconds_ThermalHistorical = IntField(None, parent=self)
        self.Interval_IPMISOL = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IomSecureMode_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IpmiLanPrivilege_Users = EnumTypeField(None,IpmiLanPrivilege_UsersTypes, parent=self)
        self.IpmiSerialPrivilege_Users = EnumTypeField(None,IpmiSerialPrivilege_UsersTypes, parent=self)
        self.IsEmptyEntry_GpGPUTable = EnumTypeField(None,IsEmptyEntry_GpGPUTableTypes, parent=self)
        self.IsOCPcardActive_CurrentNIC = EnumTypeField(None,IsOCPcardActive_CurrentNICTypes, parent=self)
        self.KRBKeytabFileName_ActiveDirectory = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.KRBKeytabPath_ActiveDirectory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.KeepPhyLinkUp_DCSCustom = EnumTypeField(None,KeepPhyLinkUp_DCSCustomTypes, parent=self)
        self.KeyEnable_VirtualMedia = EnumTypeField(None,KeyEnable_VirtualMediaTypes, parent=self)
        self.Key_SecuritySSL = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.LCBuild_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LCDCapable_PlatformCapability = EnumTypeField(None,LCDCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LCDFailSafeMSGLast_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg1_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg2_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg3_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg4_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg5_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg6_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg7_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg8_PrivateStore = StringField(None, parent=self)
        self.LCDFailSafeMsg_PrivateStore = StringField(None, parent=self)
        self.LCDriveEnable_LCAttributes = EnumTypeField(None,LCDriveEnable_LCAttributesTypes, parent=self)
        self.LCLReplication_ServiceModule = EnumTypeField(None,LCLReplication_ServiceModuleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LCVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LCWipe_LCAttributes = EnumTypeField(None,LCWipe_LCAttributesTypes, parent=self)
        self.LC_SensorThresholds = IntField(None, parent=self)
        self.LFMMode_PCIeSlotLFM = EnumTypeField(None,LFMMode_PCIeSlotLFMTypes, parent=self)
        self.LM_UTO_ISCOVERY_PMLicensing = EnumTypeField(None,LM_UTO_ISCOVERY_PMLicensingTypes, parent=self)
        self.LM_UTO_PDATE_PMLicensing = EnumTypeField(None,LM_UTO_PDATE_PMLicensingTypes, parent=self)
        self.LM_VOTON_CORE_PMLicensing = EnumTypeField(None,LM_VOTON_CORE_PMLicensingTypes, parent=self)
        self.LM_VOTON_CORE_PMLicensing = EnumTypeField(None,LM_VOTON_CORE_PMLicensingTypes, parent=self)
        self.LM_ACKUP_ESTORE_PMLicensing = EnumTypeField(None,LM_ACKUP_ESTORE_PMLicensingTypes, parent=self)
        self.LM_ASE_PMI_UI_PMLicensing = EnumTypeField(None,LM_ASE_PMI_UI_PMLicensingTypes, parent=self)
        self.LM_ASIC_EMOTE_NVENTORY_XPORT_PMLicensing = EnumTypeField(None,LM_ASIC_EMOTE_NVENTORY_XPORT_PMLicensingTypes, parent=self)
        self.LM_MC_LUS_PMLicensing = EnumTypeField(None,LM_MC_LUS_PMLicensingTypes, parent=self)
        self.LM_OOT_APTURE_PMLicensing = EnumTypeField(None,LM_OOT_APTURE_PMLicensingTypes, parent=self)
        self.LM_ONNECTION_IEW_PMLicensing = EnumTypeField(None,LM_ONNECTION_IEW_PMLicensingTypes, parent=self)
        self.LM_ONSOLE_OLLABORATION_PMLicensing = EnumTypeField(None,LM_ONSOLE_OLLABORATION_PMLicensingTypes, parent=self)
        self.LM_CS_UI_PMLicensing = EnumTypeField(None,LM_CS_UI_PMLicensingTypes, parent=self)
        self.LM_EDICATED_IC_PMLicensing = EnumTypeField(None,LM_EDICATED_IC_PMLicensingTypes, parent=self)
        self.LM_EVICE_ONITORING_PMLicensing = EnumTypeField(None,LM_EVICE_ONITORING_PMLicensingTypes, parent=self)
        self.LM_HCP_ONFIGURE_PMLicensing = EnumTypeField(None,LM_HCP_ONFIGURE_PMLicensingTypes, parent=self)
        self.LM_IRECTORY_ERVICES_PMLicensing = EnumTypeField(None,LM_IRECTORY_ERVICES_PMLicensingTypes, parent=self)
        self.LM_YNAMIC_NS_PMLicensing = EnumTypeField(None,LM_YNAMIC_NS_PMLicensingTypes, parent=self)
        self.LM_MAIL_LERTING_PMLicensing = EnumTypeField(None,LM_MAIL_LERTING_PMLicensingTypes, parent=self)
        self.LM_ULL_I_PMLicensing = EnumTypeField(None,LM_ULL_I_PMLicensingTypes, parent=self)
        self.LM_ROUP_ANAGER_PMLicensing = EnumTypeField(None,LM_ROUP_ANAGER_PMLicensingTypes, parent=self)
        self.LM_DRAC_NTERPRISE_PMLicensing = EnumTypeField(None,LM_DRAC_NTERPRISE_PMLicensingTypes, parent=self)
        self.LM_DRAC_XPRESS_LADES_PMLicensing = EnumTypeField(None,LM_DRAC_XPRESS_LADES_PMLicensingTypes, parent=self)
        self.LM_DRAC_XPRESS_PMLicensing = EnumTypeField(None,LM_DRAC_XPRESS_PMLicensingTypes, parent=self)
        self.LM_NBAND_IRMWARE_PDATE_PMLicensing = EnumTypeField(None,LM_NBAND_IRMWARE_PDATE_PMLicensingTypes, parent=self)
        self.LM_PV6_PMLicensing = EnumTypeField(None,LM_PV6_PMLicensingTypes, parent=self)
        self.LM_AST_RASH_CREEN_APTURE_PMLicensing = EnumTypeField(None,LM_AST_RASH_CREEN_APTURE_PMLicensingTypes, parent=self)
        self.LM_AST_RASH_IDEO_APTURE_PMLicensing = EnumTypeField(None,LM_AST_RASH_IDEO_APTURE_PMLicensingTypes, parent=self)
        self.LM_C_I_PMLicensing = EnumTypeField(None,LM_C_I_PMLicensingTypes, parent=self)
        self.LM_ICENSE_I_PMLicensing = EnumTypeField(None,LM_ICENSE_I_PMLicensingTypes, parent=self)
        self.LM_OCKDOWN_ODE_PMLicensing = EnumTypeField(None,LM_OCKDOWN_ODE_PMLicensingTypes, parent=self)
        self.LM_TP_PMLicensing = EnumTypeField(None,LM_TP_PMLicensingTypes, parent=self)
        self.LM_ME_PMLicensing = EnumTypeField(None,LM_ME_PMLicensingTypes, parent=self)
        self.LM_OB_PMLicensing = EnumTypeField(None,LM_OB_PMLicensingTypes, parent=self)
        self.LM_ART_EPLACEMENT_PMLicensing = EnumTypeField(None,LM_ART_EPLACEMENT_PMLicensingTypes, parent=self)
        self.LM_OWER_UDGETING_PMLicensing = EnumTypeField(None,LM_OWER_UDGETING_PMLicensingTypes, parent=self)
        self.LM_OWER_ONITORING_PMLicensing = EnumTypeField(None,LM_OWER_ONITORING_PMLicensingTypes, parent=self)
        self.LM_UALITY_ANDWIDTH_ONTROL_PMLicensing = EnumTypeField(None,LM_UALITY_ANDWIDTH_ONTROL_PMLicensingTypes, parent=self)
        self.LM_ACADM_LI_PMLicensing = EnumTypeField(None,LM_ACADM_LI_PMLicensingTypes, parent=self)
        self.LM_EDFISH_PMLicensing = EnumTypeField(None,LM_EDFISH_PMLicensingTypes, parent=self)
        self.LM_EMOTE_SSET_NVENTORY_PMLicensing = EnumTypeField(None,LM_EMOTE_SSET_NVENTORY_PMLicensingTypes, parent=self)
        self.LM_EMOTE_ONFIGURATION_PMLicensing = EnumTypeField(None,LM_EMOTE_ONFIGURATION_PMLicensingTypes, parent=self)
        self.LM_EMOTE_ILE_HARE_PMLicensing = EnumTypeField(None,LM_EMOTE_ILE_HARE_PMLicensingTypes, parent=self)
        self.LM_EMOTE_IRWARE_PDATE_PMLicensing = EnumTypeField(None,LM_EMOTE_IRWARE_PDATE_PMLicensingTypes, parent=self)
        self.LM_EMOTE_S_EPLOYMENT_PMLicensing = EnumTypeField(None,LM_EMOTE_S_EPLOYMENT_PMLicensingTypes, parent=self)
        self.LM_EMOTE_YSLOG_PMLicensing = EnumTypeField(None,LM_EMOTE_YSLOG_PMLicensingTypes, parent=self)
        self.LM_ESTORE_PMLicensing = EnumTypeField(None,LM_ESTORE_PMLicensingTypes, parent=self)
        self.LM_ECURITY_OCKOUT_PMLicensing = EnumTypeField(None,LM_ECURITY_OCKOUT_PMLicensingTypes, parent=self)
        self.LM_MASH_LP_PMLicensing = EnumTypeField(None,LM_MASH_LP_PMLicensingTypes, parent=self)
        self.LM_NMP_ET_PMLicensing = EnumTypeField(None,LM_NMP_ET_PMLicensingTypes, parent=self)
        self.LM_SH_K_UTHEN_PMLicensing = EnumTypeField(None,LM_SH_K_UTHEN_PMLicensingTypes, parent=self)
        self.LM_SH_PMLicensing = EnumTypeField(None,LM_SH_PMLicensingTypes, parent=self)
        self.LM_SO_PMLicensing = EnumTypeField(None,LM_SO_PMLicensingTypes, parent=self)
        self.LM_TORAGE_ONITORING_PMLicensing = EnumTypeField(None,LM_TORAGE_ONITORING_PMLicensingTypes, parent=self)
        self.LM_ELNET_PMLicensing = EnumTypeField(None,LM_ELNET_PMLicensingTypes, parent=self)
        self.LM_WO_ACTOR_UTHEN_PMLicensing = EnumTypeField(None,LM_WO_ACTOR_UTHEN_PMLicensingTypes, parent=self)
        self.LM_PDATE_ROM_EPO_PMLicensing = EnumTypeField(None,LM_PDATE_ROM_EPO_PMLicensingTypes, parent=self)
        self.LM_SC_SSISTED_S_EPLOYEMENT_PMLicensing = EnumTypeField(None,LM_SC_SSISTED_S_EPLOYEMENT_PMLicensingTypes, parent=self)
        self.LM_SC_EVICE_ONFIGURATION_PMLicensing = EnumTypeField(None,LM_SC_EVICE_ONFIGURATION_PMLicensingTypes, parent=self)
        self.LM_SC_MBEDDED_IAGNOSTICS_PMLicensing = EnumTypeField(None,LM_SC_MBEDDED_IAGNOSTICS_PMLicensingTypes, parent=self)
        self.LM_SC_IRMWARE_PDATE_PMLicensing = EnumTypeField(None,LM_SC_IRMWARE_PDATE_PMLicensingTypes, parent=self)
        self.LM_CONSOLE_HAT_PMLicensing = EnumTypeField(None,LM_CONSOLE_HAT_PMLicensingTypes, parent=self)
        self.LM_CONSOLE_TML5_CCESS_PMLicensing = EnumTypeField(None,LM_CONSOLE_TML5_CCESS_PMLicensingTypes, parent=self)
        self.LM_CONSOLE_PMLicensing = EnumTypeField(None,LM_CONSOLE_PMLicensingTypes, parent=self)
        self.LM_FOLDER_PMLicensing = EnumTypeField(None,LM_FOLDER_PMLicensingTypes, parent=self)
        self.LM_IRTUAL_LASH_ARTITIONS_PMLicensing = EnumTypeField(None,LM_IRTUAL_LASH_ARTITIONS_PMLicensingTypes, parent=self)
        self.LM_MEDIA_PMLicensing = EnumTypeField(None,LM_MEDIA_PMLicensingTypes, parent=self)
        self.LM_NC_PMLicensing = EnumTypeField(None,LM_NC_PMLicensingTypes, parent=self)
        self.LM_SMAN_PMLicensing = EnumTypeField(None,LM_SMAN_PMLicensingTypes, parent=self)
        self.LMFeatureBitsCheckSum_PMLicensing = StringField(None, parent=self)
        self.LNCThreshold_InletTemp = IntField(None, parent=self)
        self.LNC_SensorThresholds = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Label_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LastFWUpdate_Update = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LastPostCode_PrivateStore = IntField(None, parent=self)
        self.LastPwrState_PrivateStore = EnumTypeField(None,LastPwrState_PrivateStoreTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LastServiceTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LastTaskid_UpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LaunchSSM_LCAttributes = EnumTypeField(None,LaunchSSM_LCAttributesTypes, parent=self)
        self.LicenseMsgEnable_LCD = EnumTypeField(None,LicenseMsgEnable_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LicenseUpsellCapable_PlatformCapability = EnumTypeField(None,LicenseUpsellCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Licensed_LCAttributes = EnumTypeField(None,Licensed_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Licensed_vFlashSD = EnumTypeField(None,Licensed_vFlashSDTypes, parent=self)
        self.LifecycleControllerState_LCAttributes = EnumTypeField(None,LifecycleControllerState_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LifecyclecontrollerCapable_PlatformCapability = EnumTypeField(None,LifecyclecontrollerCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LineEdit_IPMISerial = EnumTypeField(None,LineEdit_IPMISerialTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LinkLocalAddress_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkLocalAddress_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkState_GBE = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkStatus_CurrentNIC = EnumTypeField(None,LinkStatus_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkStatus_MgmtNetworkInterface = EnumTypeField(None,LinkStatus_MgmtNetworkInterfaceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkStatus_NIC = EnumTypeField(None,LinkStatus_NICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LocalConfig_LocalSecurity = EnumTypeField(None,LocalConfig_LocalSecurityTypes, parent=self)
        self.LocalConsoleLockOut_SysInfo = IntField(None, parent=self)
        self.LocalDisable_VirtualConsole = EnumTypeField(None,LocalDisable_VirtualConsoleTypes, parent=self)
        self.LocalVideo_VirtualConsole = EnumTypeField(None,LocalVideo_VirtualConsoleTypes, parent=self)
        self.Locale_LCD = EnumTypeField(None,Locale_LCDTypes, parent=self)
        self.LocationMemoryInfo_DIMMInfo = StringField(None, parent=self)
        self.Location_ChassisTopology = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Location_SlotConfig = EnumTypeField(None,Location_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LowerCriticalThreshold_Sensor = IntField(None, parent=self)
        self.LowerEncryptionBitLength_VNCServer = EnumTypeField(None,LowerEncryptionBitLength_VNCServerTypes, parent=self)
        self.LowerEncryptionBitLength_WebServer = EnumTypeField(None,LowerEncryptionBitLength_WebServerTypes, parent=self)
        self.LowerWarningThreshold_Sensor = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MACAddress2_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddressCount_NIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_SECONDARYNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MBSELRestoreState_SupportAssist = EnumTypeField(None,MBSELRestoreState_SupportAssistTypes, parent=self)
        self.MD5v3Key_Users = StringField(None, parent=self)
        self.MEAutoResetDisable_PlatformCapability = EnumTypeField(None,MEAutoResetDisable_PlatformCapabilityTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MFSMaximumLimit_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MFSMinimumLimit_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MTU_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MTU_NIC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MTU_SECONDARYNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MacAddress_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MainCertPath_Security = StringField(None, parent=self)
        self.MainKeyPath_Security = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MajVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ManagedBy_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ManagementPortMode_USB = EnumTypeField(None,ManagementPortMode_USBTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Manufacturer_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxBootCaptureFileSize_VirtualConsole = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxConservationModeTimeStamp_ChassisPower = StringField(None, parent=self)
        self.MaxConservationMode_ChassisPower = EnumTypeField(None,MaxConservationMode_ChassisPowerTypes, parent=self)
        self.MaxDiscoveredServers_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxFans_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxGroupMembers_GroupManager = IntField(None, parent=self)
        self.MaxGroupTasks_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxIomFabricGroups_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxIomSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxLFM_PCIeSlotLFM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumCmc_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumSupported_Redundancy = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxNumberOfBackupArchives_AutoBackup = IntField(None, parent=self)
        self.MaxNumberOfSessions_WebServer = IntField(None, parent=self)
        self.MaxPCIeSlots_PlatformCapability = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxPowerConsumptionTimeStamp_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPowerConsumption_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPsuSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPsuSlots_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxSessions_Racadm = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_SSH = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSessions_Telnet = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxSessions_VNCServer = IntField(None, parent=self)
        self.MaxSessions_VirtualConsole = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_VirtualMedia = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSessions_WebServer = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSledSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSystemFans_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxTachs_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MediaAttachState_RFS = EnumTypeField(None,MediaAttachState_RFSTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MemberInventoryInterval_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Message1_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Message1_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1__ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageID1_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageID1_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MessagingMaxRetryCount_GroupManager = IntField(None, parent=self)
        self.MessagingRetryInterval_GroupManager = IntField(None, parent=self)
        self.MezzLOMCapable_PlatformCapability = EnumTypeField(None,MezzLOMCapable_PlatformCapabilityTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MgmtIfaceName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MgtNetworkNicConfig_ServerInfo = EnumTypeField(None,MgtNetworkNicConfig_ServerInfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MinNumNeeded_Redundancy = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinPowerConsumptionTimeStamp_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinPowerConsumption_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MinPrivilege_IPMISOL = EnumTypeField(None,MinPrivilege_IPMISOLTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MinTemperatureTimestamp_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinTemperature_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MinimumFanSpeed_ThermalSettings = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Mode_Redundancy = EnumTypeField(None,Mode_RedundancyTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Model_Info = StringField(None, parent=self)
        self.ModularLinkstatus_NIC = EnumTypeField(None,ModularLinkstatus_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ModularSharedLOMCapable_PlatformCapability = EnumTypeField(None,ModularSharedLOMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MuxSwitchControl_IPMISerial = IntField(None, parent=self)
        self.NDCMisconfig_PrivateStore = EnumTypeField(None,NDCMisconfig_PrivateStoreTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NGMPlatform_PlatformCapability = EnumTypeField(None,NGMPlatform_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NICEnable_SECONDARYNIC = EnumTypeField(None,NICEnable_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NICFailover_SECONDARYNIC = EnumTypeField(None,NICFailover_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NICInterface2NCSIPortCount_CurrentNIC = IntField(None, parent=self)
        self.NICInterface2NCSIPortStart_CurrentNIC = IntField(None, parent=self)
        self.NICInterface3NCSIPortCount_CurrentNIC = IntField(None, parent=self)
        self.NICInterface3NCSIPortStart_CurrentNIC = IntField(None, parent=self)
        self.NICPresenceMask_NIC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.NICSelection_SECONDARYNIC = EnumTypeField(None,NICSelection_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NICSpeed_SECONDARYNIC = EnumTypeField(None,NICSpeed_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NMCapable_PlatformCapability = EnumTypeField(None,NMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NMIResetOverride_LCD = EnumTypeField(None,NMIResetOverride_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NMPTASCapable_PlatformCapability = EnumTypeField(None,NMPTASCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NMSubSystemPwrMonitoringCapable_PlatformCapability = EnumTypeField(None,NMSubSystemPwrMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NOBladethrottleDuringCMCrebootCapable_PlatformCapability = EnumTypeField(None,NOBladethrottleDuringCMCrebootCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NTP1_NTPConfigGroup = StringField(None, parent=self)
        self.NTP2_NTPConfigGroup = StringField(None, parent=self)
        self.NTP3_NTPConfigGroup = StringField(None, parent=self)
        self.NTPEnable_NTPConfigGroup = EnumTypeField(None,NTPEnable_NTPConfigGroupTypes, parent=self)
        self.NTPMaxDist_NTPConfigGroup = IntField(None, parent=self)
        self.NameIVKey2_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.NameIVKey_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.Name_ADGroup = StringField(None, parent=self)
        self.Name_ChassisInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Name_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Name_UserDomain = StringField(None, parent=self)
        self.NativeOSLogsCollectionOverride_SupportAssist = EnumTypeField(None,NativeOSLogsCollectionOverride_SupportAssistTypes, parent=self)
        self.NativeOSLogsCollectionSupported_SupportAssist = EnumTypeField(None,NativeOSLogsCollectionSupported_SupportAssistTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NeighborChassisMAC_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NeighborChassisType_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NeighborMgmtIPv4_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NeighborMgmtIPv6_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NeighborPortName_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Netmask_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Netmask_IPv4 = StringField(None, parent=self)
        self.Netmask_IPv4Static = StringField(None, parent=self)
        self.Netmask_IPv6Static = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.NetworkConnection_ServiceModule = EnumTypeField(None,NetworkConnection_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NewLineSeq_IPMISerial = EnumTypeField(None,NewLineSeq_IPMISerialTypes, parent=self)
        self.NoAuth_Serial = EnumTypeField(None,NoAuth_SerialTypes, parent=self)
        self.NodeID_ServerInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.NumberErrsHidden_LCD = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NumberErrsVisible_LCD = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NumberOfLOM_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.OEMPayload_IPMIUserInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.OMSAPresence_ServiceModule = EnumTypeField(None,OMSAPresence_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.OSAppCollectionTime_Diagnostics = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.OSBMCPassthroughCapable_PlatformCapability = EnumTypeField(None,OSBMCPassthroughCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.OSIPV4_SysInfo = StringField(None, parent=self)
        self.OSIPV6_SysInfo = StringField(None, parent=self)
        self.OSInfo_ServiceModule = EnumTypeField(None,OSInfo_ServiceModuleTypes, parent=self)
        self.OSNameBinary_SysInfo = StringField(None, parent=self)
        self.OSNameVolatile_SysInfo = StringField(None, parent=self)
        self.OSName_ServerOS = StringField(None, parent=self)
        self.OSVersionBinary_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.OSVersion_ServerOS = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Occupied_CMCSlot = EnumTypeField(None,Occupied_CMCSlotTypes, parent=self)
        self.Occupied_FanSlot = EnumTypeField(None,Occupied_FanSlotTypes, parent=self)
        self.Occupied_IOMInterposer = EnumTypeField(None,Occupied_IOMInterposerTypes, parent=self)
        self.Occupied_IOMSlot = EnumTypeField(None,Occupied_IOMSlotTypes, parent=self)
        self.Occupied_PSUSlot = EnumTypeField(None,Occupied_PSUSlotTypes, parent=self)
        self.Occupied_SledInterposer = EnumTypeField(None,Occupied_SledInterposerTypes, parent=self)
        self.Occupied_SledSlot = EnumTypeField(None,Occupied_SledSlotTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.OperationMode_IntegratedDatacenter = EnumTypeField(None,OperationMode_IntegratedDatacenterTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Order_PSUSlotSeq = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Order_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Orientation_SlotConfig = EnumTypeField(None,Orientation_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.OsIpAddress_OS_MC = StringField(None, parent=self)
        self.OverTemperatureCLSTOverride_ChassisPower = EnumTypeField(None,OverTemperatureCLSTOverride_ChassisPowerTypes, parent=self)
        self.OverTemperatureCLSTOverride_ServerPwr = EnumTypeField(None,OverTemperatureCLSTOverride_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PCActiveEC_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PCIeSlotLFMSupport_ThermalSettings = EnumTypeField(None,PCIeSlotLFMSupport_ThermalSettingsTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PCStandbyEC_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PDSVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PEFFilterDefaultsSet_IPMIPefSeldom = EnumTypeField(None,PEFFilterDefaultsSet_IPMIPefSeldomTypes, parent=self)
        self.PMAllowableLicenses_PMLicensing = EnumTypeField(None,PMAllowableLicenses_PMLicensingTypes, parent=self)
        self.PMBUSCapablePSU_Info = EnumTypeField(None,PMBUSCapablePSU_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PMBUSCapablePSU_PlatformCapability = EnumTypeField(None,PMBUSCapablePSU_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PMBUSVRCapable_PlatformCapability = EnumTypeField(None,PMBUSVRCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PMDefaultLicenseFeatures_PMLicensing = EnumTypeField(None,PMDefaultLicenseFeatures_PMLicensingTypes, parent=self)
        self.PMDrivenLicensing_PMLicensing = EnumTypeField(None,PMDrivenLicensing_PMLicensingTypes, parent=self)
        self.PSPFCEnabled_ChassisPower = EnumTypeField(None,PSPFCEnabled_ChassisPowerTypes, parent=self)
        self.PSPFCEnabled_ServerPwr = EnumTypeField(None,PSPFCEnabled_ServerPwrTypes, parent=self)
        self.PSRapidOn_ChassisPower = EnumTypeField(None,PSRapidOn_ChassisPowerTypes, parent=self)
        self.PSRapidOn_ServerPwr = EnumTypeField(None,PSRapidOn_ServerPwrTypes, parent=self)
        self.PSRedPolicy_ChassisPower = EnumTypeField(None,PSRedPolicy_ChassisPowerTypes, parent=self)
        self.PSRedPolicy_ServerPwr = EnumTypeField(None,PSRedPolicy_ServerPwrTypes, parent=self)
        self.PSUHotSpareSleepthreshold_ChassisPower = IntField(None, parent=self)
        self.PSUHotSpareSleepthreshold_ServerPwr = IntField(None, parent=self)
        self.PSUHotSpareWakethreshold_ChassisPower = IntField(None, parent=self)
        self.PSUHotSpareWakethreshold_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PSUMismatchCapable_PlatformCapability = EnumTypeField(None,PSUMismatchCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PSUMismatchOverride_ChassisPower = EnumTypeField(None,PSUMismatchOverride_ChassisPowerTypes, parent=self)
        self.PSUMismatchOverride_ServerPwr = EnumTypeField(None,PSUMismatchOverride_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PSURedundancyCapable_PlatformCapability = EnumTypeField(None,PSURedundancyCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PTCapability_OS_MC = EnumTypeField(None,PTCapability_OS_MCTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PTMode_OS_MC = EnumTypeField(None,PTMode_OS_MCTypes, parent=self)
        self.PWDIVKey2_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.PWDIVKey_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.PWMdata_IPMIPowerManagement = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ParentConfig_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PartConfigurationUpdate_LCAttributes = EnumTypeField(None,PartConfigurationUpdate_LCAttributesTypes, parent=self)
        self.PartFirmwareUpdate_LCAttributes = EnumTypeField(None,PartFirmwareUpdate_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PartNumber_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PartReplacement_LCAttributes = EnumTypeField(None,PartReplacement_LCAttributesTypes, parent=self)
        self.Passphrase_AutoBackup = StringField(None, parent=self)
        self.Password_AutoBackup = StringField(None, parent=self)
        self.Password_AutoUpdate = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Password_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Password_RFS = StringField(None, parent=self)
        self.Password_SecureDefaultPassword = StringField(None, parent=self)
        self.Password_Users = StringField(None, parent=self)
        self.Password_VNCServer = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PeakCurrentAmps_ServerPwrMon = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakCurrentTime_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakPowerStartTime_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakPowerTime_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakPowerWatts_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PeakPower_GpGPUTable = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PeakTemperatureTimestamp_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakTemperature_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PenaltyTime_IPBlocking = IntField(None, parent=self)
        self.PendingActiveNIC_CurrentNIC = EnumTypeField(None,PendingActiveNIC_CurrentNICTypes, parent=self)
        self.PendingCSRKeyPath_Security = StringField(None, parent=self)
        self.PendingCSRPath_Security = StringField(None, parent=self)
        self.PendingSelection_NIC = EnumTypeField(None,PendingSelection_NICTypes, parent=self)
        self.PercGracefulShutdownWarning_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PercentComplete_FWUpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PercentComplete_ProfileTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PercentComplete_SupportAssist = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PerformFactoryIdentityCertValidation_MachineTrust = EnumTypeField(None,PerformFactoryIdentityCertValidation_MachineTrustTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PluginType_VirtualConsole = EnumTypeField(None,PluginType_VirtualConsoleTypes, parent=self)
        self.PortAssociation_IPMISerial = IntField(None, parent=self)
        self.PortStatus_USB = EnumTypeField(None,PortStatus_USBTypes, parent=self)
        self.Port_LDAP = IntField(None, parent=self)
        self.Port_SSH = IntField(None, parent=self)
        self.Port_SysLog = IntField(None, parent=self)
        self.Port_Telnet = IntField(None, parent=self)
        self.Port_VNCServer = IntField(None, parent=self)
        self.Port_VirtualConsole = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PostPoneNICSelectionCapable_PlatformCapability = EnumTypeField(None,PostPoneNICSelectionCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerAllocated_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerBudgetCapable_PlatformCapability = EnumTypeField(None,PowerBudgetCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerBudgetOverride_ServerPwr = EnumTypeField(None,PowerBudgetOverride_ServerPwrTypes, parent=self)
        self.PowerCapMaxThres_ChassisPower = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerCapMaxThres_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerCapMinThres_ChassisPower = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerCapMinThres_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerCapSetting_ChassisPower = IntField(None, parent=self)
        self.PowerCapSetting_ServerPwr = EnumTypeField(None,PowerCapSetting_ServerPwrTypes, parent=self)
        self.PowerCapState_PrivateStore = EnumTypeField(None,PowerCapState_PrivateStoreTypes, parent=self)
        self.PowerCapValue_ChassisPower = IntField(None, parent=self)
        self.PowerCapValue_ServerPwr = IntField(None, parent=self)
        self.PowerConfigReset_ServerPwrMon = EnumTypeField(None,PowerConfigReset_ServerPwrMonTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerConfigurationCapable_PlatformCapability = EnumTypeField(None,PowerConfigurationCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerConfigurationRemovalCapable_PlatformCapability = EnumTypeField(None,PowerConfigurationRemovalCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerConsumptionCollectedSince_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerInventoryCapable_PlatformCapability = EnumTypeField(None,PowerInventoryCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerLogEnable_SysLog = EnumTypeField(None,PowerLogEnable_SysLogTypes, parent=self)
        self.PowerLogInterval_SysLog = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerMonitoringCapable_PlatformCapability = EnumTypeField(None,PowerMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerOnDelaySeconds_ChassisPower = IntField(None, parent=self)
        self.PowerPolicy_SysInfo = StringField(None, parent=self)
        self.PowerRedundancy_Info = EnumTypeField(None,PowerRedundancy_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerState_Info = EnumTypeField(None,PowerState_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Power_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PrebootConfig_LocalSecurity = EnumTypeField(None,PrebootConfig_LocalSecurityTypes, parent=self)
        self.PreferredLanguage_SupportAssist = EnumTypeField(None,PreferredLanguage_SupportAssistTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PrefixLength_CurrentIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PrefixLength_IPv6 = IntField(None, parent=self)
        self.PrefixLength_IPv6Static = IntField(None, parent=self)
        self.PrefixLength_OS_MC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Presence_QuickSync = EnumTypeField(None,Presence_QuickSyncTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Presence_vFlashSD = EnumTypeField(None,Presence_vFlashSDTypes, parent=self)
        self.PrimaryContactAlternatePhoneNumber_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactEmail_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactFirstName_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactLastName_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactPhoneNumber_SupportAssist = StringField(None, parent=self)
        self.PrimaryDiscoveryWaitDuration_GroupManager = IntField(None, parent=self)
        self.PrimaryElectionDuration_GroupManager = IntField(None, parent=self)
        self.PrimarySecondarySyncInterval_GroupManager = IntField(None, parent=self)
        self.PrivLimit_IPMILan = EnumTypeField(None,PrivLimit_IPMILanTypes, parent=self)
        self.PrivLimit_IPMIUserInfo = StringField(None, parent=self)
        self.PrivacyProtocol_Users = EnumTypeField(None,PrivacyProtocol_UsersTypes, parent=self)
        self.Privilege_ADGroup = IntField(None, parent=self)
        self.Privilege_LDAPRoleGroup = IntField(None, parent=self)
        self.Privilege_Users = EnumTypeField(None,Privilege_UsersTypes, parent=self)
        self.ProSupportPlusRecommendationsReport_SupportAssist = EnumTypeField(None,ProSupportPlusRecommendationsReport_SupportAssistTypes, parent=self)
        self.ProbeLocation_BoardPowerConsumption = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ProbeLocation_InletTemp = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Product_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ProtocolEnable_Users = EnumTypeField(None,ProtocolEnable_UsersTypes, parent=self)
        self.ProvisioningServer_LCAttributes = StringField(None, parent=self)
        self.ProxyHostName_AutoUpdate = StringField(None, parent=self)
        self.ProxyPassword_AutoUpdate = StringField(None, parent=self)
        self.ProxyPort_AutoUpdate = StringField(None, parent=self)
        self.ProxyType_AutoUpdate = StringField(None, parent=self)
        self.ProxyUserName_AutoUpdate = StringField(None, parent=self)
        self.QualifierTemp_LCD = EnumTypeField(None,QualifierTemp_LCDTypes, parent=self)
        self.QualifierWatt_LCD = EnumTypeField(None,QualifierWatt_LCDTypes, parent=self)
        self.QuickSyncButtonEnable_QuickSync = EnumTypeField(None,QuickSyncButtonEnable_QuickSyncTypes, parent=self)
        self.QuitKey_SerialRedirection = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.RChassisServiceTag_ServerInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RMPath_RFS = StringField(None, parent=self)
        self.ROMBStatus_PrivateStore = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.RSMCapability_RSM = EnumTypeField(None,RSMCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RSMSetting_RSM = EnumTypeField(None,RSMSetting_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RSMSetting_RSM = EnumTypeField(None,RSMSetting_RSMTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.RSPICapable_PlatformCapability = EnumTypeField(None,RSPICapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RacDomain_ActiveDirectory = StringField(None, parent=self)
        self.RacName_ActiveDirectory = StringField(None, parent=self)
        self.RackName_ChassisTopology = StringField(None, parent=self)
        self.RackName_ServerTopology = StringField(None, parent=self)
        self.RackSlot_ChassisTopology = IntField(None, parent=self)
        self.RackSlot_ServerTopology = IntField(None, parent=self)
        self.RangeAddr_IPBlocking = StringField(None, parent=self)
        self.RangeEnable_IPBlocking = EnumTypeField(None,RangeEnable_IPBlockingTypes, parent=self)
        self.RangeMask_IPBlocking = StringField(None, parent=self)
        self.RapidOnPrimaryPSU_ChassisPower = EnumTypeField(None,RapidOnPrimaryPSU_ChassisPowerTypes, parent=self)
        self.RapidOnPrimaryPSU_ServerPwr = EnumTypeField(None,RapidOnPrimaryPSU_ServerPwrTypes, parent=self)
        self.ReadAuthentication_QuickSync = EnumTypeField(None,ReadAuthentication_QuickSyncTypes, parent=self)
        self.RebrandInfo_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.RedundancyEnabled_ThermalConfig = EnumTypeField(None,RedundancyEnabled_ThermalConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RedundancyPolicy_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Redundancy_Info = EnumTypeField(None,Redundancy_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RegisterHostDNS_SECONDARYNIC = EnumTypeField(None,RegisterHostDNS_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.RegistrationID_SupportAssist = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RemainingRatedWriteEnduranceAlertThreshold_Storage = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.RemoteEnablementCapable_PlatformCapability = EnumTypeField(None,RemoteEnablementCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Repeat_AutoBackup = StringField(None, parent=self)
        self.Repeat_AutoUpdate = IntField(None, parent=self)
        self.ResetType_SecureDefaultPassword = EnumTypeField(None,ResetType_SecureDefaultPasswordTypes, parent=self)
        self.Retries_SNMPAlert = IntField(None, parent=self)
        self.RetryCount_IPMISOL = IntField(None, parent=self)
        self.Role_GroupManager = EnumTypeField(None,Role_GroupManagerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.RollBackMinVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackBuild_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackLCBuild_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackLCVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackMajVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackPDSVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RollbackVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RoomName_ChassisTopology = StringField(None, parent=self)
        self.RoomName_ServerTopology = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Rows_SlotConfig = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SATAFQDDString_SATAInventory = StringField(None, parent=self)
        self.SCFWUpdateState_SC_MC = EnumTypeField(None,SCFWUpdateState_SC_MCTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SCPwrMonitoringCapable_PlatformCapability = EnumTypeField(None,SCPwrMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SCViewSledPwr_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SDCardCapable_PlatformCapability = EnumTypeField(None,SDCardCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SDRAddTimeStamp_IPMISDR = IntField(None, parent=self)
        self.SDRDelTimeStamp_IPMISDR = IntField(None, parent=self)
        self.SDid_GpGPUTable = IntField(None, parent=self)
        self.SELOEMEventFilterEnable_Logging = EnumTypeField(None,SELOEMEventFilterEnable_LoggingTypes, parent=self)
        self.SELdata_IPMISEL = StringField(None, parent=self)
        self.SHA1v3Key_Users = StringField(None, parent=self)
        self.SHA256PasswordSalt_Users = StringField(None, parent=self)
        self.SHA256Password_Users = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SHA256_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SHA512_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SLBAllocOverride_ServerPwr = EnumTypeField(None,SLBAllocOverride_ServerPwrTypes, parent=self)
        self.SLBBoundsCheck_ServerPwr = EnumTypeField(None,SLBBoundsCheck_ServerPwrTypes, parent=self)
        self.SLBPersistence_ServerPwr = EnumTypeField(None,SLBPersistence_ServerPwrTypes, parent=self)
        self.SLBState_ServerPwr = EnumTypeField(None,SLBState_ServerPwrTypes, parent=self)
        self.SMTPAuthentication_RemoteHosts = EnumTypeField(None,SMTPAuthentication_RemoteHostsTypes, parent=self)
        self.SMTPPassword_RemoteHosts = StringField(None, parent=self)
        self.SMTPPort_RemoteHosts = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SMTPSASL_RemoteHosts = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SMTPServerIPAddress_RemoteHosts = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SMTPStartTLS_RemoteHosts = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SMTPUserName_RemoteHosts = StringField(None, parent=self)
        self.SNMPOnHostOS_ServiceModule = EnumTypeField(None,SNMPOnHostOS_ServiceModuleTypes, parent=self)
        self.SNMPProtocol_SNMP = EnumTypeField(None,SNMPProtocol_SNMPTypes, parent=self)
        self.SNMPv3UserID_MSMSNMPAlert = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SNMPv3UserID_SNMPAlert = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SNMPv3Username_SNMPAlert = StringField(None, parent=self)
        self.SSLEncryptionBitLength_VNCServer = EnumTypeField(None,SSLEncryptionBitLength_VNCServerTypes, parent=self)
        self.SSLEncryptionBitLength_WebServer = EnumTypeField(None,SSLEncryptionBitLength_WebServerTypes, parent=self)
        self.SSMUnoptimized_LCAttributes = IntField(None, parent=self)
        self.SSOEnable_ActiveDirectory = EnumTypeField(None,SSOEnable_ActiveDirectoryTypes, parent=self)
        self.SVid_GpGPUTable = IntField(None, parent=self)
        self.SWRaidMonitoring_ServiceModule = EnumTypeField(None,SWRaidMonitoring_ServiceModuleTypes, parent=self)
        self.ScheduleBasedAutoCollection_SupportAssist = EnumTypeField(None,ScheduleBasedAutoCollection_SupportAssistTypes, parent=self)
        self.Schema_ActiveDirectory = EnumTypeField(None,Schema_ActiveDirectoryTypes, parent=self)
        self.SearchFilter_LDAP = StringField(None, parent=self)
        self.SecondaryContactAlternatePhoneNumber_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactEmail_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactFirstName_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactLastName_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactPhoneNumber_SupportAssist = StringField(None, parent=self)
        self.SecurityKeyKR_IPMILANConfig = StringField(None, parent=self)
        self.SecurityMode_LCD = EnumTypeField(None,SecurityMode_LCDTypes, parent=self)
        self.SecurityPolicyMessage_GUI = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Selection_CurrentNIC = EnumTypeField(None,Selection_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Selection_NIC = EnumTypeField(None,Selection_NICTypes, parent=self)
        self.SendThreshold_IPMISOL = IntField(None, parent=self)
        self.SensorName_Sensor = StringField(None, parent=self)
        self.SensorNumber_SensorThresholds = IntField(None, parent=self)
        self.SeqKey_NIC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SerialNumber_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Server1_SysLog = StringField(None, parent=self)
        self.Server2_SysLog = StringField(None, parent=self)
        self.Server3_SysLog = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ServerCachePath_LDAP = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServerGen_Info = EnumTypeField(None,ServerGen_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServerPoweredOnTime_ServerOS = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Server_LDAP = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ServiceEnabled_FWUpdateService = EnumTypeField(None,ServiceEnabled_FWUpdateServiceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ServiceModuleEnable_ServiceModule = EnumTypeField(None,ServiceModuleEnable_ServiceModuleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ServiceModuleState_ServiceModule = EnumTypeField(None,ServiceModuleState_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceModuleVersion_ServiceModule = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ServicePublishInterval_GroupManager = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ServiceTag_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceTag_ServerInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SessionTerminalTimeout_IPMISerial = IntField(None, parent=self)
        self.SessionTimeout_IPMISerial = IntField(None, parent=self)
        self.ShareName_AutoBackup = StringField(None, parent=self)
        self.ShareName_AutoUpdate = StringField(None, parent=self)
        self.ShareType_AutoBackup = StringField(None, parent=self)
        self.ShareType_AutoUpdate = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SharedNICScanTime_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SharedNICScanTime_NIC = IntField(None, parent=self)
        self.ShippingInfoCity_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoCompanyName_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoCountry_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoState_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoStreet1_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoStreet2_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoZip_SupportAssist = StringField(None, parent=self)
        self.Signature_vFlashSD = StringField(None, parent=self)
        self.SimComponentVal_ChassisPower = IntField(None, parent=self)
        self.SimComponentVal_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SizeOfManagedSystemInU_ServerTopology = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Size_vFlashPartition = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Size_vFlashSD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SledConfig_ServerInfo = EnumTypeField(None,SledConfig_ServerInfoTypes, parent=self)
        self.SledPowerOnInterval_ChassisInfo = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SledProfile_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotConfigs_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SlotName_CMCSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_FanSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotName_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SlotName_IOMSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SlotName_PSUSlot = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotName_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotNumber_EC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotNumber_MSM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SlotNumber_SATAInventory = StringField(None, parent=self)
        self.SlotPowerPriority_ChassisPower = EnumTypeField(None,SlotPowerPriority_ChassisPowerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotState_PCIeSlotLFM = EnumTypeField(None,SlotState_PCIeSlotLFMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Slots_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SmartCardCRLEnable_SmartCard = EnumTypeField(None,SmartCardCRLEnable_SmartCardTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SmartCardLoginCapable_PlatformCapability = EnumTypeField(None,SmartCardLoginCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SmartCardLogonEnable_SmartCard = EnumTypeField(None,SmartCardLogonEnable_SmartCardTypes, parent=self)
        self.SoftwareRecordID_IPMIPefOften = IntField(None, parent=self)
        self.SolEnable_Users = EnumTypeField(None,SolEnable_UsersTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Speed_CurrentNIC = EnumTypeField(None,Speed_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Speed_NIC = EnumTypeField(None,Speed_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.StartTime_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.StartTime_PowerHistorical = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.StartTime_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.StartTime_Sensor = StringField(None, parent=self)
        self.StartTime_ThermalHistorical = StringField(None, parent=self)
        self.StartTime_ThermalWatermarks = IntField(None, parent=self)
        self.StartupDelay_IPMIPefSeldom = StringField(None, parent=self)
        self.State_CMCSNMPTrapIPv6 = EnumTypeField(None,State_CMCSNMPTrapIPv6Types, parent=self)
        # readonly attribute populated by iDRAC
        self.State_FWUpdateService = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.State_Info = EnumTypeField(None,State_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.State_LDAPRoleGroup = EnumTypeField(None,State_LDAPRoleGroupTypes, parent=self)
        self.State_MSMSNMPAlert = EnumTypeField(None,State_MSMSNMPAlertTypes, parent=self)
        self.State_MSMSNMPTrapIPv4 = EnumTypeField(None,State_MSMSNMPTrapIPv4Types, parent=self)
        self.State_MSMSNMPTrapIPv6 = EnumTypeField(None,State_MSMSNMPTrapIPv6Types, parent=self)
        self.State_PrivateStore = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.State_Redundancy = EnumTypeField(None,State_RedundancyTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.State_SNMPAlert = EnumTypeField(None,State_SNMPAlertTypes, parent=self)
        self.State_SNMPTrapIPv4 = EnumTypeField(None,State_SNMPTrapIPv4Types, parent=self)
        self.State_SNMPTrapIPv6 = EnumTypeField(None,State_SNMPTrapIPv6Types, parent=self)
        self.StatisticsStartTime_ChassisPower = StringField(None, parent=self)
        self.StatisticsStartTime_ServerPwr = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.StatusHealth_FWUpdateService = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Status_GroupManager = EnumTypeField(None,Status_GroupManagerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Status_QuickSync = EnumTypeField(None,Status_QuickSyncTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Status_RFS = EnumTypeField(None,Status_RFSTypes, parent=self)
        self.Status_SupportAssist = StringField(None, parent=self)
        self.Status_Update = IntField(None, parent=self)
        self.StdPayload_IPMIUserInfo = StringField(None, parent=self)
        self.StorageTargetPersistencePolicy_IOIDOpt = EnumTypeField(None,StorageTargetPersistencePolicy_IOIDOptTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SubConfigOf_IOMSlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SubSystemPowerMonitoringCapable_PlatformCapability = EnumTypeField(None,SubSystemPowerMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SubnetMask_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SupportAssistEULAAcceptedAtiDRACTime_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAcceptedByiDRACUser_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAcceptedViaiDRACIntf_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAccepted_SupportAssist = EnumTypeField(None,SupportAssistEULAAccepted_SupportAssistTypes, parent=self)
        self.SupportAssistEnableState_SupportAssist = EnumTypeField(None,SupportAssistEnableState_SupportAssistTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SwitchConnection_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SwitchPortConnection_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SysAssetTag_ServerInfo = StringField(None, parent=self)
        self.SysLogEnable_SysLog = EnumTypeField(None,SysLogEnable_SysLogTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemCFMSupport_ThermalSettings = EnumTypeField(None,SystemCFMSupport_ThermalSettingsTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SystemGUID_IPMIPefSeldom = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemID_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SystemID_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SystemID_LCAttributes = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SystemId_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SystemInputMaxPowerCapacity_ChassisPower = IntField(None, parent=self)
        self.SystemLockdown_Lockdown = EnumTypeField(None,SystemLockdown_LockdownTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemModel_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SystemRev_SysInfo = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.TFTPTimeout_Update = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TLSProtocol_WebServer = EnumTypeField(None,TLSProtocol_WebServerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.TargetLFM_PCIeSlotLFM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TargetPwrAllocation_ServerPwr = IntField(None, parent=self)
        self.TaskID_SC_MC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.TaskState_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TaskState_ProfileTask = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.TaskStatus_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TaskStatus_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TaskType_FWUpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TempPowerThresholdCapable_PlatformCapability = EnumTypeField(None,TempPowerThresholdCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TemperaryKey_SecuritySSL = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ThermalManagementCapable_PlatformCapability = EnumTypeField(None,ThermalManagementCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThermalProfileValueSet_ThermalSettings = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ThermalProfile_ThermalSettings = EnumTypeField(None,ThermalProfile_ThermalSettingsTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ThermalStatus_Info = EnumTypeField(None,ThermalStatus_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ThermalTarget_GpGPUTable = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Thermal_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ThrottledPower_GpGPUTable = IntField(None, parent=self)
        self.TimeZoneAbbreviation_Time = StringField(None, parent=self)
        self.TimeZoneOffset_Time = IntField(None, parent=self)
        self.Time_AutoBackup = StringField(None, parent=self)
        self.Time_AutoUpdate = StringField(None, parent=self)
        self.Time_Time = IntField(None, parent=self)
        self.Timeout_Racadm = IntField(None, parent=self)
        self.Timeout_Racadm = IntField(None, parent=self)
        self.Timeout_SSH = IntField(None, parent=self)
        self.Timeout_Telnet = IntField(None, parent=self)
        self.Timeout_VNCServer = IntField(None, parent=self)
        self.Timeout_VirtualConsole = IntField(None, parent=self)
        self.Timeout_WebServer = IntField(None, parent=self)
        self.Timezone_Time = StringField(None, parent=self)
        self.TitleBarOptionCustom_WebServer = StringField(None, parent=self)
        self.TitleBarOption_WebServer = EnumTypeField(None,TitleBarOption_WebServerTypes, parent=self)
        self.TrapFormat_CMCSNMPAlert = StringField(None, parent=self)
        self.TrapFormat_SNMP = EnumTypeField(None,TrapFormat_SNMPTypes, parent=self)
        self.TroubleshootingMode_IntegratedDatacenter = EnumTypeField(None,TroubleshootingMode_IntegratedDatacenterTypes, parent=self)
        self.Type_Branding = EnumTypeField(None,Type_BrandingTypes, parent=self)
        self.Type_ButtonLCP = EnumTypeField(None,Type_ButtonLCPTypes, parent=self)
        self.Type_ButtonRCP = EnumTypeField(None,Type_ButtonRCPTypes, parent=self)
        self.Type_IndicatorLCP = EnumTypeField(None,Type_IndicatorLCPTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Type_Info = EnumTypeField(None,Type_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Type_SlotConfig = EnumTypeField(None,Type_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UC_SensorThresholds = IntField(None, parent=self)
        self.UEFIStateFlag_LCAttributes = IntField(None, parent=self)
        self.UNCThreshold_BoardPowerConsumption = IntField(None, parent=self)
        self.UNCThreshold_InletTemp = IntField(None, parent=self)
        self.UNC_SensorThresholds = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.URI_Branding = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.URI_MSMConfigBackup = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.URL_IPv6URL = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UnderVoltageCLSTOverride_ChassisPower = EnumTypeField(None,UnderVoltageCLSTOverride_ChassisPowerTypes, parent=self)
        self.UnderVoltageCLSTOverride_ServerPwr = EnumTypeField(None,UnderVoltageCLSTOverride_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Updateable_FPGAFWInventory = EnumTypeField(None,Updateable_FPGAFWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Updateable_FReDFWInventory = EnumTypeField(None,Updateable_FReDFWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Updateable_FWInventory = EnumTypeField(None,Updateable_FWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UpperCriticalThreshold_Sensor = IntField(None, parent=self)
        self.UpperThresholdCritical_ChassisPower = IntField(None, parent=self)
        self.UpperThresholdCritical_ServerPwr = IntField(None, parent=self)
        self.UpperWarningThreshold_Sensor = IntField(None, parent=self)
        self.UsbNicIpAddress_OS_MC = StringField(None, parent=self)
        self.UserAttribute_LDAP = StringField(None, parent=self)
        self.UserChannelAccess_IPMIUserInfo = StringField(None, parent=self)
        self.UserDefinedString_LCD = StringField(None, parent=self)
        self.UserName_AutoBackup = StringField(None, parent=self)
        self.UserName_AutoUpdate = StringField(None, parent=self)
        self.UserName_Users = StringField(None, parent=self)
        self.UserPayloadAccess_Users = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.UserPowerCapBoundCapable_PlatformCapability = EnumTypeField(None,UserPowerCapBoundCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.UserPowerCapCapable_PlatformCapability = EnumTypeField(None,UserPowerCapCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UserProxyPassword_LCAttributes = StringField(None, parent=self)
        self.UserProxyPort_LCAttributes = StringField(None, parent=self)
        self.UserProxyServer_LCAttributes = StringField(None, parent=self)
        self.UserProxyType_LCAttributes = EnumTypeField(None,UserProxyType_LCAttributesTypes, parent=self)
        self.UserProxyUserName_LCAttributes = StringField(None, parent=self)
        self.User_RFS = StringField(None, parent=self)
        self.VLANEnable_SECONDARYNIC = EnumTypeField(None,VLANEnable_SECONDARYNICTypes, parent=self)
        self.VLANID_SECONDARYNIC = IntField(None, parent=self)
        self.VLANPriority_SECONDARYNIC = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.VLanEnable_CurrentNIC = EnumTypeField(None,VLanEnable_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VLanEnable_NIC = EnumTypeField(None,VLanEnable_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.VLanID_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VLanID_NIC = IntField(None, parent=self)
        self.VLanPort_NIC = EnumTypeField(None,VLanPort_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.VLanPriority_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VLanPriority_NIC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.VLanSetting_CurrentNIC = EnumTypeField(None,VLanSetting_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VLanSetting_NIC = EnumTypeField(None,VLanSetting_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.VLan_IntegratedDatacenter = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VflashBootPartition_ServerBoot = IntField(None, parent=self)
        self.Vid_GpGPUTable = IntField(None, parent=self)
        self.VideoCaptureEnable_VirtualConsole = EnumTypeField(None,VideoCaptureEnable_VirtualConsoleTypes, parent=self)
        self.VideoCaptureFileExtension_VirtualConsole = StringField(None, parent=self)
        self.ViewAssetServiceExpressTag_LCD = EnumTypeField(None,ViewAssetServiceExpressTag_LCDTypes, parent=self)
        self.VirtualAddressManagementApplication_LCAttributes = StringField(None, parent=self)
        self.VirtualAddressManagement_LCAttributes = EnumTypeField(None,VirtualAddressManagement_LCAttributesTypes, parent=self)
        self.VirtualAddressPersistencePolicyAuxPwrd_IOIDOpt = EnumTypeField(None,VirtualAddressPersistencePolicyAuxPwrd_IOIDOptTypes, parent=self)
        self.VirtualAddressPersistencePolicyNonAuxPwrd_IOIDOpt = EnumTypeField(None,VirtualAddressPersistencePolicyNonAuxPwrd_IOIDOptTypes, parent=self)
        self.VolumeLabel_LCAttributes = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.VolumeLabel_vFlashPartition = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.WMIInfo_ServiceModule = EnumTypeField(None,WMIInfo_ServiceModuleTypes, parent=self)
        self.WatchdogRecoveryAction_ServiceModule = EnumTypeField(None,WatchdogRecoveryAction_ServiceModuleTypes, parent=self)
        self.WatchdogResetTime_ServiceModule = IntField(None, parent=self)
        self.WatchdogState_ServiceModule = EnumTypeField(None,WatchdogState_ServiceModuleTypes, parent=self)
        self.WeekofMonth_AutoBackup = StringField(None, parent=self)
        self.WeekofMonth_AutoUpdate = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.WiFiCapable_PlatformCapability = EnumTypeField(None,WiFiCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Width_GpGPUTable = IntField(None, parent=self)
        self.WifiEnable_QuickSync = EnumTypeField(None,WifiEnable_QuickSyncTypes, parent=self)
        self.WizardEnable_LCD = EnumTypeField(None,WizardEnable_LCDTypes, parent=self)
        self.WriteProtect_vFlashSD = EnumTypeField(None,WriteProtect_vFlashSDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.WriteProtected_RFS = EnumTypeField(None,WriteProtected_RFSTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ZipPassword_USB = StringField(None, parent=self)
        self.config_PSUSlot = StringField(None, parent=self)
        self.contains_PSUSlot = StringField(None, parent=self)
        self.d9netsettingstate_NIC = EnumTypeField(None,d9netsettingstate_NICTypes, parent=self)
        self.d9netusbsettingstate_NIC = EnumTypeField(None,d9netusbsettingstate_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.fwupdateflow_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.iDRACDirectUSBNICCapable_PlatformCapability = EnumTypeField(None,iDRACDirectUSBNICCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.iDRACHardReset_ServiceModule = EnumTypeField(None,iDRACHardReset_ServiceModuleTypes, parent=self)
        self.iDRACRev_SysInfo = EnumTypeField(None,iDRACRev_SysInfoTypes, parent=self)
        self.order_PSUSlotSeq = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.pciePowerAllocation_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.vConsoleIndication_LCD = EnumTypeField(None,vConsoleIndication_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.vFlashCapable_PlatformCapability = EnumTypeField(None,vFlashCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.vmediabufsize_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

