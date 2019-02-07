import sys, os
import platform
import json
import time
sys.path.append(os.getcwd())

counter = 1
from omsdk.sdkcreds import UserCredentials,ProtocolCredentialsFactory
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkinfra import sdkinfra
import logging



logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

creds = ProtocolCredentialsFactory()
creds.add(UserCredentials("root", "calvin"))
ipaddr = "100.96.25.119"

sd = sdkinfra()
sd.importPath()

cmc = sd.get_driver(sd.driver_enum.CMC, ipaddr, creds)
if cmc is None:
        print ("Error: Not found a device driver for: " + ipaddr)
        exit()
else:
        print("Connected to " + ipaddr)

idrac_ips = cmc.get_idrac_ips()
print(PrettyPrint.prettify_json(cmc.get_json_device()["ComputeModule"]))
