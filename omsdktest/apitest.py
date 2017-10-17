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
import os
import sys
sys.path.append(os.getcwd())
import xml.etree.ElementTree as ET
import re
from omsdk.typemgr.ClassType import *
from omsdk.typemgr.FieldType import *
from omsdk.typemgr.BuiltinTypes import *
from omsdk.sdkcreds import UserCredentials
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.enums.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.BIOS import *
from omdrivers.types.iDRAC.RAID import *
from omdrivers.types.iDRAC.NIC import *
from omdrivers.types.iDRAC.FCHBA import *
from omdrivers.types.iDRAC.SystemConfiguration import *
from omdrivers.lifecycle.iDRAC.SCPParsers import XMLParser
from omsdk.sdkinfra import sdkinfra
from omsdk.simulator.devicesim import Simulator
logging.basicConfig(level=logging.ERROR)
from omsdk.sdkfile import FileOnShare
from omsdk.sdkprint import PrettyPrint
import logging
from omdrivers.lifecycle.iDRAC.RAIDHelper import *


myshare = FileOnShare(remote ="\\\\<share>\\Share",
        mount_point='Z:\\', isFolder=True,
        creds = UserCredentials("user@domain", "password"))

ipaddr = '192.168.0.1'
logging.basicConfig(level=logging.DEBUG)
myshare.valid = True

Simulator.start_simulating()
sd = sdkinfra()
sd.importPath()
idrac = sd.get_driver('iDRAC', ipaddr, UserCredentials('user', 'pass'))
idrac.config_mgr.set_liason_share(myshare)

def emailtest(idrac, address, expected, action=1):
    print(expected)
    idrac.config_mgr._sysconfig.iDRAC.EmailAlert._index_helper.printx()
    try:
        if action == 1:
            idrac.config_mgr._sysconfig.iDRAC.EmailAlert.new(
                Address_EmailAlert = address, CustomMsg_EmailAlert = address)
        else:
            idrac.config_mgr._sysconfig.iDRAC.EmailAlert.remove(
                Address_EmailAlert = address)
    except Exception as ex:
        print(str(ex))
    idrac.config_mgr.apply_changes()
    idrac.config_mgr._sysconfig.iDRAC.EmailAlert._index_helper.printx()
    print("=============")
print("Original Data")
print(PrettyPrint.prettify_json(idrac.config_mgr._sysconfig.iDRAC.EmailAlert.Json))
print("======")
emailtest(idrac, "hola@gmail.com", "added")
emailtest(idrac, "hungama@gmail.com", "added")
emailtest(idrac, "takur@gmail.com", "added")
emailtest(idrac, "hungama@gmail.com", "deleted", action=2)
emailtest(idrac, "test@gmail.com", "non-existent-delete-no-change", action=2)
emailtest(idrac, "pacific@gmail.com", "added")
emailtest(idrac, "antartic@gmail.com", "added")
emailtest(idrac, "notalone@gmail.com", "should-fail-for-index")
emailtest(idrac, "pacific@gmail.com", "deleted", action=2)
emailtest(idrac, "pacific@gmail.com", "deletion-fail", action=2)
emailtest(idrac, "pacific@gmail.com", "added")
print(PrettyPrint.prettify_json(idrac.config_mgr._sysconfig.iDRAC.EmailAlert.Json))

idrac.config_mgr.create_virtual_disk('hola',1,1,'RAID 1',0)
print("createvd")
print(idrac.config_mgr.CreateVD('hola', 1, 1, 'RAID 1'))
print("deletevd")
print(idrac.config_mgr.DeleteVD('hola'))

### Retrieving Timezone
print(idrac.config_mgr.Time.Timezone_Time)

#### Applying Timezone
idrac.config_mgr.Time.Timezone_Time = 'Asia/Kolkata'
print(idrac.config_mgr.apply_changes())

#### Boot Mode APIs
print(idrac.config_mgr.BootMode)
print(idrac.config_mgr.change_boot_mode('Uefi'))
print(idrac.config_mgr.change_boot_mode(BootModeTypes.Uefi))

print(idrac.config_mgr.CSIOR)
print(idrac.config_mgr.enable_csior())
print(idrac.config_mgr.apply_changes())
print(idrac.config_mgr.disable_csior())
print(idrac.config_mgr.apply_changes())

print(idrac.config_mgr.Location.Json)

print(idrac.config_mgr.configure_location(loc_datacenter = 'a', loc_room='b', loc_aisle='c', loc_rack='d', loc_rack_slot =1, loc_chassis='f'))

print(idrac.config_mgr.TLSProtocol)
print(idrac.config_mgr.SSLEncryptionBits)
print(idrac.config_mgr.SyslogServers)
print(idrac.config_mgr.enable_syslog())
print(idrac.config_mgr.apply_changes())
print(idrac.config_mgr.disable_syslog())

# new style
print(idrac.config_mgr.TLSProtocol)
print(idrac.config_mgr.SSLEncryptionBits)
print(idrac.config_mgr.SyslogServers)
print(idrac.config_mgr.NTPServers)
print(idrac.config_mgr.NTPEnabled)
print(idrac.config_mgr.NTPMaxDist)

print(idrac.config_mgr._sysconfig.System.ServerTopology.Json)

idrac.config_mgr._sysconfig.iDRAC.Users.new(
    UserName_Users = "ruse1",
    Password_Users = "calvin",
    Privilege_Users = "511",
    IpmiLanPrivilege_Users = "Administrator",
    IpmiSerialPrivilege_Users = "Administrator",
    Enable_Users = "Enabled",
    SolEnable_Users = "Enabled",
    ProtocolEnable_Users = "Disabled",
    AuthenticationProtocol_Users = "SHA",
    PrivacyProtocol_Users = "AES"
)
idrac.config_mgr.apply_changes()

try:
  idrac.config_mgr._sysconfig.iDRAC.Users.new(
    UserName_Users = "ruse1",
    Password_Users = "calvin",
    Privilege_Users = "511",
    IpmiLanPrivilege_Users = "Administrator",
    IpmiSerialPrivilege_Users = "Administrator",
    Enable_Users = "Enabled",
    SolEnable_Users = "Enabled",
    ProtocolEnable_Users = "Disabled",
    AuthenticationProtocol_Users = "SHA",
    PrivacyProtocol_Users = "AES"
  )
except Exception as ex:
    print(str(ex))
    print('passed')

idrac.config_mgr.apply_changes()
user = idrac.config_mgr._sysconfig.iDRAC.Users.find_first(UserName_Users = "ruse1")
if user is None:
    print("No such user found!")
else:
    user.Password_Users = '_j2_2j_2j_j2_'
    user.SolEnable_Users = "Disabled"
    idrac.config_mgr.apply_changes()

idrac.config_mgr._sysconfig.iDRAC.Users.remove(UserName_Users = "ruse1")
idrac.config_mgr.apply_changes()
idrac.config_mgr.apply_changes()


    #.Json => gives your JSON representation
    # .XML => gives you XML representation
    # without any - you can access as a typical class
print(PrettyPrint.prettify_json(idrac.config_mgr.SyslogConfig.Json))

idrac.config_mgr.configure_idrac_dnsname('name')
idrac.config_mgr.configure_idrac_ipv4(enable_ipv4=True, dhcp_enabled=True)
idrac.config_mgr.configure_idrac_ipv4static( '1.1.1.1', '1.1.1.1', '1.1.1.1', dnsarray=None, dnsFromDHCP=False)
idrac.config_mgr.configure_idrac_ipv4dns(dnsarray= ["100.96.25.40", "100.29.44.55"], dnsFromDHCP=False)
idrac.config_mgr.configure_idrac_ipv6static( '1:1:1:1', ipv6_prefixlen = 64, ipv6_gateway="::", dnsarray=None, dnsFromDHCP=False)
idrac.config_mgr.configure_idrac_ipv6dns(dnsarray= ["100:96:25:40", "100:29:44:55"], dnsFromDHCP=False)
print(idrac.config_mgr.apply_changes())
print(PrettyPrint.prettify_json(idrac.config_mgr.iDRAC_NIC.Json))
print(idrac.config_mgr.iDRAC_IPv4Static.Json)
print(idrac.config_mgr.iDRAC_IPv6Static.Json)
print(idrac.config_mgr.Time.Json)
print(idrac.config_mgr.apply_changes())
print(idrac.config_mgr.apply_changes())

print(PrettyPrint.prettify_json(idrac.config_mgr._sysconfig.iDRAC.Users.Json))
idrac.config_mgr._sysconfig.iDRAC.Users._index_helper.printx()
