from omdrivers.enums.iDRAC.NIC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import logging

logger = logging.getLogger(__name__)

class NIC(ClassType):

    def __init__(self, parent = None):
        super().__init__("Component", None, parent)
        # readonly attribute populated by iDRAC
        self.AddressingMode = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.BannerMessageTimeout = IntField(None, parent=self)
        self.BlnkLeds = IntField("15", parent=self)
        self.BootOptionROM = EnumTypeField(None,BootOptionROMTypes, parent=self)
        self.BootOrderFirstFCoETarget = IntField("0", parent=self)
        self.BootOrderFourthFCoETarget = IntField("0", parent=self)
        self.BootOrderSecondFCoETarget = IntField("0", parent=self)
        self.BootOrderThirdFCoETarget = IntField("0", parent=self)
        self.BootRetryCnt = EnumTypeField(BootRetryCntTypes.NoRetry,BootRetryCntTypes, parent=self)
        self.BootStrapType = EnumTypeField(BootStrapTypeTypes.AutoDetect,BootStrapTypeTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.BusDeviceFunction = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ChapAuthEnable = EnumTypeField(ChapAuthEnableTypes.Disabled,ChapAuthEnableTypes, parent=self)
        self.ChapMutualAuth = EnumTypeField(ChapMutualAuthTypes.Disabled,ChapMutualAuthTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ChipMdl = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConfigureLogicalPortsSupport = EnumTypeField(ConfigureLogicalPortsSupportTypes.Unavailable,ConfigureLogicalPortsSupportTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.CongestionNotification = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectEighteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectEighthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectEleventhFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectFifteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectFifthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ConnectFirstFCoETarget = EnumTypeField(ConnectFirstFCoETargetTypes.Disabled,ConnectFirstFCoETargetTypes, parent=self)
        self.ConnectFirstTgt = EnumTypeField(ConnectFirstTgtTypes.Disabled,ConnectFirstTgtTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ConnectFourteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectFourthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectNineteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectNinthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectSecondFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.ConnectSecondTgt = EnumTypeField(ConnectSecondTgtTypes.Disabled,ConnectSecondTgtTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.ConnectSeventeenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectSeventhFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectSixteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectSixthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectThirdFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectThirteenthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectThirtyFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectThirtyFirstFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectThirtySecondFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwelfthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentiethFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyEighthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyFifthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyFirstFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyFourthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyNinthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentySecondFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentySeventhFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentySixthFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ConnectTwentyThirdFCoETarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ControllerBIOSVersion = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DCBXSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceName = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.DhcpVendId = StringField(None, parent=self)
        self.EEEControl = EnumTypeField(EEEControlTypes.varies,EEEControlTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.EFIVersion = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EVBModesSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EighteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EighteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EighthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EighthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EleventhFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EleventhFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EnergyEfficientEthernet = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.EnhancedTransmissionSelection = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FCoEBootScanSelection = EnumTypeField(FCoEBootScanSelectionTypes.Disabled,FCoEBootScanSelectionTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FCoEBootSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FCoEFabricDiscoveryRetryCnt = IntField(None, parent=self)
        self.FCoEFirstHddTarget = EnumTypeField(FCoEFirstHddTargetTypes.Disabled,FCoEFirstHddTargetTypes, parent=self)
        self.FCoELnkUpDelayTime = IntField(None, parent=self)
        self.FCoELunBusyRetryCnt = IntField(None, parent=self)
        self.FCoEOffloadMode = EnumTypeField(FCoEOffloadModeTypes.Disabled,FCoEOffloadModeTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FCoEOffloadSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FCoETgtBoot = EnumTypeField(FCoETgtBootTypes.Disabled,FCoETgtBootTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FIPMacAddr = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FamilyVersion = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FeatureLicensingSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FifteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FifteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FifthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FifthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FirstFCoEBootTargetLUN = IntField(None, parent=self)
        self.FirstFCoEFCFVLANID = IntField(None, parent=self)
        self.FirstFCoEWWPNTarget = StringField(None, parent=self)
        self.FirstHddTarget = EnumTypeField(FirstHddTargetTypes.Disabled,FirstHddTargetTypes, parent=self)
        self.FirstTgtBootLun = IntField(None, parent=self)
        self.FirstTgtChapId = StringField(None, parent=self)
        self.FirstTgtChapPwd = StringField(None, parent=self)
        self.FirstTgtIpAddress = StringField(None, parent=self)
        self.FirstTgtIpVer = EnumTypeField(FirstTgtIpVerTypes.IPv4,FirstTgtIpVerTypes, parent=self)
        self.FirstTgtIscsiName = StringField(None, parent=self)
        self.FirstTgtTcpPort = IntField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.FlexAddressing = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FlowControlSetting = EnumTypeField(FlowControlSettingTypes.Auto,FlowControlSettingTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.FourteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FourteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FourthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.FourthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.HairpinMode = EnumTypeField(HairpinModeTypes.Disabled,HairpinModeTypes, parent=self)
        self.HideSetupPrompt = EnumTypeField(HideSetupPromptTypes.Disabled,HideSetupPromptTypes, parent=self)
        self.IpAutoConfig = EnumTypeField(IpAutoConfigTypes.Disabled,IpAutoConfigTypes, parent=self)
        self.IpVer = EnumTypeField(IpVerTypes.IPv4,IpVerTypes, parent=self)
        self.IscsiInitiatorChapId = StringField(None, parent=self)
        self.IscsiInitiatorChapPwd = StringField(None, parent=self)
        self.IscsiInitiatorGateway = StringField(None, parent=self)
        self.IscsiInitiatorIpAddr = StringField(None, parent=self)
        self.IscsiInitiatorIpv4Addr = StringField(None, parent=self)
        self.IscsiInitiatorIpv4Gateway = StringField(None, parent=self)
        self.IscsiInitiatorIpv4PrimDns = StringField(None, parent=self)
        self.IscsiInitiatorIpv4SecDns = StringField(None, parent=self)
        self.IscsiInitiatorIpv6Addr = StringField(None, parent=self)
        self.IscsiInitiatorIpv6Gateway = StringField(None, parent=self)
        self.IscsiInitiatorIpv6PrimDns = StringField(None, parent=self)
        self.IscsiInitiatorIpv6SecDns = StringField(None, parent=self)
        self.IscsiInitiatorName = StringField(None, parent=self)
        self.IscsiInitiatorPrimDns = StringField(None, parent=self)
        self.IscsiInitiatorSecDns = StringField(None, parent=self)
        self.IscsiInitiatorSubnet = StringField(None, parent=self)
        self.IscsiInitiatorSubnetPrefix = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.IscsiMacAddr = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.IscsiTgtBoot = EnumTypeField(IscsiTgtBootTypes.Disabled,IscsiTgtBootTypes, parent=self)
        self.IscsiVLanId = IntField(None, parent=self)
        self.IscsiVLanMode = EnumTypeField(IscsiVLanModeTypes.Disabled,IscsiVLanModeTypes, parent=self)
        self.IscsiViaDHCP = EnumTypeField(IscsiViaDHCPTypes.Disabled,IscsiViaDHCPTypes, parent=self)
        self.LegacyBootProto = EnumTypeField(LegacyBootProtoTypes.varies,LegacyBootProtoTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.LinkStatus = EnumTypeField(None,LinkStatusTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.LnkSpeed = EnumTypeField(None,LnkSpeedTypes, parent=self)
        self.LnkUpDelayTime = IntField("0", parent=self)
        self.LocalDCBXWillingMode = EnumTypeField(LocalDCBXWillingModeTypes.Enabled,LocalDCBXWillingModeTypes, parent=self)
        self.LogicalPortEnable = EnumTypeField(LogicalPortEnableTypes.Disabled,LogicalPortEnableTypes, parent=self)
        self.LunBusyRetryCnt = IntField(None, parent=self)
        self.MTUParams = EnumTypeField(None,MTUParamsTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.MTUReconfigurationSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MacAddr = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MaxBandwidth = IntField("100", parent=self)
        # readonly attribute populated by iDRAC
        self.MaxFrameSize = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxIOsPerSession = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNPIVPerPort = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumberExchanges = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumberLogins = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumberOfFCTargets = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MaxNumberOutStandingCommands = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.MaxNumberVFSupportedByDevice = IntField("0", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.MgmtSVID = IntField("1000", parent=self, modifyAllowed = False, deleteAllowed = False)
        self.MinBandwidth = IntField("0", parent=self)
        self.NPCP = EnumTypeField(NPCPTypes.Enabled,NPCPTypes, parent=self)
        self.NParEP = EnumTypeField(NParEPTypes.Disabled,NParEPTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NWManagementPassThrough = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NetworkPartitioningMode = EnumTypeField(NetworkPartitioningModeTypes.SIP,NetworkPartitioningModeTypes, parent=self)
        self.NicMode = EnumTypeField(NicModeTypes.Varies,NicModeTypes, parent=self)
        self.NicPartitioning = EnumTypeField(NicPartitioningTypes.Disabled,NicPartitioningTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.NicPartitioningSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NineteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NineteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NinthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NinthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NumberPCIFunctionsEnabled = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.NumberPCIFunctionsSupported = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.NumberVFAdvertised = IntField("0", parent=self)
        # readonly attribute populated by iDRAC
        self.NumberVFSupported = IntField("0", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.OSBMCManagementPassThrough = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.OnChipThermalSensor = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PCIDeviceID = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PXEBootSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.PartitionStateInterpretation = EnumTypeField(None,PartitionStateInterpretationTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.PriorityFlowControl = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PriorityGroup0BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup0ProtocolAssignment = EnumTypeField(None,PriorityGroup0ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup15BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup15ProtocolAssignment = EnumTypeField(None,PriorityGroup15ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup1BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup1ProtocolAssignment = EnumTypeField(None,PriorityGroup1ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup2BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup2ProtocolAssignment = EnumTypeField(None,PriorityGroup2ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup3BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup3ProtocolAssignment = EnumTypeField(None,PriorityGroup3ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup4BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup4ProtocolAssignment = EnumTypeField(None,PriorityGroup4ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup5BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup5ProtocolAssignment = EnumTypeField(None,PriorityGroup5ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup6BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup6ProtocolAssignment = EnumTypeField(None,PriorityGroup6ProtocolAssignmentTypes, parent=self)
        self.PriorityGroup7BandwidthAllocation = IntField(None, parent=self)
        self.PriorityGroup7ProtocolAssignment = EnumTypeField(None,PriorityGroup7ProtocolAssignmentTypes, parent=self)
        self.PriorityGroupBandwidthAllocation = IntField(None, parent=self)
        self.RDMAApplicationProfile = EnumTypeField(None,RDMAApplicationProfileTypes, parent=self)
        self.RDMANICModeOnPort = EnumTypeField(RDMANICModeOnPortTypes.Varies,RDMANICModeOnPortTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.RDMAProtocolSupport = EnumTypeField(None,RDMAProtocolSupportTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RDMASupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RXFlowControl = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.RemotePHY = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SRIOVSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SecondFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SecondFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.SecondTgtBootLun = IntField(None, parent=self)
        self.SecondTgtChapId = StringField(None, parent=self)
        self.SecondTgtChapPwd = StringField(None, parent=self)
        self.SecondTgtIpAddress = StringField(None, parent=self)
        self.SecondTgtIpVer = EnumTypeField(SecondTgtIpVerTypes.IPv4,SecondTgtIpVerTypes, parent=self)
        self.SecondTgtIscsiName = StringField(None, parent=self)
        self.SecondTgtTcpPort = IntField(None, parent=self)
        self.SecondaryDeviceMacAddr = StringField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.SeventeenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SeventeenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SeventhFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SeventhFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SixteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SixteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SixthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SixthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.SwitchDepPartitioningSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TOESupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TXBandwidthControlMaximum = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TXBandwidthControlMinimum = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TXFlowControl = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TcpIpViaDHCP = EnumTypeField(TcpIpViaDHCPTypes.Disabled,TcpIpViaDHCPTypes, parent=self)
        self.TcpTimestmp = EnumTypeField(TcpTimestmpTypes.Disabled,TcpTimestmpTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.TenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirdFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirdFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirteenthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirteenthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtyFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtyFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtyFirstFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtyFirstFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtySecondFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.ThirtySecondFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.TotalNumberLogicalPorts = EnumTypeField(TotalNumberLogicalPortsTypes.T_2,TotalNumberLogicalPortsTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.TwelfthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwelfthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentiethFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentiethFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyEighthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyEighthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFifthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFifthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFirstFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFirstFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFourthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyFourthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyNinthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyNinthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySecondFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySecondFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySeventhFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySeventhFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySixthFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentySixthFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyThirdFCoEBootTargetLUN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.TwentyThirdFCoEWWPNTarget = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.UseIndTgtName = EnumTypeField(UseIndTgtNameTypes.Disabled,UseIndTgtNameTypes, parent=self)
        self.UseIndTgtPortal = EnumTypeField(UseIndTgtPortalTypes.Disabled,UseIndTgtPortalTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.VFAllocBasis = EnumTypeField(None,VFAllocBasisTypes, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.VFAllocMult = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.VFDistribution = StringField(None, parent=self)
        self.VLanId = IntField(None, parent=self)
        self.VLanMode = EnumTypeField(VLanModeTypes.Disabled,VLanModeTypes, parent=self)
        self.VirtFIPMacAddr = StringField("00:00:00:00:00:00", parent=self)
        self.VirtIscsiMacAddr = StringField("00:00:00:00:00:00", parent=self)
        self.VirtMacAddr = StringField("00:00:00:00:00:00", parent=self)
        self.VirtWWN = StringField("00:00:00:00:00:00:00:00", parent=self)
        self.VirtWWPN = StringField("00:00:00:00:00:00:00:00", parent=self)
        self.VirtualizationMode = EnumTypeField(VirtualizationModeTypes.NONE,VirtualizationModeTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.WWN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.WWPN = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.WakeOnLan = EnumTypeField(None,WakeOnLanTypes, parent=self)
        self.WakeOnLanLnkSpeed = EnumTypeField(WakeOnLanLnkSpeedTypes.AutoNeg,WakeOnLanLnkSpeedTypes, parent=self)
        self.WinHbaBootMode = EnumTypeField(WinHbaBootModeTypes.Disabled,WinHbaBootModeTypes, parent=self)
        # readonly attribute populated by iDRAC
        self.iSCSIBootSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.iSCSIDualIPVersionSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.iSCSIOffloadSupport = StringField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.iScsiOffloadMode = EnumTypeField(iScsiOffloadModeTypes.Disabled,iScsiOffloadModeTypes, parent=self)
        self.commit()

