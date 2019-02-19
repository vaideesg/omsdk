import xml.etree.ElementTree as ET
import json
import glob

tags = {
    'Criticality' : [ 'value' ],
    'ComponentType' : [ 'value' ],
    'SupportedDevices' : [ ],
    'SupportedSystems' : [ ],
    'Brand' : [ ],
    'Device' : [ 'componentID' ],
    'Model' : [ 'systemID' ],
    'PCIInfo' : [ 'deviceID', 'subDeviceID', 'subVendorID', 'vendorID' ],
}

model_map ={}
for fname in glob.glob('../omdata/SDKRepo/*/Catalog.xml'):
    tree = ET.parse(fname)
    for sc in tree.findall('./SoftwareComponent'):
        fields_1 = {
            'catalog_version' : tree.getroot().attrib['version'],
            'min_cat' :  tree.getroot().attrib['version'],
            'max_cat' :  tree.getroot().attrib['version'],
        }
        for i in ['dateTime', 'vendorVersion', 'path']:
            fields_1[i] = sc.attrib[i]
        for sc_c in sc:
            if sc_c.tag not in tags: continue
            for i in tags[sc_c.tag]:
                fields_1[sc_c.tag + "_" + i] = sc_c.attrib[i]
        if fields_1['ComponentType_value'] not in ["FRMW", "APAC"]:
            continue
        device_map = {}
        for device in sc.findall('./SupportedDevices/Device'):
            count = 0
            for pci in device.findall('./PCIInfo'):
                count = count + 1
                cid = device.attrib['componentID']
                cid="{0}-{1}-{2}-{3}-{4}".format(cid, pci.attrib['deviceID'],
                        pci.attrib['subDeviceID'], pci.attrib['vendorID'],
                        pci.attrib['subVendorID'])
                device_map[cid] = {}
                device_map[cid].update(fields_1)
                cid="-{0}-{1}-{2}-{3}".format(pci.attrib['deviceID'],
                        pci.attrib['subDeviceID'], pci.attrib['vendorID'],
                        pci.attrib['subVendorID'])
                device_map[cid] = {}
                device_map[cid].update(fields_1)
            if count <= 0:
                cid = device.attrib['componentID']
                device_map[cid] = {}
                device_map[cid].update(fields_1)
        for model in sc.findall('./SupportedSystems/Brand/Model'):
            for k in device_map:
                for mid in ["{0}-{1}".format(model.attrib['systemID'],k),"-"+k]:
                    if mid not in model_map:
                        model_map[mid] = { '_plist' : [] }
                    path = device_map[k]['path']
                    if path in model_map[mid]:
                        if model_map[mid][path]['min_cat'] > device_map[k]['min_cat']:
                            model_map[mid][path]['min_cat'] = device_map[k]['min_cat']
                        if model_map[mid][path]['max_cat'] < device_map[k]['max_cat']:
                            model_map[mid][path]['max_cat'] = device_map[k]['max_cat']
                        continue
                    model_map[mid][path] = {}
                    model_map[mid][path].update(device_map[k])
                    #model_map[mid][path]['systemID'] = model.attrib['systemID']
                    if len(model_map[mid]['_plist']) == 0:
                        model_map[mid]['_plist'].append(path)
                        continue
                    pend = model_map[mid]['_plist'][-1]
                    if model_map[mid][pend]['dateTime'] < device_map[k]['dateTime']:
                        model_map[mid]['_plist'].append(path)
                        continue
                    for i in range(0, len(model_map[mid]['_plist'])):
                        pend = model_map[mid]['_plist'][i]
                        if (device_map[k]['dateTime'] < model_map[mid][pend]['dateTime']):
                            model_map[mid]['_plist'].insert(i, path)
                            break

print(json.dumps(model_map, sort_keys=True, indent=4, \
          separators=(',', ': ')))
