import os
import sys

import re
import time
import base64
import xml.etree.ElementTree as ET
from enum import Enum
from datetime import datetime
from omsdk.sdkdevice import iDeviceRegistry, iDeviceDriver, iDeviceDiscovery
from omsdk.sdkdevice import iDeviceTopologyInfo
from omsdk.sdkprint import LogMan, pretty
from omsdk.sdkproto import PWSMAN,PREDFISH, PSNMP
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkcenum import EnumWrapper, TypeHelper

class NoConfig:
    def __init__(self, arg1):
        print("iDRAC:Not implemented")


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False

try:
    from omdrivers.lifecycle.iDRAC.iDRACJobs import iDRACJobs
    from omdrivers.lifecycle.iDRAC.iDRACJobs import iDRACJobsEnum
    from omdrivers.lifecycle.iDRAC.iDRACConfig import iDRACConfig
    from omdrivers.lifecycle.iDRAC.iDRACConfig import PowerStateEnum
    from omdrivers.lifecycle.iDRAC.iDRACConfig import iDRACRedfishCmds
    from omdrivers.lifecycle.iDRAC.iDRACConfig import iDRACWsManCmds
    from omdrivers.lifecycle.iDRAC.iDRACLogs import iDRACLogs
    from omdrivers.lifecycle.iDRAC.iDRACLogs import iDRACLogsEnum
    from omdrivers.lifecycle.iDRAC.iDRACUpdate import iDRACUpdate
    from omdrivers.lifecycle.iDRAC.iDRACUpdate import iDRACFirmEnum
    from omdrivers.lifecycle.iDRAC.iDRACLicense import iDRACLicense
    from omdrivers.lifecycle.iDRAC.iDRACLicense import iDRACLicenseEnum
    from omdrivers.lifecycle.iDRAC.iDRACCredsMgmt import iDRACCredsMgmt
except ImportError as ex:
    print(str(ex))
    iDRACJobs = NoConfig
    iDRACConfig = NoConfig
    iDRACLogs = NoConfig
    iDRACUpdate = NoConfig
    iDRACRedfishCmds = {}
    iDRACWsManCmds = {}

iDRACCompEnum = EnumWrapper("iDRACCompEnum", {
    "System" : "System",
    "Memory" : "Memory",
    "CPU" : "CPU",
    "iDRAC" : "iDRAC",
    "FC" : "FC",
    "NIC" : "NIC",
    "HostNIC" : "HostNIC",
    "PCIDevice" : "PCIDevice",
    "Fan" : "Fan",
    "PowerSupply" : "PowerSupply",
    "Enclosure" : "Enclosure",
    "EnclosureEMM" : "EnclosureEMM",
    "EnclosurePSU" : "EnclosurePSU",
    "VFlash"  : "VFlash",
    "Video" : "Video",
    "ControllerBattery" : "ControllerBattery" ,
    "Controller" : "Controller",
    "VirtualDisk" : "VirtualDisk",
    "PhysicalDisk" : "PhysicalDisk",
    "Sensors_Amperage" : "Sensors_Amperage",
    "Sensors_Temperature" : "Sensors_Temperature",
    "Sensors_Voltage" : "Sensors_Voltage",
    "Sensors_Intrusion" : "Sensors_Intrusion",
    "Sensors_Battery" : "Sensors_Battery",
    "Sensors_Fan" : "Sensors_Fan",
    "LogicalSystem" : "LogicalSystem",
    "License" : "License",
    "iDRACNIC" : "iDRACNIC"
    }).enum_type

iDRACSensorEnum = EnumWrapper("iDRACSensorEnum", {
    "ServerSensor" : "ServerSensor",
    "NumericSensor" : "NumericSensor",
    "PSNumericSensor" : "PSNumericSensor",
    }).enum_type

iDRACMiscEnum = EnumWrapper("iDRACMiscEnum", {
    "SystemString" : "SystemString",
    "NICString" : "NICString",
    "NICEnumeration" : "NICEnumeration",
    "iDRACString" : "iDRACString",
    "iDRACEnumeration" : "iDRACEnumeration",
    "NICStatistics" : "NICStatistics",
    "NICCapabilities" : "NICCapabilities",
    "SwitchConnection" : "SwitchConnection",
    "FCStatistics" : "FCStatistics",
    "HostNICView" : "HostNICView"
    }).enum_type


#iDRACFirmEnum.SelLog : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SELLogEntry",

iDRACComponentTree = {
    iDRACCompEnum.System : [ 
        iDRACCompEnum.Memory, 
        iDRACCompEnum.CPU, 
        iDRACCompEnum.iDRAC,
        iDRACCompEnum.FC,
        iDRACCompEnum.NIC,
        iDRACCompEnum.PCIDevice,
        iDRACCompEnum.Fan,
        iDRACCompEnum.PowerSupply,
        iDRACCompEnum.VFlash,
        iDRACCompEnum.Video,
        "Sensors",
        "Storage"
    ],
    "Storage" : [
        iDRACCompEnum.Controller,
    ],
    "Sensors" : [
        iDRACCompEnum.Sensors_Amperage,
        iDRACCompEnum.Sensors_Temperature,
        iDRACCompEnum.Sensors_Voltage,
        iDRACCompEnum.Sensors_Intrusion,
        iDRACCompEnum.Sensors_Battery,
        iDRACCompEnum.Sensors_Fan
    ],
    iDRACCompEnum.Controller : [
        iDRACCompEnum.Enclosure, # Enclosure.RAID.Modular.3-1
        iDRACCompEnum.ControllerBattery, # Battery.RAID.Modular.3-1
        iDRACCompEnum.VirtualDisk, #VirtualDisk.RAID.Modular.3-1
        iDRACCompEnum.PhysicalDisk, #DirectDisk.RAID
    ],
    iDRACCompEnum.Enclosure : [
        iDRACCompEnum.EnclosureEMM,
        iDRACCompEnum.EnclosurePSU,
        iDRACCompEnum.PhysicalDisk,
    ]
}

iDRACSWCompMapping = {
    'BIOS' : 'BIOS.*',
    'CMC' : 'CMC.*',
    'CPLD' : 'CPLD.*',
    'LC' : '.*LC.Embedded.*',
    'PhysicalDisk' : 'Disk.*',
    'DriverPack' : 'DriverPack.*',
    'Enclosure' : 'Enclosure.*',
    'NIC' : 'NIC.*',
    'OSCollector' : 'OSCollector.*',
    'RAID' : 'RAID.*',
    'iDRAC' : 'iDRAC.*',
    'Chassis' : '.*Chassis.*'
}

# http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_NICStatistics
iDRACWsManViews = {
    iDRACCompEnum.System: "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SystemView",
    iDRACCompEnum.Memory : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_MemoryView",
    iDRACCompEnum.CPU : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_CPUView",
    iDRACCompEnum.Fan : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_FanView",
    iDRACCompEnum.iDRAC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardView",
    iDRACCompEnum.iDRACNIC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardView",
    iDRACCompEnum.FC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_FCView",
    iDRACCompEnum.NIC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NICView",
    iDRACCompEnum.HostNIC : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_HostNetworkInterfaceView",
    iDRACCompEnum.PowerSupply : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_PowerSupplyView",
    iDRACCompEnum.VFlash : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_VFlashView",
    iDRACCompEnum.Video : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_VideoView",
    iDRACCompEnum.PhysicalDisk : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_PhysicalDiskView",
    iDRACCompEnum.ControllerBattery : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_ControllerBatteryView",
    iDRACCompEnum.Controller : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_ControllerView",
    iDRACCompEnum.EnclosureEMM : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_EnclosureEMMView",
    iDRACCompEnum.EnclosurePSU : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_EnclosurePSUView",
    iDRACCompEnum.Enclosure : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_EnclosureView",
    iDRACCompEnum.PCIDevice : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_PCIDeviceView",
    iDRACCompEnum.VirtualDisk : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_VirtualDiskView",
    iDRACSensorEnum.ServerSensor : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_Sensor",
    iDRACSensorEnum.NumericSensor : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NumericSensor",
    iDRACSensorEnum.PSNumericSensor : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_PSNumericSensor",
    iDRACFirmEnum.Firmware : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareIdentity",
    iDRACJobsEnum.Jobs : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LifecycleJob",
    iDRACMiscEnum.SystemString : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SystemString",
    iDRACMiscEnum.NICString : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NICString",
    iDRACMiscEnum.NICEnumeration : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NICEnumeration",
    iDRACMiscEnum.iDRACString : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardString",
    iDRACMiscEnum.iDRACEnumeration : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardEnumeration",
    iDRACMiscEnum.NICStatistics : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NICStatistics",
    iDRACMiscEnum.NICCapabilities : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_NICCapabilities",
    iDRACMiscEnum.SwitchConnection : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SwitchConnectionView",
    iDRACMiscEnum.FCStatistics : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_FCStatistics",
    iDRACMiscEnum.HostNICView : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_HostNetworkInterfaceView",
    iDRACCompEnum.License : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_License",
    iDRACLicenseEnum.LicensableDevice : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicensableDevice",
    iDRACLogsEnum.SELLog : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SELLogEntry",
}

iDRACWsManViews_FieldSpec = {
    iDRACCompEnum.Memory : {
        "Size" : { 'Type' : 'Bytes', 'InUnits' : "MB" },
        "Speed" : { 'Type' : 'ClockSpeed', 'InUnits' : "MHz" }
    },
    iDRACCompEnum.Controller : {
        "CacheSizeInMB" : { 'Rename' : 'CacheSize', 'Type' : 'Bytes', 'InUnits' : 'MB', 'OutUnits' : 'MB' },
    },
    iDRACCompEnum.CPU : {
        "CPUFamily" : {
            'Lookup'  :  'True',
            'Values' : {
                "1" : "Other", 
                "2" : "Unknown", 
                "3" : "8086", 
                "4" : "80286", 
                "5" : "80386",
                "6" : "80486",
                "7" : "8087",
                "8" : "80287",
                "9" : "80387",
                "A" : "80487",
                "B" : "Pentium(R)brand", 
                "C" : "Pentium(R)Pro",
                "D" : "pentium(R) II", 
                "E" : "Pentium(R) Processor with MMX(TM) technology", 
                "F" : "Celeron(TM)",
                "10" : "Pentium(R) II Xeon(TM)", 
                "11" : "Pentium(R) III", 
                "12" : "M1 Family", 
                "13" : "M2 Family", 
                "14" : "Intel(R) Celeron(R) M processor", 
                "15" : "Intel(R) Pentium(R) 4 HT processor", 
                "18" : "K5 Family", 
                "19" : "K6 Family" ,
                "1A" : "K6-2", 
                "1B" : "K6-3", 
                "1C" : "AMD Athlon(TM) Processor Family", 
                "1D" : "AMD(R) Duron(TM) Processor", 
                "1E" : "AMD29000 Family", 
                "1F" : "K6-2+", 
                "20" : "Power PC Family", 
                "21" : "Power PC 601", 
                "22" : "Power PC 603", 
                "23" : "Power PC 603+", 
                "24" : "Power PC 604", 
                "25" : "Power PC 620", 
                "26" : "Power PC X704", 
                "27" : "Power PC 750", 
                "28" : "Intel(R) Core(TM) Duo processor", 
                "29" : "Intel(R) Core(TM) Duo mobile processor", 
                "2A" : "Intel(R) Core(TM) Solo mobile processor", 
                "2B" : "Intel(R) Atom(TM) processor", 
                "30" : "Alpha Family", 
                "31" : "Alpha 21064", 
                "32" : "Alpha 21066", 
                "33" : "Alpha 21164", 
                "34" : "Alpha 21164PC", 
                "35" : "Alpha 21164a", 
                "36" : "Alpha 21264", 
                "37" : "Alpha 21364", 
                "38" : "AMD Turion(TM) II Ultra Dual-Core Mobile M Processor Family", 
                "39" : "AMD Turion(TM) II Dual-Core Mobile M Processor Family", 
                "3A" : "AMD Athlon(TM) II Dual-Core Mobile M Processor Family", 
                "3B" : "AMD Opteron(TM) 6100 Series Processor", 
                "3C" : "AMD Opteron(TM) 4100 Series Processor", 
                "3D" : "AMD Opteron(TM) 6200 Series Processor", 
                "3E" : "AMD Opteron(TM) 4200 Series Processor", 
                "40" : "MIPS Family", 
                "41" : "MIPS R4000", 
                "42" : "MIPS R4200", 
                "43" : "MIPS R4400", 
                "44" : "MIPS R4600", 
                "45" : "MIPS R10000", 
                "46" : "AMD C-Series Processor", 
                "47" : "AMD E-Series Processor", 
                "48" : "AMD S-Series Processor", 
                "49" : "AMD G-Series Processor", 
                "50" : "SPARC Family", 
                "51" : "SuperSPARC", 
                "52" : "microSPARC II", 
                "53" : "microSPARC IIep", 
                "54" : "UltraSPARC", 
                "55" : "UltraSPARC II", 
                "56" : "UltraSPARC IIi", 
                "57" : "UltraSPARC III", 
                "58" : "UltraSPARC IIIi", 
                "60" : "68040", 
                "61" : "68xxx Family", 
                "62" : "68000", 
                "63" : "68010", 
                "64" : "68020", 
                "65" : "68030", 
                "70" : "Hobbit Family",
                "78" : "Crusoe(TM) TM5000 Family", 
                "79" : "Crusoe(TM) TM3000 Family", 
                "7A" : "Efficeon(TM) TM8000 Family", 
                "80" : "Weitek", 
                "82" : "Itanium(TM) Processor", 
                "83" : "AMD Athlon(TM) 64 Processor Family", 
                "84" : "AMD Opteron(TM) Processor Family", 
                "85" : "AMD Sempron(TM) Processor Family", 
                "86" : "AMD Turion(TM) 64 Mobile Technology", 
                "87" : "Dual-Core AMD Opteron(TM) Processor Family", 
                "88" : "AMD Athlon(TM) 64 X2 Dual-Core Processor Family", 
                "89" : "AMD Turion(TM) 64 X2 Mobile Technology", 
                "8A" : "Quad-Core AMD Opteron(TM) Processor Family", 
                "8B" : "Third Generation AMD Opteron(TM) Processor Family", 
                "8C" : "AMD Phenom(TM) FX Quad-Core Processor Family", 
                "8D" : "AMD Phenom(TM) X4 Quad-Core Processor Family", 
                "8E" : "AMD Phenom(TM) X2 Dual-Core Processor Family", 
                "8F" : "AMD Athlon(TM) X2 Dual-Core Processor Family", 
                "90" : "PA-RISC Family", 
                "91" : "PA-RISC 8500", 
                "92" : "PA-RISC 8000", 
                "93" : "PA-RISC 7300LC", 
                "94" : "PA-RISC 7200", 
                "95" : "PA-RISC 7100LC", 
                "96" : "PA-RISC 7100", 
                "A0" : "V30 Family",
                "A1" : "Quad-Core Intel(R) Xeon(R) processor 3200 Series", 
                "A2" : "Dual-Core Intel(R) Xeon(R) processor 3000 Series", 
                "A3" : "Quad-Core Intel(R) Xeon(R) processor 5300 Series", 
                "A4" : "Dual-Core Intel(R) Xeon(R) processor 5100 Series", 
                "A5" : "Dual-Core Intel(R) Xeon(R) processor 5000 Series", 
                "A6" : "Dual-Core Intel(R) Xeon(R) processor LV",
                "A7" : "Dual-Core Intel(R) Xeon(R) processor ULV",
                "A8" : "Dual-Core Intel(R) Xeon(R) processor 7100 Series", 
                "A9" : "Quad-Core Intel(R) Xeon(R) processor 5400 Series",
                "AA" : "Quad-Core Intel(R) Xeon(R) processor",
                "AB" : "Dual-Core Intel(R) Xeon(R) processor 5200 Series",
                "AC" : "Dual-Core Intel(R) Xeon(R) processor 7200 Series",
                "AD" : "Quad-Core Intel(R) Xeon(R) processor 7300 Series", 
                "AE" : "Quad-Core Intel(R) Xeon(R) processor 7400 Series", 
                "AF" : "Multi-Core Intel(R) Xeon(R) processor 7400 Series", 
                "B0" : "Pentium(R) III Xeon(TM)", 
                "B1" : "Pentium(R) III Processor with Intel(R) SpeedStep(TM) Technology", 
                "B2" : "Pentium(R) 4", 
                "B3" : "Intel(R) Xeon(TM)", 
                "B4" : "AS400 Family", 
                "B5" : "Intel(R) Xeon(TM) Processor MP", 
                "B6" : "AMD Athlon(TM) XP Family", 
                "B7" : "AMD Athlon(TM) MP Family",
                "B8" : "Intel(R) Itanium(R) 2",
                "B9" : "Intel(R) Pentium(R) M Processor", 
                "BA" : "Intel(R) Celeron(R) D Processor", 
                "BB" : "Intel(R) Pentium(R) D Processor", 
                "BC" : "Intel(R) Pentium(R) Processor Extreme Edition", 
                "BD" : "Intel(R) Core(TM) Solo Processor", 
                "BE" : "K7", 
                "BF" : "Intel(R) Core(TM) 2 Duo Processor", 
                "C0" : "Intel(R) Core(TM) 2 Solo Processor", 
                "C1" : "Intel(R) Core(TM) 2 Extreme Processor", 
                "C2" : "Intel(R) Core(TM) 2 Quad Processor", 
                "C3" : "Intel(R) Core(TM) 2 Extreme mobile Processor", 
                "C4" : "Intel(R) Core(TM) 2 Duo mobile Processor", 
                "C5" : "Intel(R) Core(TM) 2 solo mobile Processor", 
                "C6" : "Intel(R) Core(TM) i7 processor", 
                "C7" : "Dual-Core Intel(R) Celeron(R) Processor", 
                "C8" : "S/390 and zSeries Family", 
                "C9" : "ESA/390 G4", 
                "CA" : "ESA/390 G5", 
                "CB" : "ESA/390 G6", 
                "CC" : "z/Architecture base", 
                "CD" : "Intel(R) Core(TM) i5 processor", 
                "CE" : "Intel(R) Core(TM) i3 processor", 
                "D2" : "VIA C7(TM)-M Processor Family", 
                "D3" : "VIA C7(TM)-D Processor Family", 
                "D4" : "VIA C7(TM) Processor Family", 
                "D5" : "VIA Eden(TM) Processor Family", 
                "D6" : "Multi-Core Intel(R) Xeon(R) processor", 
                "D7" : "Dual-Core Intel(R) Xeon(R) processor 3xxx Series", 
                "D8" : "Quad-Core Intel(R) Xeon(R) processor 3xxx Series", 
                "D9" : "VIA Nano(TM) Processor Family", 
                "DA" : "Dual-Core Intel(R) Xeon(R) processor 5xxx Series", 
                "DB" : "Quad-Core Intel(R) Xeon(R) processor 5xxx Series", 
                "DD" : "Dual-Core Intel(R) Xeon(R) processor 7xxx Series", 
                "DE" : "Quad-Core Intel(R) Xeon(R) processor 7xxx Series", 
                "DF" : "Multi-Core Intel(R) Xeon(R) processor 7xxx Series", 
                "E0" : "Multi-Core Intel(R) Xeon(R) processor 3400 Series", 
                "E6" : "Embedded AMD Opteron(TM) Quad-Core Processor Family", 
                "E7" : "AMD Phenom(TM) Triple-Core Processor Family", 
                "E8" : "AMD Turion(TM) Ultra Dual-Core Mobile Processor Family", 
                "E9" : "AMD Turion(TM) Dual-Core Mobile Processor Family", 
                "EA" : "AMD Athlon(TM) Dual-Core Processor Family", 
                "EB" : "AMD Sempron(TM) SI Processor Family", 
                "EC" : "AMD Phenom(TM) II Processor Family", 
                "ED" : "AMD Athlon(TM) II Processor Family", 
                "EE" : "Six-Core AMD Opteron(TM) Processor Family", 
                "EF" : "AMD Sempron(TM) M Processor Family", 
                "FA" : "i860", 
                "FB" : "i960", 
                "FE" : "Reserved (SMBIOS Extension)", 
                "FF" : "Reserved (Un-initialized Flash Content - Lo)", 
                "104" : "SH-3", 
                "105" : "SH-4", 
                "118" : "ARM", 
                "119" : "StrongARM", 
                "12C" : "6x86", 
                "12D" : "MediaGX", 
                "12E" : "MII", 
                "140" : "WinChip", 
                "15E" : "DSP", 
                "1F4" : "Video Processor", 
                "FFFE" : "Reserved (For Future Special Purpose Assignment)", 
                "FFFF" : "Reserved (Un-initialized Flash Content - Hi)"
            }
        },
        "HyperThreadingCapable" : {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },            
        "VirtualizationTechnologyCapable": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "TurboModeCapable": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "HyperThreadingEnabled": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "TurboModeEnabled": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "VirtualizationTechnologyEnabled": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "ExecuteDisabledEnabled": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes",
                "2" : "Not Applicable"
            }
        },
        "ExecuteDisabledCapable": {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "No", 
                "1" : "Yes" 
            }
        },
        "MaxClockSpeed" : { 'Type' : 'ClockSpeed', 'InUnits' : "MHz" }
    },
    iDRACMiscEnum.NICStatistics : {
        "LinkStatus" : {'Rename' : 'PrimaryStatus',
            'Lookup'  :  'True',
            'Values' : {
                '0' : "Warning",
                '1' : "Healthy",      
                '3' : "Critical"
            }
        }
    },
    iDRACCompEnum.PhysicalDisk : {
        "SizeInBytes" : { 'Rename' : 'Size', 'Type' : 'Bytes' , 'InUnits' : 'B' },
        "UsedSpace" : { 'Type' : 'Bytes' , 'InUnits' : 'B', 'Metrics' : 'GB' },
        "FreeSizeInBytes" : { 'Rename' : 'FreeSize', 'Type' : 'Bytes' , 'InUnits' : 'B', 'Metrics' : 'GB' },
        "BlockSizeInBytes":  { 'Rename' : 'BlockSize', 'Type' : 'Bytes' , 'InUnits' : 'B', 'Metrics' : 'KB' },
        "RemainingRatedWriteEndurance":  {
            'Lookup' : 'True',
            'Values' : {
                '255' : "Not Available"
            }
        }
    },
    iDRACCompEnum.System: {
        "SysMemMaxCapacitySize" : { 'Type' : 'Bytes' , 'InUnits' : 'KB' },
        "SysMemTotalSize" : { 'Type' : 'Bytes' , 'InUnits' : 'KB' },
    },
    iDRACCompEnum.VirtualDisk : {
        "SizeInBytes" : { 'Rename' : 'Size', 'Type' : 'Bytes' , 'InUnits' : 'B' , 'Metrics' : 'GB'},
        "BlockSizeInBytes":  { 'Rename' : 'BlockSize', 'Type' : 'Bytes' , 'InUnits' : 'B' },
        "RAIDTypes" : {
            'Lookup'  :  'True',
            'Values' : {
                '1'       :  'No RAID',
                '2'       :  'RAID-0',
                '4'       :  'RAID-1',
                '64'      :  'RAID-5',
                '128'     :  'RAID-6',
                '2048'    :  'RAID-10',
                '8192'    :  'RAID-50',
                '16384'   :  'RAID-60'
            }
        },
        "StripeSize" : {
            'Lookup'  :  'True',
            'Values' : {
                "0" : "Default",
                "1" : "512 Bytes",
                "2" : "1 KB",
                "4" : "2 KB",
                "8" : "4 KB",
                "16" : "8 KB",
                "32" : "16 KB",
                "64" : "32 KB",
                "128" : "64 KB",
                "256" : "128 KB",
                "512" : "256 KB",
                "1024" : "512 KB",
                "2048" : "1 MB",
                "4096" : "2 MB",
                "8192" : "4 MB",
                "16384" : "8 MB",
                "32768" : "16 MB"
            }
        }
    },
    iDRACCompEnum.VFlash : {
        "Capacity" : { 'Type' : 'Bytes', 'InUnits' : 'MB' },
        "AvailableSize" : { 'Type' : 'Bytes', 'InUnits' : 'MB' },
        "HealthStatus":  { 'Rename' : 'PrimaryStatus'},
    },
    iDRACSensorEnum.NumericSensor : {
        "CurrentReading" :  {'UnitModify': 'UnitModifier', 
                             'UnitName' : 'BaseUnits',
                             'BaseUnits' : {
                                '6' : None, #'Amps',
                                '7' : None, #'Watts',
                                '2' : None, #'Degrees C',
                                '5' : None, #'Volts',
                                '19' : None, #'RPM',
                                '65' : None, #'Percentage'
                            }
                        }
    },
    iDRACSensorEnum.PSNumericSensor : {
        "CurrentReading" :  {'UnitModify': 'UnitModifier', 
                             'UnitName' : 'BaseUnits',
                             'BaseUnits' : {
                                '6' : None, #'Amps',
                                '7' : None, #'Watts',
                                '2' : None, # 'Degrees C',
                                '5' : None, # 'Volts',
                                '19' : None, # 'RPM',
                                '65' : None, #'Percentage'
                            }
                        }   
    },
    iDRACMiscEnum.iDRACEnumeration : {
        "InstanceID" : {
            'Lookup'  :  'True',
            'Values' : {
                "iDRAC.Embedded.1#GroupManager.1#Status" : 'GroupStatus',
                "iDRAC.Embedded.1#NIC.1#Duplex" : 'NICDuplex',
                "iDRAC.Embedded.1#NIC.1#Speed": 'NICSpeed',
                "iDRAC.Embedded.1#NIC.1#Enable": 'PrimaryStatus',
                "iDRAC.Embedded.1#Lockdown.1#SystemLockdown" : 'SystemLockDown'
            }
        }
    },
    iDRACMiscEnum.iDRACString : {
        "InstanceID" : {
            'Lookup'  :  'True',
            'Values' : {
                "iDRAC.Embedded.1#IPv4.1#Address" : 'IPv4Address',
                "iDRAC.Embedded.1#Info.1#Product" : 'ProductInfo',
                "iDRAC.Embedded.1#CurrentNIC.1#MACAddress" : 'MACAddress',
                "iDRAC.Embedded.1#CurrentIPv6.1#Address1" : 'IPv6Address',
                "iDRAC.Embedded.1#GroupManager.1#GroupName" : 'GroupName',
                "iDRAC.Embedded.1#NIC.1#SwitchConnection" : 'SwitchConnection',
                "iDRAC.Embedded.1#NIC.1#SwitchPortConnection" : 'SwitchPortConnection'
            }
        }
    },
    iDRACCompEnum.PowerSupply : {
        "TotalOutputPower" : {'UnitScale': '0', 'UnitAppend' : 'Watts'}
    }
}


iDRACClassifier = [ iDRACCompEnum.System ]

iDRACRedfishViews = {
    iDRACCompEnum.System: "/redfish/v1/Systems/System.Embedded.1",
    iDRACCompEnum.NIC : "/redfish/v1/Managers/iDRAC.Embedded.1/SerialInterfaces",
}

if PySnmpPresent:
    iDRACSNMPViews = {
        iDRACCompEnum.System : {
            'SysObjectID' : ObjectIdentity('SNMPv2-MIB', 'sysObjectID'),
            "ServiceTag" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.3.1'),
            "NodeID" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.3.18'),
            "Model" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.3.12'),
            "SystemGeneration" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.1.7'),
            "ChassisServiceTag" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.2.1'),
            "PrimaryStatus" : ObjectIdentity(' 1.3.6.1.4.1.674.10892.5.4.200.10.1.2'),
            'ChassisModel' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.6"), 
            'StateSettings' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.3"), 
            'Manufacturer' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.8"), 
            'ChassisName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.7"), 
            'parentIndexReference' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.5"), 
            'StateCapabilities' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.2"), 
            'Status' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.4"), 
            'HostName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.15"), 
            "OSVersion" :  ObjectIdentity('1.3.6.1.4.1.674.10892.5.1.3.14'),
            'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.11"), 
            'SystemRevisionName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.48"), 
            'SystemRevisionNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.47"), 
            'ExpressServiceCodeName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.49"), 
            'AssetTag' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.10"), 
            'SysMemPrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.10.1.27"), 
            "CPURollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.50"),
            "FanRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.44"),
            "PSRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.9"),
            "StorageRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.2.3"),
            "VoltRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.12"),
            "TempRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.24"),
            "AmpRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.15"),
            "BatteryRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.52"),
            "SDCardRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.56"),
            "IDSDMRollupStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.58"),
            "ChassisIntrusion" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.30"),
            "ChassisStatus" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.200.10.1.4"),
        },
        iDRACCompEnum.CPU : {
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.2"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.5"), 
            'Type' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.7"), 
            'Manufacturer' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.8"), 
            'CPUFamily' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.10"), 
            'MaxClockSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.11"), 
            'CurrentClockSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.12"), 
            'ExternalClockSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.13"), 
            'Voltage' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.14"), 
            'Version' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.16"), 
            "NumberOfProcessorCores" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.17"), 
            "CoreEnabledCount" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.18"), 
            "ThreadCount" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.19"), 
            "Characteristics" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.20"), 
            "ExtendedCapabilities" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.21"), 
            "ExtendedEnabled" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.22"), 
            'Model' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.23"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.30.1.26"), 
        },
        iDRACCompEnum.Memory : {
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.26"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.5"), 
            'MemoryType' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.7"), 
            'LocationName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.8"), 
            'BankLabel' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.10"), 
            'Size' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.14"), 
            'Speed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.15"), 
            'Manufacturer' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.21"), 
            'PartNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.22"), 
            'SerialNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.23"), 
            'StateCapabilities' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.3"), 
            # 'Rank' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.50.1.2"),
            # The OID above corresponds to Index and Rank not in iDRAC MIB
        },
        iDRACCompEnum.NIC : {
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.2"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.3"), 
            'LinkStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.4"), 
            'ProductName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.6"), 
            'Vendor' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.7"), 
            'CurrentMACAddress' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.15"), 
            'PermanentMACAddress' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.16"), 
            'PCIBusNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.17"), 
            'PCIDeviceNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.18"), 
            'PCIFunctionNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.19"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.30"), 

            "TOECapabilityFlags" :  ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.23"), 
            "iSCSICapabilityFlags" :  ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.27"), 
            "iSCSIEnabled" : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.90.1.28"), 
        },
        iDRACCompEnum.PCIDevice : {
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.2"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.5"), 
            'DataBusWidth' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.7"), 
            'Manufacturer' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.8"), 
            'Description' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.9"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.1100.80.1.12"), 
        },
        iDRACCompEnum.Fan : {
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.2"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.5"), 
            'coolingUnitIndexReference' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.15"), 
            'CurrentReading' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.6"), 
            'Type' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.7"), 
            'Location' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.8"), 
            'SubType' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.16"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.700.12.1.19"), 
        },
        iDRACCompEnum.PowerSupply : {
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.2"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.5"), 
            "TotalOutputPower" :  ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.6"), 
            'Type' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.7"), 
            'Location' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.8"), 
            'InputVoltage' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.9"), 
            'RatedInputWattage' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.14"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.15"), 
            'IndexReference' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.600.12.1.10"), 
        },
        iDRACCompEnum.Enclosure : {
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.1"), 
            'ProductName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.2"), 
            'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.8"), 
            'AssetTag' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.9"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.4"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.24"), 
            'Version' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.26"), 
            'SASAddress' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.30"), 
            'DriveCount' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.31"), 
            'TotalSlots' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.32"), 
            'FanCount' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.40"), 
            'PSUCount' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.41"), 
            'EMMCount' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.42"), 
            'TempProbeCount' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.43"), 
            'Position' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.45"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.47"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.48"), 
            'RollUpStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.23"), 
        },
        iDRACCompEnum.EnclosureEMM : {
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.15"), 
            'Name' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.2"), 
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.1"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.4"), 
            'PartNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.6"), 
            'FWVersion' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.8"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.16"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.13.1.11"), 
        },
        "EnclosureFan" : {
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.1"), 
            'Name' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.2"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.4"), 
            'CurrentSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.11"), 
            'PartNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.7"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.15"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.20"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.7.1.21"), 
        },
        iDRACCompEnum.EnclosurePSU : {
            'Name' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.2"), 
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.1"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.4"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.15"), 
            'PartNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.7"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.9"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.9.1.16"), 
        },
        iDRACCompEnum.ControllerBattery : {
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.1"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.4"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.6"), 
            'PredictedCapacity' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.10"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.20"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.15.1.21"), 
        },
        iDRACCompEnum.Controller : {
            'ProductName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.2"), 
            'ControllerFirmwareVersion' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.8"), 
            'CacheSize' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.9"), 
            'RollUpStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.37"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.38"), 
            'DriverVersion' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.41"), 
            'PCISlot' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.42"), 
            'HotspareStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.59"), 
            'CopyBackMode' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.71"), 
            'SecurityStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.72"), 
            'EncryptionCapability' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.74"), 
            'LoadBalancingMode' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.75"), 
            'MaxSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.76"), 
            'SASAddress' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.77"), 
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.1"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.78"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.79"), 
        },
        iDRACCompEnum.VirtualDisk : {
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.1"), 
            'Name' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.2"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.4"), 
            'Size' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.6"), 
            'WritePolicy' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.10"), 
            'ReadPolicy' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.11"), 
            'Layout' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.13"), 
            'StripeSize' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.14"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20"), 
            'Secured' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.24"), 
            'IsCacheCade' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.25"), 
            'DiskCachePolicy' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.26"), 
            'MediaType' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.33"), 
            'RemainingRedundancy' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.34"), 
            'OperationalState' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.30"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.35"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.36"), 
        },
        iDRACCompEnum.PhysicalDisk : {
            'Number' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.1"), 
            'Name' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2"), 
            'State' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4"), 
            'Model' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.6"), 
            'SerialNumber' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.7"), 
            'Revision' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.8"), 
            'Size' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.11"), 
            'UsedSpace' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.17"), 
            'FreeSpace' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.19"), 
            'BusType' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.21"), 
            'SpareState' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.22"), 
            'PrimaryStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24"), 
            'PPID' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.27"), 
            'SASAddress' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.28"), 
            'NegotiatedSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.29"), 
            'CapableSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.30"), 
            'PredictiveFailureState' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.31"), 
            'CapableSpeed' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.30"), 
            'MediaType' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.35"), 
            'PowerState' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.42"), 
            'DriveFormFactor' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.53"), 
            'Manufacturer' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.3"), 
            'ManufacturingDay' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.32"), 
            'ManufacturingWeek' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.33"), 
            'ManufacturingYear' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.34"), 
            'OperationalState' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.50"), 
            'SecurityStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.52"), 
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.54"), 
            'DeviceDescription' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.55"), 
        },
        "FRU" : {
            'FQDD' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.12"), 
            'ChassisIndex' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.1"), 
            'SerialNumberName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.7"), 
            'RevisionName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.9"), 
            'InformationStatus' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.3"), 
            'ManufacturerName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.6"), 
            'PartNumberName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.8"), 
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.2000.10.1.2"), 
        },
      #  "systemBattery" : {
        #    "ChassisIndex" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBatteryChassisIndex'),
        #    "Index" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBatteryIndex'),
        #    "Status" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBatteryStatus'),
        #    "Reading" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBatteryReading'),
        #    "LocationName" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBatteryLocationName'),
      #  },
        "firmware" : {
            'Status' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.5"), 
            'VersionName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.11"), 
            'StateSettings' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.4"), 
            'Type' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.7"), 
            'Size' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.6"), 
            'chassisIndex' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.1"), 
            'TypeName' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.8"), 
            'StateCapabilities' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.3"), 
            'Index' : ObjectIdentity("1.3.6.1.4.1.674.10892.5.4.300.60.1.2"), 
        },
        "SystemBIOS" : {
            "chassisIndex" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSchassisIndex'),
            "Index" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSIndex'),
        #    "Status" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSStatus'),
        #    "ReleaseDateName" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSReleaseDateName'),
            "VersionName" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSVersionName'),
            "ManufacturerName" : ObjectIdentity('IDRAC-MIB-SMIv2', 'systemBIOSManufacturerName'),
        },
        iDRACCompEnum.Sensors_Amperage : {
            "DeviceID" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.30.1.8'),
            "PrimaryStatus" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.30.1.5'),
            "State" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.30.1.4'),
            "ProbeReading" : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.30.1.6'),
            "Reading"       : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.30.1.16'),
        },
        iDRACCompEnum.Sensors_Battery : {
            "State"           : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.50.1.4'),
            "PrimaryStatus"   : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.50.1.5'),
            "Reading"         : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.50.1.6'),
            "DeviceID"        : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.50.1.7'),
        },
        iDRACCompEnum.Sensors_Intrusion : {
            "State"           : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.300.70.1.4'),
            "Type"            : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.300.70.1.7'),
            "PrimaryStatus"   : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.300.70.1.5'),
            "Reading"         : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.300.70.1.6'),
            "DeviceID"        : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.300.70.1.8'),
        },
        iDRACCompEnum.Sensors_Voltage : {
            "State"           : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.20.1.4'),
            "Reading"         : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.20.1.16'),
            "PrimaryStatus"   : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.20.1.5'),
            "Reading(V)"      : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.20.1.6'),
            "DeviceID"        : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.600.20.1.8'),
        },
        iDRACCompEnum.Sensors_Temperature : {
            "State"           : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.700.20.1.4'),
            "Reading"         : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.700.20.1.16'),
            "PrimaryStatus"   : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.700.20.1.5'),
            "Reading(Degree Celsius)"      : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.700.20.1.6'),
            "DeviceID"        : ObjectIdentity('1.3.6.1.4.1.674.10892.5.4.700.20.1.8'),
        },
    }
    iDRACSNMPViews_FieldSpec = {
        iDRACCompEnum.Memory : {
            "Size" : { 'Type' : 'Bytes', 'InUnits' : "KB" },
        },
        iDRACCompEnum.Controller : {
            "CacheSize" : { 'Type' : 'Bytes', 'InUnits' : 'MB' },
        },
        iDRACCompEnum.CPU : {
            "CPUFamily" : {
                'Lookup'  :  'True',
                'Values' : {
                    "1"                           :  "Other",
                    "2"                         :  "Unknown",
                    "3"                            :  "8086",
                    "4"                           :  "80286",
                    "5"                        :  "Intel386 processor",
                    "6"                        :  "Intel486 processor",
                    "7"                            :  "8087",
                    "8"                           :  "80287",
                    "9"                           :  "80387",
                    "10"                          :  "80487",
                    "11"                        :  "Pentium processor Family",
                    "12"                     :  "Pentium Pro processor",
                    "13"                      :  "Pentium II processor",
                    "14"                     :  "Pentium processor with MMX technology",
                    "15"                        :  "Celeron processor",
                    "16"                  :  "Pentium II Xeon processor",
                    "17"                     :  "Pentium III processor",
                    "18"                 :  "Pentium III Xeon processor",
                    "19"            :  "Pentium III Processor with Intel SpeedStep Technology",
                    "20"                        :  "Itanium processor",
                    "21"                      :  "Intel Xeon",
                    "22"                       :  "Pentium 4 Processor",
                    "23"                    :  "Intel Xeon processor MP",
                    "24"                  :  "Intel Itanium 2 processor",
                    "25"                             :  "K5 Family",
                    "26"                             :  "K6 Family",
                    "27"                        :  "K6-2",
                    "28"                        :  "K6-3",
                    "29"                      :  "AMD Athlon Processor Family",
                    "30"                        :  "AMD2900 Family",
                    "31"                    :  "K6-2+",
                    "32"                        :  "Power PC Family",
                    "33"                     :  "Power PC 601",
                    "34"                     :  "Power PC 603",
                    "35"                 :  "Power PC 603+",
                    "36"                     :  "Power PC 604",
                    "37"                     :  "Power PC 620",
                    "38"                    :  "Power PC x704",
                    "39"                     :  "Power PC 750",
                    "40"                   :  "Intel(R) Core(TM) Duo processor",
                    "41"             :  "Intel(R) Core(TM) Duo mobile processor",
                    "42"            :  "Intel(R) Core(TM) Solo mobile processor",
                    "43"                      :  "Intel(R) Atom(TM) processor",
                    "48"                          :  "Alpha Family",
                    "49"                     :  "Alpha 21064",
                    "50"                     :  "Alpha 21066",
                    "51"                     :  "Alpha 21164",
                    "52"                   :  "Alpha 21164PC",
                    "53"                    :  "Alpha 21164a",
                    "54"                     :  "Alpha 21264",
                    "55"                     :  "Alpha 21364",
                    "56"    :  "AMD Turion(TM) II Ultra Dual-Core Mobile M Processor Family",
                    "57"         :  "AMD Turion(TM) II Dual-Core Mobile M Processor Family",
                    "58"         :  "AMD Athlon(TM) II Dual-Core Mobile M Processor Family",
                    "59"                 :  "AMD Opteron(TM) 6100 Series Processor",
                    "60"                 :  "AMD Opteron(TM) 4100 Series Processor",
                    "61"                 :  "AMD Opteron(TM) 6200 Series Processor",
                    "62"                 :  "AMD Opteron(TM) 4200 Series Processor",
                    "64"                           :  "MIPS Family",
                    "65"                      :  "MIPS R4000",
                    "66"                      :  "MIPS R4200",
                    "67"                      :  "MIPS R4400",
                    "68"                      :  "MIPS R4600",
                    "69"                     :  "MIPS R10000",
                    "80"                          :  "SPARC Family",
                    "81"                     :  "SuperSPARC",
                    "82"                   :  "microSPARC II",
                    "83"                 :  "microSPARC IIep",
                    "84"                     :  "UltraSPARC",
                    "85"                   :  "UltraSPARC II",
                    "86"                  :  "UltraSPARC IIi",
                    "87"                  :  "UltraSPARC III",
                    "88"                 :  "UltraSPARC IIIi",
                    "96"                          :  "68040 Family",
                    "97"                          :  "68xxx",
                    "98"                          :  "68000",
                    "99"                          :  "68010",
                    "100"                         :  "68020",
                    "101"                         :  "68030",
                    "112"                        :  "Hobbit Family",
                    "120"                  :  "Crusoe TM5000 Family",
                    "121"                  :  "Crusoe TM3000 Family",
                    "122"                :  "Efficeon TM8000 Family",
                    "128"                        :  "Weitek",
                    "130"                 :  "Intel(R) Celeron(R) M processor",
                    "131"                   :  "AMD Athlon 64 Processor Family",
                    "132"                    :  "AMD Opteron Processor Family",
                    "133"                    :  "AMD Sempron Processor Family",
                    "134"             :  "AMD Turion 64 Mobile Technology",
                    "135"            :  "Dual-Core AMD Opteron(TM) Processor Family",
                    "136"         :  "AMD Athlon 64 X2 Dual-Core Processor Family",
                    "137"           :  "AMD Turion(TM) 64 X2 Mobile Technology",
                    "138"            :  "Quad-Core AMD Opteron(TM) Processor Family",
                    "139"     :  "Third-Generation AMD Opteron(TM) Processor Family",
                    "140"           :  "AMD Phenom(TM) FX Quad-Core Processor Family",
                    "141"           :  "AMD Phenom(TM) X4 Quad-Core Processor Family",
                    "142"           :  "AMD Phenom(TM) X2 Dual-Core Processor Family",
                    "143"           :  "AMD Athlon(TM) X2 Dual-Core Processor Family",
                    "144"                        :  "PA-RISC Family",
                    "145"                    :  "PA-RISC 8500",
                    "146"                    :  "PA-RISC 8000",
                    "147"                  :  "PA-RISC 7300LC",
                    "148"                    :  "PA-RISC 7200",
                    "149"                  :  "PA-RISC 7100LC",
                    "150"                    :  "PA-RISC 7100",
                    "160"                           :  "V30 Family",
                    "161"         :  "Quad-Core Intel(R) Xeon(R) processor 3200 Series",
                    "162"         :  "Dual-Core Intel(R) Xeon(R) processor 3000 Series",
                    "163"         :  "Quad-Core Intel(R) Xeon(R) processor 5300 Series",
                    "164"         :  "Dual-Core Intel(R) Xeon(R) processor 5100 Series",
                    "165"         :  "Dual-Core Intel(R) Xeon(R) processor 5000 Series",
                    "166"           :  "Dual-Core Intel(R) Xeon(R) processor LV",
                    "167"          :  "Dual-Core Intel(R) Xeon(R) processor ULV",
                    "168"         :  "Dual-Core Intel(R) Xeon(R) processor 7100 Series",
                    "169"         :  "Quad-Core Intel(R) Xeon(R) processor 5400 Series",
                    "170"             :  "Quad-Core Intel(R) Xeon(R) processor",
                    "171"         :  "Dual-Core Intel(R) Xeon(R) processor 5200 Series",
                    "172"         :  "Dual-Core Intel(R) Xeon(R) processor 7200 Series",
                    "173"         :  "Quad-Core Intel(R) Xeon(R) processor 7300 Series",
                    "174"         :  "Quad-Core Intel(R) Xeon(R) processor 7400 Series",
                    "175"        :  "Multi-Core Intel(R) Xeon(R) processor 7400 Series",
                    "176"                            :  "M1 Family",
                    "177"                            :  "M2 Family",
                    "179"               :  "Intel(R) Pentium(R) 4 HT processor",
                    "180"                         :  "AS400 Family",
                    "182"                   :  "AMD Athlon XP Processor Family",
                    "183"                   :  "AMD Athlon MP Processor Family",
                    "184"                      :  "AMD Duron Processor Family",
                    "185"                 :  "Intel Pentium M processor",
                    "186"                 :  "Intel Celeron D processor",
                    "187"                 :  "Intel Pentium D processor",
                    "188"           :  "Intel Pentium Processor Extreme Edition",
                    "189"                 :  "Intel(R) Core(TM) Solo processor",
                    "190"                    :  "Intel(R) Core(TM)2 processor",
                    "191"                 :  "Intel(R) Core(TM)2 Duo processor",
                    "192"                :  "Intel(R) Core(TM)2 Solo processor",
                    "193"             :  "Intel(R) Core(TM)2 Extreme processor",
                    "194"                :  "Intel(R) Core(TM)2 Quad processor",
                    "195"       :  "Intel(R) Core(TM)2 Extreme mobile processor",
                    "196"           :  "Intel(R) Core(TM)2 Duo mobile processor",
                    "197"          :  "Intel(R) Core(TM)2 Solo mobile processor",
                    "198"                   :  "Intel(R) Core(TM) i7 processor",
                    "199"          :  "Dual-Core Intel(R) Celeron(R) Processor",
                    "200"                        :  "IBM390 Family",
                    "201"                            :  "G4",
                    "202"                            :  "G5",
                    "203"                      :  "ESA/390 G6",
                    "204"                  :  "z/Architectur base",
                    "205"                   :  "Intel(R) Core(TM) i5 processor",
                    "206"                   :  "Intel(R) Core(TM) i3 processor",
                    "210"                        :  "VIA C7(TM)-M Processor Family",
                    "211"                        :  "VIA C7(TM)-D Processor Family",
                    "212"                         :  "VIA C7(TM) Processor Family",
                    "213"                       :  "VIA Eden(TM) Processor Family",
                    "214"            :  "Multi-Core Intel(R) Xeon(R) processor",
                    "215"         :  "Dual-Core Intel(R) Xeon(R) processor 3xxx Series",
                    "216"         :  "Quad-Core Intel(R) Xeon(R) processor 3xxx Series",
                    "217"                       :  "VIA Nano(TM) Processor Family",
                    "218"         :  "Dual-Core Intel(R) Xeon(R) processor 5xxx Series",
                    "219"         :  "Quad-Core Intel(R) Xeon(R)  processor 5xxx Series",
                    "221"         :  "Dual-Core Intel(R) Xeon(R) processor 7xxx Series",
                    "222"         :  "Quad-Core Intel(R) Xeon(R) processor 7xxx Series",
                    "223"        :  "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
                    "224"        :  "Multi-Core Intel(R) Xeon(R) processor 3400 Series ",
                    "230"    :  "Embedded AMD Opteron(TM) Quad-Core Processor Family",
                    "231"           :  "AMD Phenom(TM) Triple-Core Processor Family",
                    "232"  :  "AMD Turion(TM) Ultra Dual-Core Mobile Processor Family",
                    "233"       :  "AMD Turion(TM) Dual-Core Mobile Processor Family",
                    "234"             :  "AMD Athlon(TM) Dual-Core Processor Family",
                    "235"                  :  "AMD Sempron(TM) SI Processor Family",
                    "236"                   :  "AMD Phenom(TM) II Processor Family",
                    "237"                   :  "AMD Athlon(TM) II Processor Family",
                    "238"             :  "Six-Core AMD Opteron(TM) Processor Family",
                    "239"                   :  "AMD Sempron(TM) M Processor Family",
                    "250"                          :  "i860",
                    "251"                          :  "i960"
                }
            }
        },
        iDRACCompEnum.NIC : {
            "LinkStatus" : {
                'Lookup'  :  'True',
                'Values' : {
                    "0" : "Warning", 
                    "1" : "OK",      
                    "2" : "Critical",
                    "3" : "Warning", 
                    "4" : "Warning", 
                    "10" : "Warning",
                    "11" : "Warning",
                    "12" : "Warning",
                    "13" : "Warning",
                }
            }
        },
        iDRACCompEnum.VirtualDisk : {
            "Size" : { 'Type' : 'Bytes', 'InUnits' : 'MB' },
            "RAIDTypes" : {
                'Lookup'  :  'True',
                'Values' : {
                    '1'       :  'Other',
                    '2'       :  'RAID-0',
                    '3'       :  'RAID-1',
                    '4'       :  'RAID-5',
                    '5'       :  'RAID-6',
                    '6'       :  'RAID-10',
                    '7'       :  'RAID-50',
                    '8'       :  'RAID-60',
                    '9'       :  'ConcatRAID-1',
                    '10'      :  'ConcatRAID-5'
                }
            },
            "StripeSize" : {
                'Lookup'  :  'True',
                'Values' : {
                    "1" : "Other",
                    "2" : "default",
                    "3" : "512 Bytes",
                    "4" : "1 KB",
                    "5" : "2 KB",
                    "6" : "4 KB",
                    "7" : "8 KB",
                    "8" : "16 KB",
                    "9" : "32 KB",
                    "10" : "64 KB",
                    "11" : "128 KB",
                    "12" : "256 KB",
                    "13" : "512 KB",
                    "14" : "1 MB",
                    "15" : "2 MB",
                    "16" : "4 MB",
                    "17" : "8 MB",
                    "18" : "16 MB",
                }
            }
        },
        iDRACCompEnum.PhysicalDisk : {
            "Size" : { 'Type' : 'Bytes' , 'InUnits' : 'MB' },
            "UsedSpace" : { 'Type' : 'Bytes' , 'InUnits' : 'MB' , 'Metrics' : 'GB'},
            "FreeSize" : { 'Type' : 'Bytes' , 'InUnits' : 'MB', 'Metrics' : 'GB' },
        },
        iDRACCompEnum.System : {
            'PrimaryStatus' : { 'CopyTo' : 'RollupStatus' },
        },
        iDRACCompEnum.PowerSupply : {
            'TotalOutputPower' :  {'UnitScale': '-1', 'UnitAppend' : 'W'},
            'RatedInputWattage' :  {'UnitScale': '-1', 'UnitAppend' : 'W'}
        },
        iDRACCompEnum.Sensors_Temperature : {
            'Reading(Degree Celsius)' :  {'UnitScale': '-1', 'UnitAppend' : 'Degree Celsius'}
        },
        iDRACCompEnum.Sensors_Voltage : {
            'Reading(V)' :  {'UnitScale': '-3', 'UnitAppend' : 'V'}
        }
    }

    iDRACSNMPClassifier = {
        iDRACCompEnum.System : {
            'SysObjectID' : 'SNMPv2-SMI::enterprises\\.674\\.10892\\.5|IDRAC-MIB-SMIv2::outOfBandGroup'
        }
    }

# Agnostic of protocols
iDRACSubsystemHealthSpec = {
    iDRACCompEnum.Memory : { "Component" : iDRACCompEnum.System, "Field" : 'SysMemPrimaryStatus' },
    iDRACCompEnum.CPU : { "Component" : iDRACCompEnum.System, "Field": 'CPURollupStatus' },
    'Sensors_Fan' : { "Component" : iDRACCompEnum.System, "Field": 'FanRollupStatus' },
    iDRACCompEnum.iDRAC : { "Component" : iDRACCompEnum.System, "Field": 'RollupStatus' },
    iDRACCompEnum.PowerSupply : { "Component" : iDRACCompEnum.System, "Field": 'PSRollupStatus' },
    'Storage' : { "Component" : iDRACCompEnum.System, "Field": 'StorageRollupStatus' },
    'License' : { "Component" : iDRACCompEnum.System, "Field": 'LicensingRollupStatus' },
    'Sensors_Voltage' : { "Component" : iDRACCompEnum.System, "Field": 'VoltRollupStatus' },
    'Sensors_Temperature' : { "Component" : iDRACCompEnum.System, "Field": 'TempRollupStatus' },
    'Sensors_Battery' : { "Component" : iDRACCompEnum.System, "Field": 'BatteryRollupStatus' },
    'VFlash' : { "Component" : iDRACCompEnum.System, "Field": 'SDCardRollupStatus' },
    'Sensors_Intrusion' : { "Component" : iDRACCompEnum.System, "Field": 'IntrusionRollupStatus' },
}

iDRACUnionCompSpec = {
   "Sensors":{
        "_components": [
            "ServerSensor",
            "NumericSensor",
            "PSNumericSensor"
        ],
        "_components_enum": [
            iDRACSensorEnum.ServerSensor,
            iDRACSensorEnum.NumericSensor,
            iDRACSensorEnum.PSNumericSensor
        ],
        "_remove_duplicates" : "True",
        "_pivot" : "SensorType",
        "SensorType" : {
            "1": "Battery",
            "2" : "Temperature",
            "3" : "Voltage",
            "5" : "Fan",
            "13" : "Amperage",
            "16" : "Intrusion"
        }
    }
}

iDRACDynamicValUnion = {
    "System":{
        "_complexkeys": {
            "SystemString" : ["FQDD", "AttributeName", "CurrentValue"]
        },
        "_components_enum": [
          iDRACMiscEnum.SystemString
        ],
        "_createFlag" : False
    },
    "NIC":{
        "_complexkeys": {
            "NICString" :["FQDD", "AttributeName", "CurrentValue"],
        },
        "_components_enum": [
          iDRACMiscEnum.NICString,
        ]
    },
    "iDRAC":{
        "_complexkeys": {
            "iDRACEnumeration" :["FQDD", "InstanceID", "CurrentValue"],
            "iDRACString" :["FQDD", "InstanceID", "CurrentValue"]
        },
        "_components_enum": [
          iDRACMiscEnum.iDRACEnumeration,
          iDRACMiscEnum.iDRACString
        ]
    },
    "iDRACNIC":{
        "_complexkeys": {
            "iDRACEnumeration" :["FQDD", "InstanceID", "CurrentValue"],
            "iDRACString" :["FQDD", "InstanceID", "CurrentValue"]
        },
        "_components_enum": [
          iDRACMiscEnum.iDRACEnumeration,
          iDRACMiscEnum.iDRACString
        ],
        "_createFlag" : False
    }    
}

iDRACMergeJoinCompSpec = {
   "NIC" : {
        "_components" : [
            ["NIC", "FQDD", "NICStatistics", "FQDD"],
            ["NIC", "FQDD", "NICCapabilities", "FQDD"],
            ["NIC", "FQDD", "SwitchConnection", "FQDD"],
            ["NIC", "FQDD", "HostNICView", "DeviceFQDD"]
        ],
        "_components_enum": [
            iDRACCompEnum.NIC,
            iDRACMiscEnum.NICStatistics,
            iDRACMiscEnum.NICCapabilities,
            iDRACMiscEnum.SwitchConnection,
            iDRACMiscEnum.HostNICView
        ]
   },
   "FC" : {
        "_components" : [
            ["FC", "FQDD", "FCStatistics", "FQDD"]
        ],
        "_components_enum": [
            iDRACCompEnum.FC,
            iDRACMiscEnum.FCStatistics
        ]
   }
}
 

class iDRAC(iDeviceDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(iDRAC, self).__init__(iDeviceRegistry("iDRAC", srcdir, iDRACCompEnum))
        else:
            super().__init__(iDeviceRegistry("iDRAC", srcdir, iDRACCompEnum))
        self.srcdir = srcdir
        self.protofactory.add(PWSMAN(
            selectors = { }, #"__cimnamespace" : "root/dcim" },
            views = iDRACWsManViews,
            view_fieldspec = iDRACWsManViews_FieldSpec,
            compmap = iDRACSWCompMapping,
            cmds = iDRACWsManCmds
        ))
        self.protofactory.add(PREDFISH(
            views = iDRACRedfishViews,
            cmds = iDRACRedfishCmds
        ))
        if PySnmpPresent:
            self.protofactory.add(PSNMP(
                views = iDRACSNMPViews,
                classifier = iDRACSNMPClassifier,
                view_fieldspec = iDRACSNMPViews_FieldSpec
            ))
        self.protofactory.addCTree(iDRACComponentTree)
        self.protofactory.addSubsystemSpec(iDRACSubsystemHealthSpec)
        self.protofactory.addClassifier(iDRACClassifier)

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return iDRACEntity(self.ref, protofactory, ipaddr, creds, self.srcdir, 'iDRAC')

    def my_aliases(self):
        return ['Server']


class iDRACEntity(iDeviceDriver):
    def __init__(self, ref, protofactory, ipaddr, creds, srcdir, name):
        if PY2:
            super(iDRACEntity, self).__init__(ref, protofactory, ipaddr, creds)
        else:
            super().__init__(ref, protofactory, ipaddr, creds)
        self.config_dir = os.path.join(srcdir, name, "Config")
        self.ePowerStateEnum = PowerStateEnum
        self.job_mgr = iDRACJobs(self)
        self.config_mgr = iDRACConfig(self)
        self.log_mgr = iDRACLogs(self)
        self.update_mgr = iDRACUpdate(self)
        self.license_mgr = iDRACLicense(self)
        self.user_mgr = iDRACCredsMgmt(self)
        self.comp_union_spec = iDRACUnionCompSpec
        self.comp_misc_join_spec = iDRACDynamicValUnion
        self.comp_merge_join_spec = iDRACMergeJoinCompSpec
        self.device_type = 'Server'

    def my_reset(self):
        if hasattr(self, 'update_mgr'):
            self.update_mgr.reset()
        #self.config_mgr.reset()
        #self.log_mgr.reset()

    def my_fix_obj_index(self, clsName, key, js):
        retval = None
        if clsName == "System":
            if 'ServiceTag' not in js or js['ServiceTag'] is None:
                js['ServiceTag'] = self.ipaddr
            retval = js['ServiceTag']
        else:
            if 'DeviceID' in js:
                retval = js['DeviceID']
            if retval is None:
                retval = clsName + "_null"
        return retval

    def _isin(self, parentClsName, parent, childClsName, child):
        if TypeHelper.resolve(parentClsName) == "Controller" and \
           TypeHelper.resolve(childClsName) == "PhysicalDisk" and \
           ("Disk.Direct" not in self._get_obj_index(childClsName, child)):
           return False
        return self._get_obj_index(parentClsName, parent) in \
               self._get_obj_index(childClsName, child)

    def _get_MemoryType(self, idx):
        ty = self._get_field_device("Memory", "type", idx)
        return self.ref.Translate("Memory", "type", ty)

    @property
    def ServiceTag(self):
        return self._get_field_device(self.ComponentEnum.System, "ServiceTag")

    @property
    def SystemID(self):
        return self._get_field_device(self.ComponentEnum.System, "SystemID")

    @property
    def SystemIDInHex(self):
        sid = self._get_field_device(self.ComponentEnum.System, "SystemID")
        # following line is kludge for reflection api
        if sid == None or sid == '<not_found>': sid = '0'
        return (('0000' + str(hex(int(sid)))[2:])[-4:])

    @property
    def Model(self):
        return self._get_field_device(self.ComponentEnum.System, "Model")

    @property
    def ServerGeneration(self):
        return self._get_field_device(self.ComponentEnum.System, "SystemGeneration")

    @property
    def CMCIPAddress(self):
        val = self._get_field_device(self.ComponentEnum.System, "CMCIP")
        if val is None or val in ['<not_found>', "Not Available", '']:
            return None
        return val

    @property
    def IsRackStyleManaged(self):
        # return true if rack server, pounce platform
        if not "Modular" in self.get_server_generation():
            return True

        # check if psu is enumerable from idrac. if yes, it is rsm mode
        self.get_partial_entityjson(self.ComponentEnum.PowerSupply)
        psfq= self._get_field_device(self.ComponentEnum.PowerSupply, "FQDD", 0)
        if psfq is None or psfq in ['<not_found>', "Not Available", '']:
            return False
        return True

    @property
    def AssetTag(self):
        return self._get_field_device(self.ComponentEnum.System, "AssetTag")

    @property
    def IDRACURL(self):
        self.get_partial_entityjson(self.ComponentEnum.iDRAC)
        return self._get_field_device(self.ComponentEnum.iDRAC, "URLString")

    @property
    def IDRACFirmwareVersion(self):
        self.get_partial_entityjson(self.ComponentEnum.iDRAC)
        return self._get_field_device(self.ComponentEnum.iDRAC, "FirmwareVersion")

    @property
    def PowerCap(self):
        return self._get_field_device(self.ComponentEnum.System, "PowerCap")

    @property
    def PowerState(self):
        return self._get_field_device(self.ComponentEnum.System, "PowerState")

    @property
    def IDRACDNSName(self):
        self.get_partial_entityjson(self.ComponentEnum.iDRAC)
        return self._get_field_device(self.ComponentEnum.iDRAC, "DnsDRACName")

    def _should_i_include(self, component, entry):
        #if component in ["PhysicalDisk"]:
        #    if entry["RollupStatus"] == 0 or entry["PrimaryStatus"] == 0: 
        #        return False
        if component in ["Sensors_Battery"]:
           if "OtherSensorTypeDescription" in entry:
                if not entry["OtherSensorTypeDescription"] == 'Battery':
                    return False
        if component == "NIC":
            supportedBootProtocol = ""
            sbpDict = {"FCoEBootSupport" : "FCOE,",
                        "PXEBootSupport" : "PXE,",
                        "iSCSIBootSupport" : "iSCSI,"}  
            for bootproto in sbpDict:
                if(bootproto in entry) and (entry[bootproto] == "2"):
                    supportedBootProtocol=supportedBootProtocol+sbpDict[bootproto]
            if(supportedBootProtocol != ""):
                entry["SupportedBootProtocol"] = supportedBootProtocol.rstrip(',')
                
            nicCapabilities = ""
            ncpDict = {"WOLSupport" : "WOL,",
                        "FlexAddressingSupport" : "FlexAddressing,",
                        "VFSRIOVSupport" : "SR-IOV,",
                        "iSCSIOffloadSupport" : "iSCSI Offload,",
                        "FCoEOffloadSupport" : "FCoE Offload,",
                        "NicPartitioningSupport" : "Partitioning,",
                        "TCPChimneySupport" : "TOE,",
                        "DCBExchangeProtocol" : "DCB,"}  
            for ncp in ncpDict:
                if(ncp in entry) and (entry[ncp] == "2"):
                    nicCapabilities=nicCapabilities+ncpDict[ncp]
            if(nicCapabilities != ""):
                entry["NICCapabilities"] = nicCapabilities.rstrip(',')
        return True

    def _get_topology_info(self):
        return iDRACTopologyInfo(self.get_json_device())

    def _get_topology_influencers(self):
        return { 'System' : [
                        'ServiceTag',
                        'SystemGeneration',
                        'Model',
                        'GroupManager'
                ] }

class iDRACTopologyInfo(iDeviceTopologyInfo):
    def __init__(self, json):
        if PY2:
            super(iDeviceTopologyInfo, self).__init__('Server', json)
        else:
            super().__init__('Server', json)

    def my_static_groups(self, tbuild):
        tbuild.add_group('Dell', static=True)
        tbuild.add_group('Dell Servers', 'Dell', static=True)
        tbuild.add_group('Dell Rack Workstations', 'Dell', static=True)
        tbuild.add_group('Dell Modular Servers', 'Dell Servers', static=True)
        tbuild.add_group('Dell Rack Servers', 'Dell Servers', static=True)
        tbuild.add_group('Dell FM Servers', 'Dell Servers', static=True)
        tbuild.add_group('Dell Unmanaged Servers', 'Dell Servers', static=True)
        tbuild.add_group('Dell iDRAC GMs', 'Dell', static=True)

    def my_groups(self, tbuild):

        if 'ServiceTag' not in self.system:
            return False

        serviceTag = self.system['ServiceTag']
        if 'SystemGeneration' in self.system:
            grpname = 'Dell Unmanaged Servers'
            if re.match('.* Modular', self.system['SystemGeneration']):
                grpname = 'Dell Modular Servers'
            elif re.match('.* Monolithic|DCS', self.system['SystemGeneration']):
                grpname = 'Dell Rack Servers'
            self._add_myself(tbuild, grpname)

        if 'Model' in self.system and self.system['Model'] == 'FMServer':
            fmgrp = 'FMServer-' + serviceTag
            tbuild.add_group(fmgrp, 'Dell FM Servers')
            self._add_myself(tbuild, fmgrp)

        if 'GroupManager' in self.system and self.system['GroupManager']:
            fmgrp = 'iGM-' + self.system['GroupManager']
            tbuild.add_group(fmgrp, 'Dell iDRAC GMs')
            self._add_myself(tbuild, fmgrp)

        return True

    def my_assoc(self, tbuild):
        if 'ServiceTag' not in self.system:
            return False

        serviceTag = self.system['ServiceTag']

        if 'ChassisServiceTag' not in self.system:
            # Rack Server or Rack Station or Tower system
            return True

        chassisSvcTag = self.system['ChassisServiceTag']

        if chassisSvcTag is None or chassisSvcTag == serviceTag:
            return True

        ### Commented out this section as slot
        ### returned by iDRAC is different from CMC-Slot FQDD
        #slot = 'undef'
        #if 'BaseBoardChassisSlot' in self.system:
        #    slot = self.system['BaseBoardChassisSlot']
        #
        #self._add_assoc(tbuild, ['CMC', chassisSvcTag],
        #                        ['ComputeModule', slot],
        #                        [self.mytype, self.system['Key']])

        return True
