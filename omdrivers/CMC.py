from enum import Enum
from omsdk.sdkdevice import iDeviceRegistry, iDeviceDriver, iDeviceDiscovery
from omsdk.sdkdevice import iDeviceTopologyInfo
from omsdk.sdkproto import PWSMAN
from omsdk.sdkcenum import EnumWrapper
from omsdk.sdkprint import PrettyPrint
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# MessageID, Message
CMCCompEnum = EnumWrapper("CMCCompEnum", {
    "System" : "System",
    "ComputeModule" : "ComputeModule",
    "StorageModule" : "StorageModule",
    "IOModule" : "IOModule",
    "Fan" : "Fan",
    "CMC" : "CMC",
    "PowerSupply" : "PowerSupply",
    "Controller" : "Controller",
    "Enclosure" : "Enclosure",
    "EnclosureEMM" : "EnclosureEMM",
    "EnclosurePSU" : "EnclosurePSU",
    "PCIDevice" : "PCIDevice",
    "ControllerBattery" : "ControllerBattery" ,
    "VirtualDisk" : "VirtualDisk",
    "PhysicalDisk" : "PhysicalDisk",
    "KVM" : "KVM",
    }).enum_type

CMCMiscEnum = EnumWrapper("CMCMiscEnum", {
    "PassThroughModule" : "PassThroughModule",
    "PSPackage" : "PSPackage",
    "PSSlot" : "PSSlot",
    "PCISlot" : "PCISlot",
    "FanPackage" : "FanPackage",
    "FanSlot" : "FanSlot"
    }).enum_type

CMCLogsEnum = EnumWrapper("CMCLogEnum", {
    "Logs" : "Logs",
    }).enum_type

CMCJobsEnum = EnumWrapper("CMCJobEnum", {
    "Jobs" : "Jobs",
    }).enum_type

CMCFirmEnum = EnumWrapper("CMCFirmEnum", {
    "Firmware" : "Firmware",
    }).enum_type

CMCWsManViews = {
    CMCCompEnum.System: "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_ModularChassisView",
    CMCCompEnum.ComputeModule : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_BladeServerView",
    CMCCompEnum.StorageModule : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_StorageSledView",
    CMCCompEnum.Fan : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_Fan",
    CMCMiscEnum.FanPackage : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_FanPackage",
    CMCMiscEnum.FanSlot : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_FanSlot",
    CMCCompEnum.PCIDevice : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_ChassisPCIDeviceView",
    CMCMiscEnum.PCISlot : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_ChassisPCISlot",
    CMCCompEnum.CMC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_ChMgrPackage",
    CMCCompEnum.IOModule : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_IOMPackage",
    CMCMiscEnum.PassThroughModule : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_PassThroughModule",
    CMCCompEnum.PowerSupply : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_PowerSupply",
    CMCMiscEnum.PSPackage : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_PSPackage",
    CMCMiscEnum.PSSlot : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_PSSlot",
    CMCFirmEnum.Firmware : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/DCIM_SoftwareIdentity",
    CMCJobsEnum.Jobs : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob",
    CMCLogsEnum.Logs : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_HWLogEntry",
    CMCCompEnum.Controller : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_ControllerView",
    CMCCompEnum.EnclosureEMM : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EnclosureEMMView",
    CMCCompEnum.EnclosurePSU : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EnclosurePSUView",
    CMCCompEnum.Enclosure : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EnclosureView",
    CMCCompEnum.ControllerBattery : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_ControllerBatteryView",
    CMCCompEnum.VirtualDisk : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_VirtualDiskView",
    CMCCompEnum.PhysicalDisk : "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_PhysicalDiskView",
    CMCCompEnum.KVM : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/Dell_KVM",
}

CMCWsManCmds = { }
CMCWsManCompMap = { }

CMCMergeJoinCompSpec = {
   "Fan" : {
        "_components" : [
            ["Fan", "ClassId", "FanSlot", "ClassId"],
            ["Fan", "ClassId", "FanPackage", "ClassId"]
        ],
        "_components_enum": [
            CMCCompEnum.Fan,
            CMCMiscEnum.FanPackage,
            CMCMiscEnum.FanSlot
        ],
        "_overwrite" : True
   },
   "PowerSupply" : {
        "_components" : [
            ["PowerSupply", "ClassId", "PSPackage", "ClassId"],
            ["PowerSupply", "ClassId", "PSSlot", "ClassId"]
        ],
        "_components_enum": [
            CMCCompEnum.PowerSupply,
            CMCMiscEnum.PSPackage,
            CMCMiscEnum.PSSlot
        ],
        "_overwrite" : False
   },
   "IOModule" : {
        "_components" : [
            ["IOModule", "ClassId", "PassThroughModule", "ClassId"]
        ],
        "_components_enum": [
            CMCCompEnum.IOModule,
            CMCMiscEnum.PassThroughModule
        ],
        "_overwrite" : False
   },
   "PCIDevice" : {
        "_components" : [
            ["PCIDevice", "SlotFQDD", "PCISlot", "FQDD"]
        ],
        "_components_enum": [
            CMCCompEnum.PCIDevice,
            CMCMiscEnum.PCISlot
        ],
        "_overwrite" : True
   }
}
CMCWsManViews_FieldSpec = {
    CMCCompEnum.PowerSupply : {
        "HealthState":  { 'Rename' : 'PrimaryStatus' }
    },
    CMCCompEnum.Fan : {
        "HealthState":  { 'Rename' : 'PrimaryStatus' }
    },
    CMCMiscEnum.FanSlot : {
        "Number": {'Rename' : 'SlotNumber'}
    },
    CMCCompEnum.KVM : {
        "HealthState":  { 'Rename' : 'PrimaryStatus' }
    },
    CMCMiscEnum.PSPackage : {
        "Tag":  { 'Rename' : 'PSPackage_Tag' }
    },
    CMCMiscEnum.PSSlot : {
        "Tag":  { 'Rename' : 'PSSlot_Tag' }
    },
    
}

class CMC(iDeviceDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(CMC, self).__init__(iDeviceRegistry("CMC", srcdir, CMCCompEnum))
        else:
            super().__init__(iDeviceRegistry("CMC", srcdir, CMCCompEnum))
        self.protofactory.add(PWSMAN(
            selectors = {"__cimnamespace" : "root/dell/cmc" },
            views = CMCWsManViews,
            view_fieldspec = CMCWsManViews_FieldSpec,
            cmds = CMCWsManCmds,
            compmap = CMCWsManCompMap
        ))
        self.protofactory.addClassifier([CMCCompEnum.System])

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return CMCEntity(self.ref, protofactory, ipaddr, creds)

class CMCEntity(iDeviceDriver):
    def __init__(self, ref, protofactory, ipaddr, creds):
        if PY2:
            super(CMCEntity, self).__init__(ref, protofactory, ipaddr, creds)
        else:
            super().__init__(ref, protofactory, ipaddr, creds)
        self.comp_merge_join_spec = CMCMergeJoinCompSpec

    def my_fix_obj_index(self, clsName, key, js):
        retval = None
        if clsName == "System":
            if 'ServiceTag' not in js or js['ServiceTag'] is None:
                js['ServiceTag'] = self.ipaddr
            retval = js['ServiceTag']
        if retval is None:
            retval = self.ipaddr + "cmc_null"
        return retval

    def get_idrac_ips(self):
        self.get_partial_entityjson(self.ComponentEnum.ComputeModule)
        return self._get_field_device_for_all(self.ComponentEnum.ComputeModule, "IPv4Address")

    def _get_topology_info(self):
        self.get_partial_entityjson(self.ComponentEnum.ComputeModule)
        return CMCTopologyInfo(self.get_json_device())

    def _get_topology_influencers(self):
        return { 'System' : [ 'Model' ],
                 'ComputeModule' : [ 'ServiceTag' ] }

class CMCTopologyInfo(iDeviceTopologyInfo):
    def __init__(self, json):
        if PY2:
            super(iDeviceTopologyInfo, self).__init__('CMC', json)
        else:
            super().__init__('CMC', json)

    def my_static_groups(self, tbuild):
        tbuild.add_group('Dell', static=True)
        tbuild.add_group('Dell Chassis', 'Dell', static=True)

    def my_groups(self, tbuild):
        if 'Model' in self.system:
            fmgrp = self.system['Model']
            tbuild.add_group(fmgrp, 'Dell Chassis')
            self._add_myself(tbuild, fmgrp)

    def my_assoc(self, tbuild):
        if 'ComputeModule' not in self.json:
            return
        self._remove_assoc(tbuild, [self.mytype, self.system['Key']])
        for slot in self.json['ComputeModule']:
            self._add_assoc(tbuild,
                            [self.mytype, self.system['Key']],
                            ['ComputeModule', slot['Key']],
                            ['Server', slot['ServiceTag']])
