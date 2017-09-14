import sys
import glob
import json
import logging
import os

from omsdk.catalog.sdkupdatemgr import UpdateManager
from omdrivers.enums.iDRAC.iDRACEnums import *

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class UpdateHelper(object):

    # Save the firmware inventory of the representative servers
    # to the <UpdateShare>\_inventory folder
    @staticmethod
    def save_firmware_inventory(devices):
        if not isinstance(devices,list):
            devices = [devices]
        if not UpdateManager.get_instance():
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        myshare = UpdateManager.get_instance().getInventoryShare()
        mydevinv = myshare.new_file('%ip_firmware.json')
        for device in devices:
            device.update_mgr.serialize_inventory(mydevinv)
        return { 'Status' : 'Success' }

    # Download the catalog and scope to selected inventory
    @staticmethod
    def build_repo(*components):
        if not UpdateManager.get_instance():
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        myshare = UpdateManager.get_instance().getInventoryShare()
        catscope = UpdateManager.get_instance().getCatalogScoper()
        for fname in glob.glob(os.path.join(myshare.local_full_path, '*_firmware.json')):
            fwinventory = None
            with open(fname) as firmware_data:
                fwinventory = json.load(firmware_data)
            if not fwinventory:
                logger.debug(' no data found in '+ fname)
                continue
            flist = []
            for comp in components:
                if comp in fwinventory['ComponentMap']:
                    flist.extend(fwinventory['ComponentMap'][comp])

            catscope.add_to_scope(fwinventory['Model_Hex'], fwinventory, *flist)
        catscope.save()
        return { 'Status' : 'Success' }
