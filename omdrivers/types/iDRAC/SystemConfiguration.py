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
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType, FQDDHelper
from omsdk.typemgr.BuiltinTypes import RootClassType
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.BIOS import *
from omdrivers.types.iDRAC.NIC import *
from omdrivers.types.iDRAC.FCHBA import *
from omdrivers.types.iDRAC.RAID import *
import sys
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class SystemConfiguration(RootClassType):

    def __init__(self, parent = None, loading_from_scp=False):
        if PY2:
            super(SystemConfiguration, self).__init__("SystemConfiguration", None, parent)
        else:
            super().__init__("SystemConfiguration", None, parent)
        self.LifecycleController = LifecycleController(parent=self, loading_from_scp=loading_from_scp)
        self.System = System(parent=self, loading_from_scp=loading_from_scp)
        self.iDRAC = iDRAC(parent=self, loading_from_scp=loading_from_scp)
        self.FCHBA = ArrayType(FCHBA, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self.NIC = ArrayType(NetworkInterface, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self.BIOS = BIOS(parent=self, loading_from_scp=loading_from_scp)
        self.Controller = ArrayType(Controller, parent=self, index_helper=FQDDHelper(), loading_from_scp=loading_from_scp)
        self._ignore_attribs('ServiceTag', 'Model', 'TimeStamp')
        self.commit(loading_from_scp)

