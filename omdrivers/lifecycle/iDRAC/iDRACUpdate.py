import sys
import os
import re
import json
import time
import glob
import xml.etree.ElementTree as ET
from enum import Enum
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkupdate import Update
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omdrivers.enums.iDRAC.iDRACEnums import *
from omsdk.sdkcunicode import UnicodeWriter
from omsdk.sdkcunicode import UnicodeWriter

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False


class iDRACUpdate(Update):
    def __init__(self, entity):
        if PY2:
            super(iDRACUpdate, self).__init__(entity, iDRACFirmEnum)
        else:
            super().__init__(entity, iDRACFirmEnum)
        self.reset()
        self._job_mgr = entity.job_mgr

    def _sw_instance(self, comp):
        ilist = []
        clist = self._comp_to_fqdd(comp)
        for firmware in self.firmware_json["Firmware"]:
            if firmware['FQDD'] in clist and firmware['Status'] == "Installed":
                ilist.append(firmware['InstanceID'])
        return ilist


    def _update_from_uri(self, firm_image_path, componentFQDD, job_wait = True):
        rjson = self.entity._install_from_uri(uri = firm_image_path, target = componentFQDD)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    def reset(self):
        self.sw_inited = False
        self._swidentity = {}
        self.firmware_json = {}
        self.installed_firmware = {}

    def get_swidentity(self):
        if self.sw_inited:
            logger.debug("Already present")
            return self.firmware_json
        self.entity._get_entries(self.firmware_json, self.firmware_enum)
        logger.debug(PrettyPrint.prettify_json(self.firmware_json))
        for obj in self.firmware_json:
            self.installed_firmware[obj] = []
            for entry in self.firmware_json[obj]:
                if 'Status' in entry and entry['Status'] == 'Installed':
                    self.installed_firmware[obj].append(entry)
        return self.firmware_json

    def _get_swidentity_hash(self):
        self.get_swidentity()
        for comp in self.firmware_json:
            for swentry in self.firmware_json[comp]:
                if not "FQDD" in swentry:
                    continue
                if swentry["FQDD"] in self._swidentity:
                    if not isinstance(self._swidentity[swentry["FQDD"]], list):
                        self._swidentity[swentry["FQDD"]] = [ self._swidentity[swentry["FQDD"]] ]
                else:
                    self._swidentity[swentry["FQDD"]] = {}
                self._swidentity[swentry["FQDD"]] = {}
                if "ComponentID" in swentry and swentry["ComponentID"]:
                    for val in ["ComponentID"]:
                        self._swidentity[swentry["FQDD"]][val] = swentry[val]
                else:
                    for val in ["VendorID", "SubVendorID", "DeviceID", "SubDeviceID"]:
                        self._swidentity[swentry["FQDD"]][val] = swentry[val]
                
                for val in ["ComponentType", "InstanceID", "VersionString", "Status"]:
                    self._swidentity[swentry["FQDD"]][val] = swentry[val]
                self._swidentity[swentry["FQDD"]]["ComponentClass"] = "unknown"
                # TODO RESTORE
                #for mycomp in self.protocolspec.compmap:
                #    if re.match(self.protocolspec.compmap[mycomp],swentry["FQDD"]):
                #        self.swidentity[swentry["FQDD"]]["ComponentClass"] = mycomp
        self.sw_inited = True
        return self._swidentity

    @property
    def InstalledFirmware(self):
        self.get_swidentity()
        return self.installed_firmware


    def save_invcollector_file(self, invcol_output_file):
        with UnicodeWriter(invcol_output_file) as output:
            self._save_invcollector(output)

    def serialize_inventory(self, myshare):
        share = myshare.format(ip = self.entity.ipaddr)
        swfqdd_list = [firmware['FQDD'] for firmware in \
                        self.InstalledFirmware["Firmware"]]
        with UnicodeWriter(share.local_full_path) as f:
            f._write_output(json.dumps({
                'Model_Hex' : self.entity.SystemIDInHex,
                'Model' : self.entity.Model,
                'IPAddress' : self.entity.ipaddr,
                'ServiceTag' : self.entity.ServiceTag,
                'Firmware' :  self.InstalledFirmware['Firmware'],
                'ComponentMap' : self.entity.config_mgr._fqdd_to_comp_map(swfqdd_list)},
                sort_keys=True, indent=4, separators=(',', ': ')))

    def update_from_repo(self, myshare, catalog="Catalog.xml", apply_update = True, reboot_needed = False, job_wait = True):
        appUpdateLookup = { True : 1, False : 0 }
        rebootLookup = { True : "TRUE", False : "FALSE" }
        appUpdate = appUpdateLookup[apply_update]
        rebootNeeded = rebootLookup[reboot_needed]
        share = myshare.format(ip = self.entity.ipaddr)
        rjson = self.entity._update_repo(share = share, creds = myshare.creds, catalog = catalog, apply = appUpdate, reboot = rebootNeeded)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    def update_get_repolist(self):
        return self.entity._update_get_repolist()


    def _save_invcollector(self, output):
        #self.entity.get_entityjson()
        #if not "System" in self.entity.entityjson:
        #    logger.debug("ERROR: Entityjson is empty")
        #    return
        self._get_swidentity_hash()
        output._write_output( '<SVMInventory>\n')
        output._write_output( '    <System')
        if "System" in self.entity.entityjson:
            for (invstr, field) in [ ("Model", "Model"), ("systemID", "SystemID"), ("Name", "HostName") ]:
                if field in self.entity.entityjson["System"]:
                    output._write_output( " " + invstr + "=\"" + self.entity.entityjson["System"][field] + "\"")
        output._write_output( ' InventoryTime="{0}">\n'.format(str(datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"))))
        for ent in self._swidentity:
            output._write_output( '        <Device')
            for (invstr, field) in [ ("componentID", "ComponentID"),
                ("vendorID", "VendorID"),
                ("deviceID", "DeviceID"),
                ("subVendorID", "SubVendorID"),
                ("subDeviceID", "SubDeviceID") ]:
                if field in self._swidentity[ent]:
                    output._write_output( " " + invstr + "=\"" + self._swidentity[ent][field] + "\"")
            output._write_output( ' bus="" display="">\n')
            output._write_output( '            <Application componentType="{0}" version="{1}" display="" />\n'.format(self._swidentity[ent]["ComponentType"], self._swidentity[ent]["VersionString"]))
            output._write_output( '        </Device>\n')
        output._write_output( '    </System>\n')
        output._write_output( '</SVMInventory>\n')

