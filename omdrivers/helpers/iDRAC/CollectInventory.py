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
from argparse import ArgumentParser
from omsdk.sdkfile import LocalFile
from omsdk.sdkcenum import TypeHelper
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
from omsdk.sdkinfra import sdkinfra
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkprint import PrettyPrint
import sys

def CollectInventory(arglist):
    parser = ArgumentParser(description='Inventory Collector')
    parser.add_argument('-u', '--user', 
        action="store", dest="user", type=str, nargs='?',
        default='root', help="Username to use for iDRAC")
    parser.add_argument('-p', '--password', 
        action="store", dest="password", type=str,
        default='password', help="Password to use for iDRAC")
    parser.add_argument('-i', '--ipaddress',
        action="store", dest="idrac_ip", nargs='+',
        help="ipaddress of iDRAC")
    parser.add_argument('-f', '--folder', 
        action="store", dest="folder", type=str,
        help="folder from where inventory is serialized")

    options = parser.parse_args(arglist)

    if options.password is None:
        print("password must be provided")
        return -1
    if options.user is None:
        print("user must be provided")
        return -1
    if options.folder is None:
        print("Folder must be provided")
        return -1
    if options.idrac_ip is None or len(options.idrac_ip) <= 0:
        print("iDRAC ip addresses must be provided")
        return -1


    updshare = LocalFile(local = options.folder, isFolder=True)
    if not updshare.IsValid:
        print("Folder is not writable!")
        return -2

    print("Configuring Update Share...")
    UpdateManager.configure(updshare)

    sd = sdkinfra()
    sd.importPath()
    creds = UserCredentials(options.user, options.password)
    for ipaddr in options.idrac_ip:
        try:
            print("Connecting to " + ipaddr + " ... ")
            idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr, creds)
            if idrac:
                print("    ... saving firmware!")
                UpdateHelper.save_firmware_inventory(idrac)
                idrac.disconnect()
            else:
                print("    failed to connect to iDRAC")
        except Exception as ex:
            print(str(ex))

if __name__ == "__main__":
    CollectInventory(sys.argv[1:])
