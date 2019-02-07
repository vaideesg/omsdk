from enum import Enum
from omsdk.sdkdevice import iDeviceDiscovery, iDeviceRegistry, iDeviceDriver
from omsdk.sdkcenum import EnumWrapper
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkproto import PSNMP
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto import rfc1902
    from pysnmp import debug
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False


CompellentCompEnum = EnumWrapper('CompellentCompEnum', {
    "System" : "System",
    "Controller" : "Controller",
    "Enclosure" : "Enclosure",
    "Disk" : "Disk",
    "Volume" : "Volume",
    "EnclosurePSU" : "EnclosurePSU",
    "UPS" : "UPS",
    "PowerSupply" : "PowerSupply",
    "EnclosureFan" : "EnclosureFan",
    "EnclosureIOM" : "EnclosureIOM",
    "ControllerFan" : "ControllerFan",
}).enum_type

if PySnmpPresent:
    CompellentSNMPViews = {
     "System" : {
		'ProductID' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.1'),
		'Description' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.2'),
		'Vendor' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.3'),
		'Version' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.4'),
        'ServiceTag' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.5'),
        'Status' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.6'),
		'URLString' : ObjectIdentity('1.3.6.1.4.1.674.11000.2000.500.1.2.8')
     },
     "StorageCenter" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.1"), 
       'IPv6MgmtIPPrefix' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.12"), 
       'Location' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.6"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.3"), 
       'MangementIP' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.8"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.2"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.4"), 
       'IPv6MgmtIP' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.11"), 
       'SerialNumber' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.9"), 
       'Contact' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.29.1.5"), 
     },
     "Controller" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.1"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.2"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.3"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.4"), 
       'Model' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.7"), 
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.8"), 
       'AssetTag' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.9"), 
       'Leader' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.12"), 
       'IpAddress' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.5"), 
       'IPv6Eth0IPPrefix' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.11"), 
       'IPv6Eth0IP' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.10"), 
       'ForceTrap' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.13.1.6"), 
     },
     "Disk" : { 
       #'scDiskIndex' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.1"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.2"), 
       #'scDiskStatusMsg' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.6"), 
       'Position' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.4"), 
       'Size' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.9"), 
       'Enclosure' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.11"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.3"), 
       'Healthy' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.5"), 
       'IoPortType' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.14.1.10"), 
     },
     "Enclosure" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.1"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.2"), 
       'AssetTag' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.10"), 
       'Type' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.6"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.3"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.4"), 
       'Model' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.7"), 
       'ServiceTag' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.15.1.9"), 
     },
     "EnclosureFan" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.20.1.1"), 
       'Location' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.20.1.4"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.20.1.2"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.20.1.3"), 
     },
     "EnclosurePSU" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.21.1.1"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.21.1.2"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.21.1.3"), 
       'Position' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.21.1.4"), 
     },
     "EnclosureIOM" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.22.1.1"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.22.1.3"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.22.1.2"), 
       'Position' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.22.1.4"), 
     },
     "ControllerFan" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.16.1.1"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.16.1.4"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.16.1.2"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.16.1.3"), 
     },
     "Volume" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.26.1.1"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.26.1.4"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.26.1.3"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.26.1.2"), 
     },
     "UPS" : { 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.30.1.1"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.30.1.3"), 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.30.1.4"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.30.1.2"), 
       'BatteryLife' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.30.1.5"), 
     },
     "PowerSupply" : { 
       'Name' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.17.1.4"), 
       'ID' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.17.1.2"), 
       'Status' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.17.1.3"), 
       #'Index' : ObjectIdentity("1.3.6.1.4.1.674.11000.2000.500.1.2.17.1.1"), 
     },
    }
    CompellentSNMPClassifier = {
        'SysObjectID' : 'SNMPv2-SMI::enterprises\.674\.11000'
    }

    CompellentComponentTree = {
        "Full" : [ 
            CompellentCompEnum.System
        ]
    }
else:
    CompellentSNMPViews = {}
    CompellentComponentTree = {}
    CompellentSNMPClassifier = {}

class Compellent(iDeviceDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(Compellent, self).__init__(iDeviceRegistry("Compellent", srcdir, CompellentCompEnum))
        else:
            super().__init__(iDeviceRegistry("Compellent", srcdir, CompellentCompEnum))
        if PySnmpPresent:
            self.protofactory.add(PSNMP(
                views = CompellentSNMPViews,
                classifier=CompellentSNMPClassifier
            ))
        self.protofactory.addCTree(CompellentComponentTree)

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return iDeviceDriver(self.ref, protofactory, ipaddr, creds)

