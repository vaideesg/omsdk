import os
import pprint
import json
import re
import logging

import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import xml.dom.minidom
from omsdk.sdkprint import PrettyPrint


logger = logging.getLogger(__name__)


class UpdateRepo:
    def __init__(self, folder, catalog='Catalog.xml', source=None, mkdirs=False):
        self.tree = None
        self.root = None
        self.catalog = catalog
        self.source = None
        self.folder = None
        self.bundles = {}
        self.exist_bundles = {}
        self.exist_bundles_source = {}
        self.components = []
        self.exist_components = []
        self.entries = {}
        self.path_entries = {}
        self.wcompinbundle = {}
        self.wcomps = {}
        self.set_source(source)
        self.set_folder(folder, mkdirs)
        self._finish_init()

    def set_folder(self, folder, mkdirs=False):
        if self.folder:
            logger.debug("ERROR: folder already initialized!")
            return self
        if not os.path.exists(folder):
            if mkdirs:
                os.makedirs(folder)
                self.folder = folder
            else:
                logger.debug("ERROR: Folder not found!")
        elif os.path.isdir(folder):
            self.folder = folder
            self._load_catalog()
        else:
            self.folder = None
            logger.debug("ERROR: Folder is actually a file!")

    @property
    def UpdateFilePaths(self):
        return list(self.path_entries.keys())

    @property
    def Models(self):
        lmodels = list(self.exist_bundles.keys())
        lmodels.extend(list(self.bundles.keys()))
        return lmodels

    @property
    def BundleIDs(self):
        lbundleids = [self.exist_bundles[i][0].get("bundleID") for i in self.exist_bundles]
        lbundleids.extend([self.bundles[i][0].get("bundleID") for i in self.bundles])
        return lbundleids

    def _load_catalog(self):
        if not os.path.isfile(os.path.join(self.folder, self.catalog)):
            return self
        try:
            self.tree = ET.parse(os.path.join(self.folder, self.catalog))
        except Exception as ex:
            return self
        self.root = self.tree.getroot()
        cnodes = self.root.findall("./SoftwareBundle")
        for node in cnodes:
            nodes = node.findall("./TargetSystems/Brand/Model")
            if len(nodes) <= 0:
                continue
            model = nodes[0].get('systemID')
            if not model:
                logger.debug("Could not find model")
                continue
            self.addBundle(model, node, False)
            components = self.root.findall("./SoftwareComponent/SupportedSystems/Brand/Model[@systemID='{0}']/.../.../...".format(model))
            for comp in components:
                self.addComponent(model, comp, False)

    def _finish_init(self):
        if not self.tree:
            if not self.source:
                logger.debug("Initialization failed!")
                return self
            self.root = ET.Element(self.source.root.tag)
            for (k, v) in self.source.root.items():
                self.root.set(k, v)
            self.tree = ET.ElementTree(self.root)
        return self

    def set_source(self, source):
        if self.source:
            logger.debug("ERROR: Source already initialized!")
            return self
        self.source = source
        return self

    def _copybundle(self, rnode, node):
        cnt_index = 0
        for i in rnode:
            if i.tag == 'SoftwareBundle':
                cnt_index += 1
        if cnt_index > 0:
            mynode = ET.Element(node.tag)
            rnode.insert(cnt_index, mynode)
        else:
            mynode = ET.SubElement(rnode, node.tag)
        for (k,v) in node.items():
            mynode.set(k, v)
        for subnode in node:
            self._copynode(mynode, subnode)

    def _copynode(self, rnode, node):
        if node.tag == "Package":
            if not node.get("path") in self.entries:
                return 
            self.wcompinbundle[node.get("path")] = "done"
        mynode = ET.SubElement(rnode, node.tag)
        for (k,v) in node.items():
            mynode.set(k, v)
        for subnode in node:
            self._copynode(mynode, subnode)

    def _copypackage(self, rnode, node):
        packages = node.findall("./Contents/Package")
        insertnode = rnode.find("./Contents")
        for node in packages:
            if not node.get("path") in self.wcompinbundle and \
               node.get("path") in self.entries:
                self._copynode(insertnode, node)

    def filter_bundle(self, model, ostype="WIN"):
        if self.source:
            return self.source.filter_bundle(model, ostype, tosource=self)
        return 0

    def filter_by_compid(self, model, cid, ostype="WIN"):
        if self.source:
            return self.source.filter_by_compid(model, cid, ostype, tosource=self)
        return 0

    def filter_by_pci(self, model, pcispec, ostype="WIN"):
        if self.source:
            return self.source.filter_by_pci(model, pcispec, ostype, tosource=self)
        return 0

    def filter_by_model(self, model, ostype="WIN"):
        self.filter_bundle(model, "WIN")
        return self.source.filter_by_model(model, ostype, tosource=self)

    def filter_by_component(self, model,swidentity, compfqdd=None,ostype="WIN"):
        if len(compfqdd) <= 0: compfqdd = None
        logger.debug('filter_by_component::compfqdd=' + str(compfqdd))
        logger.debug(PrettyPrint.prettify_json(swidentity))
        count = self.filter_bundle(model, "WIN")
        logger.debug('filtered bundle ' + str(count))
        count = 0
        for firm in swidentity["Firmware"]:
            if compfqdd and firm['FQDD'] not in compfqdd:
                continue
            logger.debug(firm['FQDD'])
            if 'ComponentID' in firm and firm['ComponentID']:
                count += self.filter_by_compid(model, firm['ComponentID'], ostype)
                continue
            pcispec = {}
            if 'VendorID' in firm and firm['VendorID']:
                pcispec['vendorID'] = firm['VendorID']
            if 'DeviceID' in firm and firm['DeviceID']:
                pcispec['deviceID'] = firm['DeviceID']
            if 'SubVendorID' in firm and firm['SubVendorID']:
                pcispec['subVendorID'] = firm['SubVendorID']
            if 'SubDeviceID' in firm and firm['SubDeviceID']:
                pcispec['subDeviceID'] = firm['SubDeviceID']
            if len(pcispec) > 0:
                count += self.filter_by_pci(model, pcispec, ostype)
                continue
        logger.debug('Filtered ' + str(count) + ' entries!')
        return count

    def addBundle(self, model, node, newNode=True):
        if not newNode:
            if not model in self.exist_bundles:
                self.exist_bundles[model] = []
            self.exist_bundles[model].append(node)
        if newNode:
            if model in self.exist_bundles:
                for bundle in self.exist_bundles[model]:
                    if bundle.get("bundleID") != node.get("bundleID"):
                        continue
                    self.exist_bundles_source[bundle.get("bundleID")] = node
                    return
            if not model in self.bundles:
                self.bundles[model] = []
            self.bundles[model].append(node)

    def addComponent(self, model, node, newNode=True):
        fpath = node.get("path").split("/")[-1]
        if fpath in self.entries:
            return
        if not newNode:
            self.exist_components.append(node)
            self.wcompinbundle[fpath] = "done"
        else:
            self.components.append(node)
        self.entries[fpath] = node
        self.path_entries[node.get("path")] = node

    # version = -1 : latest
    # version =  0 : n-1
    def store(self, version = -1, target=None):
        if not target:
            target = self.catalog
        self.root.set('baseLocation', '')
        # insert new bundles
        for model in self.bundles:
            self.bundles[model].sort(key = lambda x: x.get("vendorVersion"))
            self._copybundle(self.root, self.bundles[model][version])
        # Insert new components into existing bundles
        for model in self.exist_bundles:
            for bundle in self.exist_bundles[model]:
                if bundle.get("bundleID") in self.exist_bundles_source:
                    node=self.exist_bundles_source[bundle.get("bundleID")]
                    self._copypackage(bundle, node)
        # Add new components
        for node in self.components:
            if not node.get("path").split("/")[-1] in self.wcompinbundle:
                continue
            if node.get("path") in self.wcomps:
                continue
            self.wcomps[node.get("path")] = "done"
            self._copynode(self.root, node)
        self.tree.write(os.path.join(self.folder, target))
