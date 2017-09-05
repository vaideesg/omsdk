import xml.etree.ElementTree as ET
import re
import json
import logging
import sys, os
import glob

logger = logging.getLogger(__name__)

# Attribute Registry Convertor
#   .xml to .json file converter

class AttribRegistry(object):

    def __init__(self, file_name):
        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()
        regentry = None
        for regent in self.root:
            if regent.tag == "REGISTRY_ENTRIES":
                regentry = regent
                break
        self.comp = re.sub("^.*[\\\\]", "", file_name)
        self.comp = re.sub("\..*$", "", self.comp)
        self.addGroup = re.match('iDRAC', self.comp)
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

        attmap = {
            'IsReadOnly' : 'readonly',
            'DisplayName' : 'description',
            'HelpText' : 'longDescription',
            'Partition' : 'partition',
            'RegEx' : 'pattern',
            'GroupName' : 'qualifier',
            'AttributeName' : 'name',
            'DefaultValue' : 'default',
        }
        attrx_group = {}
        all_entries = []
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
                    myentry["enum"].append(enum_value)
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
        for group in attrx_group:
            tt = self.attr_json["definitions"][self.comp]["config_groups"]
            tt[group] = []
            for ent in attrx_group[group]:
                fld_name = ent["AttributeName"]
                if self.addGroup:
                    fld_name += "_" + group
                tt[group].append(fld_name)

        for entry in all_entries:
            tt = self.attr_json["definitions"][self.comp]["properties"]
            fld_name = entry["AttributeName"]
            if self.addGroup and "GroupName" in entry:
                fld_name = fld_name + "_" + entry["GroupName"]
            tt[fld_name] = {}
            for fld in attmap:
                if fld in entry:
                    tt[fld_name][attmap[fld]] = entry[fld]
            if "AttributeValue" in entry:
                typName = fld_name + "Types"
                tt[fld_name]["type"] = typName
                self.attr_json["definitions"][typName] = {
                    "enum" : entry["enum"],
                    "enumDescriptions" : entry["enumDescriptions"],
                    "type" : "string",
                }

    def save_file(self, directory = None, filename = None):
        if not directory: directory = self.direct
        if not filename: filename = self.comp + ".json"
        dest_file = os.path.join(directory, filename)
        print ("Saving to :" + dest_file)
        with open(dest_file, "w") as out:
            out.write(json.dumps(self.attr_json, sort_keys=True,
                                 indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    driver_dir = os.path.join('omdrivers', 'iDRAC')
    for file1 in glob.glob(os.path.join(driver_dir, "xml", "*.xml")):
        AttribRegistry(file1).save_file(
             directory=os.path.join(driver_dir, 'Config'))
