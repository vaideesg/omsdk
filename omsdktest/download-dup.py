import sys, os
import platform
import json
import time
sys.path.append(os.getcwd())

counter = 1
from sys import stdout, path
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkfile import FileOnShare, LocalFile

from omsdk.sdkinfra import sdkinfra
import logging
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omsdk.omlogs.Logger import LogManager, LoggerConfigTypeEnum
from omdrivers.helpers.iDRAC.UpdateHelper import *

#LogManager.setup_logging()

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

# Bugs: not element>>#cdata-section

###############################
# Local Functions
###############################
def _get_arg(argsinfo, field, default = None):
    arg = default
    if field in argsinfo:
        arg = argsinfo[field]
    return arg

def get_optional(argsinfo, field, default = None):
    return _get_arg(argsinfo, field, default)

def get_args(argsinfo, field, default=None):
    arg = _get_arg(argsinfo, field, default)
    if arg is None:
        print(field + " is missing in argsinfo!")
        exit()
    return arg


def dprint(module, msg):
    global counter
    print("")
    print("=-=-=-=-=-==============================================-=-=-=-=-=")
    print("=-=-=-=-=-= "+str(counter)+ ". "+module + ": " + msg+ "=-=-=-=-=-=")
    counter = counter + 1

def wait_idrac(idrac, sl=5):
    for i in range(1, 1000):
        print('waiting for ' + str(i))
        time.sleep(sl)
        if idrac.reconnect():
                break
    print('acheived nirvana')


###############################
# Initializing Arguments
###############################

with open("omsdktest\\idrac.info", "r") as enum_data:
    argsinfo = json.load(enum_data)

ipaddr = get_args(argsinfo, 'ipaddr')
driver = get_optional(argsinfo, 'driver')
uname = get_optional(argsinfo, 'user.name')
upass = get_optional(argsinfo, 'user.password', '')
pref = get_optional(argsinfo, 'protocol', 'WSMAN')
nshare = get_optional(argsinfo, 'share')
nsharename = get_optional(argsinfo, 'share.user.name')
nsharepass = get_optional(argsinfo, 'share.user.password', '')
creds = UserCredentials(uname, upass)

@property
def not_implemented():
    print("===== not implemented ====")


myshare = LocalFile(local='C:\\Users\\vaideeswaran_ganesan\\Work\\omsdk', isFolder=True)
updshare = myshare.makedirs('DD')

UpdateManager.configure(updshare)
if updshare.IsValid:
    sd = sdkinfra()
    sd.importPath()
    idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr, creds)
    UpdateHelper.save_firmware_inventory(idrac)
    idrac.disconnect()

    UpdateManager.update_catalog()
    print("Building repo....")
    UpdateHelper.build_repo_catalog('NIC')
