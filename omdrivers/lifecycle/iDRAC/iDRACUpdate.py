import os
import re
import time
import xml.etree.ElementTree as ET
from enum import Enum
from datetime import datetime
from omsdk.sdkprint import LogMan, pretty
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkupdate import Update
from omsdk.catalog.sdkupdatemgr import UpdateManager
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False

iDRACFirmEnum = EnumWrapper("iDRACFirmEnum", {
    "Firmware" : "Firmware",
    }).enum_type

iDRACFirmwareWsManViews = {
    iDRACFirmEnum.Firmware : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareIdentity",
}

class iDRACUpdate(Update):
    def __init__(self, entity):
        if PY2:
            super(iDRACUpdate, self).__init__(entity, iDRACFirmEnum)
        else:
            super().__init__(entity, iDRACFirmEnum)
        self._job_mgr = entity.job_mgr

    def _sw_instance(self, comp):
        ilist = []
        clist = self._comp_to_fqdd(comp)
        for firmware in self.firmware_json["Firmware"]:
            if firmware['FQDD'] in clist and firmware['Status'] == "Installed":
                ilist.append(firmware['InstanceID'])
        return ilist

    def _get_swfqdd_list(self):
        self.get_swidentity()
        return [firmware['FQDD'] \
                    for firmware in self.firmware_json["Firmware"] \
                    if firmware['Status'] == "Installed"]

    def _update_from_uri_async(self, firm_image_path, componentFQDD):
        rjson = self.entity._install_from_uri(uri = firm_image_path, target = componentFQDD)
        rjson['file'] = str(share)
        return rjson

    def _update_from_uri(self, firm_image_path, componentFQDD):
        rjson = self.update_from_uri(uri = firm_image_path, target = componentFQDD)
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def update_from_repo_async(self, myshare, catalog="Catalog.xml", apply_update = True, reboot_needed = False):
        appUpdateLookup = { True : 1, False : 0 }
        rebootLookup = { True : "TRUE", False : "FALSE" }
        appUpdate = appUpdateLookup[apply_update]
        rebootNeeded = rebootLookup[reboot_needed]
        share = myshare.format(ip = self.entity.ipaddr)
        rjson = self.entity._update_repo(share = share, creds = myshare.creds, catalog = catalog, apply = appUpdate, reboot = rebootNeeded)
        rjson['file'] = str(share)
        return rjson

    def update_from_repo(self, myshare, catalog="Catalog.xml", apply_update = True, reboot_needed = False):
        rjson = self.update_from_repo_async(myshare, catalog, apply_update, reboot_needed)
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def update_get_repolist(self):
        return self.entity._update_get_repolist()

    def catalog_scoped_to_model(self, catscope= None):
        return UpdateManager.get_instance().scoped_to_model(catscope,
                        self.entity.SystemIDInHex)

    def catalog_scoped_to_device(self, catscope = None):
        return UpdateManager.get_instance().scoped_to_device(catscope,
                        self.entity.SystemIDInHex,
                        self.get_swidentity())

    def catalog_scoped_to_components(self, *components):
        config = self.entity.config_mgr
        sw_list = self._get_swfqdd_list()
        flist = []
        for comp in components:
            flist.extend(config._comp_to_fqdd(sw_list, comp, default=[comp]))
        return UpdateManager.get_instance().scoped_to_components(None,
                        self.entity.SystemIDInHex,
                        self.get_swidentity(), compfqdd=flist)
