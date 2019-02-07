from enum import Enum
from omsdk.sdkdevice import iDeviceDiscovery, iDeviceRegistry, iDeviceDriver
from omsdk.sdkcenum import EnumWrapper
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkproto import PSNMP
import sys
import logging


logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto import rfc1902
    from pysnmp import debug
    PyPSNMP = True
except ImportError:
    PyPSNMP = False

try:
    from omdrivers.lifecycle.F10.F10Config import F10Config
    from omdrivers.lifecycle.F10.F10Config import F10SNMPCmds
    from omdrivers.lifecycle.F10.F10Config import ConfigFileTypeEnum
    Pyconfig_mgr = True
except ImportError:
    Pyconfig_mgr = False

class NoConfig:
    def __init__(self, obj):
        logger.debug("not implemented")

if not Pyconfig_mgr:
    F10Config = NoConfig
if not Pyconfig_mgr and PyPSNMP:
    F10PSNMPCmds = {}

F10CompEnum = EnumWrapper('F10CompEnum', {
    "System" : "System",
    "dellNetFanTray" : "dellNetFanTray",
    "dellNetPEBinding" : "dellNetPEBinding",
    "dellNetCard" : "dellNetCard",
    "dellNetChassis" : "dellNetChassis",
    "dellNetPowerSupply" : "dellNetPowerSupply",
    "dellNetFlash" : "dellNetFlash",
    "dellNetSwModule" : "dellNetSwModule",
#    "dellNetSysIf" : "dellNetSysIf",
    "dellNetStackPort" : "dellNetStackPort",
    "dellNetSysCores" : "dellNetSysCores",
    "dellNetStackUnit" : "dellNetStackUnit",
    "dellNetCpuUtil" : "dellNetCpuUtil",
    "dellNetPE" : "dellNetPE",
    "dellNetProcessor" : "dellNetProcessor",
}).enum_type

if PyPSNMP:
    F10PSNMPViews = {
     F10CompEnum.System : {
         'SysObjectID' : ObjectIdentity('SNMPv2-MIB', 'sysObjectID')
     },
     F10CompEnum.dellNetFanTray : {
       'FQDD' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.3"),
       'dellNetFanDeviceIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.2"),
       'PiecePartID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.5"),
       'dellNetFanDeviceType' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.1"),
       'ExpressServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.8"),
       'PPIDRevision' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.6"),
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.7"),
       'OperStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.7.1.4"),
     },
     F10CompEnum.dellNetPEBinding : {
       'dellNetPEBindPEIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.1.1.2"),
       'dellNetPEBindCascadePortIfIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.1.1.1"),
     },
     F10CompEnum.dellNetCard : {
       'PartNum' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.9"),
       'NumOfPorts' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.17"),
       'Type' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.2"),
       'MfgDate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.8"),
       'Status' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.5"),
       'ProductRev' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.10"),
       'VendorId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.7"),
       'CountryCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.12"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.1"),
       'Description' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.3"),
       'PPIDRevision' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.14"),
       'ChassisIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.4"),
       'PiecePartID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.13"),
       'ProductOrder' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.11"),
       'ExpServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.16"),
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.15"),
       'Temp' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.4.1.6"),
     },
     F10CompEnum.dellNetChassis : {
       'MfgDate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.8"),
       'ExpServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.12"),
       'NumSlots' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.13"),
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.11"),
       'PPIDRev' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.10"),
       'CountryCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.9"),
       'PartNum' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.5"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.1"),
       'NumPowerSupplies' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.16"),
       'NumLineCardSlots' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.14"),
       'NumFanTrays' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.15"),
       'Type' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.2"),
       'ProductRev' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.6"),
       'VendorId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.7"),
       'MacAddr' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.3"),
       'SerialNumber' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.2.3.1.4"),
     },
     F10CompEnum.dellNetPowerSupply : {
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.8"),
       'OperStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.4"),
       'FQDD' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.3"),
       'dellNetPowerDeviceType' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.1"),
       'PiecePartID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.6"),
       'ExpressServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.9"),
       'Type' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.5"),
       'dellNetPowerDeviceIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.2"),
       'Usage' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.10"),
       'PPIDRevision' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.6.1.7"),
     },
     F10CompEnum.dellNetFlash : {
       'PartitionFree' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.5"),
       'PartitionNumber' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.1"),
       'PartitionSize' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.3"),
       'FQDD' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.2"),
       'PartitionMountPoint' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.6"),
       'PartitionUsed' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.8.1.4"),
     },
     F10CompEnum.dellNetSwModule : {
       'BootSelectorImgVersion' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.4"),
       'NextRebootImage' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.5"),
       'BootFlashImgVersion' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.3"),
       'CurrentBootImage' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.6"),
       'RuntimeImgDate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.2"),
       'RuntimeImgVersion' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.1"),
       'InPartitionAImgVers' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.7"),
       'InPartitionBImgVers' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.5.1.8"),
     },
     "dellNetSysIf" : {
       'Type' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.1"),
       'XfpRecvPower' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.5"),
       'OperStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.4"),
       'AdminStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.3"),
       'XfpTxPower' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.7"),
       'XfpRecvTemp' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.6"),
       'Name' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.10.1.2"),
     },
     F10CompEnum.dellNetStackPort : {
       'ConfiguredMode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.2"),
       'RunningMode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.3"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.1"),
       'LinkSpeed' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.5"),
       'RxTotalErrors' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.8"),
       'TxDataRate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.9"),
       'RxErrorRate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.7"),
       'TxTotalErrors' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.11"),
       'RxDataRate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.6"),
       'TxErrorRate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.10"),
       'LinkStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.5.1.4"),
     },
     F10CompEnum.dellNetSysCores : {
       'StackUnitNumber' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.9.1.4"),
       'FileName' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.9.1.2"),
       'Instance' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.9.1.1"),
       'TimeCreated' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.9.1.3"),
       'Process' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.9.1.5"),
     },
     F10CompEnum.dellNetStackUnit : {
       'ProductOrder' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.19"),
       'VendorId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.14"),
       'MgmtStatus' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.4"),
       'MacAddress' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.16"),
       'MfgDate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.15"),
       'Status' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.8"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.2"),
       'Number' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.1"),
       'CountryCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.20"),
       'PPIDRevision' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.22"),
       'AdmMgmtPreference' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.6"),
       'Description' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.9"),
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.23"),
       'NumPluggableModules' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.28"),
       'ModelId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.7"),
       'PartNum' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.17"),
       'NumOfPorts' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.25"),
       'HwMgmtPreference' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.5"),
       'NumFanTrays' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.26"),
       'UpTime' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.12"),
       'CodeVersion' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.10"),
       'ProductRev' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.18"),
       'IOMMode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.29"),
       'PiecePartID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.21"),
       'ExpServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.24"),
       'Temp' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.13"),
       'NumPowerSupplies' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.27"),
       'BladeSlotId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.30"),
       'SerialNumber' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.3.4.1.11"),
     },
     F10CompEnum.dellNetCpuUtil : {
       'dellNetCpuFlashUsage' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.4.1.7"),
       'MemUsage' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.4.1.6"),
       '5Min' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.4.1.5"),
       '5Sec' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.4.1.1"),
       '1Min' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.4.1.4"),
     },
     F10CompEnum.dellNetPE : {
       'VendorId' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.8"),
       'Description' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.5"),
       'PEID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.2"),
       'PiecePartID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.14"),
       'CountryCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.13"),
       'UnitID' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.3"),
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.16"),
       'PartNum' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.10"),
       'ExpServiceCode' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.17"),
       'NumPowerSupplies' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.20"),
       'MfgDate' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.9"),
       'NumPluggableModules' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.21"),
       'Temp' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.7"),
       'Status' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.6"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.1"),
       'PPIDRevision' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.15"),
       'ProductRev' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.11"),
       'NumFanTrays' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.19"),
       'Type' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.4"),
       'NumOfPorts' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.18"),
       'ProductOrder' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.2.1.12"),
     },
     F10CompEnum.dellNetProcessor : {
       'DeviceType' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.1"),
       'Module' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.4"),
       'DeviceIndex' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.2"),
       'UpTime' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.5"),
       'MemSize' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.6"),
       'Index' : ObjectIdentity("1.3.6.1.4.1.6027.3.26.1.4.3.1.3"),
     },
    }
    F10PSNMPClassifier = {
        F10CompEnum.System : {
            'SysObjectID' : 'SNMPv2-SMI::enterprises\\.6027'
        }
    }
else:
    F10PSNMPViews = {}
    F10PSNMPClassifier = {}

F10ComponentTree = {
    "Full" : [
        F10CompEnum.System,
        F10CompEnum.dellNetSwModule,
        F10CompEnum.dellNetStackUnit,
#    "dellNetSysIf" : "dellNetSysIf",
        F10CompEnum.dellNetPE,
        F10CompEnum.dellNetFanTray,
        F10CompEnum.dellNetStackPort,
        F10CompEnum.dellNetChassis,
        F10CompEnum.dellNetPowerSupply,
        F10CompEnum.dellNetProcessor,
        F10CompEnum.dellNetFlash,
        F10CompEnum.dellNetCard,
        F10CompEnum.dellNetSysCores,
        F10CompEnum.dellNetPEBinding,
        F10CompEnum.dellNetCpuUtil,
    ],
}

F10Classifier = [ F10CompEnum.System ]

class F10(iDeviceDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(F10, self).__init__(iDeviceRegistry("F10", srcdir, F10CompEnum))
        else:
            super().__init__(iDeviceRegistry("F10", srcdir, F10CompEnum))
        if PyPSNMP:
            self.protofactory.add(PSNMP(
                views = F10PSNMPViews,
                classifier = F10PSNMPClassifier,
                cmds = F10SNMPCmds))
        self.protofactory.addCTree(F10ComponentTree)
        self.protofactory.addClassifier(F10Classifier)

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return F10Entity(self.ref, protofactory, ipaddr, creds)

class F10Entity(iDeviceDriver):
    def __init__(self, ref, protofactory, ipaddr, creds):
        if PY2:
            super(F10Entity, self).__init__(ref, protofactory, ipaddr, creds)
        else:
            super().__init__(ref, protofactory, ipaddr, creds)

        if Pyconfig_mgr:
            self.config_mgr = F10Config(self)
        self.supports_entity_mib = True

    def _isin(self, parentClsName, parent, childClsName, child):
        if 'MyPos' in parent:
            return parent['MyPos'] == child['ContainedIn']
        else:
            return self._get_obj_index(parentClsName, parent) in \
                   self._get_obj_index(childClsName, child)
