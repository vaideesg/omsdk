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
import sys, os
import logging
sys.path.append(os.getcwd())

counter = 1
from omsdk.sdkprint import PrettyPrint
from omsdk.omlogs.Logger import LogManager
from omdrivers.enums.iDRAC.iDRACEnums import *

#LogManager.setup_logging()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from omsdktest.init_device import sd, dprint
from omsdktest.init_device import ipaddr, creds, liason_share

dprint("Driver SDK", "1. Connect to " + ipaddr)
idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr, creds)
if idrac is None:
    print ("Error: Not found a device driver for: " + ipaddr)
    exit()

print("INFO: Connected to " + ipaddr)
dprint("Driver SDK", "2. Configure liason share " + str(liason_share))
idrac.config_mgr.set_liason_share(liason_share)

VDName = 'OS'
dprint("Driver SDK", "3. Delete Virtual Disk" + str(VDName))
msg = idrac.config_mgr.delete_virtual_disk(VDName)
print('delete_virtual_disk(' + VDName + ') = '  + msg['Status'])
logger.info(PrettyPrint.prettify_json(msg))

dprint("Driver SDK", "3. Create Virtual Disk" + str(VDName))
msg = idrac.config_mgr.create_virtual_disk(VDName, 1, 1, RAIDLevelsEnum.RAID_0)
print('create_virtual_disk(' + VDName + ') = '  + msg['Status'])
logger.info(PrettyPrint.prettify_json(msg))

dprint("Driver SDK", "4. Get details of Virtual Disk" + str(VDName))
msg = idrac.config_mgr.get_virtual_disk(VDName)
if not msg:
    print('get_virtual_disk(' + VDName + ') = None')
else:
    print('get_virtual_disk(' + VDName + ') = ')
    print(PrettyPrint.prettify_json(msg))

idrac.disconnect()
