import os
import re
import json
import xml.etree.ElementTree as ET
from omsdk.typemgr.ClassType import *
from omsdk.typemgr.Formatters import *
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.BIOS import *
from omdrivers.types.iDRAC.RAID import *
from omdrivers.types.iDRAC.NIC import *
from omdrivers.types.iDRAC.FCHBA import *
from omdrivers.types.iDRAC.SystemConfiguration import *

import logging


class XMLParser(object):

    def __init__(self, cspecfile):
        self.config_spec = {}
        if os.path.exists(cspecfile):
            with open(cspecfile) as f:
                self.config_spec = json.load(f)

    def _get_entry(self, comp_fqdd, sysconfig):
        for i in self.config_spec:
            if 'pattern' in self.config_spec[i]:
                if re.match(self.config_spec[i]['pattern'], comp_fqdd):
                    if i in sysconfig.__dict__:
                        return sysconfig.__dict__[i]
        return None

    def _load_attrib(self, node, entry):
        for attrib in node:
            if attrib.tag == 'Component':
                subnode = self._get_entry(attrib.get('FQDD'), entry)
                if subnode is None:
                    logger.warning('No component spec found for ' + attrib.get('FQDD'))
                    continue
                parent = None
                if isinstance(entry, ArrayType):
                    parent = entry
                    subentry = parent._cls(loading_from_scp=True)
        
                if subnode.attrib:
                    for attr in subnode.attrib:
                        subentry.add_attribute(attr, subnode.attrib[attr])
    
                _load_attrib(subnode, subentry)
                continue
    
            attrname = attrib.get("Name")
            if attrname is None:
                logging.error("ERROR: No attribute found!!")
                continue
    
            if '.' not in attrname:
                # plain attribute
                if attrname not in entry.__dict__:
                    entry.__setattr__(attrname, StringField(attrib.text, parent=entry))
                    logging.warning(attrname + ' not found in ' + type(entry).__name__)
                    logging.warning("Ensure the attribute registry is updated.")
                    continue
    
                if attrib.text is None or attrib.text.strip() == '':
                    # empty - what to do?
                    if entry.__dict__[attrname]._type == str:
                        entry.__dict__[attrname]._value = ""
                else:
                    entry.__dict__[attrname]._value = attrib.text.strip()
                continue
    
            match = re.match('(.*)\.([0-9]+)#(.*)', attrname)
            if not match:
                print(attrname + ' not good ')
                continue
    
            (group, index, field) = match.groups()
            if group in entry.__dict__:
                grp = entry.__dict__[group]
    
                subentry = grp
                if isinstance(grp, ArrayType):
                    subentry = grp.find_or_create(index=index)
    
                if field not in subentry.__dict__:
                    field = field + '_' + group
                if field not in subentry.__dict__:
                    subentry.__dict__[field] = StringField(attrib.text, parent=subentry)
                    logging.warning(field+' not found in '+type(subentry).__name__)
                    logging.warning("Ensure the attribute registry is updated.")
                    continue
                if attrib.text is None or attrib.text.strip() == '':
                    # empty - what to do?
                    if subentry.__dict__[field]._type == str:
                        subentry.__dict__[field]._value = ""
                else:
                    try:
                        subentry.__dict__[field]._value = attrib.text.strip()
                    except Exception as ex:
                        print(group + "..." + field)
                        print(subentry._state)
                        print("ERROR:" + str(ex))
    
    def _load_scp(self, node, sysconfig):
        if sysconfig._alias and node.tag != sysconfig._alias:
            logger.warning(node.tag +  " no match to " +  sysconfig._alias)
    
        for attrib in node.attrib:
            sysconfig.add_attribute(attrib, node.attrib[attrib])
    
        for subnode in node:
            # Component!
            entry = self._get_entry(subnode.get('FQDD'), sysconfig)
    
            if entry is None:
                logger.warning('No component spec found for ' + subnode.get('FQDD'))
                continue
    
            parent = None
            if isinstance(entry, ArrayType):
                parent = entry
                entry = parent._cls(loading_from_scp=True)
    
            for attrib in subnode.attrib:
                entry.add_attribute(attrib, subnode.attrib[attrib])
    
            self._load_attrib(subnode, entry)
    
    def parse_scp(self, fname):
        tree= ET.parse(fname)
        root = tree.getroot()
        sysconfig = SystemConfiguration(loading_from_scp=True)
        # Do a pre-commit - to save original values
        sysconfig.commit(loading_from_scp=True)
        self._load_scp(tree.getroot(), sysconfig)
        sysconfig._clear_duplicates()
        sysconfig.commit()
        return sysconfig

    def save_scp(self, fname, sysconfig):
        print(XMLFormatter(everything=False).format_type(sysconfig)._get_str())

