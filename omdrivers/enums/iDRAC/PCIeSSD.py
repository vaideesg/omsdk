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

BusProtocolTypes = EnumWrapper("BusProtocolTypes", {
    "PCIe" : "PCIe",
}).enum_type

BusProtocolVersionTypes = EnumWrapper("BusProtocolVersionTypes", {
    "T_2_0" : "2.0",
    "T_2_1" : "2.1",
    "T_3_0" : "3.0",
    "T_3_1" : "3.1",
    "Unknown" : "Unknown",
}).enum_type

CapableSpeedTypes = EnumWrapper("CapableSpeedTypes", {
    "T_2_5_GT_s" : "2.5 GT/s",
    "T_5_0_GT_s" : "5.0 GT/s",
    "T_8_0_GT_s" : "8.0 GT/s",
    "Unknown" : "Unknown",
}).enum_type

CryptographicEraseTypes = EnumWrapper("CryptographicEraseTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

DeviceProtocolTypes = EnumWrapper("DeviceProtocolTypes", {
    "NVMe_1_1" : "NVMe 1.1",
    "Nvme1_0" : "Nvme1.0",
    "Unknown" : "Unknown",
}).enum_type

FailurePredictedTypes = EnumWrapper("FailurePredictedTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

PcieMaxLinkWidthTypes = EnumWrapper("PcieMaxLinkWidthTypes", {
    "Unknown" : "Unknown",
    "x1" : "x1",
    "x2" : "x2",
    "x4" : "x4",
    "x8" : "x8",
}).enum_type

PcieNegotiatedLinkSpeedTypes = EnumWrapper("PcieNegotiatedLinkSpeedTypes", {
    "T_2_5_GT_s" : "2.5 GT/s",
    "T_5_0_GT_s" : "5.0 GT/s",
    "T_8_0_GT_s" : "8.0 GT/s",
    "Unknown" : "Unknown",
}).enum_type

PcieNegotiatedLinkWidthTypes = EnumWrapper("PcieNegotiatedLinkWidthTypes", {
    "Unknown" : "Unknown",
    "x1" : "x1",
    "x2" : "x2",
    "x4" : "x4",
    "x8" : "x8",
}).enum_type

SecureEraseTypes = EnumWrapper("SecureEraseTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

SmartStatusTypes = EnumWrapper("SmartStatusTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

StateTypes = EnumWrapper("StateTypes", {
    "Failed" : "Failed",
    "Not_Ready_Locked" : "Not Ready/Locked",
    "Overheat" : "Overheat",
    "ReadOnly" : "ReadOnly",
    "Ready" : "Ready",
    "Unknown" : "Unknown",
}).enum_type

