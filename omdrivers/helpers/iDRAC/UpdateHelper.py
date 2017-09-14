import sys

from omsdk.catalog.sdkupdatemgr import UpdateManager
from omdrivers.enums.iDRAC.iDRACEnums import *

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


class UpdateScoper(object):
    def __init__(self, entity):
        self.entity = entity

    def model_scope(self, catscope= None):
        if catscope is None:
            catscope = UpdateManager.get_instance().getCatalogScoper()
        catscope.add_model_to_scope(self.entity.SystemIDInHex)

    def device_scope(self, catscope = None):
        if catscope is None:
            catscope = UpdateManager.get_instance().getCatalogScoper()
        catscope.add_to_scope(self.entity.SystemIDInHex,
                 self.entity.update_mgr.get_swidentity())

    def component_scope(self, *components, catscope = None):
        if catscope is None:
            catscope = UpdateManager.get_instance().getCatalogScoper()
        config = self.entity.config_mgr
        sw_list = self.entity.update_mgr._get_swfqdd_list()
        flist = []
        for comp in components:
            flist.extend(config._comp_to_fqdd(sw_list, comp, default=[comp]))
        catscope.add_to_scope(self.entity.SystemIDInHex,
                 self.entity.update_mgr.get_swidentity(), comfqdd=flist)

class UpdateHelper(object):

    @staticmethod
    def add_device_models(ids):
        if not isinstance(ids,list):
            ids = [ids]
        if UpdateManager.get_instance():
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        catscope = UpdateManager.get_instance().getCatalogScoper()
        for model in ids:
            catscope.add_model_to_scope(model)
        catscope.save()
        return { 'Status' : 'Success' }

    @staticmethod
    def add_devices(devices):
        if not isinstance(devices,list):
            devices = [devices]
        if UpdateManager.get_instance():
            return { 'Status' : 'Failed',
                     'Message' : 'Update Manager is not initialized' }
        catscope = UpdateManager.get_instance().getCatalogScoper()
        for device in devices:
            try:
                UpdateScoper(device).device_scope(catscope)
            except Exception as ex:
                logger.error(str(ex))
        catscope.save()
        return { 'Status' : 'Success' }
