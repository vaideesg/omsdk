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
from omsdk.sdkcenum import EnumWrapper
import sys
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

BootScanSelectionTypes = EnumWrapper("BootScanSelectionTypes", {
    "Disabled" : "Disabled",
    "FabricDiscovered" : "FabricDiscovered",
    "FirstLUN" : "FirstLUN",
    "FirstLUN0" : "FirstLUN0",
    "FirstNOTLUN0" : "FirstNOTLUN0",
    "SpecifiedLUN" : "SpecifiedLUN",
}).enum_type

FCTapeTypes = EnumWrapper("FCTapeTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

FramePayloadSizeTypes = EnumWrapper("FramePayloadSizeTypes", {
    "Auto" : "Auto",
    "T_1024" : "1024",
    "T_2048" : "2048",
    "T_2112" : "2112",
    "T_512" : "512",
}).enum_type

HardZoneTypes = EnumWrapper("HardZoneTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

PortSpeedTypes = EnumWrapper("PortSpeedTypes", {
    "Auto" : "Auto",
    "T_16G" : "16G",
    "T_1G" : "1G",
    "T_2G" : "2G",
    "T_32G" : "32G",
    "T_4G" : "4G",
    "T_8G" : "8G",
}).enum_type

