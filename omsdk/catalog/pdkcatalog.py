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
import pprint
import json
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import xml.dom.minidom

from omsdk.sdkprint import PrettyPrint
import logging


logger = logging.getLogger(__name__)

class DellPDKCatalog:

    OSTypes = {
        "WIN" : "LWXP",
        "WIN64" : "LW64",
    }

    def __init__(self, source_file):
        self.source_file = source_file
        if not os.path.isfile(self.source_file):
            logger.debug(self.source_file + " does not exist!")
            self.root = ET.Element("Manifest")
            self.tree = ET.ElementTree(self.root)
            self.valid = False
        else:
            self.tree = ET.parse(self.source_file)
            self.root = self.tree.getroot()
            self.valid = True

    #ostype = None => all os types
    #ostype = "WIN" => only win32
    #ostype = ["WIN", "LIN"] => only win32 and Lin32
    def filter_bundle(self, model, ostype="WIN64", tosource = None):
        # Find all Software Bundles for this model
        model = model.upper()
        model_path = "./SoftwareBundle/TargetSystems/Brand/Model[@systemID='{0}']/.../.../...".format(model)
        os_path = "./TargetOSes/OperatingSystem"
        if ostype:
            lostype = ostype
            if not isinstance(ostype, list):
                lostype = [lostype]
            for os in lostype:
                os_path += "[@osCode='{0}']".format(os)
        cnodes = self.root.findall(model_path)
        count = 0
        for node in cnodes:
            if len(node.findall(os_path)) <= 0:
                continue
            count += 1
            if tosource:
                tosource.addBundle(model, node)
        return count

    def _filter_byid(self, model, ostype, compid_path, firm, tosource):
        model = model.upper()
        model_path = "./SupportedSystems/Brand/Model[@systemID='{0}']".format(model)
        comp_path = "./SoftwareComponent"
        lostype = [""]
        if ostype:
            _ostype=ostype
            lostype = []
            if not isinstance(ostype, list):
                _ostype = [_ostype]
            for os in _ostype:
                lostype.append("[@packageType='{0}']".format(self.OSTypes[os]))
        count = 0
        for oses in lostype:
            xpth = comp_path + oses + "/SupportedDevices/Device" + compid_path + "/.../..."
            cnodes = self.root.findall(xpth)
            for node in cnodes:
                if len(node.findall(model_path)) <= 0:
                    continue
                count = count + 1
                if tosource:
                    tosource.addComponent(model, node, firm)
        return count

    def filter_by_model(self, model, ostype="WIN64", firm = None, tosource=None):
        model = model.upper()
        return self._filter_byid(model, ostype, "", firm, tosource)

    def filter_by_compid(self, model, cid, ostype="WIN64", firm=None, tosource=None):
        model = model.upper()
        compid_path = ""
        if cid:
            compid_path = "[@componentID='{0}']".format(cid)
        return self._filter_byid(model, ostype, compid_path, firm, tosource)

    def filter_by_pci(self, model, pcispec, ostype="WIN64", firm=None, tosource = None):
        model = model.upper()
        compid_path = "/PCIInfo"
        for field in ['deviceID', 'subDeviceID', 'subVendorID', 'vendorID']:
            if field not in pcispec or not pcispec[field]:
                logger.debug(field + " is not present or null")
                continue
            compid_path += "[@" + field + "='" + pcispec[field] + "']"
        compid_path += "/..."
        return self._filter_byid(model, ostype, compid_path, firm, tosource)

    def get_json(self, rjson):
        for node in self.root.findall("./SoftwareComponent"):
            for comp in node.findall('./SupportedDevices/Device'):
                pcientries = []
                pcis = comp.findall('./PCIInfo')
                for vals in pcis:
                    pcientries.append(vals.attrib)
                if len(pcientries) == 0:
                    pcientries.append({})
                package = re.sub('.*/', '', node.attrib['path'])
                for pcis in pcientries:
                  for bundle in self.root.findall("./SoftwareBundle/Contents/Package[@path='{0}']/.../...".format(package)):
                    for model in bundle.findall("./TargetSystems/Brand/Model"):
                        entry = {'Package':  package}
                        entry.update(node.attrib)
                        for attr in comp.attrib:
                            entry['component_'+ attr] = comp.attrib[attr]
                        for attr in ['dateTime', 'releaseID', 'version']:
                            entry['catalog_'+attr]=self.root.attrib[attr]
                        for attr in bundle.attrib:
                            if (attr == "Package"): continue
                            entry['bundle_'+attr]=bundle.attrib[attr]
                        for attr in model.attrib:
                            entry['model_'+attr]=model.attrib[attr]
                        for attr in pcis:
                            entry['pci_'+attr]=pcis[attr]
                        rjson.append(entry)
        return rjson

class DellPDKIndexCatalog:

    UpdateTypes = {
        "LC" : "MTLC",
    }

    def __init__(self, source_file):
        self.source_file = source_file
        if not os.path.isfile(self.source_file):
            logger.debug(self.source_file + " does not exist!")
            self.root = ET.Element("Manifest")
            self.tree = ET.ElementTree(self.root)
            self.valid = False
        else:
            self.tree = ET.parse(self.source_file)
            self.root = self.tree.getroot()
            self.valid = True

    def filter_index(self, update_type="LC"):
        update_path = "./{0}GroupManifest[@type='{1}']/{0}ManifestInformation".format('{openmanage/cm/dm}', self.UpdateTypes[update_type])
        return [node.attrib for node in self.root.findall(update_path)]
