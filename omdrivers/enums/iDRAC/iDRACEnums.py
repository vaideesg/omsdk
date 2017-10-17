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
from omsdk.sdkcenum import EnumWrapper, TypeHelper
import logging

logger = logging.getLogger(__name__)

iDRACLicenseEnum = EnumWrapper("iDRACLicenseEnum", {
    "License" : "License",
    "LicensableDevice" : "LicensableDevice",
    }).enum_type

iDRACFirmEnum = EnumWrapper("iDRACFirmEnum", {
    "Firmware" : "Firmware",
    }).enum_type


iDRACLogsEnum = EnumWrapper("iDRACLogEnum", {
    "Logs" : "Logs",
    "SELLog" : "SELLog"
    }).enum_type

JobStatusEnum = EnumWrapper("iDRACJSE",  {
    'Success' : 'Success',
    'InProgress' : 'InProgress',
    'Failed' : 'Failed',
    'Invalid' : 'Invalid',
    }).enum_type

ReturnValue = EnumWrapper("RV", {
    "Success" : 0,
    "Error" : 2,
    "JobCreated" : 4096,
    "Invalid" : -1,
    }).enum_type

iDRACJobsEnum = EnumWrapper("iDRACJobEnum", {
    "Jobs" : "Jobs",
    }).enum_type

iDRACOSDJobsEnum = EnumWrapper("iDRACOSDJobEnum", {
    "OSDJobs" : "OSDJobs",
    }).enum_type

PowerStateEnum = EnumWrapper("PSE",  { "PowerOn" : 2,
    "SoftPowerCycle" : 5,
    "SoftPowerOff" : 8,
    "PowerCycle" : 9,
    "HardReset" : 10,
    "DiagnosticInterrupt" : 11,
    "GracefulPowerOff" : 12
    }).enum_type

PowerBootEnum = EnumWrapper("PSE",  { "Enabled" : 2,
    "Disabled" : 3,
    "Reset" : 11,
    }).enum_type

ConfigStateEnum = EnumWrapper("CSE",  {
    "Enabled" : 'Enabled',
    "Disabled" : 'Disabled',
    "Unknown" : 'Unknown',
    }).enum_type

RebootJobType = EnumWrapper("RJT", {
    'PowerCycle' : 1, # 30 s
    'GracefulRebootWithoutShutdown' : 2, # 5 min
    'GracefulRebootWithForcedShutdown' :  3 # 5 min
}).enum_type

BootModeEnum = EnumWrapper('BME', {
    'Bios' : 'Bios',
    'Uefi' : 'Uefi',
    'Unknown' : 'Unknown'
}).enum_type

BlinkLEDEnum = EnumWrapper('BL', {
    # Off and Disable are same
    'Off'     : 0,
    'Disable' : 0,
    # On and Enable are same
    'On'      : 1,
    'Enable'  : 1,
    # OnForDuration and EnableForDuration are same
    'OnForDuration'     : 2,
    'EnableForDuration' : 2
}).enum_type

BIOSPasswordTypeEnum = EnumWrapper("BIOSPasswordType", {
    'System' : 1,
    'Setup' : 2
}).enum_type

ExportFormatEnum = EnumWrapper("ExportFormatEnum", {
    'XML' : 'XML',
    'JSON' : 'JSON',
}).enum_type

ExportMethodEnum = EnumWrapper("ExportMethod", {
    'Default' : 'Default',
    'Clone' : 'Clone',
    'Replace' : 'Replace',
}).enum_type

ResetToFactoryPreserveEnum = EnumWrapper('RFD', {
    'ResetExceptNICAndUsers' : 0,
    'ResetAll' : 1,
    'ResetAllExceptDefaultUser' : 2
}).enum_type

ResetForceEnum = EnumWrapper('RFD', {
    'Graceful' : 0,
    'Force' : 1,
}).enum_type

SCPTargetEnum = EnumWrapper("SCPTargetEnum", {
    'ALL' :'ALL',
    'IDRAC' : 'IDRAC',
    'BIOS' : 'BIOS',
    'NIC' : 'NIC',
    'RAID' : 'RAID',
    }).enum_type

RAIDLevelsEnum = EnumWrapper("RLE", {
    'RAID_0' : 'RAID 0',
    'RAID_1' : 'RAID 1',
    'RAID_5' : 'RAID 5',
    'RAID_6' : 'RAID 6',
    'RAID_10' : 'RAID 10',
    'RAID_50' : 'RAID 50',
    'RAID_60' : 'RAID 60',
    }).enum_type

LicenseApiOptionsEnum = EnumWrapper("LAO", {
    'NoOptions' : 0,
    'Force' : 1,
    'All' : 2
}).enum_type

TLSOptions_Map = {
    'TLS_1_0' : 'TLS 1.0 and Higher',
    'TLS_1_1' : 'TLS 1.1 and Higher',
    'TLS_1_2' : 'TLS 1.2 Only'
}

TLSOptions = EnumWrapper("TLS", TLSOptions_Map).enum_type

SSLBits_Map =  {
    'S128' : '128-Bit or higher',
    'S168' : '168-Bit or higher',
    'S256' : '256-Bit or higher',
    'Auto' : 'Auto Negotiate'
}

SSLBits = EnumWrapper("SSL", SSLBits_Map).enum_type

SSLCertTypeEnum = EnumWrapper("SSLCertTypeEnum", {
    'Web_Server_Cert': 1,
    'CA_Cert': 2,
    'Custom_Signing_Cert': 3,
    'Client_Trust_Cert': 4
}).enum_type

ShutdownTypeEnum = EnumWrapper('STE', {
    'Graceful' : 0,
    'Forced' : 1,
    'NoReboot' : 2,
}).enum_type

HostEndPowerStateEnum = EnumWrapper('EPSE', {
    'On' : 1,
    'Off' : 2,
}).enum_type

UserPrivilegeEnum = EnumWrapper("UserPrivilegeEnum", {
    "Administrator" : 511,
    "Operator" : 499,
    "ReadOnly" : 1,
    "NoPrivilege" : 0,
    }).enum_type

SNMPTrapFormatEnum = EnumWrapper("SNMPTrapFormatEnum", {
    "SNMPv1" : 'SNMPv1',
    "SNMPv2" : 'SNMPv2',
    "SNMPv3" : 'SNMPv3',
    }).enum_type

SNMPProtocolEnum = EnumWrapper("SPE", {
    "All" : 'All',
    "SNMPv3" : 'SNMPv3',
    }).enum_type
