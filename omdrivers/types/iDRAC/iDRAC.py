from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import logging

logger = logging.getLogger(__name__)

class ADGroup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ADGroup", parent)
        self.Domain_ADGroup = StringField(None, parent=self)
        self.Name_ADGroup = StringField(None, parent=self)
        self.Privilege_ADGroup = IntField(None, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.Name_ADGroup

    @property
    def Index(self):
        return self.Name_ADGroup._index

class ASRConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ASRConfig", parent)
        self.Enable_ASRConfig = EnumTypeField(None,Enable_ASRConfigTypes, parent=self)
        self.commit()

class ActiveDirectory(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ActiveDirectory", parent)
        self.AuthTimeout_ActiveDirectory = IntField(None, parent=self)
        self.CertValidationEnable_ActiveDirectory = EnumTypeField(None,CertValidationEnable_ActiveDirectoryTypes, parent=self)
        self.DCLookupByUserDomain_ActiveDirectory = EnumTypeField(None,DCLookupByUserDomain_ActiveDirectoryTypes, parent=self)
        self.DCLookupDomainName_ActiveDirectory = StringField(None, parent=self)
        self.DCLookupEnable_ActiveDirectory = EnumTypeField(None,DCLookupEnable_ActiveDirectoryTypes, parent=self)
        self.DomainController1_ActiveDirectory = StringField(None, parent=self)
        self.DomainController2_ActiveDirectory = StringField(None, parent=self)
        self.DomainController3_ActiveDirectory = StringField(None, parent=self)
        self.Enable_ActiveDirectory = EnumTypeField(None,Enable_ActiveDirectoryTypes, parent=self)
        self.GCLookupEnable_ActiveDirectory = EnumTypeField(None,GCLookupEnable_ActiveDirectoryTypes, parent=self)
        self.GCRootDomain_ActiveDirectory = StringField(None, parent=self)
        self.GlobalCatalog1_ActiveDirectory = StringField(None, parent=self)
        self.GlobalCatalog2_ActiveDirectory = StringField(None, parent=self)
        self.GlobalCatalog3_ActiveDirectory = StringField(None, parent=self)
        self.KRBKeytabFileName_ActiveDirectory = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.KRBKeytabPath_ActiveDirectory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RacDomain_ActiveDirectory = StringField(None, parent=self)
        self.RacName_ActiveDirectory = StringField(None, parent=self)
        self.SSOEnable_ActiveDirectory = EnumTypeField(None,SSOEnable_ActiveDirectoryTypes, parent=self)
        self.Schema_ActiveDirectory = EnumTypeField(None,Schema_ActiveDirectoryTypes, parent=self)
        self.commit()

class AutoBackup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "AutoBackup", parent)
        self.DayofMonth_AutoBackup = StringField(None, parent=self)
        self.DayofWeek_AutoBackup = StringField(None, parent=self)
        self.Domain_AutoBackup = StringField(None, parent=self)
        self.IPAddress_AutoBackup = StringField(None, parent=self)
        self.ImageName_AutoBackup = StringField(None, parent=self)
        self.MaxNumberOfBackupArchives_AutoBackup = IntField(None, parent=self)
        self.Passphrase_AutoBackup = StringField(None, parent=self)
        self.Password_AutoBackup = StringField(None, parent=self)
        self.Repeat_AutoBackup = StringField(None, parent=self)
        self.ShareName_AutoBackup = StringField(None, parent=self)
        self.ShareType_AutoBackup = StringField(None, parent=self)
        self.Time_AutoBackup = StringField(None, parent=self)
        self.UserName_AutoBackup = StringField(None, parent=self)
        self.WeekofMonth_AutoBackup = StringField(None, parent=self)
        self.commit()

class AutoOSLockGroup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "AutoOSLockGroup", parent)
        self.AutoOSLockState_AutoOSLockGroup = EnumTypeField(None,AutoOSLockState_AutoOSLockGroupTypes, parent=self)
        self.commit()

class AutoUpdate(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "AutoUpdate", parent)
        self.ApplyReboot_AutoUpdate = IntField(None, parent=self)
        self.CatalogID_AutoUpdate = StringField(None, parent=self)
        self.CatalogName_AutoUpdate = StringField(None, parent=self)
        self.DayofMonth_AutoUpdate = StringField(None, parent=self)
        self.DayofWeek_AutoUpdate = StringField(None, parent=self)
        self.Domain_AutoUpdate = StringField(None, parent=self)
        self.IPAddress_AutoUpdate = StringField(None, parent=self)
        self.Password_AutoUpdate = StringField(None, parent=self)
        self.ProxyHostName_AutoUpdate = StringField(None, parent=self)
        self.ProxyPassword_AutoUpdate = StringField(None, parent=self)
        self.ProxyPort_AutoUpdate = StringField(None, parent=self)
        self.ProxyType_AutoUpdate = StringField(None, parent=self)
        self.ProxyUserName_AutoUpdate = StringField(None, parent=self)
        self.Repeat_AutoUpdate = IntField(None, parent=self)
        self.ShareName_AutoUpdate = StringField(None, parent=self)
        self.ShareType_AutoUpdate = StringField(None, parent=self)
        self.Time_AutoUpdate = StringField(None, parent=self)
        self.UserName_AutoUpdate = StringField(None, parent=self)
        self.WeekofMonth_AutoUpdate = StringField(None, parent=self)
        self.commit()

class Backplane(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Backplane", parent)
        # readonly attribute populated by iDRAC
        self.BackplaneBusMode_Backplane = EnumTypeField(None,BackplaneBusMode_BackplaneTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BackplaneSplitMode_Backplane = IntField(None, parent=self)
        self.commit()

class BoardPowerConsumption(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "BoardPowerConsumption", parent)
        self.ProbeLocation_BoardPowerConsumption = StringField(None, parent=self)
        self.UNCThreshold_BoardPowerConsumption = IntField(None, parent=self)
        self.commit()

class Branding(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Branding", parent)
        self.Type_Branding = EnumTypeField(None,Type_BrandingTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.URI_Branding = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ButtonLCP(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ButtonLCP", parent)
        self.Type_ButtonLCP = EnumTypeField(None,Type_ButtonLCPTypes, parent=self)
        self.commit()

class ButtonRCP(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ButtonRCP", parent)
        self.Type_ButtonRCP = EnumTypeField(None,Type_ButtonRCPTypes, parent=self)
        self.commit()

class CMC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CMC", parent)
        self.FirmwareVersion_CMC = StringField(None, parent=self)
        self.commit()

class CMCSNMPAlert(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CMCSNMPAlert", parent)
        self.AlertPort_CMCSNMPAlert = IntField(None, parent=self)
        self.CommunityName_CMCSNMPAlert = StringField(None, parent=self)
        self.TrapFormat_CMCSNMPAlert = StringField(None, parent=self)
        self.commit()

class CMCSNMPTrapIPv6(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CMCSNMPTrapIPv6", parent)
        self.DestIPv6Address_CMCSNMPTrapIPv6 = StringField(None, parent=self)
        self.State_CMCSNMPTrapIPv6 = EnumTypeField(None,State_CMCSNMPTrapIPv6Types, parent=self)
        self.commit()

class CMCSlot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CMCSlot", parent)
        self.Config_CMCSlot = StringField(None, parent=self)
        self.Contains_CMCSlot = StringField(None, parent=self)
        self.Occupied_CMCSlot = EnumTypeField(None,Occupied_CMCSlotTypes, parent=self)
        self.SlotName_CMCSlot = StringField(None, parent=self)
        self.commit()

class Certificate(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Certificate", parent)
        self.HardwareIdentityCertStatus_Certificate = EnumTypeField(None,HardwareIdentityCertStatus_CertificateTypes, parent=self)
        self.commit()

class ChassisControl(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisControl", parent)
        self.ChassisManagementMonitoring_ChassisControl = EnumTypeField(None,ChassisManagementMonitoring_ChassisControlTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisManagementatServer_ChassisControl = EnumTypeField(None,ChassisManagementatServer_ChassisControlTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ChassisHealthIndicator(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisHealthIndicator", parent)
        self.ID_ChassisHealthIndicator = StringField(None, parent=self)
        self.IndicatorColor_ChassisHealthIndicator = EnumTypeField(None,IndicatorColor_ChassisHealthIndicatorTypes, parent=self)
        self.IndicatorState_ChassisHealthIndicator = EnumTypeField(None,IndicatorState_ChassisHealthIndicatorTypes, parent=self)
        self.commit()

class ChassisInfo(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisInfo", parent)
        self.Description_ChassisInfo = StringField(None, alias="?Description_ChassisInfo", parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisHeight_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChassisModel_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChassisName_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChassisServiceTag_ChassisInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisType_ChassisInfo = EnumTypeField(None,ChassisType_ChassisInfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CompDisplayName_ChassisInfo = StringField(None, alias="CompDisplayName?_ChassisInfo", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ECComponentID_ChassisInfo = IntField(None, alias="ECComponentID?_ChassisInfo", parent=self, modifyAllowed = False, deleteAllowed = False)
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
        self.IomSecureMode_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxFans_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxIomFabricGroups_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxIomSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumCmc_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPsuSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSledSlots_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxSystemFans_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxTachs_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Name_ChassisInfo = StringField(None, parent=self)
        self.SledPowerOnInterval_ChassisInfo = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemID_ChassisInfo = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ChassisPower(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisPower", parent)
        self.ActivePowerCapVal_ChassisPower = IntField(None, parent=self)
        self.DisablePowerButton_ChassisPower = EnumTypeField(None,DisablePowerButton_ChassisPowerTypes, parent=self)
        self.ECStartTime_ChassisPower = StringField(None, parent=self)
        self.FaceplatePowerWatts_ChassisPower = IntField(None, parent=self)
        self.MaxConservationModeTimeStamp_ChassisPower = StringField(None, parent=self)
        self.MaxConservationMode_ChassisPower = EnumTypeField(None,MaxConservationMode_ChassisPowerTypes, parent=self)
        self.OverTemperatureCLSTOverride_ChassisPower = EnumTypeField(None,OverTemperatureCLSTOverride_ChassisPowerTypes, parent=self)
        self.PSPFCEnabled_ChassisPower = EnumTypeField(None,PSPFCEnabled_ChassisPowerTypes, parent=self)
        self.PSRapidOn_ChassisPower = EnumTypeField(None,PSRapidOn_ChassisPowerTypes, parent=self)
        self.PSRedPolicy_ChassisPower = EnumTypeField(None,PSRedPolicy_ChassisPowerTypes, parent=self)
        self.PSUHotSpareSleepthreshold_ChassisPower = IntField(None, parent=self)
        self.PSUHotSpareWakethreshold_ChassisPower = IntField(None, parent=self)
        self.PSUMismatchOverride_ChassisPower = EnumTypeField(None,PSUMismatchOverride_ChassisPowerTypes, parent=self)
        self.PowerCapMaxThres_ChassisPower = IntField(None, parent=self)
        self.PowerCapMinThres_ChassisPower = IntField(None, parent=self)
        self.PowerCapSetting_ChassisPower = IntField(None, parent=self)
        self.PowerCapValue_ChassisPower = IntField(None, parent=self)
        self.PowerOnDelaySeconds_ChassisPower = IntField(None, parent=self)
        self.RapidOnPrimaryPSU_ChassisPower = EnumTypeField(None,RapidOnPrimaryPSU_ChassisPowerTypes, parent=self)
        self.SimComponentVal_ChassisPower = IntField(None, parent=self)
        self.SlotPowerPriority_ChassisPower = EnumTypeField(None,SlotPowerPriority_ChassisPowerTypes, parent=self)
        self.StatisticsStartTime_ChassisPower = StringField(None, parent=self)
        self.SystemInputMaxPowerCapacity_ChassisPower = IntField(None, parent=self)
        self.UnderVoltageCLSTOverride_ChassisPower = EnumTypeField(None,UnderVoltageCLSTOverride_ChassisPowerTypes, parent=self)
        self.UpperThresholdCritical_ChassisPower = IntField(None, parent=self)
        self.commit()

class ChassisPwrState(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisPwrState", parent)
        self.ChassisLEDState_ChassisPwrState = EnumTypeField(None,ChassisLEDState_ChassisPwrStateTypes, parent=self)
        self.commit()

class ChassisTopology(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ChassisTopology", parent)
        self.AisleName_ChassisTopology = StringField(None, parent=self)
        self.DataCenterName_ChassisTopology = StringField(None, parent=self)
        self.Location_ChassisTopology = StringField(None, parent=self)
        self.RackName_ChassisTopology = StringField(None, parent=self)
        self.RackSlot_ChassisTopology = IntField(None, parent=self)
        self.RoomName_ChassisTopology = StringField(None, parent=self)
        self.commit()

class CurrentIPv4(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CurrentIPv4", parent)
        # readonly attribute populated by iDRAC
        self.Address_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DHCPEnable_CurrentIPv4 = EnumTypeField(None,DHCPEnable_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS1_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS2_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSFromDHCP_CurrentIPv4 = EnumTypeField(None,DNSFromDHCP_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentIPv4 = EnumTypeField(None,Enable_CurrentIPv4Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Gateway_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Netmask_CurrentIPv4 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class CurrentIPv6(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CurrentIPv6", parent)
        # readonly attribute populated by iDRAC
        self.Address10_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address11_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address12_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address13_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address14_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address15_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address1_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address2_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address3_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address4_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address5_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address6_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address7_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address8_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address9_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AutoConfig_CurrentIPv6 = EnumTypeField(None,AutoConfig_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS1_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNS2_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSFromDHCP6_CurrentIPv6 = EnumTypeField(None,DNSFromDHCP6_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentIPv6 = EnumTypeField(None,Enable_CurrentIPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Gateway_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IPV6NumOfExtAddress_CurrentIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkLocalAddress_CurrentIPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PrefixLength_CurrentIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class CurrentNIC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "CurrentNIC", parent)
        # readonly attribute populated by iDRAC
        self.ActiveNIC_CurrentNIC = EnumTypeField(None,ActiveNIC_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ActiveSharedLOM_CurrentNIC = EnumTypeField(None,ActiveSharedLOM_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AutoDetect_CurrentNIC = EnumTypeField(None,AutoDetect_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Autoneg_CurrentNIC = EnumTypeField(None,Autoneg_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSDomainFromDHCP_CurrentNIC = EnumTypeField(None,DNSDomainFromDHCP_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSDomainName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSRacName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DNSRegister_CurrentNIC = EnumTypeField(None,DNSRegister_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DedicatedNICScanTime_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Duplex_CurrentNIC = EnumTypeField(None,Duplex_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Enable_CurrentNIC = EnumTypeField(None,Enable_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FactoryMAC_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Failover_CurrentNIC = EnumTypeField(None,Failover_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IsOCPcardActive_CurrentNIC = EnumTypeField(None,IsOCPcardActive_CurrentNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LinkStatus_CurrentNIC = EnumTypeField(None,LinkStatus_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress2_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MTU_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MgmtIfaceName_CurrentNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NICInterface2NCSIPortCount_CurrentNIC = IntField(None, parent=self)
        self.NICInterface2NCSIPortStart_CurrentNIC = IntField(None, parent=self)
        self.NICInterface3NCSIPortCount_CurrentNIC = IntField(None, parent=self)
        self.NICInterface3NCSIPortStart_CurrentNIC = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.NumberOfLOM_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PendingActiveNIC_CurrentNIC = EnumTypeField(None,PendingActiveNIC_CurrentNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Selection_CurrentNIC = EnumTypeField(None,Selection_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SharedNICScanTime_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Speed_CurrentNIC = EnumTypeField(None,Speed_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VLanEnable_CurrentNIC = EnumTypeField(None,VLanEnable_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VLanID_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VLanPriority_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VLanSetting_CurrentNIC = EnumTypeField(None,VLanSetting_CurrentNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.vmediabufsize_CurrentNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class DCMIThermal(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DCMIThermal", parent)
        self.DCMIControl_DCMIThermal = IntField(None, parent=self)
        self.ExceptionAction_DCMIThermal = IntField(None, parent=self)
        self.ExceptionTime_DCMIThermal = IntField(None, parent=self)
        self.commit()

class DCSCustom(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DCSCustom", parent)
        self.BackplaneCable0ErrorMask_DCSCustom = IntField(None, parent=self)
        self.BackplaneCable1ErrorMask_DCSCustom = IntField(None, parent=self)
        self.BackplaneCable2ErrorMask_DCSCustom = IntField(None, parent=self)
        self.CustomUI_DCSCustom = EnumTypeField(None,CustomUI_DCSCustomTypes, parent=self)
        self.KeepPhyLinkUp_DCSCustom = EnumTypeField(None,KeepPhyLinkUp_DCSCustomTypes, parent=self)
        self.commit()

class DCSResetCtlr(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DCSResetCtlr", parent)
        self.DCSCtlr1Reset_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr1Status_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr2Reset_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlr2Status_DCSResetCtlr = StringField(None, parent=self)
        self.DCSCtlrSync_DCSResetCtlr = StringField(None, parent=self)
        self.commit()

class DIMMInfo(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DIMMInfo", parent)
        self.LocationMemoryInfo_DIMMInfo = StringField(None, parent=self)
        self.commit()

class DefaultCredentialMitigationConfigGroup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DefaultCredentialMitigationConfigGroup", parent)
        self.DefaultCredentialMitigation_DefaultCredentialMitigationConfigGroup = EnumTypeField(None,DefaultCredentialMitigation_DefaultCredentialMitigationConfigGroupTypes, parent=self)
        self.commit()

class DefaultFactoryPassword(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "DefaultFactoryPassword", parent)
        # readonly attribute populated by iDRAC
        self.Password_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SHA256_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SHA512_DefaultFactoryPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class Diagnostics(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Diagnostics", parent)
        # readonly attribute
        self.OSAppCollectionTime_Diagnostics = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class EC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "EC", parent)
        # readonly attribute populated by iDRAC
        self.ClusterState_EC = EnumTypeField(None,ClusterState_ECTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotNumber_EC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class EmailAlert(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "EmailAlert", parent)
        self.Address_EmailAlert = StringField(None, parent=self)
        self.CustomMsg_EmailAlert = StringField(None, parent=self)
        self.Enable_EmailAlert = EnumTypeField(None,Enable_EmailAlertTypes, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.Address_EmailAlert

    @property
    def Index(self):
        return self.Address_EmailAlert._index

class FPGAFWInventory(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FPGAFWInventory", parent)
        # readonly attribute populated by iDRAC
        self.Description_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FQDD_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Label_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Updateable_FPGAFWInventory = EnumTypeField(None,Updateable_FPGAFWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FPGAFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FReDFWInventory(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FReDFWInventory", parent)
        # readonly attribute populated by iDRAC
        self.Description_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FQDD_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Updateable_FReDFWInventory = EnumTypeField(None,Updateable_FReDFWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FReDFWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FWInventory(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FWInventory", parent)
        # readonly attribute populated by iDRAC
        self.Description_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceClass_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceContext_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceInstance_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FQDD_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.InstallDate_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Updateable_FWInventory = EnumTypeField(None,Updateable_FWInventoryTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VersionSequence_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_FWInventory = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FWUpdateService(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FWUpdateService", parent)
        # readonly attribute populated by iDRAC
        self.ServiceEnabled_FWUpdateService = EnumTypeField(None,ServiceEnabled_FWUpdateServiceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.State_FWUpdateService = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.StatusHealth_FWUpdateService = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FWUpdateTask(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FWUpdateTask", parent)
        # readonly attribute populated by iDRAC
        self.EndTime_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Id_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Message1_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_1_FWUpdateTask = StringField(None, alias="MessageArg1-1_FWUpdateTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_2_FWUpdateTask = StringField(None, alias="MessageArg1-2_FWUpdateTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_3_FWUpdateTask = StringField(None, alias="MessageArg1-3_FWUpdateTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageID1_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PercentComplete_FWUpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.StartTime_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TaskState_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TaskStatus_FWUpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TaskType_FWUpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FanSlot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FanSlot", parent)
        self.Config_FanSlot = StringField(None, parent=self)
        self.Contains_FanSlot = StringField(None, parent=self)
        self.Occupied_FanSlot = EnumTypeField(None,Occupied_FanSlotTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_FanSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class FrontPanel(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "FrontPanel", parent)
        self.ButtonDisable_FrontPanel = EnumTypeField(None,ButtonDisable_FrontPanelTypes, alias="ButtonDisable?_FrontPanel", parent=self)
        self.commit()

class GBE(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "GBE", parent)
        # readonly attribute populated by iDRAC
        self.ChassisModel_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisName_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkState_GBE = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
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
        self.ServiceTag_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SystemID_GBE = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class GUI(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "GUI", parent)
        self.SecurityPolicyMessage_GUI = StringField(None, parent=self)
        self.commit()

class GpGPUTable(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "GpGPUTable", parent)
        self.CardType_GpGPUTable = IntField(None, parent=self)
        self.Did_GpGPUTable = IntField(None, parent=self)
        self.Gen_GpGPUTable = IntField(None, parent=self)
        self.GpuDCT_GpGPUTable = IntField(None, parent=self)
        self.GpuHotSup_GpGPUTable = IntField(None, parent=self)
        self.IsEmptyEntry_GpGPUTable = EnumTypeField(None,IsEmptyEntry_GpGPUTableTypes, parent=self)
        self.PeakPower_GpGPUTable = IntField(None, parent=self)
        self.SDid_GpGPUTable = IntField(None, parent=self)
        self.SVid_GpGPUTable = IntField(None, parent=self)
        self.ThermalTarget_GpGPUTable = IntField(None, parent=self)
        self.ThrottledPower_GpGPUTable = IntField(None, parent=self)
        self.Vid_GpGPUTable = IntField(None, parent=self)
        self.Width_GpGPUTable = IntField(None, parent=self)
        self.commit()

class GroupManager(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "GroupManager", parent)
        self.CloneStatus_GroupManager = EnumTypeField(None,CloneStatus_GroupManagerTypes, parent=self)
        self.ConfigurationUpdateTimeStamp_GroupManager = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CreatingUser_GroupManager = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.EncryptionStatus_GroupManager = EnumTypeField(None,EncryptionStatus_GroupManagerTypes, parent=self)
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
        self.MaxDiscoveredServers_GroupManager = IntField(None, parent=self)
        self.MaxGroupMembers_GroupManager = IntField(None, parent=self)
        self.MaxGroupTasks_GroupManager = IntField(None, parent=self)
        self.MemberInventoryInterval_GroupManager = IntField(None, parent=self)
        self.MessagingMaxRetryCount_GroupManager = IntField(None, parent=self)
        self.MessagingRetryInterval_GroupManager = IntField(None, parent=self)
        self.PrimaryDiscoveryWaitDuration_GroupManager = IntField(None, parent=self)
        self.PrimaryElectionDuration_GroupManager = IntField(None, parent=self)
        self.PrimarySecondarySyncInterval_GroupManager = IntField(None, parent=self)
        self.Role_GroupManager = EnumTypeField(None,Role_GroupManagerTypes, parent=self)
        self.ServicePublishInterval_GroupManager = IntField(None, parent=self)
        self.Status_GroupManager = EnumTypeField(None,Status_GroupManagerTypes, parent=self)
        self.commit()

class IOIDOpt(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IOIDOpt", parent)
        self.IOIDOptEnable_IOIDOpt = EnumTypeField(None,IOIDOptEnable_IOIDOptTypes, parent=self)
        self.InitiatorPersistencePolicy_IOIDOpt = EnumTypeField(None,InitiatorPersistencePolicy_IOIDOptTypes, parent=self)
        self.StorageTargetPersistencePolicy_IOIDOpt = EnumTypeField(None,StorageTargetPersistencePolicy_IOIDOptTypes, parent=self)
        self.VirtualAddressPersistencePolicyAuxPwrd_IOIDOpt = EnumTypeField(None,VirtualAddressPersistencePolicyAuxPwrd_IOIDOptTypes, parent=self)
        self.VirtualAddressPersistencePolicyNonAuxPwrd_IOIDOpt = EnumTypeField(None,VirtualAddressPersistencePolicyNonAuxPwrd_IOIDOptTypes, parent=self)
        self.commit()

class IOMInterposer(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IOMInterposer", parent)
        # readonly attribute populated by iDRAC
        self.Config_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Contains_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Occupied_IOMInterposer = EnumTypeField(None,Occupied_IOMInterposerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_IOMInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class IOMSlot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IOMSlot", parent)
        self.Config_IOMSlot = StringField(None, parent=self)
        self.Contains_IOMSlot = StringField(None, parent=self)
        self.Occupied_IOMSlot = EnumTypeField(None,Occupied_IOMSlotTypes, parent=self)
        self.SlotName_IOMSlot = StringField(None, parent=self)
        self.commit()

class IOMSlotConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IOMSlotConfig", parent)
        # readonly attribute populated by iDRAC
        self.SubConfigOf_IOMSlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class IPBlocking(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPBlocking", parent)
        self.BlockEnable_IPBlocking = EnumTypeField(None,BlockEnable_IPBlockingTypes, parent=self)
        self.FailCount_IPBlocking = IntField(None, parent=self)
        self.FailWindow_IPBlocking = IntField(None, parent=self)
        self.PenaltyTime_IPBlocking = IntField(None, parent=self)
        self.RangeAddr_IPBlocking = StringField(None, parent=self)
        self.RangeEnable_IPBlocking = EnumTypeField(None,RangeEnable_IPBlockingTypes, parent=self)
        self.RangeMask_IPBlocking = StringField(None, parent=self)
        self.commit()

class IPMIChassisData(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIChassisData", parent)
        self.ChassisData_IPMIChassisData = StringField(None, parent=self)
        self.commit()

class IPMIFireWall(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIFireWall", parent)
        self.ChannelOffset_IPMIFireWall = StringField(None, parent=self)
        self.Header_IPMIFireWall = StringField(None, parent=self)
        self.commit()

class IPMIFireWallChannel(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIFireWallChannel", parent)
        self.ChannelEnableCommand_IPMIFireWallChannel = StringField(None, parent=self)
        self.ChannelHeader_IPMIFireWallChannel = StringField(None, parent=self)
        self.ChannelSubFunctionSetting_IPMIFireWallChannel = StringField(None, parent=self)
        self.commit()

class IPMIIPConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIIPConfig", parent)
        self.ArpControl_IPMIIPConfig = StringField(None, parent=self)
        self.ArpInterval_IPMIIPConfig = StringField(None, parent=self)
        self.BackupGatewayIP_IPMIIPConfig = StringField(None, parent=self)
        self.BackupGatewayMac_IPMIIPConfig = StringField(None, parent=self)
        self.DefaultGatewayMAC_IPMIIPConfig = StringField(None, parent=self)
        self.IPHeader_IPMIIPConfig = StringField(None, parent=self)
        self.commit()

class IPMILANConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMILANConfig", parent)
        self.AuthenticationEnables_IPMILANConfig = StringField(None, parent=self)
        self.ChannelAccess_IPMILANConfig = StringField(None, parent=self)
        self.CipherSuitePrivilege_IPMILANConfig = StringField(None, parent=self)
        self.SecurityKeyKR_IPMILANConfig = StringField(None, parent=self)
        self.commit()

class IPMILANPEFConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMILANPEFConfig", parent)
        self.DestinationMACAddress_IPMILANPEFConfig = StringField(None, parent=self)
        self.GatewaySelector_IPMILANPEFConfig = EnumTypeField(None,GatewaySelector_IPMILANPEFConfigTypes, parent=self)
        self.commit()

class IPMILan(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMILan", parent)
        self.AlertEnable_IPMILan = EnumTypeField(None,AlertEnable_IPMILanTypes, parent=self)
        self.CommunityName_IPMILan = StringField(None, parent=self)
        self.Enable_IPMILan = EnumTypeField(None,Enable_IPMILanTypes, parent=self)
        self.EncryptionKey_IPMILan = StringField(None, parent=self)
        self.PrivLimit_IPMILan = EnumTypeField(None,PrivLimit_IPMILanTypes, parent=self)
        self.commit()

class IPMIPEFSeldomFilter(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIPEFSeldomFilter", parent)
        self.FilterEntry_IPMIPEFSeldomFilter = StringField(None, parent=self)
        self.commit()

class IPMIPefOften(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIPefOften", parent)
        self.BMCRecordID_IPMIPefOften = IntField(None, parent=self)
        self.SoftwareRecordID_IPMIPefOften = IntField(None, parent=self)
        self.commit()

class IPMIPefSeldom(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIPefSeldom", parent)
        self.AlertStartupDelay_IPMIPefSeldom = StringField(None, parent=self)
        self.Control_IPMIPefSeldom = StringField(None, parent=self)
        self.GlobalControl_IPMIPefSeldom = StringField(None, parent=self)
        self.PEFFilterDefaultsSet_IPMIPefSeldom = EnumTypeField(None,PEFFilterDefaultsSet_IPMIPefSeldomTypes, parent=self)
        self.StartupDelay_IPMIPefSeldom = StringField(None, parent=self)
        self.SystemGUID_IPMIPefSeldom = StringField(None, parent=self)
        self.commit()

class IPMIPefSeldomAlerts(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIPefSeldomAlerts", parent)
        self.AlertEntry_IPMIPefSeldomAlerts = StringField(None, parent=self)
        self.AlertStringEntry_IPMIPefSeldomAlerts = StringField(None, parent=self)
        self.commit()

class IPMIPowerManagement(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIPowerManagement", parent)
        self.PWMdata_IPMIPowerManagement = StringField(None, parent=self)
        self.commit()

class IPMISDR(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMISDR", parent)
        self.SDRAddTimeStamp_IPMISDR = IntField(None, parent=self)
        self.SDRDelTimeStamp_IPMISDR = IntField(None, parent=self)
        self.commit()

class IPMISEL(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMISEL", parent)
        self.SELdata_IPMISEL = StringField(None, parent=self)
        self.commit()

class IPMISOL(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMISOL", parent)
        self.AccumulateInterval_IPMISOL = IntField(None, parent=self)
        self.Authentication_IPMISOL = EnumTypeField(None,Authentication_IPMISOLTypes, parent=self)
        self.BaudRate_IPMISOL = EnumTypeField(None,BaudRate_IPMISOLTypes, parent=self)
        self.Enable_IPMISOL = EnumTypeField(None,Enable_IPMISOLTypes, parent=self)
        self.Interval_IPMISOL = IntField(None, parent=self)
        self.MinPrivilege_IPMISOL = EnumTypeField(None,MinPrivilege_IPMISOLTypes, parent=self)
        self.RetryCount_IPMISOL = IntField(None, parent=self)
        self.SendThreshold_IPMISOL = IntField(None, parent=self)
        self.commit()

class IPMISerial(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMISerial", parent)
        self.AuthenticationTypeEnables_IPMISerial = StringField(None, parent=self)
        self.BaudRate_IPMISerial = EnumTypeField(None,BaudRate_IPMISerialTypes, parent=self)
        self.ChanPrivLimit_IPMISerial = EnumTypeField(None,ChanPrivLimit_IPMISerialTypes, parent=self)
        self.ChannelAccess_IPMISerial = IntField(None, parent=self)
        self.ConnectionMode_IPMISerial = EnumTypeField(None,ConnectionMode_IPMISerialTypes, parent=self)
        self.DeleteControl_IPMISerial = EnumTypeField(None,DeleteControl_IPMISerialTypes, parent=self)
        self.EchoControl_IPMISerial = EnumTypeField(None,EchoControl_IPMISerialTypes, parent=self)
        self.FlowControl_IPMISerial = EnumTypeField(None,FlowControl_IPMISerialTypes, parent=self)
        self.HandshakeControl_IPMISerial = EnumTypeField(None,HandshakeControl_IPMISerialTypes, parent=self)
        self.InputNewLineSeq_IPMISerial = EnumTypeField(None,InputNewLineSeq_IPMISerialTypes, parent=self)
        self.LineEdit_IPMISerial = EnumTypeField(None,LineEdit_IPMISerialTypes, parent=self)
        self.MuxSwitchControl_IPMISerial = IntField(None, parent=self)
        self.NewLineSeq_IPMISerial = EnumTypeField(None,NewLineSeq_IPMISerialTypes, parent=self)
        self.PortAssociation_IPMISerial = IntField(None, parent=self)
        self.SessionTerminalTimeout_IPMISerial = IntField(None, parent=self)
        self.SessionTimeout_IPMISerial = IntField(None, parent=self)
        self.commit()

class IPMISystemParameter(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMISystemParameter", parent)
        self.ControllerIPMBAddress_IPMISystemParameter = StringField(None, parent=self)
        self.DeviceGUID_IPMISystemParameter = StringField(None, parent=self)
        self.commit()

class IPMIUserEncryptIVKey(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIUserEncryptIVKey", parent)
        self.NameIVKey2_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.NameIVKey_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.PWDIVKey2_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.PWDIVKey_IPMIUserEncryptIVKey = StringField(None, parent=self)
        self.commit()

class IPMIUserInfo(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPMIUserInfo", parent)
        self.OEMPayload_IPMIUserInfo = StringField(None, parent=self)
        self.PrivLimit_IPMIUserInfo = StringField(None, parent=self)
        self.StdPayload_IPMIUserInfo = StringField(None, parent=self)
        self.UserChannelAccess_IPMIUserInfo = StringField(None, parent=self)
        self.commit()

class IPv4(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPv4", parent)
        self.Address_IPv4 = StringField(None, parent=self)
        self.DHCPEnable_IPv4 = EnumTypeField(None,DHCPEnable_IPv4Types, parent=self)
        self.DNS1_IPv4 = StringField(None, parent=self)
        self.DNS2_IPv4 = StringField(None, parent=self)
        self.DNSFromDHCP_IPv4 = EnumTypeField(None,DNSFromDHCP_IPv4Types, parent=self)
        self.Enable_IPv4 = EnumTypeField(None,Enable_IPv4Types, parent=self)
        self.Gateway_IPv4 = StringField(None, parent=self)
        self.Netmask_IPv4 = StringField(None, parent=self)
        self.commit()

class IPv4Static(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPv4Static", parent)
        self.Address_IPv4Static = StringField(None, parent=self)
        self.DNS1_IPv4Static = StringField(None, parent=self)
        self.DNS2_IPv4Static = StringField(None, parent=self)
        self.DNSFromDHCP_IPv4Static = EnumTypeField(None,DNSFromDHCP_IPv4StaticTypes, parent=self)
        self.Gateway_IPv4Static = StringField(None, parent=self)
        self.Netmask_IPv4Static = StringField(None, parent=self)
        self.DNSServers = CompositeFieldType(self.DNS1_IPv4Static, self.DNS2_IPv4Static)
        self.commit()

class IPv6(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPv6", parent)
        # readonly attribute populated by iDRAC
        self.Address10_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address11_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address12_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address13_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address14_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address15_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Address1_IPv6 = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Address2_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address3_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address4_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address5_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address6_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address7_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address8_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Address9_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AddressState_IPv6 = EnumTypeField(None,AddressState_IPv6Types, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Address_IPv6 = StringField(None, parent=self)
        self.AutoConfig_IPv6 = EnumTypeField(None,AutoConfig_IPv6Types, parent=self)
        self.DNS1_IPv6 = StringField(None, parent=self)
        self.DNS2_IPv6 = StringField(None, parent=self)
        self.DNSFromDHCP6_IPv6 = EnumTypeField(None,DNSFromDHCP6_IPv6Types, parent=self)
        self.Enable_IPv6 = EnumTypeField(None,Enable_IPv6Types, parent=self)
        self.Gateway_IPv6 = StringField(None, parent=self)
        self.IPV6NumOfExtAddress_IPv6 = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.LinkLocalAddress_IPv6 = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PrefixLength_IPv6 = IntField(None, parent=self)
        self.commit()

class IPv6Static(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPv6Static", parent)
        self.Address1_IPv6Static = StringField(None, parent=self)
        self.Address_IPv6Static = StringField(None, parent=self)
        self.DNS1_IPv6Static = StringField(None, parent=self)
        self.DNS2_IPv6Static = StringField(None, parent=self)
        self.DNSFromDHCP6_IPv6Static = EnumTypeField(None,DNSFromDHCP6_IPv6StaticTypes, parent=self)
        self.Gateway_IPv6Static = StringField(None, parent=self)
        self.Netmask_IPv6Static = StringField(None, parent=self)
        self.PrefixLength_IPv6Static = IntField(None, parent=self)
        self.DNSServers = CompositeFieldType(self.DNS1_IPv6Static, self.DNS2_IPv6Static)
        self.commit()

class IPv6URL(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IPv6URL", parent)
        # readonly attribute populated by iDRAC
        self.URL_IPv6URL = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class IdentifyButton(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IdentifyButton", parent)
        self.ID_IdentifyButton = StringField(None, parent=self)
        self.IndicatorColor_IdentifyButton = EnumTypeField(None,IndicatorColor_IdentifyButtonTypes, parent=self)
        self.IndicatorState_IdentifyButton = EnumTypeField(None,IndicatorState_IdentifyButtonTypes, parent=self)
        self.commit()

class IndicatorLCP(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IndicatorLCP", parent)
        self.BlinkPattern_IndicatorLCP = EnumTypeField(None,BlinkPattern_IndicatorLCPTypes, parent=self)
        self.Type_IndicatorLCP = EnumTypeField(None,Type_IndicatorLCPTypes, parent=self)
        self.commit()

class Info(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Info", parent)
        # readonly attribute populated by iDRAC
        self.AssetTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Build_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CPLDVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Capacity_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChassisName_Info = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ChassisPowerPolicy_Info = EnumTypeField(None,ChassisPowerPolicy_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisPowerStatus_Info = EnumTypeField(None,ChassisPowerStatus_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisResetOperation_Info = EnumTypeField(None,ChassisResetOperation_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisSubType_Info = EnumTypeField(None,ChassisSubType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisType_Info = EnumTypeField(None,ChassisType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ContainedIn_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Description_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ExpressServiceCode_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FReDFWVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanHealth_Info = EnumTypeField(None,FanHealth_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FanName_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FanRedundancy_Info = EnumTypeField(None,FanRedundancy_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FirmwareVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.GraphicsURI_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.HWRev_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HardwareVersion_Info = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.HelpURL_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ID_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOMFWVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IOMType_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IPMIVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IndicatorLED_Info = EnumTypeField(None,IndicatorLED_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.InputVoltageType_Info = EnumTypeField(None,InputVoltageType_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LCBuild_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LCVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LastServiceTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MajVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ManagedBy_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Manufacturer_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPowerConsumptionTimeStamp_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxPowerConsumption_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinPowerConsumptionTimeStamp_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinPowerConsumption_Info = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Model_Info = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Name_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PDSVersion_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PMBUSCapablePSU_Info = EnumTypeField(None,PMBUSCapablePSU_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PartNumber_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerConsumptionCollectedSince_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerRedundancy_Info = EnumTypeField(None,PowerRedundancy_InfoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerState_Info = EnumTypeField(None,PowerState_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Power_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Product_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Redundancy_Info = EnumTypeField(None,Redundancy_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
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
        # readonly attribute populated by iDRAC
        self.SerialNumber_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServerGen_Info = EnumTypeField(None,ServerGen_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceTag_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SledProfile_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotConfigs_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotName_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Slots_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.State_Info = EnumTypeField(None,State_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThermalStatus_Info = EnumTypeField(None,ThermalStatus_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Thermal_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Type_Info = EnumTypeField(None,Type_InfoTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Version_Info = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class InletTemp(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "InletTemp", parent)
        self.LNCThreshold_InletTemp = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ProbeLocation_InletTemp = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UNCThreshold_InletTemp = IntField(None, parent=self)
        self.commit()

class IntegratedDatacenter(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "IntegratedDatacenter", parent)
        self.DiscoveryEnable_IntegratedDatacenter = EnumTypeField(None,DiscoveryEnable_IntegratedDatacenterTypes, parent=self)
        self.Eject_IntegratedDatacenter = EnumTypeField(None,Eject_IntegratedDatacenterTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.OperationMode_IntegratedDatacenter = EnumTypeField(None,OperationMode_IntegratedDatacenterTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TroubleshootingMode_IntegratedDatacenter = EnumTypeField(None,TroubleshootingMode_IntegratedDatacenterTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.VLan_IntegratedDatacenter = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class LCAttributes(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "LCAttributes", parent)
        self.AutoBackup_LCAttributes = EnumTypeField(None,AutoBackup_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.AutoDiscovery_LCAttributes = EnumTypeField(None,AutoDiscovery_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AutoRestore_LCAttributes = EnumTypeField(None,AutoRestore_LCAttributesTypes, parent=self)
        self.AutoUpdate_LCAttributes = EnumTypeField(None,AutoUpdate_LCAttributesTypes, parent=self)
        self.BIOSRTDRequested_LCAttributes = EnumTypeField(None,BIOSRTDRequested_LCAttributesTypes, parent=self)
        self.BootToMaser_LCAttributes = EnumTypeField(None,BootToMaser_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CMCIP_LCAttributes = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CSIORLaunched_LCAttributes = EnumTypeField(None,CSIORLaunched_LCAttributesTypes, parent=self)
        self.CollectSystemInventoryOnRestart_LCAttributes = EnumTypeField(None,CollectSystemInventoryOnRestart_LCAttributesTypes, parent=self)
        self.DiagsJobScheduled_LCAttributes = EnumTypeField(None,DiagsJobScheduled_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DiscoveryFactoryDefaults_LCAttributes = EnumTypeField(None,DiscoveryFactoryDefaults_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IPAddress_LCAttributes = StringField(None, parent=self)
        self.IPChangeNotifyPS_LCAttributes = EnumTypeField(None,IPChangeNotifyPS_LCAttributesTypes, parent=self)
        self.IgnoreCertWarning_LCAttributes = EnumTypeField(None,IgnoreCertWarning_LCAttributesTypes, parent=self)
        self.LCDriveEnable_LCAttributes = EnumTypeField(None,LCDriveEnable_LCAttributesTypes, parent=self)
        self.LCWipe_LCAttributes = EnumTypeField(None,LCWipe_LCAttributesTypes, parent=self)
        self.LaunchSSM_LCAttributes = EnumTypeField(None,LaunchSSM_LCAttributesTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Licensed_LCAttributes = EnumTypeField(None,Licensed_LCAttributesTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LifecycleControllerState_LCAttributes = EnumTypeField(None,LifecycleControllerState_LCAttributesTypes, parent=self)
        self.PartConfigurationUpdate_LCAttributes = EnumTypeField(None,PartConfigurationUpdate_LCAttributesTypes, parent=self)
        self.PartFirmwareUpdate_LCAttributes = EnumTypeField(None,PartFirmwareUpdate_LCAttributesTypes, parent=self)
        self.PartReplacement_LCAttributes = EnumTypeField(None,PartReplacement_LCAttributesTypes, parent=self)
        self.ProvisioningServer_LCAttributes = StringField(None, parent=self)
        self.SSMUnoptimized_LCAttributes = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemID_LCAttributes = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UEFIStateFlag_LCAttributes = IntField(None, parent=self)
        self.UserProxyPassword_LCAttributes = StringField(None, parent=self)
        self.UserProxyPort_LCAttributes = StringField(None, parent=self)
        self.UserProxyServer_LCAttributes = StringField(None, parent=self)
        self.UserProxyType_LCAttributes = EnumTypeField(None,UserProxyType_LCAttributesTypes, parent=self)
        self.UserProxyUserName_LCAttributes = StringField(None, parent=self)
        self.VirtualAddressManagementApplication_LCAttributes = StringField(None, parent=self)
        self.VirtualAddressManagement_LCAttributes = EnumTypeField(None,VirtualAddressManagement_LCAttributesTypes, parent=self)
        self.VolumeLabel_LCAttributes = StringField(None, parent=self)
        self.commit()

class LCD(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "LCD", parent)
        self.BladeInsertionPrompt_LCD = EnumTypeField(None,BladeInsertionPrompt_LCDTypes, parent=self)
        self.ChassisIdentifyDuration_LCD = IntField(None, parent=self)
        self.ChassisIdentifyEnable_LCD = EnumTypeField(None,ChassisIdentifyEnable_LCDTypes, parent=self)
        self.Configuration_LCD = EnumTypeField(None,Configuration_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.CurrentDisplay_LCD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CurrentFPStates_LCD = IntField(None, parent=self)
        self.DefaultScreen_LCD = EnumTypeField(None,DefaultScreen_LCDTypes, parent=self)
        self.ErrorDisplayMode_LCD = EnumTypeField(None,ErrorDisplayMode_LCDTypes, parent=self)
        self.FrontPanelLocking_LCD = EnumTypeField(None,FrontPanelLocking_LCDTypes, parent=self)
        self.HideErrs_LCD = EnumTypeField(None,HideErrs_LCDTypes, parent=self)
        self.LicenseMsgEnable_LCD = EnumTypeField(None,LicenseMsgEnable_LCDTypes, parent=self)
        self.Locale_LCD = EnumTypeField(None,Locale_LCDTypes, parent=self)
        self.NMIResetOverride_LCD = EnumTypeField(None,NMIResetOverride_LCDTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NumberErrsHidden_LCD = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NumberErrsVisible_LCD = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.QualifierTemp_LCD = EnumTypeField(None,QualifierTemp_LCDTypes, parent=self)
        self.QualifierWatt_LCD = EnumTypeField(None,QualifierWatt_LCDTypes, parent=self)
        self.SecurityMode_LCD = EnumTypeField(None,SecurityMode_LCDTypes, parent=self)
        self.UserDefinedString_LCD = StringField(None, parent=self)
        self.ViewAssetServiceExpressTag_LCD = EnumTypeField(None,ViewAssetServiceExpressTag_LCDTypes, parent=self)
        self.WizardEnable_LCD = EnumTypeField(None,WizardEnable_LCDTypes, parent=self)
        self.vConsoleIndication_LCD = EnumTypeField(None,vConsoleIndication_LCDTypes, parent=self)
        self.commit()

class LDAP(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "LDAP", parent)
        self.BaseDN_LDAP = StringField(None, parent=self)
        self.BindDN_LDAP = StringField(None, parent=self)
        self.BindPassword_LDAP = StringField(None, parent=self)
        self.CertValidationEnable_LDAP = EnumTypeField(None,CertValidationEnable_LDAPTypes, parent=self)
        self.Enable_LDAP = EnumTypeField(None,Enable_LDAPTypes, parent=self)
        self.GroupAttributeIsDN_LDAP = EnumTypeField(None,GroupAttributeIsDN_LDAPTypes, parent=self)
        self.GroupAttribute_LDAP = StringField(None, parent=self)
        self.Port_LDAP = IntField(None, parent=self)
        self.SearchFilter_LDAP = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.ServerCachePath_LDAP = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Server_LDAP = StringField(None, parent=self)
        self.UserAttribute_LDAP = StringField(None, parent=self)
        self.commit()

class LDAPRoleGroup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "LDAPRoleGroup", parent)
        self.DN_1_LDAPRoleGroup = StringField(None, alias="DN.1_LDAPRoleGroup", parent=self)
        self.DN_2_LDAPRoleGroup = StringField(None, alias="DN.2_LDAPRoleGroup", parent=self)
        self.DN_3_LDAPRoleGroup = StringField(None, alias="DN.3_LDAPRoleGroup", parent=self)
        self.DN_4_LDAPRoleGroup = StringField(None, alias="DN.4_LDAPRoleGroup", parent=self)
        self.DN_5_LDAPRoleGroup = StringField(None, alias="DN.5_LDAPRoleGroup", parent=self)
        self.DN_LDAPRoleGroup = StringField(None, parent=self)
        self.DestIPv6Addr_LDAPRoleGroup = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.DestinationNum_LDAPRoleGroup = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Privilege_LDAPRoleGroup = IntField(None, parent=self)
        self.State_LDAPRoleGroup = EnumTypeField(None,State_LDAPRoleGroupTypes, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.DN_LDAPRoleGroup

    @property
    def Index(self):
        return self.DN_LDAPRoleGroup._index

class LocalSecurity(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "LocalSecurity", parent)
        self.LocalConfig_LocalSecurity = EnumTypeField(None,LocalConfig_LocalSecurityTypes, parent=self)
        self.PrebootConfig_LocalSecurity = EnumTypeField(None,PrebootConfig_LocalSecurityTypes, parent=self)
        self.commit()

class Lockdown(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Lockdown", parent)
        self.SystemLockdown_Lockdown = EnumTypeField(None,SystemLockdown_LockdownTypes, parent=self)
        self.commit()

class Logging(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Logging", parent)
        self.SELOEMEventFilterEnable_Logging = EnumTypeField(None,SELOEMEventFilterEnable_LoggingTypes, parent=self)
        self.commit()

class MSM(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MSM", parent)
        # readonly attribute populated by iDRAC
        self.ClusterState_MSM = EnumTypeField(None,ClusterState_MSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HealthStatus_MSM = EnumTypeField(None,HealthStatus_MSMTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotNumber_MSM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class MSMConfigBackup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MSMConfigBackup", parent)
        # readonly attribute populated by iDRAC
        self.URI_MSMConfigBackup = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class MSMSNMPAlert(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MSMSNMPAlert", parent)
        self.SNMPv3UserID_MSMSNMPAlert = IntField(None, parent=self)
        self.State_MSMSNMPAlert = EnumTypeField(None,State_MSMSNMPAlertTypes, parent=self)
        self.commit()

class MSMSNMPTrapIPv4(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MSMSNMPTrapIPv4", parent)
        self.DestIPv4Address_MSMSNMPTrapIPv4 = StringField(None, parent=self)
        self.State_MSMSNMPTrapIPv4 = EnumTypeField(None,State_MSMSNMPTrapIPv4Types, parent=self)
        self.commit()

class MSMSNMPTrapIPv6(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MSMSNMPTrapIPv6", parent)
        self.DestIPv6Address_MSMSNMPTrapIPv6 = StringField(None, parent=self)
        self.State_MSMSNMPTrapIPv6 = EnumTypeField(None,State_MSMSNMPTrapIPv6Types, parent=self)
        self.commit()

class MachineTrust(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MachineTrust", parent)
        # readonly attribute populated by iDRAC
        self.PerformFactoryIdentityCertValidation_MachineTrust = EnumTypeField(None,PerformFactoryIdentityCertValidation_MachineTrustTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class MgmtNetworkInterface(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "MgmtNetworkInterface", parent)
        # readonly attribute populated by iDRAC
        self.EnableStatus_MgmtNetworkInterface = EnumTypeField(None,EnableStatus_MgmtNetworkInterfaceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IPv4_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LinkStatus_MgmtNetworkInterface = EnumTypeField(None,LinkStatus_MgmtNetworkInterfaceTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MacAddress_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SubnetMask_MgmtNetworkInterface = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class NIC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "NIC", parent)
        self.ApplyNICSelection_NIC = EnumTypeField(None,ApplyNICSelection_NICTypes, parent=self)
        self.AutoConfigIPV6_NIC = EnumTypeField(None,AutoConfigIPV6_NICTypes, parent=self)
        self.AutoConfig_NIC = EnumTypeField(None,AutoConfig_NICTypes, parent=self)
        self.AutoDetect_NIC = EnumTypeField(None,AutoDetect_NICTypes, parent=self)
        self.Autoduplex_NIC = EnumTypeField(None,Autoduplex_NICTypes, parent=self)
        self.Autoneg_NIC = EnumTypeField(None,Autoneg_NICTypes, parent=self)
        self.CMCResetState_NIC = EnumTypeField(None,CMCResetState_NICTypes, parent=self)
        self.ConfigChangedByUser_NIC = EnumTypeField(None,ConfigChangedByUser_NICTypes, parent=self)
        self.ConfigMaxDelay_NIC = IntField(None, parent=self)
        self.DCMIDHCPmgmtstring_NIC = StringField(None, parent=self)
        self.DCMIDHCPopt12_NIC = EnumTypeField(None,DCMIDHCPopt12_NICTypes, parent=self)
        self.DCMIDHCPopt60opt43_NIC = EnumTypeField(None,DCMIDHCPopt60opt43_NICTypes, parent=self)
        self.DCMIDHCPpkttimeout_NIC = IntField(None, parent=self)
        self.DCMIDHCPrandombackoff_NIC = EnumTypeField(None,DCMIDHCPrandombackoff_NICTypes, parent=self)
        self.DCMIDHCPretrytimeout_NIC = IntField(None, parent=self)
        self.DCMIDHCPwaitinterval_NIC = IntField(None, parent=self)
        self.DNSDomainFromDHCP_NIC = EnumTypeField(None,DNSDomainFromDHCP_NICTypes, parent=self)
        self.DNSDomainNameFromDHCP_NIC = EnumTypeField(None,DNSDomainNameFromDHCP_NICTypes, parent=self)
        self.DNSDomainName_NIC = StringField(None, parent=self)
        self.DNSRacName_NIC = StringField(None, parent=self)
        self.DNSRegister_NIC = EnumTypeField(None,DNSRegister_NICTypes, parent=self)
        self.DedicatedNICScanTime_NIC = IntField(None, parent=self)
        self.DummySwitchConnection_NIC = StringField(None, parent=self)
        self.DummySwitchPortConnection_NIC = StringField(None, parent=self)
        self.Duplex_NIC = EnumTypeField(None,Duplex_NICTypes, parent=self)
        self.EmbeddedNICBIBInfo_NIC = StringField(None, parent=self)
        self.Enable_NIC = EnumTypeField(None,Enable_NICTypes, parent=self)
        self.Failover_NIC = EnumTypeField(None,Failover_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FlexMacCompleted_NIC = EnumTypeField(None,FlexMacCompleted_NICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Flexmacaddress_NIC = StringField(None, parent=self)
        self.G5KxcablePresence_NIC = EnumTypeField(None,G5KxcablePresence_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LinkStatus_NIC = EnumTypeField(None,LinkStatus_NICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddressCount_NIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MACAddress_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MTU_NIC = IntField(None, parent=self)
        self.ModularLinkstatus_NIC = EnumTypeField(None,ModularLinkstatus_NICTypes, parent=self)
        self.NICPresenceMask_NIC = IntField(None, parent=self)
        self.PendingSelection_NIC = EnumTypeField(None,PendingSelection_NICTypes, parent=self)
        self.Selection_NIC = EnumTypeField(None,Selection_NICTypes, parent=self)
        self.SeqKey_NIC = IntField(None, parent=self)
        self.SharedNICScanTime_NIC = IntField(None, parent=self)
        self.Speed_NIC = EnumTypeField(None,Speed_NICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SwitchConnection_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SwitchPortConnection_NIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VLanEnable_NIC = EnumTypeField(None,VLanEnable_NICTypes, parent=self)
        self.VLanID_NIC = IntField(None, parent=self)
        self.VLanPort_NIC = EnumTypeField(None,VLanPort_NICTypes, parent=self)
        self.VLanPriority_NIC = IntField(None, parent=self)
        self.VLanSetting_NIC = EnumTypeField(None,VLanSetting_NICTypes, parent=self)
        self.d9netsettingstate_NIC = EnumTypeField(None,d9netsettingstate_NICTypes, parent=self)
        self.d9netusbsettingstate_NIC = EnumTypeField(None,d9netusbsettingstate_NICTypes, parent=self)
        self.commit()

class NICStatic(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "NICStatic", parent)
        self.DNSDomainFromDHCP_NICStatic = EnumTypeField(None,DNSDomainFromDHCP_NICStaticTypes, parent=self)
        self.DNSDomainName_NICStatic = StringField(None, parent=self)
        self.commit()

class NTPConfigGroup(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "NTPConfigGroup", parent)
        self.NTP1_NTPConfigGroup = StringField(None, parent=self)
        self.NTP2_NTPConfigGroup = StringField(None, parent=self)
        self.NTP3_NTPConfigGroup = StringField(None, parent=self)
        self.NTPEnable_NTPConfigGroup = EnumTypeField(None,NTPEnable_NTPConfigGroupTypes, parent=self)
        self.NTPMaxDist_NTPConfigGroup = IntField(None, parent=self)
        self.NTPServers = CompositeFieldType(self.NTP1_NTPConfigGroup, self.NTP2_NTPConfigGroup, self.NTP3_NTPConfigGroup)
        self.commit()

class OS_BMC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "OS-BMC", parent)
        self.AdminState_OS_BMC = EnumTypeField(None,AdminState_OS_BMCTypes, alias="AdminState_OS-BMC", parent=self)
        self.IdracPTEpIpAddr_OS_BMC = StringField(None, alias="IdracPTEpIpAddr_OS-BMC", parent=self)
        self.OsIpAddress_OS_BMC = StringField(None, alias="OsIpAddress_OS-BMC", parent=self)
        # readonly attribute populated by iDRAC
        self.PTCapability_OS_BMC = EnumTypeField(None,PTCapability_OS_BMCTypes, alias="PTCapability_OS-BMC", parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PTMode_OS_BMC = EnumTypeField(None,PTMode_OS_BMCTypes, alias="PTMode_OS-BMC", parent=self)
        self.PrefixLength_OS_BMC = IntField(None, alias="PrefixLength_OS-BMC", parent=self)
        self.UsbNicIpAddress_OS_BMC = StringField(None, alias="UsbNicIpAddress_OS-BMC", parent=self)
        self.commit()

class PCIeSlotLFM(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PCIeSlotLFM", parent)
        # readonly attribute populated by iDRAC
        self.E_3rdPartyCard_PCIeSlotLFM = EnumTypeField(None,E_3rdPartyCard_PCIeSlotLFMTypes, alias="3rdPartyCard_PCIeSlotLFM", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CardType_PCIeSlotLFM = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CustomLFM_PCIeSlotLFM = IntField(None, parent=self)
        self.LFMMode_PCIeSlotLFM = EnumTypeField(None,LFMMode_PCIeSlotLFMTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxLFM_PCIeSlotLFM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SlotState_PCIeSlotLFM = EnumTypeField(None,SlotState_PCIeSlotLFMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TargetLFM_PCIeSlotLFM = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class PMLicensing(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PMLicensing", parent)
        self.DataVersion_PMLicensing = StringField(None, parent=self)
        self.LM_AUTO_DISCOVERY_PMLicensing = EnumTypeField(None,LM_AUTO_DISCOVERY_PMLicensingTypes, alias="LM-AUTO-DISCOVERY_PMLicensing", parent=self)
        self.LM_AUTO_UPDATE_PMLicensing = EnumTypeField(None,LM_AUTO_UPDATE_PMLicensingTypes, alias="LM-AUTO-UPDATE_PMLicensing", parent=self)
        self.LM_AVOTON_4CORE_PMLicensing = EnumTypeField(None,LM_AVOTON_4CORE_PMLicensingTypes, alias="LM-AVOTON-4CORE_PMLicensing", parent=self)
        self.LM_AVOTON_8CORE_PMLicensing = EnumTypeField(None,LM_AVOTON_8CORE_PMLicensingTypes, alias="LM-AVOTON-8CORE_PMLicensing", parent=self)
        self.LM_BACKUP_RESTORE_PMLicensing = EnumTypeField(None,LM_BACKUP_RESTORE_PMLicensingTypes, alias="LM-BACKUP-RESTORE_PMLicensing", parent=self)
        self.LM_BASE_IPMI_GUI_PMLicensing = EnumTypeField(None,LM_BASE_IPMI_GUI_PMLicensingTypes, alias="LM-BASE-IPMI-GUI_PMLicensing", parent=self)
        self.LM_BASIC_REMOTE_INVENTORY_EXPORT_PMLicensing = EnumTypeField(None,LM_BASIC_REMOTE_INVENTORY_EXPORT_PMLicensingTypes, alias="LM-BASIC-REMOTE-INVENTORY-EXPORT_PMLicensing", parent=self)
        self.LM_BMC_PLUS_PMLicensing = EnumTypeField(None,LM_BMC_PLUS_PMLicensingTypes, alias="LM-BMC-PLUS_PMLicensing", parent=self)
        self.LM_BOOT_CAPTURE_PMLicensing = EnumTypeField(None,LM_BOOT_CAPTURE_PMLicensingTypes, alias="LM-BOOT-CAPTURE_PMLicensing", parent=self)
        self.LM_CONNECTION_VIEW_PMLicensing = EnumTypeField(None,LM_CONNECTION_VIEW_PMLicensingTypes, alias="LM-CONNECTION-VIEW_PMLicensing", parent=self)
        self.LM_CONSOLE_COLLABORATION_PMLicensing = EnumTypeField(None,LM_CONSOLE_COLLABORATION_PMLicensingTypes, alias="LM-CONSOLE-COLLABORATION_PMLicensing", parent=self)
        self.LM_DCS_GUI_PMLicensing = EnumTypeField(None,LM_DCS_GUI_PMLicensingTypes, alias="LM-DCS-GUI_PMLicensing", parent=self)
        self.LM_DEDICATED_NIC_PMLicensing = EnumTypeField(None,LM_DEDICATED_NIC_PMLicensingTypes, alias="LM-DEDICATED-NIC_PMLicensing", parent=self)
        self.LM_DEVICE_MONITORING_PMLicensing = EnumTypeField(None,LM_DEVICE_MONITORING_PMLicensingTypes, alias="LM-DEVICE-MONITORING_PMLicensing", parent=self)
        self.LM_DHCP_CONFIGURE_PMLicensing = EnumTypeField(None,LM_DHCP_CONFIGURE_PMLicensingTypes, alias="LM-DHCP-CONFIGURE_PMLicensing", parent=self)
        self.LM_DIRECTORY_SERVICES_PMLicensing = EnumTypeField(None,LM_DIRECTORY_SERVICES_PMLicensingTypes, alias="LM-DIRECTORY-SERVICES_PMLicensing", parent=self)
        self.LM_DYNAMIC_DNS_PMLicensing = EnumTypeField(None,LM_DYNAMIC_DNS_PMLicensingTypes, alias="LM-DYNAMIC-DNS_PMLicensing", parent=self)
        self.LM_EMAIL_ALERTING_PMLicensing = EnumTypeField(None,LM_EMAIL_ALERTING_PMLicensingTypes, alias="LM-EMAIL-ALERTING_PMLicensing", parent=self)
        self.LM_FULL_UI_PMLicensing = EnumTypeField(None,LM_FULL_UI_PMLicensingTypes, alias="LM-FULL-UI_PMLicensing", parent=self)
        self.LM_GROUP_MANAGER_PMLicensing = EnumTypeField(None,LM_GROUP_MANAGER_PMLicensingTypes, alias="LM-GROUP-MANAGER_PMLicensing", parent=self)
        self.LM_IDRAC_ENTERPRISE_PMLicensing = EnumTypeField(None,LM_IDRAC_ENTERPRISE_PMLicensingTypes, alias="LM-IDRAC-ENTERPRISE_PMLicensing", parent=self)
        self.LM_IDRAC_EXPRESS_BLADES_PMLicensing = EnumTypeField(None,LM_IDRAC_EXPRESS_BLADES_PMLicensingTypes, alias="LM-IDRAC-EXPRESS-BLADES_PMLicensing", parent=self)
        self.LM_IDRAC_EXPRESS_PMLicensing = EnumTypeField(None,LM_IDRAC_EXPRESS_PMLicensingTypes, alias="LM-IDRAC-EXPRESS_PMLicensing", parent=self)
        self.LM_INBAND_FIRMWARE_UPDATE_PMLicensing = EnumTypeField(None,LM_INBAND_FIRMWARE_UPDATE_PMLicensingTypes, alias="LM-INBAND-FIRMWARE-UPDATE_PMLicensing", parent=self)
        self.LM_IPV6_PMLicensing = EnumTypeField(None,LM_IPV6_PMLicensingTypes, alias="LM-IPV6_PMLicensing", parent=self)
        self.LM_LAST_CRASH_SCREEN_CAPTURE_PMLicensing = EnumTypeField(None,LM_LAST_CRASH_SCREEN_CAPTURE_PMLicensingTypes, alias="LM-LAST-CRASH-SCREEN-CAPTURE_PMLicensing", parent=self)
        self.LM_LAST_CRASH_VIDEO_CAPTURE_PMLicensing = EnumTypeField(None,LM_LAST_CRASH_VIDEO_CAPTURE_PMLicensingTypes, alias="LM-LAST-CRASH-VIDEO-CAPTURE_PMLicensing", parent=self)
        self.LM_LC_UI_PMLicensing = EnumTypeField(None,LM_LC_UI_PMLicensingTypes, alias="LM-LC-UI_PMLicensing", parent=self)
        self.LM_LICENSE_UI_PMLicensing = EnumTypeField(None,LM_LICENSE_UI_PMLicensingTypes, alias="LM-LICENSE-UI_PMLicensing", parent=self)
        self.LM_LOCKDOWN_MODE_PMLicensing = EnumTypeField(None,LM_LOCKDOWN_MODE_PMLicensingTypes, alias="LM-LOCKDOWN-MODE_PMLicensing", parent=self)
        self.LM_NTP_PMLicensing = EnumTypeField(None,LM_NTP_PMLicensingTypes, alias="LM-NTP_PMLicensing", parent=self)
        self.LM_OME_PMLicensing = EnumTypeField(None,LM_OME_PMLicensingTypes, alias="LM-OME_PMLicensing", parent=self)
        self.LM_OOB_PMLicensing = EnumTypeField(None,LM_OOB_PMLicensingTypes, alias="LM-OOB_PMLicensing", parent=self)
        self.LM_PART_REPLACEMENT_PMLicensing = EnumTypeField(None,LM_PART_REPLACEMENT_PMLicensingTypes, alias="LM-PART-REPLACEMENT_PMLicensing", parent=self)
        self.LM_POWER_BUDGETING_PMLicensing = EnumTypeField(None,LM_POWER_BUDGETING_PMLicensingTypes, alias="LM-POWER-BUDGETING_PMLicensing", parent=self)
        self.LM_POWER_MONITORING_PMLicensing = EnumTypeField(None,LM_POWER_MONITORING_PMLicensingTypes, alias="LM-POWER-MONITORING_PMLicensing", parent=self)
        self.LM_QUALITY_BANDWIDTH_CONTROL_PMLicensing = EnumTypeField(None,LM_QUALITY_BANDWIDTH_CONTROL_PMLicensingTypes, alias="LM-QUALITY-BANDWIDTH-CONTROL_PMLicensing", parent=self)
        self.LM_RACADM_CLI_PMLicensing = EnumTypeField(None,LM_RACADM_CLI_PMLicensingTypes, alias="LM-RACADM-CLI_PMLicensing", parent=self)
        self.LM_REDFISH_PMLicensing = EnumTypeField(None,LM_REDFISH_PMLicensingTypes, alias="LM-REDFISH_PMLicensing", parent=self)
        self.LM_REMOTE_ASSET_INVENTORY_PMLicensing = EnumTypeField(None,LM_REMOTE_ASSET_INVENTORY_PMLicensingTypes, alias="LM-REMOTE-ASSET-INVENTORY_PMLicensing", parent=self)
        self.LM_REMOTE_CONFIGURATION_PMLicensing = EnumTypeField(None,LM_REMOTE_CONFIGURATION_PMLicensingTypes, alias="LM-REMOTE-CONFIGURATION_PMLicensing", parent=self)
        self.LM_REMOTE_FILE_SHARE_PMLicensing = EnumTypeField(None,LM_REMOTE_FILE_SHARE_PMLicensingTypes, alias="LM-REMOTE-FILE-SHARE_PMLicensing", parent=self)
        self.LM_REMOTE_FIRWARE_UPDATE_PMLicensing = EnumTypeField(None,LM_REMOTE_FIRWARE_UPDATE_PMLicensingTypes, alias="LM-REMOTE-FIRWARE-UPDATE_PMLicensing", parent=self)
        self.LM_REMOTE_OS_DEPLOYMENT_PMLicensing = EnumTypeField(None,LM_REMOTE_OS_DEPLOYMENT_PMLicensingTypes, alias="LM-REMOTE-OS-DEPLOYMENT_PMLicensing", parent=self)
        self.LM_REMOTE_SYSLOG_PMLicensing = EnumTypeField(None,LM_REMOTE_SYSLOG_PMLicensingTypes, alias="LM-REMOTE-SYSLOG_PMLicensing", parent=self)
        self.LM_RESTORE_PMLicensing = EnumTypeField(None,LM_RESTORE_PMLicensingTypes, alias="LM-RESTORE_PMLicensing", parent=self)
        self.LM_SECURITY_LOCKOUT_PMLicensing = EnumTypeField(None,LM_SECURITY_LOCKOUT_PMLicensingTypes, alias="LM-SECURITY-LOCKOUT_PMLicensing", parent=self)
        self.LM_SMASH_CLP_PMLicensing = EnumTypeField(None,LM_SMASH_CLP_PMLicensingTypes, alias="LM-SMASH-CLP_PMLicensing", parent=self)
        self.LM_SNMP_GET_PMLicensing = EnumTypeField(None,LM_SNMP_GET_PMLicensingTypes, alias="LM-SNMP-GET_PMLicensing", parent=self)
        self.LM_SSH_PK_AUTHEN_PMLicensing = EnumTypeField(None,LM_SSH_PK_AUTHEN_PMLicensingTypes, alias="LM-SSH-PK-AUTHEN_PMLicensing", parent=self)
        self.LM_SSH_PMLicensing = EnumTypeField(None,LM_SSH_PMLicensingTypes, alias="LM-SSH_PMLicensing", parent=self)
        self.LM_SSO_PMLicensing = EnumTypeField(None,LM_SSO_PMLicensingTypes, alias="LM-SSO_PMLicensing", parent=self)
        self.LM_STORAGE_MONITORING_PMLicensing = EnumTypeField(None,LM_STORAGE_MONITORING_PMLicensingTypes, alias="LM-STORAGE-MONITORING_PMLicensing", parent=self)
        self.LM_TELNET_PMLicensing = EnumTypeField(None,LM_TELNET_PMLicensingTypes, alias="LM-TELNET_PMLicensing", parent=self)
        self.LM_TWO_FACTOR_AUTHEN_PMLicensing = EnumTypeField(None,LM_TWO_FACTOR_AUTHEN_PMLicensingTypes, alias="LM-TWO-FACTOR-AUTHEN_PMLicensing", parent=self)
        self.LM_UPDATE_FROM_REPO_PMLicensing = EnumTypeField(None,LM_UPDATE_FROM_REPO_PMLicensingTypes, alias="LM-UPDATE-FROM-REPO_PMLicensing", parent=self)
        self.LM_USC_ASSISTED_OS_DEPLOYEMENT_PMLicensing = EnumTypeField(None,LM_USC_ASSISTED_OS_DEPLOYEMENT_PMLicensingTypes, alias="LM-USC-ASSISTED-OS-DEPLOYEMENT_PMLicensing", parent=self)
        self.LM_USC_DEVICE_CONFIGURATION_PMLicensing = EnumTypeField(None,LM_USC_DEVICE_CONFIGURATION_PMLicensingTypes, alias="LM-USC-DEVICE-CONFIGURATION_PMLicensing", parent=self)
        self.LM_USC_EMBEDDED_DIAGNOSTICS_PMLicensing = EnumTypeField(None,LM_USC_EMBEDDED_DIAGNOSTICS_PMLicensingTypes, alias="LM-USC-EMBEDDED-DIAGNOSTICS_PMLicensing", parent=self)
        self.LM_USC_FIRMWARE_UPDATE_PMLicensing = EnumTypeField(None,LM_USC_FIRMWARE_UPDATE_PMLicensingTypes, alias="LM-USC-FIRMWARE-UPDATE_PMLicensing", parent=self)
        self.LM_VCONSOLE_CHAT_PMLicensing = EnumTypeField(None,LM_VCONSOLE_CHAT_PMLicensingTypes, alias="LM-VCONSOLE-CHAT_PMLicensing", parent=self)
        self.LM_VCONSOLE_HTML5_ACCESS_PMLicensing = EnumTypeField(None,LM_VCONSOLE_HTML5_ACCESS_PMLicensingTypes, alias="LM-VCONSOLE-HTML5-ACCESS_PMLicensing", parent=self)
        self.LM_VCONSOLE_PMLicensing = EnumTypeField(None,LM_VCONSOLE_PMLicensingTypes, alias="LM-VCONSOLE_PMLicensing", parent=self)
        self.LM_VFOLDER_PMLicensing = EnumTypeField(None,LM_VFOLDER_PMLicensingTypes, alias="LM-VFOLDER_PMLicensing", parent=self)
        self.LM_VIRTUAL_FLASH_PARTITIONS_PMLicensing = EnumTypeField(None,LM_VIRTUAL_FLASH_PARTITIONS_PMLicensingTypes, alias="LM-VIRTUAL-FLASH-PARTITIONS_PMLicensing", parent=self)
        self.LM_VMEDIA_PMLicensing = EnumTypeField(None,LM_VMEDIA_PMLicensingTypes, alias="LM-VMEDIA_PMLicensing", parent=self)
        self.LM_VNC_PMLicensing = EnumTypeField(None,LM_VNC_PMLicensingTypes, alias="LM-VNC_PMLicensing", parent=self)
        self.LM_WSMAN_PMLicensing = EnumTypeField(None,LM_WSMAN_PMLicensingTypes, alias="LM-WSMAN_PMLicensing", parent=self)
        self.LMFeatureBitsCheckSum_PMLicensing = StringField(None, parent=self)
        self.PMAllowableLicenses_PMLicensing = EnumTypeField(None,PMAllowableLicenses_PMLicensingTypes, parent=self)
        self.PMDefaultLicenseFeatures_PMLicensing = EnumTypeField(None,PMDefaultLicenseFeatures_PMLicensingTypes, parent=self)
        self.PMDrivenLicensing_PMLicensing = EnumTypeField(None,PMDrivenLicensing_PMLicensingTypes, parent=self)
        self.commit()

class PSUSlot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PSUSlot", parent)
        self.Config_PSUSlot = StringField(None, parent=self)
        self.Contains_PSUSlot = StringField(None, parent=self)
        self.Occupied_PSUSlot = EnumTypeField(None,Occupied_PSUSlotTypes, parent=self)
        self.SlotName_PSUSlot = StringField(None, parent=self)
        self.config_PSUSlot = StringField(None, parent=self)
        self.contains_PSUSlot = StringField(None, parent=self)
        self.commit()

class PSUSlotSeq(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PSUSlotSeq", parent)
        # readonly attribute populated by iDRAC
        self.Order_PSUSlotSeq = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.order_PSUSlotSeq = StringField(None, parent=self)
        self.commit()

class PlatformCapability(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PlatformCapability", parent)
        # readonly attribute populated by iDRAC
        self.E_12GBackplaneon13GCapable_PlatformCapability = EnumTypeField(None,E_12GBackplaneon13GCapable_PlatformCapabilityTypes, alias="12GBackplaneon13GCapable_PlatformCapability", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BackplaneCapable_PlatformCapability = EnumTypeField(None,BackplaneCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BluetoothCapable_PlatformCapability = EnumTypeField(None,BluetoothCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CUPSCapable_PlatformCapability = EnumTypeField(None,CUPSCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisIntrusionCapable_PlatformCapability = EnumTypeField(None,ChassisIntrusionCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DPCapable_PlatformCapability = EnumTypeField(None,DPCapable_PlatformCapabilityTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.DedicatedNICCapable_PlatformCapability = EnumTypeField(None,DedicatedNICCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FTRCapable_PlatformCapability = EnumTypeField(None,FTRCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FreshAirCapable_PlatformCapability = EnumTypeField(None,FreshAirCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FrontPanelCapable_PlatformCapability = EnumTypeField(None,FrontPanelCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FrontPanelUSBCapable_PlatformCapability = EnumTypeField(None,FrontPanelUSBCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.IDSDMCapable_PlatformCapability = EnumTypeField(None,IDSDMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LCDCapable_PlatformCapability = EnumTypeField(None,LCDCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LicenseUpsellCapable_PlatformCapability = EnumTypeField(None,LicenseUpsellCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LifecyclecontrollerCapable_PlatformCapability = EnumTypeField(None,LifecyclecontrollerCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MEAutoResetDisable_PlatformCapability = EnumTypeField(None,MEAutoResetDisable_PlatformCapabilityTypes, parent=self)
        self.MaxPCIeSlots_PlatformCapability = IntField(None, parent=self)
        self.MezzLOMCapable_PlatformCapability = EnumTypeField(None,MezzLOMCapable_PlatformCapabilityTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ModularSharedLOMCapable_PlatformCapability = EnumTypeField(None,ModularSharedLOMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NGMPlatform_PlatformCapability = EnumTypeField(None,NGMPlatform_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NMCapable_PlatformCapability = EnumTypeField(None,NMCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NMPTASCapable_PlatformCapability = EnumTypeField(None,NMPTASCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NMSubSystemPwrMonitoringCapable_PlatformCapability = EnumTypeField(None,NMSubSystemPwrMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NOBladethrottleDuringCMCrebootCapable_PlatformCapability = EnumTypeField(None,NOBladethrottleDuringCMCrebootCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.OSBMCPassthroughCapable_PlatformCapability = EnumTypeField(None,OSBMCPassthroughCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PMBUSCapablePSU_PlatformCapability = EnumTypeField(None,PMBUSCapablePSU_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PMBUSVRCapable_PlatformCapability = EnumTypeField(None,PMBUSVRCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PSUMismatchCapable_PlatformCapability = EnumTypeField(None,PSUMismatchCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PSURedundancyCapable_PlatformCapability = EnumTypeField(None,PSURedundancyCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PostPoneNICSelectionCapable_PlatformCapability = EnumTypeField(None,PostPoneNICSelectionCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerBudgetCapable_PlatformCapability = EnumTypeField(None,PowerBudgetCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerConfigurationCapable_PlatformCapability = EnumTypeField(None,PowerConfigurationCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerConfigurationRemovalCapable_PlatformCapability = EnumTypeField(None,PowerConfigurationRemovalCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerInventoryCapable_PlatformCapability = EnumTypeField(None,PowerInventoryCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerMonitoringCapable_PlatformCapability = EnumTypeField(None,PowerMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RSPICapable_PlatformCapability = EnumTypeField(None,RSPICapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RemoteEnablementCapable_PlatformCapability = EnumTypeField(None,RemoteEnablementCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SCPwrMonitoringCapable_PlatformCapability = EnumTypeField(None,SCPwrMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SDCardCapable_PlatformCapability = EnumTypeField(None,SDCardCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SmartCardLoginCapable_PlatformCapability = EnumTypeField(None,SmartCardLoginCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SubSystemPowerMonitoringCapable_PlatformCapability = EnumTypeField(None,SubSystemPowerMonitoringCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TempPowerThresholdCapable_PlatformCapability = EnumTypeField(None,TempPowerThresholdCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThermalManagementCapable_PlatformCapability = EnumTypeField(None,ThermalManagementCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.UserPowerCapBoundCapable_PlatformCapability = EnumTypeField(None,UserPowerCapBoundCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.UserPowerCapCapable_PlatformCapability = EnumTypeField(None,UserPowerCapCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.WiFiCapable_PlatformCapability = EnumTypeField(None,WiFiCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.iDRACDirectUSBNICCapable_PlatformCapability = EnumTypeField(None,iDRACDirectUSBNICCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.vFlashCapable_PlatformCapability = EnumTypeField(None,vFlashCapable_PlatformCapabilityTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class PlatformLicense(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PlatformLicense", parent)
        # readonly attribute populated by iDRAC
        self.AllowableLicenses_PlatformLicense = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DefaultLicenseFeatures_PlatformLicense = EnumTypeField(None,DefaultLicenseFeatures_PlatformLicenseTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class PowerButton(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PowerButton", parent)
        self.ID_PowerButton = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IndicatorColor_PowerButton = EnumTypeField(None,IndicatorColor_PowerButtonTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IndicatorState_PowerButton = EnumTypeField(None,IndicatorState_PowerButtonTypes, parent=self)
        self.commit()

class PowerHealthIndicator(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PowerHealthIndicator", parent)
        self.ID_PowerHealthIndicator = StringField(None, parent=self)
        self.IndicatorColor_PowerHealthIndicator = EnumTypeField(None,IndicatorColor_PowerHealthIndicatorTypes, parent=self)
        self.IndicatorState_PowerHealthIndicator = EnumTypeField(None,IndicatorState_PowerHealthIndicatorTypes, parent=self)
        self.commit()

class PowerHistorical(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PowerHistorical", parent)
        self.IntervalInSeconds_PowerHistorical = IntField(None, parent=self)
        self.StartTime_PowerHistorical = StringField(None, parent=self)
        self.commit()

class PrivateStore(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "PrivateStore", parent)
        self.ACRestoreState_PrivateStore = EnumTypeField(None,ACRestoreState_PrivateStoreTypes, parent=self)
        self.ActiveSATACount_PrivateStore = IntField(None, parent=self)
        self.AlertAddrMigration_PrivateStore = EnumTypeField(None,AlertAddrMigration_PrivateStoreTypes, parent=self)
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
        self.BladeStorNormalPwr_PrivateStore = IntField(None, parent=self)
        self.BladeStorThrottlePwr_PrivateStore = IntField(None, parent=self)
        self.CIPHERSuiteDisable_PrivateStore = EnumTypeField(None,CIPHERSuiteDisable_PrivateStoreTypes, parent=self)
        self.IDSDMState_PrivateStore = EnumTypeField(None,IDSDMState_PrivateStoreTypes, parent=self)
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
        self.LastPostCode_PrivateStore = IntField(None, parent=self)
        self.LastPwrState_PrivateStore = EnumTypeField(None,LastPwrState_PrivateStoreTypes, parent=self)
        self.NDCMisconfig_PrivateStore = EnumTypeField(None,NDCMisconfig_PrivateStoreTypes, parent=self)
        self.PowerCapState_PrivateStore = EnumTypeField(None,PowerCapState_PrivateStoreTypes, parent=self)
        self.ROMBStatus_PrivateStore = IntField(None, parent=self)
        self.State_PrivateStore = IntField(None, parent=self)
        self.commit()

class ProfileTask(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ProfileTask", parent)
        # readonly attribute populated by iDRAC
        self.EndTime_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Id_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Message1_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_1_ProfileTask = StringField(None, alias="MessageArg1-1_ProfileTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_2_ProfileTask = StringField(None, alias="MessageArg1-2_ProfileTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageArg1_3_ProfileTask = StringField(None, alias="MessageArg1-3_ProfileTask", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MessageID1_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PercentComplete_ProfileTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.StartTime_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TaskState_ProfileTask = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.TaskStatus_ProfileTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class QuickSync(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "QuickSync", parent)
        self.Access_QuickSync = EnumTypeField(None,Access_QuickSyncTypes, parent=self)
        self.AuthFailureCount_QuickSync = IntField(None, parent=self)
        self.AuthFailureTime_QuickSync = StringField(None, parent=self)
        self.InactivityTimeout_QuickSync = IntField(None, parent=self)
        self.InactivityTimerEnable_QuickSync = EnumTypeField(None,InactivityTimerEnable_QuickSyncTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Presence_QuickSync = EnumTypeField(None,Presence_QuickSyncTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.QuickSyncButtonEnable_QuickSync = EnumTypeField(None,QuickSyncButtonEnable_QuickSyncTypes, parent=self)
        self.ReadAuthentication_QuickSync = EnumTypeField(None,ReadAuthentication_QuickSyncTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Status_QuickSync = EnumTypeField(None,Status_QuickSyncTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.WifiEnable_QuickSync = EnumTypeField(None,WifiEnable_QuickSyncTypes, parent=self)
        self.commit()

class RFS(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "RFS", parent)
        self.AttachMode_RFS = EnumTypeField(None,AttachMode_RFSTypes, parent=self)
        self.Enable_RFS = EnumTypeField(None,Enable_RFSTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Image_RFS = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MediaAttachState_RFS = EnumTypeField(None,MediaAttachState_RFSTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Password_RFS = StringField(None, parent=self)
        self.RMPath_RFS = StringField(None, parent=self)
        self.Status_RFS = EnumTypeField(None,Status_RFSTypes, parent=self)
        self.User_RFS = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.WriteProtected_RFS = EnumTypeField(None,WriteProtected_RFSTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class RSM(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "RSM", parent)
        # readonly attribute populated by iDRAC
        self.ChassisPSUInfoCapability_RSM = EnumTypeField(None,ChassisPSUInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisPowerInfoCapability_RSM = EnumTypeField(None,ChassisPowerInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisSystemInfoCapability_RSM = EnumTypeField(None,ChassisSystemInfoCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RSMCapability_RSM = EnumTypeField(None,RSMCapability_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RSMSetting_RSM = EnumTypeField(None,RSMSetting_RSMTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class RSM_(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "RSM?", parent)
        self.RSMSetting_RSM = EnumTypeField(None,RSMSetting_RSMTypes, alias="RSMSetting_RSM?", parent=self)
        self.commit()

class Racadm(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Racadm", parent)
        self.ActiveSessions_Racadm = IntField(None, parent=self)
        self.Enable_Racadm = EnumTypeField(None,Enable_RacadmTypes, parent=self)
        self.MaxSessions_Racadm = IntField(None, parent=self)
        self.Timeout_Racadm = IntField(None, parent=self)
        self.commit()

class Racadm_(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Racadm?", parent)
        self.Enable_Racadm = EnumTypeField(None,Enable_RacadmTypes, alias="Enable_Racadm?", parent=self)
        self.Timeout_Racadm = IntField(None, alias="Timeout_Racadm?", parent=self)
        self.commit()

class Redfish(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Redfish", parent)
        self.Enable_Redfish = EnumTypeField(None,Enable_RedfishTypes, parent=self)
        self.commit()

class RedfishEventing(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "RedfishEventing", parent)
        self.DeliveryRetryAttempts_RedfishEventing = IntField(None, parent=self)
        self.DeliveryRetryIntervalInSeconds_RedfishEventing = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IgnoreCertificateErrors_RedfishEventing = EnumTypeField(None,IgnoreCertificateErrors_RedfishEventingTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class Redundancy(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Redundancy", parent)
        # readonly attribute populated by iDRAC
        self.MaxNumSupported_Redundancy = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinNumNeeded_Redundancy = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Mode_Redundancy = EnumTypeField(None,Mode_RedundancyTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.State_Redundancy = EnumTypeField(None,State_RedundancyTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class RemoteHosts(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "RemoteHosts", parent)
        self.SMTPAuthentication_RemoteHosts = EnumTypeField(None,SMTPAuthentication_RemoteHostsTypes, parent=self)
        self.SMTPPassword_RemoteHosts = StringField(None, parent=self)
        self.SMTPPort_RemoteHosts = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SMTPSASL_RemoteHosts = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SMTPServerIPAddress_RemoteHosts = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SMTPStartTLS_RemoteHosts = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SMTPUserName_RemoteHosts = StringField(None, parent=self)
        self.commit()

class SATAInventory(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SATAInventory", parent)
        self.DeviceProp_SATAInventory = StringField(None, parent=self)
        self.SATAFQDDString_SATAInventory = StringField(None, parent=self)
        self.SlotNumber_SATAInventory = StringField(None, parent=self)
        self.commit()

class SC_BMC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SC-BMC", parent)
        self.ChassisInfraPower_SC_BMC = IntField(None, alias="ChassisInfraPower_SC-BMC", parent=self)
        self.ChassisPowerCap_SC_BMC = IntField(None, alias="ChassisPowerCap_SC-BMC", parent=self)
        self.ChassisServiceTagCRC_SC_BMC = IntField(None, alias="ChassisServiceTagCRC_SC-BMC", parent=self)
        self.ChassisServiceTagLen_SC_BMC = IntField(None, alias="ChassisServiceTagLen_SC-BMC", parent=self)
        self.ChassisServiceTagSet_SC_BMC = IntField(None, alias="ChassisServiceTagSet_SC-BMC", parent=self)
        self.ChassisServiceTag_SC_BMC = StringField(None, alias="ChassisServiceTag_SC-BMC", parent=self)
        self.EnableSCAttributes_SC_BMC = IntField(None, alias="EnableSCAttributes_SC-BMC", parent=self)
        self.SCFWUpdateState_SC_BMC = EnumTypeField(None,SCFWUpdateState_SC_BMCTypes, alias="SCFWUpdateState_SC-BMC", parent=self)
        self.TaskID_SC_BMC = IntField(None, alias="TaskID_SC-BMC", parent=self)
        self.commit()

class SECONDARYNIC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SECONDARYNIC", parent)
        # readonly attribute populated by iDRAC
        self.AutoNegotiate_SECONDARYNIC = EnumTypeField(None,AutoNegotiate_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DHCPEnable_SECONDARYNIC = EnumTypeField(None,DHCPEnable_SECONDARYNICTypes, parent=self)
        self.DNSDRACName_SECONDARYNIC = StringField(None, parent=self)
        self.DNSFromDHCP_SECONDARYNIC = EnumTypeField(None,DNSFromDHCP_SECONDARYNICTypes, parent=self)
        self.DNSServer1_SECONDARYNIC = StringField(None, parent=self)
        self.DNSServer2_SECONDARYNIC = StringField(None, parent=self)
        self.DomainNameDHCP_SECONDARYNIC = EnumTypeField(None,DomainNameDHCP_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Duplex_SECONDARYNIC = EnumTypeField(None,Duplex_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HostName_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4Address_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4Gateway_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4NetMask_SECONDARYNIC = StringField(None, parent=self)
        self.IPV4StaticDomainName_SECONDARYNIC = StringField(None, parent=self)
        self.IPv4Enable_SECONDARYNIC = EnumTypeField(None,IPv4Enable_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MACAddress_SECONDARYNIC = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MTU_SECONDARYNIC = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NICEnable_SECONDARYNIC = EnumTypeField(None,NICEnable_SECONDARYNICTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NICFailover_SECONDARYNIC = EnumTypeField(None,NICFailover_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NICSelection_SECONDARYNIC = EnumTypeField(None,NICSelection_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NICSpeed_SECONDARYNIC = EnumTypeField(None,NICSpeed_SECONDARYNICTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.RegisterHostDNS_SECONDARYNIC = EnumTypeField(None,RegisterHostDNS_SECONDARYNICTypes, parent=self)
        self.VLANEnable_SECONDARYNIC = EnumTypeField(None,VLANEnable_SECONDARYNICTypes, parent=self)
        self.VLANID_SECONDARYNIC = IntField(None, parent=self)
        self.VLANPriority_SECONDARYNIC = StringField(None, parent=self)
        self.commit()

class SNMP(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SNMP", parent)
        self.AgentCommunity_SNMP = StringField(None, parent=self)
        self.AgentEnable_SNMP = EnumTypeField(None,AgentEnable_SNMPTypes, parent=self)
        self.AlertPort_SNMP = IntField(None, parent=self)
        self.DiscoveryPort_SNMP = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.EngineID_SNMP = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SNMPProtocol_SNMP = EnumTypeField(None,SNMPProtocol_SNMPTypes, parent=self)
        self.TrapFormat_SNMP = EnumTypeField(None,TrapFormat_SNMPTypes, parent=self)
        self.commit()

class SNMPAlert(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SNMPAlert", parent)
        self.Destination_SNMPAlert = StringField(None, alias="? Destination_SNMPAlert", parent=self)
        self.AlertAckInterval_SNMPAlert = IntField(None, parent=self)
        self.DestinationType_SNMPAlert = IntField(None, parent=self)
        self.Destination_SNMPAlert = StringField(None, parent=self)
        self.Enable_SNMPAlert = EnumTypeField(None,Enable_SNMPAlertTypes, parent=self)
        self.Retries_SNMPAlert = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SNMPv3UserID_SNMPAlert = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SNMPv3Username_SNMPAlert = StringField(None, parent=self)
        self.State_SNMPAlert = EnumTypeField(None,State_SNMPAlertTypes, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.Destination_SNMPAlert

    @property
    def Index(self):
        return self.Destination_SNMPAlert._index

class SNMPTrapIPv4(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SNMPTrapIPv4", parent)
        self.DestIPv4Addr_SNMPTrapIPv4 = StringField(None, parent=self)
        # readonly attribute
        self.DestinationNum_SNMPTrapIPv4 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.State_SNMPTrapIPv4 = EnumTypeField(None,State_SNMPTrapIPv4Types, parent=self)
        self.commit()

class SNMPTrapIPv6(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SNMPTrapIPv6", parent)
        self.DestIPv6Addr_SNMPTrapIPv6 = StringField(None, parent=self)
        # readonly attribute
        self.DestinationNum_SNMPTrapIPv6 = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.State_SNMPTrapIPv6 = EnumTypeField(None,State_SNMPTrapIPv6Types, parent=self)
        self.commit()

class SSH(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SSH", parent)
        self.Enable_SSH = EnumTypeField(None,Enable_SSHTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_SSH = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Port_SSH = IntField(None, parent=self)
        self.Timeout_SSH = IntField(None, parent=self)
        self.commit()

class SecureDefaultPassword(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SecureDefaultPassword", parent)
        # readonly attribute populated by iDRAC
        self.AESKey_SecureDefaultPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AESiv_SecureDefaultPassword = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DefaultUserCreated_SecureDefaultPassword = EnumTypeField(None,DefaultUserCreated_SecureDefaultPasswordTypes, parent=self)
        self.DisplayToeTagError_SecureDefaultPassword = EnumTypeField(None,DisplayToeTagError_SecureDefaultPasswordTypes, parent=self)
        self.Password_SecureDefaultPassword = StringField(None, parent=self)
        self.ResetType_SecureDefaultPassword = EnumTypeField(None,ResetType_SecureDefaultPasswordTypes, parent=self)
        self.commit()

class Security(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Security", parent)
        self.CaCertPath_Security = StringField(None, parent=self)
        self.ConfigCertStatus_Security = IntField(None, parent=self)
        self.CsrCommonName_Security = StringField(None, parent=self)
        self.CsrCountryCode_Security = StringField(None, parent=self)
        self.CsrEmailAddr_Security = StringField(None, parent=self)
        self.CsrKeySize_Security = EnumTypeField(None,CsrKeySize_SecurityTypes, parent=self)
        self.CsrLocalityName_Security = StringField(None, parent=self)
        self.CsrOrganizationName_Security = StringField(None, parent=self)
        self.CsrOrganizationUnit_Security = StringField(None, parent=self)
        self.CsrStateName_Security = StringField(None, parent=self)
        self.FIPSMode_Security = EnumTypeField(None,FIPSMode_SecurityTypes, parent=self)
        self.FieldSupportDebugAESIV_Security = StringField(None, parent=self)
        self.MainCertPath_Security = StringField(None, parent=self)
        self.MainKeyPath_Security = StringField(None, parent=self)
        self.PendingCSRKeyPath_Security = StringField(None, parent=self)
        self.PendingCSRPath_Security = StringField(None, parent=self)
        self.commit()

class SecurityCSC(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SecurityCSC", parent)
        self.CSCCsrBusiness_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCityName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCommonName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrCountryCode_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrDeptName_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrEmailAddr_SecurityCSC = StringField(None, parent=self)
        self.CSCCsrStateName_SecurityCSC = StringField(None, parent=self)
        self.commit()

class SecuritySSL(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SecuritySSL", parent)
        self.CACertificate_SecuritySSL = StringField(None, parent=self)
        self.Certificate_SecuritySSL = StringField(None, parent=self)
        self.Key_SecuritySSL = StringField(None, parent=self)
        self.TemperaryKey_SecuritySSL = StringField(None, parent=self)
        self.commit()

class Sensor(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Sensor", parent)
        self.LowerCriticalThreshold_Sensor = IntField(None, parent=self)
        self.LowerWarningThreshold_Sensor = IntField(None, parent=self)
        self.SensorName_Sensor = StringField(None, parent=self)
        self.StartTime_Sensor = StringField(None, parent=self)
        self.UpperCriticalThreshold_Sensor = IntField(None, parent=self)
        self.UpperWarningThreshold_Sensor = IntField(None, parent=self)
        self.commit()

class SensorThresholds(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SensorThresholds", parent)
        self.LC_SensorThresholds = IntField(None, parent=self)
        self.LNC_SensorThresholds = IntField(None, parent=self)
        self.SensorNumber_SensorThresholds = IntField(None, parent=self)
        self.UC_SensorThresholds = IntField(None, parent=self)
        self.UNC_SensorThresholds = IntField(None, parent=self)
        self.commit()

class Serial(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Serial", parent)
        self.BaudRate_Serial = EnumTypeField(None,BaudRate_SerialTypes, parent=self)
        self.Command_Serial = StringField(None, parent=self)
        self.Enable_Serial = EnumTypeField(None,Enable_SerialTypes, parent=self)
        self.HistorySize_Serial = IntField(None, parent=self)
        self.IdleTimeout_Serial = IntField(None, parent=self)
        self.NoAuth_Serial = EnumTypeField(None,NoAuth_SerialTypes, parent=self)
        self.commit()

class SerialRedirection(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SerialRedirection", parent)
        self.AutoEnable_SerialRedirection = EnumTypeField(None,AutoEnable_SerialRedirectionTypes, parent=self)
        self.Enable_SerialRedirection = EnumTypeField(None,Enable_SerialRedirectionTypes, parent=self)
        self.QuitKey_SerialRedirection = StringField(None, parent=self)
        self.commit()

class ServerBoot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerBoot", parent)
        self.BootOnce_ServerBoot = EnumTypeField(None,BootOnce_ServerBootTypes, parent=self)
        self.FirstBootDevice_ServerBoot = EnumTypeField(None,FirstBootDevice_ServerBootTypes, parent=self)
        self.VflashBootPartition_ServerBoot = IntField(None, parent=self)
        self.commit()

class ServerInfo(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerInfo", parent)
        self.AssetTagSetByDCMI_ServerInfo = EnumTypeField(None,AssetTagSetByDCMI_ServerInfoTypes, parent=self)
        self.AssetTag_ServerInfo = StringField(None, parent=self)
        self.MgtNetworkNicConfig_ServerInfo = EnumTypeField(None,MgtNetworkNicConfig_ServerInfoTypes, parent=self)
        self.NodeID_ServerInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.RChassisServiceTag_ServerInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceTag_ServerInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SledConfig_ServerInfo = EnumTypeField(None,SledConfig_ServerInfoTypes, parent=self)
        self.SysAssetTag_ServerInfo = StringField(None, parent=self)
        self.commit()

class ServerOS(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerOS", parent)
        self.HostName_ServerOS = StringField(None, parent=self)
        self.OSName_ServerOS = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.OSVersion_ServerOS = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServerPoweredOnTime_ServerOS = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ServerPwr(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerPwr", parent)
        # readonly attribute populated by iDRAC
        self.ActivePolicyName_ServerPwr = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ActivePowerCapVal_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DynamicStepUp_ServerPwr = EnumTypeField(None,DynamicStepUp_ServerPwrTypes, parent=self)
        self.GpGPUActiveEntries_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxPsuSlots_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.OverTemperatureCLSTOverride_ServerPwr = EnumTypeField(None,OverTemperatureCLSTOverride_ServerPwrTypes, parent=self)
        self.PSPFCEnabled_ServerPwr = EnumTypeField(None,PSPFCEnabled_ServerPwrTypes, parent=self)
        self.PSRapidOn_ServerPwr = EnumTypeField(None,PSRapidOn_ServerPwrTypes, parent=self)
        self.PSRedPolicy_ServerPwr = EnumTypeField(None,PSRedPolicy_ServerPwrTypes, parent=self)
        self.PSUHotSpareSleepthreshold_ServerPwr = IntField(None, parent=self)
        self.PSUHotSpareWakethreshold_ServerPwr = IntField(None, parent=self)
        self.PSUMismatchOverride_ServerPwr = EnumTypeField(None,PSUMismatchOverride_ServerPwrTypes, parent=self)
        self.PercGracefulShutdownWarning_ServerPwr = IntField(None, parent=self)
        self.PowerAllocated_ServerPwr = IntField(None, parent=self)
        self.PowerBudgetOverride_ServerPwr = EnumTypeField(None,PowerBudgetOverride_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.PowerCapMaxThres_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PowerCapMinThres_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PowerCapSetting_ServerPwr = EnumTypeField(None,PowerCapSetting_ServerPwrTypes, parent=self)
        self.PowerCapValue_ServerPwr = IntField(None, parent=self)
        self.RapidOnPrimaryPSU_ServerPwr = EnumTypeField(None,RapidOnPrimaryPSU_ServerPwrTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SCViewSledPwr_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SLBAllocOverride_ServerPwr = EnumTypeField(None,SLBAllocOverride_ServerPwrTypes, parent=self)
        self.SLBBoundsCheck_ServerPwr = EnumTypeField(None,SLBBoundsCheck_ServerPwrTypes, parent=self)
        self.SLBPersistence_ServerPwr = EnumTypeField(None,SLBPersistence_ServerPwrTypes, parent=self)
        self.SLBState_ServerPwr = EnumTypeField(None,SLBState_ServerPwrTypes, parent=self)
        self.SimComponentVal_ServerPwr = IntField(None, parent=self)
        self.StatisticsStartTime_ServerPwr = StringField(None, parent=self)
        self.TargetPwrAllocation_ServerPwr = IntField(None, parent=self)
        self.UnderVoltageCLSTOverride_ServerPwr = EnumTypeField(None,UnderVoltageCLSTOverride_ServerPwrTypes, parent=self)
        self.UpperThresholdCritical_ServerPwr = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.pciePowerAllocation_ServerPwr = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ServerPwrMon(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerPwrMon", parent)
        # readonly attribute populated by iDRAC
        self.AccumulativePower_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.AccumulativeStartEnergy_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CumulativePowerStartTime_ServerPwrMon = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
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
        self.PowerConfigReset_ServerPwrMon = EnumTypeField(None,PowerConfigReset_ServerPwrMonTypes, parent=self)
        self.commit()

class ServerTopology(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServerTopology", parent)
        self.AisleName_ServerTopology = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BladeSlotNumInChassis_ServerTopology = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ChassisName_ServerTopology = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DataCenterName_ServerTopology = StringField(None, parent=self)
        self.RackName_ServerTopology = StringField(None, parent=self)
        self.RackSlot_ServerTopology = IntField(None, parent=self)
        self.RoomName_ServerTopology = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SizeOfManagedSystemInU_ServerTopology = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ServiceModule(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ServiceModule", parent)
        self.HostSNMPAlert_ServiceModule = EnumTypeField(None,HostSNMPAlert_ServiceModuleTypes, parent=self)
        self.LCLReplication_ServiceModule = EnumTypeField(None,LCLReplication_ServiceModuleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NetworkConnection_ServiceModule = EnumTypeField(None,NetworkConnection_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.OMSAPresence_ServiceModule = EnumTypeField(None,OMSAPresence_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.OSInfo_ServiceModule = EnumTypeField(None,OSInfo_ServiceModuleTypes, parent=self)
        self.SNMPOnHostOS_ServiceModule = EnumTypeField(None,SNMPOnHostOS_ServiceModuleTypes, parent=self)
        self.SWRaidMonitoring_ServiceModule = EnumTypeField(None,SWRaidMonitoring_ServiceModuleTypes, parent=self)
        self.ServiceModuleEnable_ServiceModule = EnumTypeField(None,ServiceModuleEnable_ServiceModuleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ServiceModuleState_ServiceModule = EnumTypeField(None,ServiceModuleState_ServiceModuleTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ServiceModuleVersion_ServiceModule = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.WMIInfo_ServiceModule = EnumTypeField(None,WMIInfo_ServiceModuleTypes, parent=self)
        self.WatchdogRecoveryAction_ServiceModule = EnumTypeField(None,WatchdogRecoveryAction_ServiceModuleTypes, parent=self)
        self.WatchdogResetTime_ServiceModule = IntField(None, parent=self)
        self.WatchdogState_ServiceModule = EnumTypeField(None,WatchdogState_ServiceModuleTypes, parent=self)
        self.iDRACHardReset_ServiceModule = EnumTypeField(None,iDRACHardReset_ServiceModuleTypes, parent=self)
        self.commit()

class SledInterposer(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SledInterposer", parent)
        # readonly attribute populated by iDRAC
        self.Config_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Contains_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Occupied_SledInterposer = EnumTypeField(None,Occupied_SledInterposerTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_SledInterposer = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class SledSlot(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SledSlot", parent)
        # readonly attribute populated by iDRAC
        self.Config_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Contains_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Occupied_SledSlot = EnumTypeField(None,Occupied_SledSlotTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SlotName_SledSlot = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class SlotConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SlotConfig", parent)
        # readonly attribute populated by iDRAC
        self.Columns_SlotConfig = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Location_SlotConfig = EnumTypeField(None,Location_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Name_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Order_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Orientation_SlotConfig = EnumTypeField(None,Orientation_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ParentConfig_SlotConfig = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Rows_SlotConfig = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.Type_SlotConfig = EnumTypeField(None,Type_SlotConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class SmartCard(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SmartCard", parent)
        self.SmartCardCRLEnable_SmartCard = EnumTypeField(None,SmartCardCRLEnable_SmartCardTypes, parent=self)
        self.SmartCardLogonEnable_SmartCard = EnumTypeField(None,SmartCardLogonEnable_SmartCardTypes, parent=self)
        self.commit()

class Storage(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Storage", parent)
        self.AvailableSpareAlertThreshold_Storage = IntField(None, parent=self)
        self.RemainingRatedWriteEnduranceAlertThreshold_Storage = IntField(None, parent=self)
        self.commit()

class SupportAssist(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SupportAssist", parent)
        self.Action_SupportAssist = StringField(None, parent=self)
        self.DefaultIPAddress_SupportAssist = StringField(None, parent=self)
        self.DefaultLocalPathName_SupportAssist = StringField(None, parent=self)
        self.DefaultPassword_SupportAssist = StringField(None, parent=self)
        self.DefaultProtocol_SupportAssist = EnumTypeField(None,DefaultProtocol_SupportAssistTypes, parent=self)
        self.DefaultShareName_SupportAssist = StringField(None, parent=self)
        self.DefaultUserName_SupportAssist = StringField(None, parent=self)
        self.DefaultWorkgroupName_SupportAssist = StringField(None, parent=self)
        self.EmailOptIn_SupportAssist = EnumTypeField(None,EmailOptIn_SupportAssistTypes, parent=self)
        self.ErrorCode_SupportAssist = StringField(None, parent=self)
        self.EventBasedAutoCollection_SupportAssist = EnumTypeField(None,EventBasedAutoCollection_SupportAssistTypes, parent=self)
        self.FilePath_SupportAssist = StringField(None, parent=self)
        self.FilterAutoCollections_SupportAssist = EnumTypeField(None,FilterAutoCollections_SupportAssistTypes, parent=self)
        self.HostOSProxyAddress_SupportAssist = StringField(None, parent=self)
        self.HostOSProxyConfigured_SupportAssist = EnumTypeField(None,HostOSProxyConfigured_SupportAssistTypes, parent=self)
        self.HostOSProxyPassword_SupportAssist = StringField(None, parent=self)
        self.HostOSProxyPort_SupportAssist = IntField(None, parent=self)
        self.HostOSProxyUserName_SupportAssist = StringField(None, parent=self)
        self.MBSELRestoreState_SupportAssist = EnumTypeField(None,MBSELRestoreState_SupportAssistTypes, parent=self)
        self.NativeOSLogsCollectionOverride_SupportAssist = EnumTypeField(None,NativeOSLogsCollectionOverride_SupportAssistTypes, parent=self)
        self.NativeOSLogsCollectionSupported_SupportAssist = EnumTypeField(None,NativeOSLogsCollectionSupported_SupportAssistTypes, parent=self)
        self.PercentComplete_SupportAssist = IntField(None, parent=self)
        self.PreferredLanguage_SupportAssist = EnumTypeField(None,PreferredLanguage_SupportAssistTypes, parent=self)
        self.PrimaryContactAlternatePhoneNumber_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactEmail_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactFirstName_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactLastName_SupportAssist = StringField(None, parent=self)
        self.PrimaryContactPhoneNumber_SupportAssist = StringField(None, parent=self)
        self.ProSupportPlusRecommendationsReport_SupportAssist = EnumTypeField(None,ProSupportPlusRecommendationsReport_SupportAssistTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.RegistrationID_SupportAssist = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ScheduleBasedAutoCollection_SupportAssist = EnumTypeField(None,ScheduleBasedAutoCollection_SupportAssistTypes, parent=self)
        self.SecondaryContactAlternatePhoneNumber_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactEmail_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactFirstName_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactLastName_SupportAssist = StringField(None, parent=self)
        self.SecondaryContactPhoneNumber_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoCity_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoCompanyName_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoCountry_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoState_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoStreet1_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoStreet2_SupportAssist = StringField(None, parent=self)
        self.ShippingInfoZip_SupportAssist = StringField(None, parent=self)
        self.Status_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAcceptedAtiDRACTime_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAcceptedByiDRACUser_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAcceptedViaiDRACIntf_SupportAssist = StringField(None, parent=self)
        self.SupportAssistEULAAccepted_SupportAssist = EnumTypeField(None,SupportAssistEULAAccepted_SupportAssistTypes, parent=self)
        self.SupportAssistEnableState_SupportAssist = EnumTypeField(None,SupportAssistEnableState_SupportAssistTypes, parent=self)
        self.commit()

class SwitchConnectionView(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SwitchConnectionView", parent)
        self.Enable_SwitchConnectionView = EnumTypeField(None,Enable_SwitchConnectionViewTypes, parent=self)
        self.commit()

class SysInfo(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SysInfo", parent)
        self.AcSysRecovery_SysInfo = StringField(None, parent=self)
        self.BIOSFeature_SysInfo = StringField(None, parent=self)
        self.BIOSStatus_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BladeSlotInfo_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BrdRevision_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CMCIPv6Info_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCIPv6Url_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCInfo_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CMCUrl_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.CPUInfos_SysInfo = StringField(None, parent=self)
        self.EmbeddedNICMAC_SysInfo = StringField(None, parent=self)
        self.FPConfig_SysInfo = StringField(None, parent=self)
        self.FPStatus_SysInfo = StringField(None, parent=self)
        self.FWVersion_SysInfo = StringField(None, parent=self)
        self.GUID_SysInfo = StringField(None, parent=self)
        self.HostNameBinary_SysInfo = StringField(None, parent=self)
        self.ISInfos_SysInfo = StringField(None, parent=self)
        self.LocalConsoleLockOut_SysInfo = IntField(None, parent=self)
        self.OSIPV4_SysInfo = StringField(None, parent=self)
        self.OSIPV6_SysInfo = StringField(None, parent=self)
        self.OSNameBinary_SysInfo = StringField(None, parent=self)
        self.OSNameVolatile_SysInfo = StringField(None, parent=self)
        self.OSVersionBinary_SysInfo = StringField(None, parent=self)
        self.PowerPolicy_SysInfo = StringField(None, parent=self)
        self.RebrandInfo_SysInfo = StringField(None, parent=self)
        self.RedundancyPolicy_SysInfo = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemId_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SystemModel_SysInfo = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SystemRev_SysInfo = IntField(None, parent=self)
        self.iDRACRev_SysInfo = EnumTypeField(None,iDRACRev_SysInfoTypes, parent=self)
        self.commit()

class SysLog(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "SysLog", parent)
        self.Port_SysLog = IntField(None, parent=self)
        self.PowerLogEnable_SysLog = EnumTypeField(None,PowerLogEnable_SysLogTypes, parent=self)
        self.PowerLogInterval_SysLog = IntField(None, parent=self)
        self.Server1_SysLog = StringField(None, parent=self)
        self.Server2_SysLog = StringField(None, parent=self)
        self.Server3_SysLog = StringField(None, parent=self)
        self.SysLogEnable_SysLog = EnumTypeField(None,SysLogEnable_SysLogTypes, parent=self)
        self.Servers = CompositeFieldType(self.Server1_SysLog, self.Server2_SysLog, self.Server3_SysLog)
        self.commit()

class Telnet(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Telnet", parent)
        self.Enable_Telnet = EnumTypeField(None,Enable_TelnetTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_Telnet = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Port_Telnet = IntField(None, parent=self)
        self.Timeout_Telnet = IntField(None, parent=self)
        self.commit()

class ThermalConfig(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ThermalConfig", parent)
        self.CriticalEventGenerationInterval_ThermalConfig = IntField(None, parent=self)
        self.EventGenerationInterval_ThermalConfig = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.FreshAirCompliantConfiguration_ThermalConfig = EnumTypeField(None,FreshAirCompliantConfiguration_ThermalConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RedundancyEnabled_ThermalConfig = EnumTypeField(None,RedundancyEnabled_ThermalConfigTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class ThermalHealthIndicator(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ThermalHealthIndicator", parent)
        self.ID_ThermalHealthIndicator = StringField(None, parent=self)
        self.IndicatorColor_ThermalHealthIndicator = EnumTypeField(None,IndicatorColor_ThermalHealthIndicatorTypes, parent=self)
        self.IndicatorState_ThermalHealthIndicator = EnumTypeField(None,IndicatorState_ThermalHealthIndicatorTypes, parent=self)
        self.commit()

class ThermalHistorical(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ThermalHistorical", parent)
        self.IntervalInSeconds_ThermalHistorical = IntField(None, parent=self)
        self.StartTime_ThermalHistorical = StringField(None, parent=self)
        self.commit()

class ThermalSettings(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ThermalSettings", parent)
        # readonly attribute populated by iDRAC
        self.AirExhaustTempSupport_ThermalSettings = EnumTypeField(None,AirExhaustTempSupport_ThermalSettingsTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.AirExhaustTempValueSet_ThermalSettings = StringField(None, parent=self)
        self.AirExhaustTemp_ThermalSettings = EnumTypeField(None,AirExhaustTemp_ThermalSettingsTypes, parent=self)
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
        # readonly attribute populated by iDRAC
        self.MFSMaximumLimit_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MFSMinimumLimit_ThermalSettings = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MinimumFanSpeed_ThermalSettings = IntField(None, parent=self)
        self.PCIeSlotLFMSupport_ThermalSettings = EnumTypeField(None,PCIeSlotLFMSupport_ThermalSettingsTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.SystemCFMSupport_ThermalSettings = EnumTypeField(None,SystemCFMSupport_ThermalSettingsTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThermalProfileValueSet_ThermalSettings = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ThermalProfile_ThermalSettings = EnumTypeField(None,ThermalProfile_ThermalSettingsTypes, parent=self)
        self.commit()

class ThermalWatermarks(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "ThermalWatermarks", parent)
        # readonly attribute populated by iDRAC
        self.MinTemperatureTimestamp_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MinTemperature_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakTemperatureTimestamp_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PeakTemperature_ThermalWatermarks = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.StartTime_ThermalWatermarks = IntField(None, parent=self)
        self.commit()

class Time(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Time", parent)
        self.DayLightOffset_Time = IntField(None, parent=self)
        self.TimeZoneAbbreviation_Time = StringField(None, parent=self)
        self.TimeZoneOffset_Time = IntField(None, parent=self)
        self.Time_Time = IntField(None, parent=self)
        self.Timezone_Time = StringField(None, parent=self)
        self.commit()

class USB(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "USB", parent)
        self.ConfigurationXML_USB = EnumTypeField(None,ConfigurationXML_USBTypes, parent=self)
        self.HostFrontPortStatus_USB = EnumTypeField(None,HostFrontPortStatus_USBTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.HostFrontPortsDynamicMode_USB = EnumTypeField(None,HostFrontPortsDynamicMode_USBTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ManagementPortMode_USB = EnumTypeField(None,ManagementPortMode_USBTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PortStatus_USB = EnumTypeField(None,PortStatus_USBTypes, parent=self)
        self.ZipPassword_USB = StringField(None, parent=self)
        self.commit()

class Update(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Update", parent)
        self.Begin_Update = EnumTypeField(None,Begin_UpdateTypes, parent=self)
        self.EnableSharedCompUpdate_Update = EnumTypeField(None,EnableSharedCompUpdate_UpdateTypes, parent=self)
        self.FwUpdateIPAddr_Update = StringField(None, parent=self)
        self.FwUpdatePath_Update = StringField(None, parent=self)
        self.FwUpdateTFTPEnable_Update = EnumTypeField(None,FwUpdateTFTPEnable_UpdateTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LastFWUpdate_Update = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Status_Update = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.TFTPTimeout_Update = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class UpdateTask(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "UpdateTask", parent)
        # readonly attribute populated by iDRAC
        self.FwupdatePart_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.LastTaskid_UpdateTask = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PCActiveEC_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PCStandbyEC_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.fwupdateflow_UpdateTask = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class UserDomain(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "UserDomain", parent)
        self.Name_UserDomain = StringField(None, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.Name_UserDomain

    @property
    def Index(self):
        return self.Name_UserDomain._index

class Users(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "Users", parent)
        self.AuthenticationProtocol_Users = EnumTypeField(None,AuthenticationProtocol_UsersTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ETAG_Users = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Enable_Users = EnumTypeField(None,Enable_UsersTypes, parent=self)
        self.IPMIKey_Users = StringField(None, parent=self)
        self.IpmiLanPrivilege_Users = EnumTypeField(None,IpmiLanPrivilege_UsersTypes, parent=self)
        self.IpmiSerialPrivilege_Users = EnumTypeField(None,IpmiSerialPrivilege_UsersTypes, parent=self)
        self.MD5v3Key_Users = StringField(None, parent=self)
        self.Password_Users = StringField(None, parent=self)
        self.PrivacyProtocol_Users = EnumTypeField(None,PrivacyProtocol_UsersTypes, parent=self)
        self.Privilege_Users = EnumTypeField(None,Privilege_UsersTypes, parent=self)
        self.ProtocolEnable_Users = EnumTypeField(None,ProtocolEnable_UsersTypes, parent=self)
        self.SHA1v3Key_Users = StringField(None, parent=self)
        self.SHA256PasswordSalt_Users = StringField(None, parent=self)
        self.SHA256Password_Users = StringField(None, parent=self)
        self.SolEnable_Users = EnumTypeField(None,SolEnable_UsersTypes, parent=self)
        self.UserName_Users = StringField(None, parent=self)
        self.UserPayloadAccess_Users = StringField(None, parent=self)
        self.commit()

    @property
    def Key(self):
        return self.UserName_Users

    @property
    def Index(self):
        return self.UserName_Users._index

class VNCServer(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "VNCServer", parent)
        # readonly attribute populated by iDRAC
        self.ActiveSessions_VNCServer = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Enable_VNCServer = EnumTypeField(None,Enable_VNCServerTypes, parent=self)
        self.LowerEncryptionBitLength_VNCServer = EnumTypeField(None,LowerEncryptionBitLength_VNCServerTypes, parent=self)
        self.MaxSessions_VNCServer = IntField(None, parent=self)
        self.Password_VNCServer = StringField(None, parent=self)
        self.Port_VNCServer = IntField(None, parent=self)
        self.SSLEncryptionBitLength_VNCServer = EnumTypeField(None,SSLEncryptionBitLength_VNCServerTypes, parent=self)
        self.Timeout_VNCServer = IntField(None, parent=self)
        self.commit()

class VirtualConsole(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "VirtualConsole", parent)
        self.AccessPrivilege_VirtualConsole = EnumTypeField(None,AccessPrivilege_VirtualConsoleTypes, parent=self)
        self.AttachState_VirtualConsole = EnumTypeField(None,AttachState_VirtualConsoleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.BSODBootCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BSODBootCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BootCaptureFileCount_VirtualConsole = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.BootCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.BootCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BootCaptureSequence_VirtualConsole = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.CrashVideoCaptureFileName_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CrashVideoCaptureFilePath_VirtualConsole = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.EnableChassisConsoleAccess_VirtualConsole = EnumTypeField(None,EnableChassisConsoleAccess_VirtualConsoleTypes, parent=self)
        self.Enable_VirtualConsole = EnumTypeField(None,Enable_VirtualConsoleTypes, parent=self)
        self.EnabledOnFrontPanel_VirtualConsole = EnumTypeField(None,EnabledOnFrontPanel_VirtualConsoleTypes, parent=self)
        self.EncryptEnable_VirtualConsole = EnumTypeField(None,EncryptEnable_VirtualConsoleTypes, parent=self)
        self.InactivityTimeoutDuration_VirtualConsole = IntField(None, parent=self)
        self.InactivityTimeoutEnable_VirtualConsole = EnumTypeField(None,InactivityTimeoutEnable_VirtualConsoleTypes, parent=self)
        self.LocalDisable_VirtualConsole = EnumTypeField(None,LocalDisable_VirtualConsoleTypes, parent=self)
        self.LocalVideo_VirtualConsole = EnumTypeField(None,LocalVideo_VirtualConsoleTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxBootCaptureFileSize_VirtualConsole = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxSessions_VirtualConsole = IntField(None, parent=self)
        self.PluginType_VirtualConsole = EnumTypeField(None,PluginType_VirtualConsoleTypes, parent=self)
        self.Port_VirtualConsole = IntField(None, parent=self)
        self.Timeout_VirtualConsole = IntField(None, parent=self)
        self.VideoCaptureEnable_VirtualConsole = EnumTypeField(None,VideoCaptureEnable_VirtualConsoleTypes, parent=self)
        self.VideoCaptureFileExtension_VirtualConsole = StringField(None, parent=self)
        self.commit()

class VirtualMedia(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "VirtualMedia", parent)
        self.ActiveSessions_VirtualMedia = IntField(None, parent=self)
        self.Attached_VirtualMedia = EnumTypeField(None,Attached_VirtualMediaTypes, parent=self)
        self.BootOnce_VirtualMedia = EnumTypeField(None,BootOnce_VirtualMediaTypes, parent=self)
        self.EncryptEnable_VirtualMedia = EnumTypeField(None,EncryptEnable_VirtualMediaTypes, parent=self)
        self.FloppyEmulation_VirtualMedia = EnumTypeField(None,FloppyEmulation_VirtualMediaTypes, parent=self)
        self.ImageFileName_VirtualMedia = StringField(None, parent=self)
        self.ImagePath_VirtualMedia = StringField(None, parent=self)
        self.ImageType_VirtualMedia = StringField(None, parent=self)
        self.KeyEnable_VirtualMedia = EnumTypeField(None,KeyEnable_VirtualMediaTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_VirtualMedia = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class WebServer(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "WebServer", parent)
        self.ControlCollaboration_WebServer = IntField(None, parent=self)
        self.ControlVFLoder_WebServer = IntField(None, parent=self)
        self.Enable_WebServer = EnumTypeField(None,Enable_WebServerTypes, parent=self)
        self.HttpPort_WebServer = IntField(None, parent=self)
        self.HttpsPort_WebServer = IntField(None, parent=self)
        self.HttpsRedirection_WebServer = EnumTypeField(None,HttpsRedirection_WebServerTypes, parent=self)
        self.LowerEncryptionBitLength_WebServer = EnumTypeField(None,LowerEncryptionBitLength_WebServerTypes, parent=self)
        self.MaxNumberOfSessions_WebServer = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.MaxSessions_WebServer = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SSLEncryptionBitLength_WebServer = EnumTypeField(None,SSLEncryptionBitLength_WebServerTypes, parent=self)
        self.TLSProtocol_WebServer = EnumTypeField(None,TLSProtocol_WebServerTypes, parent=self)
        self.Timeout_WebServer = IntField(None, parent=self)
        self.TitleBarOptionCustom_WebServer = StringField(None, parent=self)
        self.TitleBarOption_WebServer = EnumTypeField(None,TitleBarOption_WebServerTypes, parent=self)
        self.commit()

class _STP_(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "[STP]", parent)
        self.Enabled_STP = EnumTypeField(None,Enabled_STPTypes, alias="Enabled_[STP]", parent=self)
        self.commit()

class vFlashPartition(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "vFlashPartition", parent)
        self.AccessType_vFlashPartition = EnumTypeField(None,AccessType_vFlashPartitionTypes, parent=self)
        self.AttachState_vFlashPartition = EnumTypeField(None,AttachState_vFlashPartitionTypes, parent=self)
        self.EmulationType_vFlashPartition = EnumTypeField(None,EmulationType_vFlashPartitionTypes, parent=self)
        self.FormatType_vFlashPartition = EnumTypeField(None,FormatType_vFlashPartitionTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.Size_vFlashPartition = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VolumeLabel_vFlashPartition = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit()

class vFlashSD(ClassType):

    def __init__(self, parent = None):
        super().__init__(None, "vFlashSD", parent)
        # readonly attribute populated by iDRAC
        self.AvailableSize_vFlashSD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.Bitmap_vFlashSD = StringField(None, parent=self)
        self.Enable_vFlashSD = EnumTypeField(None,Enable_vFlashSDTypes, parent=self)
        self.Health_vFlashSD = EnumTypeField(None,Health_vFlashSDTypes, parent=self)
        self.Initialized_vFlashSD = EnumTypeField(None,Initialized_vFlashSDTypes, parent=self)
        self.Licensed_vFlashSD = EnumTypeField(None,Licensed_vFlashSDTypes, parent=self)
        self.Presence_vFlashSD = EnumTypeField(None,Presence_vFlashSDTypes, parent=self)
        self.Signature_vFlashSD = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.Size_vFlashSD = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.WriteProtect_vFlashSD = EnumTypeField(None,WriteProtect_vFlashSDTypes, parent=self)
        self.commit()

class LifecycleController(ClassType):

    def __init__(self, parent = None):
        super().__init__("Component", None, parent)
        self.LCAttributes = LCAttributes(parent=self)
        self.commit()

class System(ClassType):

    def __init__(self, parent = None):
        super().__init__("Component", None, parent)
        self.LCD = LCD(parent=self)
        self.ServerOS = ServerOS(parent=self)
        self.ServerPwr = ServerPwr(parent=self)
        self.ServerTopology = ServerTopology(parent=self)
        self.ThermalConfig = ThermalConfig(parent=self)
        self.commit()

class iDRAC(ClassType):

    def __init__(self, parent = None):
        super().__init__("Component", None, parent)
        self.ADGroup = ArrayType(ADGroup, parent=self, min_index=1, max_index=5)
        self.ASRConfig = ASRConfig(parent=self)
        self.ActiveDirectory = ActiveDirectory(parent=self)
        self.AutoBackup = AutoBackup(parent=self)
        self.AutoOSLockGroup = AutoOSLockGroup(parent=self)
        self.AutoUpdate = AutoUpdate(parent=self)
        self.Backplane = Backplane(parent=self)
        self.BoardPowerConsumption = BoardPowerConsumption(parent=self)
        self.Branding = Branding(parent=self)
        self.ButtonLCP = ButtonLCP(parent=self)
        self.ButtonRCP = ButtonRCP(parent=self)
        self.CMC = CMC(parent=self)
        self.CMCSNMPAlert = CMCSNMPAlert(parent=self)
        self.CMCSNMPTrapIPv6 = CMCSNMPTrapIPv6(parent=self)
        self.CMCSlot = CMCSlot(parent=self)
        self.Certificate = Certificate(parent=self)
        self.ChassisControl = ChassisControl(parent=self)
        self.ChassisHealthIndicator = ChassisHealthIndicator(parent=self)
        self.ChassisInfo = ChassisInfo(parent=self)
        self.ChassisPower = ChassisPower(parent=self)
        self.ChassisPwrState = ChassisPwrState(parent=self)
        self.ChassisTopology = ChassisTopology(parent=self)
        self.CurrentIPv4 = CurrentIPv4(parent=self)
        self.CurrentIPv6 = CurrentIPv6(parent=self)
        self.CurrentNIC = CurrentNIC(parent=self)
        self.DCMIThermal = DCMIThermal(parent=self)
        self.DCSCustom = DCSCustom(parent=self)
        self.DCSResetCtlr = DCSResetCtlr(parent=self)
        self.DIMMInfo = DIMMInfo(parent=self)
        self.DefaultCredentialMitigationConfigGroup = DefaultCredentialMitigationConfigGroup(parent=self)
        self.DefaultFactoryPassword = DefaultFactoryPassword(parent=self)
        self.Diagnostics = Diagnostics(parent=self)
        self.EC = EC(parent=self)
        self.EmailAlert = ArrayType(EmailAlert, parent=self, min_index=1, max_index=4)
        self.FPGAFWInventory = FPGAFWInventory(parent=self)
        self.FReDFWInventory = FReDFWInventory(parent=self)
        self.FWInventory = FWInventory(parent=self)
        self.FWUpdateService = FWUpdateService(parent=self)
        self.FWUpdateTask = FWUpdateTask(parent=self)
        self.FanSlot = FanSlot(parent=self)
        self.FrontPanel = FrontPanel(parent=self)
        self.GBE = GBE(parent=self)
        self.GUI = GUI(parent=self)
        self.GpGPUTable = GpGPUTable(parent=self)
        self.GroupManager = GroupManager(parent=self)
        self.IOIDOpt = IOIDOpt(parent=self)
        self.IOMInterposer = IOMInterposer(parent=self)
        self.IOMSlot = IOMSlot(parent=self)
        self.IOMSlotConfig = IOMSlotConfig(parent=self)
        self.IPBlocking = IPBlocking(parent=self)
        self.IPMIChassisData = IPMIChassisData(parent=self)
        self.IPMIFireWall = IPMIFireWall(parent=self)
        self.IPMIFireWallChannel = IPMIFireWallChannel(parent=self)
        self.IPMIIPConfig = IPMIIPConfig(parent=self)
        self.IPMILANConfig = IPMILANConfig(parent=self)
        self.IPMILANPEFConfig = IPMILANPEFConfig(parent=self)
        self.IPMILan = IPMILan(parent=self)
        self.IPMIPEFSeldomFilter = IPMIPEFSeldomFilter(parent=self)
        self.IPMIPefOften = IPMIPefOften(parent=self)
        self.IPMIPefSeldom = IPMIPefSeldom(parent=self)
        self.IPMIPefSeldomAlerts = IPMIPefSeldomAlerts(parent=self)
        self.IPMIPowerManagement = IPMIPowerManagement(parent=self)
        self.IPMISDR = IPMISDR(parent=self)
        self.IPMISEL = IPMISEL(parent=self)
        self.IPMISOL = IPMISOL(parent=self)
        self.IPMISerial = IPMISerial(parent=self)
        self.IPMISystemParameter = IPMISystemParameter(parent=self)
        self.IPMIUserEncryptIVKey = IPMIUserEncryptIVKey(parent=self)
        self.IPMIUserInfo = IPMIUserInfo(parent=self)
        self.IPv4 = IPv4(parent=self)
        self.IPv4Static = IPv4Static(parent=self)
        self.IPv6 = IPv6(parent=self)
        self.IPv6Static = IPv6Static(parent=self)
        self.IPv6URL = IPv6URL(parent=self)
        self.IdentifyButton = IdentifyButton(parent=self)
        self.IndicatorLCP = IndicatorLCP(parent=self)
        self.Info = Info(parent=self)
        self.InletTemp = InletTemp(parent=self)
        self.IntegratedDatacenter = IntegratedDatacenter(parent=self)
        self.LCAttributes = LCAttributes(parent=self)
        self.LDAP = LDAP(parent=self)
        self.LDAPRoleGroup = ArrayType(LDAPRoleGroup, parent=self, min_index=1, max_index=5)
        self.LocalSecurity = LocalSecurity(parent=self)
        self.Lockdown = Lockdown(parent=self)
        self.Logging = Logging(parent=self)
        self.MSM = MSM(parent=self)
        self.MSMConfigBackup = MSMConfigBackup(parent=self)
        self.MSMSNMPAlert = MSMSNMPAlert(parent=self)
        self.MSMSNMPTrapIPv4 = MSMSNMPTrapIPv4(parent=self)
        self.MSMSNMPTrapIPv6 = MSMSNMPTrapIPv6(parent=self)
        self.MachineTrust = MachineTrust(parent=self)
        self.MgmtNetworkInterface = MgmtNetworkInterface(parent=self)
        self.NIC = NIC(parent=self)
        self.NICStatic = NICStatic(parent=self)
        self.NTPConfigGroup = NTPConfigGroup(parent=self)
        self.OS_BMC = OS_BMC(parent=self)
        self.PCIeSlotLFM = PCIeSlotLFM(parent=self)
        self.PMLicensing = PMLicensing(parent=self)
        self.PSUSlot = PSUSlot(parent=self)
        self.PSUSlotSeq = PSUSlotSeq(parent=self)
        self.PlatformCapability = PlatformCapability(parent=self)
        self.PlatformLicense = PlatformLicense(parent=self)
        self.PowerButton = PowerButton(parent=self)
        self.PowerHealthIndicator = PowerHealthIndicator(parent=self)
        self.PowerHistorical = PowerHistorical(parent=self)
        self.PrivateStore = PrivateStore(parent=self)
        self.ProfileTask = ProfileTask(parent=self)
        self.QuickSync = QuickSync(parent=self)
        self.RFS = RFS(parent=self)
        self.RSM = RSM(parent=self)
        self.RSM_ = RSM_(parent=self)
        self.Racadm = Racadm(parent=self)
        self.Racadm_ = Racadm_(parent=self)
        self.Redfish = Redfish(parent=self)
        self.RedfishEventing = RedfishEventing(parent=self)
        self.Redundancy = Redundancy(parent=self)
        self.RemoteHosts = RemoteHosts(parent=self)
        self.SATAInventory = SATAInventory(parent=self)
        self.SC_BMC = SC_BMC(parent=self)
        self.SECONDARYNIC = SECONDARYNIC(parent=self)
        self.SNMP = SNMP(parent=self)
        self.SNMPAlert = ArrayType(SNMPAlert, parent=self, min_index=1, max_index=8)
        self.SNMPTrapIPv4 = SNMPTrapIPv4(parent=self)
        self.SNMPTrapIPv6 = SNMPTrapIPv6(parent=self)
        self.SSH = SSH(parent=self)
        self.SecureDefaultPassword = SecureDefaultPassword(parent=self)
        self.Security = Security(parent=self)
        self.SecurityCSC = SecurityCSC(parent=self)
        self.SecuritySSL = SecuritySSL(parent=self)
        self.Sensor = Sensor(parent=self)
        self.SensorThresholds = SensorThresholds(parent=self)
        self.Serial = Serial(parent=self)
        self.SerialRedirection = SerialRedirection(parent=self)
        self.ServerBoot = ServerBoot(parent=self)
        self.ServerInfo = ServerInfo(parent=self)
        self.ServerPwrMon = ServerPwrMon(parent=self)
        self.ServiceModule = ServiceModule(parent=self)
        self.SledInterposer = SledInterposer(parent=self)
        self.SledSlot = SledSlot(parent=self)
        self.SlotConfig = SlotConfig(parent=self)
        self.SmartCard = SmartCard(parent=self)
        self.Storage = Storage(parent=self)
        self.SupportAssist = SupportAssist(parent=self)
        self.SwitchConnectionView = SwitchConnectionView(parent=self)
        self.SysInfo = SysInfo(parent=self)
        self.SysLog = SysLog(parent=self)
        self.Telnet = Telnet(parent=self)
        self.ThermalHealthIndicator = ThermalHealthIndicator(parent=self)
        self.ThermalHistorical = ThermalHistorical(parent=self)
        self.ThermalSettings = ThermalSettings(parent=self)
        self.ThermalWatermarks = ThermalWatermarks(parent=self)
        self.Time = Time(parent=self)
        self.USB = USB(parent=self)
        self.Update = Update(parent=self)
        self.UpdateTask = UpdateTask(parent=self)
        self.UserDomain = ArrayType(UserDomain, parent=self, min_index=1, max_index=40)
        self.Users = ArrayType(Users, parent=self, min_index=1, max_index=16)
        self.VNCServer = VNCServer(parent=self)
        self.VirtualConsole = VirtualConsole(parent=self)
        self.VirtualMedia = VirtualMedia(parent=self)
        self.WebServer = WebServer(parent=self)
        self._STP_ = _STP_(parent=self)
        self.vFlashPartition = vFlashPartition(parent=self)
        self.vFlashSD = vFlashSD(parent=self)
        self.commit()

