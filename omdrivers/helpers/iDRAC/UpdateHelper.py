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

    @staticmethod
    def build_repo_catalog(*components):
        UpdateHelper.build_repo('Catalog', True, *components)

    @staticmethod
    def build_repo_catalog_model():
        UpdateHelper.build_repo('Catalog', False)

    @staticmethod
    def build_repo(catalog, scoped, *components):
        updmgr = UpdateManager.get_instance()
        if not updmgr:
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        myshare = updmgr.getInventoryShare()
        (catshare, catscope) = updmgr.getCatalogScoper(catalog)
        fwfiles_path = os.path.join(myshare.local_full_path, '*_firmware.json')
        for fname in glob.glob(fwfiles_path):
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

            swidentity = fwinventory
            if not scoped: swidentity = None
            catscope.add_to_scope(fwinventory['Model_Hex'], swidentity, *flist)

        catscope.save()
        return { 'Status' : 'Success' }

    @staticmethod
    def get_firmware_inventory():
        updmgr = UpdateManager.get_instance()
        if not updmgr:
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        myshare = updmgr.getInventoryShare()
        fwfiles_path = os.path.join(myshare.local_full_path, '*_firmware.json')
        device_fw = {}
        for fname in glob.glob(fwfiles_path):
            fwinventory = None
            with open(fname) as firmware_data:
                fwinventory = json.load(firmware_data)
            if not fwinventory:
                logger.debug(' no data found in '+ fname)
                continue
            device_fw[fwinventory['ServiceTag']] = fwinventory

        return { 'Status' : 'Success', 'retval' : device_fw }
