import json
import os
import logging
from omsdk.sdkproto import PCONSOLE
from omsdk.sdkconsole import iConsoleRegistry, iConsoleDriver, iConsoleDiscovery
from omsdk.sdkprint import PrettyPrint

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class OME(iConsoleDiscovery):
    def __init__(self, srcdir):
        if PY2:
            super(OME, self).__init__(iConsoleRegistry("OME", srcdir, None))
        else:
            super().__init__(iConsoleRegistry("OME", srcdir, None))
        self.protofactory.add(PCONSOLE(obj = self))

    def my_entitytype(self, pinfra, ipaddr, creds, protofactory):
        return OMEEntity(self.ref, protofactory, ipaddr, creds)

class OMEEntity(iConsoleDriver):
    def __init__(self, ref, protofactory, ipaddr, creds):
        if PY2:
            super(OMEEntity, self).__init__(ref, protofactory, ipaddr, creds)
        else:
            super().__init__(ref, protofactory, ipaddr, creds)

    def my_connect(self, pOptions):
        status = False
        try :
            if os.path.isfile("d\\" + self.ipaddr + "\\topology"):
                status = True
        except:
            status = False
        logger.debug(self.ref.name + '::connect(' + self.ipaddr + ', ' + str(self.creds) + ")=" + str(status))
        return status

    def my_get_entityjson(self):
        logger.debug("Loading entity")
        # https://100.96.20.115:2607/api/OME.svc/DeviceGroups
        with open("d\\" + self.ipaddr + "\\topology") as idrac_data:
            self.entityjson["topology"] = json.load(idrac_data)
        # https://100.96.20.115:2607/api/OME.svc/Devices
        # https://100.96.20.115:2607/api/OME.svc/Devices/187
        with open("d\\" + self.ipaddr + "\\devices") as idrac_data:
            self.entityjson["devices"] = json.load(idrac_data)
        return True

    def get_service_tag(self):
        return self.ipaddr

    def get_device_identifier(self, device):
        retval = None
        if not device is None and "System" in device:
            if "ServiceTag" in device["System"]:
                retval = device["System"]["ServiceTag"]
        return retval

    def add_device_props(self, device):
        retval = self.get_device_identifier(device)
        if not retval is None:
            retval = "10.94.44." + retval
            device["doc.prop"] = {}
            device["doc.prop"]["ipaddr"] = retval
            device["doc.prop"]["creds"] = ""
        return retval
