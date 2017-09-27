import xml.etree.ElementTree as ET
import re
import json
import logging
import sys, os
import glob
import threading

logger = logging.getLogger(__name__)

# Attribute Registry Convertor
#   .xml to .json file converter
class maj:
    def __init__(self):
        self.cntr = 0
        self.ids = 0
    def incr(self):
        self.cntr += 1
    def ids(self):
        self.ids += 1

class AttribRegistry(object):

    def _sanitize_name(self, fld_name, suffix):
        typName = fld_name.strip() + suffix
        typName = re.sub('^(^[0-9])', 'E_\\1', typName)
        typName = re.sub('[[]([^]:]+)[^]]*[]]', '\\1', typName)
        typName = re.sub('[?]', '', typName)
        typName = re.sub('[-.]', '_', typName)
        typName = re.sub('^[ \t]+', '', typName)
        return typName

    def get_type(self, config_spec, origtype, fname):
        types_in = config_spec
        if self.comp not in types_in:
            return origtype
        for field_type in types_in[self.comp]:
            if '_' in fname:
                (field_name, group_name) = fname.split('_')
            else:
                (field_name, group_name) = (fname, 'NA')
            if group_name in types_in[self.comp][field_type] and \
                field_name in types_in[self.comp][field_type][group_name]:
                    return field_type
        return origtype

    def build_attrentry(self, regentry, all_entries, attrx_group):
        for attr in regentry:
            myentry = {}
            for attrfield in attr:
                if len(attrfield) <= 0:
                    # attribute
                    myentry [attrfield.tag] = attrfield.text
                    if attrfield.tag in ["GroupName"]:
                        if not attrfield.text in attrx_group:
                            attrx_group[attrfield.text] = []
                        attrx_group[attrfield.text].append(myentry)
                elif attrfield.tag in ["AttributeType"]:
                    if not attrfield.tag in myentry:
                        myentry[attrfield.tag] = {}
                    myentry [attrfield.tag] = attrfield.text
                elif attrfield.tag in ["AttributeValue"]:
                    if not attrfield.tag in myentry:
                        myentry[attrfield.tag] = {}
                        myentry["enum"] = []
                        myentry["enumDescriptions"] = []
                    enum_name = None
                    enum_value = None
                    for child in attrfield:
                        if (child.tag == "ValueName"):
                            if enum_value:
                                logger.debug("WARN: Duplicate value found!")
                            else:
                                enum_value = child.text
                        else:
                            if enum_name:
                                logger.debug("WARN: Duplicate name found!")
                            else:
                                enum_name = child.text
                    myentry[attrfield.tag][enum_name] = enum_value
                    myentry["enum"].append(enum_value.strip())
                    myentry["enumDescriptions"].append(enum_name)
                elif attrfield.tag in ["Modifiers"]:
                    for modifiers in attrfield:
                        if modifiers.tag in ['BrowserRead', 'BrowserWrite',
                                'BrowserSuppressed', 'ProgrammaticRead',
                                'ProgrammaticWrite']:
                            pass
                        elif modifiers.tag in ['RegEx', 'Partition']:
                            myentry[modifiers.tag] = modifiers.text
                        else:
                            logger.debug("WARN: Unknown!!" + modifiers.tag)
                else:
                    logger.debug("WARN: Unknown!!" + attrfield.tag)
            all_entries.append(myentry)

    def build_groups(self, attrx_group):
        for group in attrx_group:
            tt = self.attr_json["definitions"][self.comp]["config_groups"]
            tt[group] = []
            for ent in attrx_group[group]:
                fld_name = ent["AttributeName"]
                if self.addGroup:
                    fld_name += "_" + group
                tt[group].append(fld_name)

    def load_json(self, all_entries, comp, MAJ):
        attmap = {
            'IsReadOnly' : 'readonly',
            'DisplayName' : 'description',
            'HelpText' : 'longDescription',
            'Partition' : 'partition',
            'RegEx' : 'pattern',
            'GroupName' : 'qualifier',
            'AttributeName' : 'name',
            'AttributeType' : 'baseType',
            'DefaultValue' : 'default',
        }
        typemaps = {
            'integer' : 'int',
            'string' : 'str',
            'enumeration' : 'enum',

            'orderlistseq' : 'list',
            'password' : 'str',
            'binary' : 'str',
            'minmaxrange' : 'int',
            'range' : 'int',
        }

        for entry in all_entries:
            tt = self.attr_json["definitions"][comp]["properties"]
            if entry['AttributeType'].lower() in [
                'form title', 'form ref', 'checkbox', 'formset title'
            ]: continue

            MAJ.ids += 1
            fld_name = entry["AttributeName"]
            if self.addGroup and "GroupName" in entry:
                fld_name = fld_name + "_" + entry["GroupName"]
            tt[fld_name] = {}
            for fld in attmap:
                if fld in entry:
                    if attmap[fld] in ['baseType']:
                        ntype = typemaps[entry[fld].lower()]
                        tt[fld_name][attmap[fld]] = ntype
                    else:
                        if entry[fld] == "FALSE": entry[fld] = False
                        if entry[fld] == "TRUE": entry[fld] = True
                        tt[fld_name][attmap[fld]] = entry[fld]

            tt[fld_name]['modDeleteAllowed'] = True
            tt[fld_name]['uneditable'] = False
            if 'readonly' in tt[fld_name] and tt[fld_name]['readonly'] in ['true']:
                if 'longDescription' in tt[fld_name] and \
                    'Configurable via XML' not in tt[fld_name]['longDescription']:
                    tt[fld_name]['uneditable'] = True
                tt[fld_name]['modDeleteAllowed'] = False

            attr_type = 'string'
            if "AttributeType" in entry:
                attr_type = entry["AttributeType"].lower()
            if "AttributeValue" in entry:
                typName = self._sanitize_name(fld_name, 'Types')
                tt[fld_name]["type"] = typName
                self.attr_json["definitions"][typName] = {
                    "enum" : entry["enum"],
                    "enumDescriptions" : entry["enumDescriptions"],
                    "type" : attr_type,
                }

    def update_type(self, comp, config_spec, MAJ):
        tt = self.attr_json["definitions"][comp]["properties"]
        for fld_name in self.attr_json["definitions"][comp]["properties"]:
            ntype = self.get_type(config_spec, tt[fld_name]['baseType'], fld_name)
            if tt[fld_name]['baseType'] != ntype:
                MAJ.incr()
                tt[fld_name]['baseType'] = ntype

    def __init__(self, file_name, dconfig, config_spec, MAJ):
        self.lock = threading.Lock()
        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()
        regentry = None
        for regent in self.root:
            if regent.tag == "REGISTRY_ENTRIES":
                regentry = regent
                break
        self.comp = re.sub("^.*[\\\\]", "", file_name)
        self.comp = re.sub("\..*$", "", self.comp)
        self.addGroup = (self.comp == 'iDRAC')
        self.direct = re.sub("[^\\\\]+$", "", file_name)
        self.attr_json = {
            "$schema" : file_name,
            "title" : file_name,
            "$ref" : "#/definitions/" + self.comp,
            "definitions" : {
                self.comp : {
                    "config_groups" : {},
                    "type" : "object",
                    "properties" : {}
                }
            }
        }

        attrx_group = {}
        all_entries = []
        with self.lock:
            self.build_attrentry(regentry, all_entries, attrx_group)
        with self.lock:
            self.build_groups(attrx_group)
        with self.lock:
            self.load_json(all_entries, self.comp,MAJ)
        with self.lock:
            self.update_type(self.comp, config_spec, MAJ)


        props = self.attr_json["definitions"][self.comp]["properties"]
        if 'StripeSize' in props:
            props['StripeSize']['type'] = 'StripeSizeTypes'
            self.attr_json["definitions"]['StripeSizeTypes'] = {
                "enum": [
                    "Default",
                    "512",
                    "1KB", "2KB", "4KB", "8KB",
                    "16KB", "32KB", "64KB",
                    "128KB", "256KB", "512KB",
                    "1MB", "2MB", "4MB", "8MB",
                ],
                "enumDescriptions": [
                    "Default",
                    "512",
                    "1KB", "2KB", "4KB", "8KB",
                    "16KB", "32KB", "64KB",
                    "128KB", "256KB", "512KB",
                    "1MB", "2MB", "4MB", "8MB",
                ],
                "type": "string"
            }

    def save_file(self, directory = None, filename = None):
        if not directory: directory = self.direct
        if not filename: filename = self.comp + ".json"
        dest_file = os.path.join(directory, filename)
        print ("Saving to :" + dest_file)
        with open(dest_file, "w") as out:
            out.write(json.dumps(self.attr_json, sort_keys=True,
                                 indent=4, separators=(',', ': ')))


def do_dump(file1, dconfig, config_spec, group, MAJ):
    ar= AttribRegistry(file1, dconfig, config_spec, MAJ)
    ar.save_file(directory=dconfig)

if __name__ == "__main__":
    MAJ = maj()
    device = 'iDRAC'
    driver_dir = os.path.join('omdrivers', device)
    types_dir = os.path.join('omdrivers', 'types', device)
    dconfig = os.path.join(driver_dir, 'Config')
    f_config_spec = os.path.join(dconfig, 'iDRAC.comp_spec')
    config_spec = {}
    if os.path.exists(f_config_spec):
        with open(f_config_spec) as f:
            config_spec = json.load(f)
    for file1 in glob.glob(os.path.join(driver_dir, "xml", "*.xml")):
        if file1.endswith('EventFilters.xml') is True: continue
        do_dump(file1, dconfig, config_spec['types'], file1.endswith('iDRAC.xml'), MAJ)
    print(str(MAJ.cntr) + " objects have special types")
    print(str(MAJ.ids) + " attributes created!")
