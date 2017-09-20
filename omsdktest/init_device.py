import sys, os
import platform
import json
import time
import logging
sys.path.append(os.getcwd())

counter = 1
from omsdk.sdkcreds import UserCredentials,ProtocolCredentialsFactory
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkfile import FileOnShare
from omsdk.sdkinfra import sdkinfra
from omsdk.omlog.Logger import LogManager, LoggerConfigTypeEnum
from omdrivers.enums.iDRAC.iDRACEnums import *

#LogManager.setup_logging()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
_argsinfo = {}

###############################
# Local Functions
###############################
def _get_arg(field, default = None):
    arg = default
    if field in _argsinfo:
        arg = _argsinfo[field]
    return arg

def _get_optional(field, default = None):
    return _get_arg(field, default)

def _get_args(field, default=None):
    arg = _get_arg(field, default)
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


###############################
# Initializing Arguments
###############################

with open("omsdktest\\idrac.info", "r") as enum_data:
    _argsinfo = json.load(enum_data)

ipaddr = _get_args('ipaddr')
driver = _get_optional('driver')
uname = _get_optional('user.name')
upass = _get_optional('user.password', '')
pref = _get_optional('protocol', 'WSMAN')
nshare = _get_optional('share')
nsharename = _get_optional('share.user.name')
nsharepass = _get_optional('share.user.password', '')
image = _get_optional('image', '')
creds = ProtocolCredentialsFactory()
if uname :
    creds.add(UserCredentials(uname, upass))

@property
def not_implemented():
    print("===== not implemented ====")


if platform.system() == "Windows":
    liason_share = FileOnShare(remote =nshare,
        mount_point='Z:\\', isFolder=True,
        creds = UserCredentials(nsharename, nsharepass))
else:
    liason_share = FileOnShare(remote =nshare,
        mount_point='/tst', isFolder=True,
        creds = UserCredentials(nsharename, nsharepass))

sd = sdkinfra()
sd.importPath()

