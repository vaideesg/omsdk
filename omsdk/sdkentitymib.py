from enum import Enum
from omsdk.sdkcenum import EnumWrapper
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

EntityCompEnum = EnumWrapper("EntityCompEnum", {
        "System" : "System",
        "other" : "other",
        "chassis" : "chassis",
        "backplane" : "backplane",
        "container" : "container",
        "powerSupply" : "powerSupply",
        "fan" : "fan",
        "sensor" : "sensor",
        "module" : "module",
        "port" : "port",
        "stack" : "stack",
        "cpu" : "cpu",
        "Entity" : "Entity"
    }).enum_type


if PySnmpPresent:
    EntityComponentTree = {
        "Full" : [ 
            EntityCompEnum.stack
        ],
        EntityCompEnum.stack : [
            EntityCompEnum.chassis
        ],
        EntityCompEnum.chassis : [
            EntityCompEnum.container
        ],
        EntityCompEnum.container : [
            EntityCompEnum.module
        ],
        EntityCompEnum.module : [
            EntityCompEnum.port,
            EntityCompEnum.fan,
            EntityCompEnum.powerSupply,
        ]
    }

    EntitySNMPViews = {
        EntityCompEnum.Entity : {
            'FQDD' : ObjectIdentity('ENTITY-MIB', 'entPhysicalIndex'),
            'Name' : ObjectIdentity('ENTITY-MIB', 'entPhysicalName'),
            'Description' : ObjectIdentity('ENTITY-MIB', 'entPhysicalDescr'),
            'ContainedIn' : ObjectIdentity('ENTITY-MIB', 'entPhysicalContainedIn'),
            'Class' : ObjectIdentity('ENTITY-MIB', 'entPhysicalClass'),
            'HardwareRev' : ObjectIdentity('ENTITY-MIB', 'entPhysicalHardwareRev'),
            'FirmwareRev' : ObjectIdentity('ENTITY-MIB', 'entPhysicalSoftwareRev'),
            'ParentRelPos' : ObjectIdentity('ENTITY-MIB', 'entPhysicalParentRelPos'),
            'SerialNo' : ObjectIdentity('ENTITY-MIB', 'entPhysicalSerialNum'),
            'Manufacturer' : ObjectIdentity('ENTITY-MIB', 'entPhysicalMfgName'),
            'Model' : ObjectIdentity('ENTITY-MIB', 'entPhysicalModelName'),
            'AssetTag' : ObjectIdentity('ENTITY-MIB', 'entPhysicalAssetID'),
            'IsFRU' : ObjectIdentity('ENTITY-MIB', 'entPhysicalIsFRU'),
    #        'ManufacturerDate' : ObjectIdentity('ENTITY-MIB', 'entPhysicalMfgDate'),
        }
    }
else:        
    EntityComponentTree = {}
    EntitySNMPViews = {}
