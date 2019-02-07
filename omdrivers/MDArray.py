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


MDArrayCompEnum = EnumWrapper('MDArrayCompEnum', {
    "System" : "System",
}).enum_type

if PySnmpPresent:
    MDArraySNMPViews = {
     "System" : {
		'Name' : ObjectIdentity('1.3.6.1.4.1.674.10893.2.31.500.1.1'),
		'WWID' : ObjectIdentity('1.3.6.1.4.1.674.10893.2.31.500.1.2'),
		'ServiceTag' : ObjectIdentity('1.3.6.1.4.1.674.10893.2.31.500.1.3'),
		'ProductID' : ObjectIdentity('1.3.6.1.4.1.674.10893.2.31.500.1.5'),
		'Status' : ObjectIdentity('1.3.6.1.4.1.674.10893.2.31.500.1.7'),
     }
    }
    MDArraySNMPClassifier = {
        'SysObjectID' : 'SNMPv2-SMI::enterprises\\.674\\.10893'
    }

    MDArrayComponentTree = {
        "Full" : [ 
            MDArrayCompEnum.System
        ]
    }
else:
    MDArraySNMPViews = {}
    MDArrayComponentTree = {}
    MDArraySNMPClassifier = {}

class MDArray(iDeviceDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(MDArray, self).__init__(iDeviceRegistry("MDArray", srcdir, MDArrayCompEnum))
        else:
            super().__init__(iDeviceRegistry("MDArray", srcdir, MDArrayCompEnum))
        if PySnmpPresent:
            self.protofactory.add(PSNMP(
                views = MDArraySNMPViews,
                classifier = MDArraySNMPClassifier
            ))
        self.protofactory.addCTree(MDArrayComponentTree)

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return iDeviceDriver(self.ref, protofactory, ipaddr, creds)

