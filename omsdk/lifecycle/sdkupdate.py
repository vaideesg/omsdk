import json
import glob
import re
import os
from enum import Enum
from sys import stdout
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkcunicode import UnicodeWriter
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
import logging

logger = logging.getLogger(__name__)

class Update(object):

    def __init__(self, entity, firmware_enum):
        self.entity = entity
        self.firmware_enum = firmware_enum
        self.reset()

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

    @property
    def InstalledFirmware(self):
        self.get_swidentity()
        return self.installed_firmware

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

    def save_invcollector_file(self, invcol_output_file):
        with UnicodeWriter(invcol_output_file) as output:
            self._save_invcollector(output)

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
