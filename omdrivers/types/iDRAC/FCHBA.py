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
from omdrivers.enums.iDRAC.FCHBA import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.typemgr.BuiltinTypes import *
import sys
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class FCHBA(ClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        if PY2: 
            super(FCHBA, self).__init__("Component", None, parent)
        else: 
            super().__init__("Component", None, parent)
        self.BootScanSelection = EnumTypeField(BootScanSelectionTypes.Disabled,BootScanSelectionTypes, parent=self)
        # readonly attribute
        self.BusDeviceFunction = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.ChipMdl = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.DeviceName = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute
        self.EFIVersion = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FCTape = EnumTypeField(FCTapeTypes.Disabled,FCTapeTypes, parent=self)
        self.FabricLoginRetryCount = IntField(3, parent=self)
        self.FabricLoginTimeout = IntField(3000, parent=self)
        # readonly attribute
        self.FamilyVersion = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        self.FirstFCTargetLUN = IntField(None, parent=self)
        self.FirstFCTargetWWPN = WWPNAddressField(None, parent=self)
        self.FramePayloadSize = EnumTypeField(FramePayloadSizeTypes.Auto,FramePayloadSizeTypes, parent=self)
        self.HardZone = EnumTypeField(HardZoneTypes.Disabled,HardZoneTypes, parent=self)
        self.HardZoneAddress = IntField(0, parent=self)
        self.LinkDownTimeout = IntField(3000, parent=self)
        self.LoopResetDelay = IntField(5, parent=self)
        # readonly attribute
        self.PCIDeviceID = StringField("", parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PortDownRetryCount = IntField(None, parent=self)
        self.PortDownTimeout = IntField(3000, parent=self)
        self.PortLoginRetryCount = IntField(3, parent=self)
        self.PortLoginTimeout = IntField(3000, parent=self)
        # readonly attribute populated by iDRAC
        self.PortNumber = IntField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.PortSpeed = EnumTypeField(PortSpeedTypes.Auto,PortSpeedTypes, parent=self)
        self.SecondFCTargetLUN = IntField(None, parent=self)
        self.SecondFCTargetWWPN = WWPNAddressField(None, parent=self)
        self.VirtualWWN = WWPNAddressField(None, parent=self)
        self.VirtualWWPN = WWPNAddressField(None, parent=self)
        # readonly attribute populated by iDRAC
        self.WWN = WWPNAddressField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        # readonly attribute populated by iDRAC
        self.WWPN = WWPNAddressField(None, parent=self, modifyAllowed = False, deleteAllowed = False)
        self.commit(loading_from_scp)

