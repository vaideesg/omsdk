#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan
#
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
