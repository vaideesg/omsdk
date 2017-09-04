import json
import glob
import re
import os
from enum import Enum
from sys import stdout
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
import logging

PY2UC = (sys.version_info < (3,0,0))

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

    def get_swidentity(self):
        if self.sw_inited:
            logger.debug("Already present")
            return self.firmware_json
        self.entity._get_entries(self.firmware_json, self.firmware_enum)
        logger.debug(PrettyPrint.prettify_json(self.firmware_json))
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

    def save_invcollector_file(self, invcol_output_file):
        with open(invcol_output_file, "w") as output:
            self._save_invcollector(output)

    def _save_invcollector(self, output):
        #self.entity.get_entityjson()
        #if not "System" in self.entity.entityjson:
        #    logger.debug("ERROR: Entityjson is empty")
        #    return
        self._get_swidentity_hash()
        self._write_output(output, '<SVMInventory>\n')
        self._write_output(output, '    <System')
        if "System" in self.entity.entityjson:
            for (invstr, field) in [ ("Model", "Model"), ("systemID", "SystemID"), ("Name", "HostName") ]:
                if field in self.entity.entityjson["System"]:
                    self._write_output(output, " " + invstr + "=\"" + self.entity.entityjson["System"][field] + "\"")
        self._write_output(output, ' InventoryTime="{0}">\n'.format(str(datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"))))
        for ent in self._swidentity:
            self._write_output(output, '        <Device')
            for (invstr, field) in [ ("componentID", "ComponentID"),
                ("vendorID", "VendorID"),
                ("deviceID", "DeviceID"),
                ("subVendorID", "SubVendorID"),
                ("subDeviceID", "SubDeviceID") ]:
                if field in self._swidentity[ent]:
                    self._write_output(output, " " + invstr + "=\"" + self._swidentity[ent][field] + "\"")
            self._write_output(output, ' bus="" display="">\n')
            self._write_output(output, '            <Application componentType="{0}" version="{1}" display="" />\n'.format(self._swidentity[ent]["ComponentType"], self._swidentity[ent]["VersionString"]))
            self._write_output(output, '        </Device>\n')
        self._write_output(output, '    </System>\n')
        self._write_output(output, '</SVMInventory>\n')

    def _write_output(self, output, line):
        if PY2UC:
            output.write(unicode(line))
        else:
            output.write(line)
