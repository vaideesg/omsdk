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
                typName = fld_name.strip() + "Types"
                typName = re.sub('^(^[0-9])', 'E_\\1', typName)
                typName = re.sub('[[]([^]:]+)[^]]*[]]', '\\1', typName)
                typName = re.sub('[?]', '', typName)
                typName = re.sub('-', '_', typName)
                tt[fld_name]["type"] = typName
                self.attr_json["definitions"][typName] = {
                    "enum" : entry["enum"],
                    "enumDescriptions" : entry["enumDescriptions"],
                    "type" : "string",
                }

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

    def save_enums(self, directory = None, filename = None):
        if self.comp == 'EventFilters': return
        if not directory: directory = self.direct
        if not filename: filename = self.comp + ".py"
        dest_file = os.path.join(directory, filename)
        print('Saving to :' + dest_file)
        with open(dest_file, 'w') as out:
            out.write('from omsdk.sdkcenum import EnumWrapper\n')
            out.write('import logging\n')
            out.write('\n')
            out.write('logger = logging.getLogger(__name__)\n')
            out.write('\n')
            props = self.attr_json
            sprops = []
            for i in props['definitions']:
                if 'enum' not in props['definitions'][i]:
                    continue
                sprops.append(i)
            sprops = sorted(sprops)

            for i in sprops:
                en_val = [k.strip() for k in props['definitions'][i]['enum']]
                en_name = []
                out.write('{0} = EnumWrapper("{0}", '.format(i) + '{\n')
                MBLOOKUP = {
                  '1KB' : 1*1024,
                  '2KB' : 2*1024,
                  '4KB' : 4*1024,
                  '8KB' : 8*1024,
                  '16KB' : 16*1024,
                  '32KB' : 32*1024,
                  '64KB' : 64*1024,
                  '128KB' : 128*1024,
                  '256KB' : 256*1024,
                  '512KB' : 512*1024,
                  '1MB' : 1*1024*1024,
                  '2MB' : 2*1024*1024,
                  '4MB' : 4*1024*1024,
                  '8MB' : 8*1024*1024,
                  'Default' : 'Default',
                  '512' : '512',
                }

                for ent in en_val:
                    en_name.append(self._sanitize(ent))
                if i == 'StripeSizeTypes':
                    t_en_val = []
                    for ent in en_val:
                        t_en_val.append(MBLOOKUP[ent])
                    en_val = t_en_val
                en_dict = dict(zip(en_name, en_val))
                snames = sorted([i for i in en_dict])
                for j in snames:
                    out.write('    "{0}" : "{1}",\n'.format(j, en_dict[j]))
                out.write('}).enum_type\n')
                out.write('\n')

    def _sanitize(self, tval):
        if tval:
            tval = re.sub('[^A-Za-z0-9]', '_', tval)
            tval = re.sub('[^A-Za-z0-9]', '_', tval)
            tval = re.sub('^(True|None|False)$', 'T_\\1', tval)
            tval = re.sub('^(^[0-9])', 'T_\\1', tval)
        return tval

    def _print(self, out, props, mode):
        cls_props = {}
        for i in props:
            include_prop = True

            if 'readonly' in props[i] and \
                props[i]['readonly'].lower() in ['true']:
                # readonly attributes not applicable for Delete, Modify

                if mode in ['Delete', 'Modify'] or \
                    'longDescription' not in props[i] or \
                    'Configurable via XML' not in props[i]['longDescription']:
                    continue

            if 'default' not in props[i]:
                props[i]['default'] = None
            cls_props[i] = props[i]['default']

        s_cls_props = sorted([i for i in cls_props])
        out.write('    def my_{0}(self):\n'.format(mode))
        for i in s_cls_props:
            if '[Partition:n]' in i:
                continue
            defval = cls_props[i]

            if defval:
                typename = None
                if 'type' in props[i]:
                    typename = props[i]['type']
                    if typename in self.attr_json["definitions"]:
                        typedef = self.attr_json['definitions'][typename]
                        if 'enum' not in typedef or defval not in typedef['enum']:
                            print(defval + " not in " + self.comp+'.'+typename)
                            defval = None
            if defval and 'type' in props[i]:
                defval = props[i]['type'] + '.' + self._sanitize(defval)
            elif defval:
                defval = '"' + defval + '"'
            else:
                defval = str(defval)
            out.write('        self.{0} = {1}\n'.format(i, str(defval)))
        out.write('        return self\n')
        out.write('\n')

    def save_types(self, directory = None, filename = None):
        # BIOS, FCHBA
        # iDRAC??
        if self.comp == 'EventFilters': return
        if not directory: directory = self.direct
        if not filename: filename = self.comp + ".py"
        dest_file = os.path.join(directory, filename)
        print('Saving to :' + dest_file)

        with open(dest_file, 'w') as out:
            props = self.attr_json['definitions'][self.comp]['properties']
            out.write('from omsdk.sdkcenum import EnumWrapper\n')
            out.write('from omdrivers.types.iDRAC.BaseARType import *\n')
            out.write('from omdrivers.enums.iDRAC.{0} import *\n'.format(self.comp))
            out.write('import logging\n')
            out.write('\n')
            out.write('logger = logging.getLogger(__name__)\n')
            out.write('\n')
            out.write('class {0}(BaseARType):\n'.format(self.comp))
            out.write('\n')
            self._print(out, props, 'create')
            self._print(out, props, 'modify')
            self._print(out, props, 'delete')

if __name__ == "__main__":
    driver_dir = os.path.join('omdrivers', 'iDRAC')
    for file1 in glob.glob(os.path.join(driver_dir, "xml", "*.xml")):
        ar= AttribRegistry(file1)
        ar.save_file(directory=os.path.join(driver_dir, 'Config'))
        ar.save_enums(directory=os.path.join('omdrivers', 'enums', 'iDRAC'))
        ar.save_types(directory=os.path.join('omdrivers', 'types', 'iDRAC'))
