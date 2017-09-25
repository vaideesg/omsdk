import sys, os
import platform
import json
import time
sys.path.append(os.getcwd())

counter = 1
from sys import stdout, path
from omsdk.sdkcreds import UserCredentials,ProtocolCredentialsFactory
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkfile import FileOnShare, LocalFile
from omsdk.sdkenum import MonitorScopeFilter, MonitorScope
from omsdk.sdkproto import ProtocolEnum
from omsdk.sdkinfra import sdkinfra
from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum, ProtoMethods
from omsdk.catalog.sdkupdatemgr import UpdateManager
import logging
from omsdk.omlogs.Logger import LogManager, LoggerConfigTypeEnum
from omdrivers.enums.iDRAC.iDRACEnums import *
from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
from omsdk.sdkproto import Simulator

#Simulator.start_simulating()

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
image = get_optional(argsinfo, 'image', '')
creds = ProtocolCredentialsFactory()
if uname :
    creds.add(UserCredentials(uname, upass))
protopref = None
if pref == "WSMAN":
    protopref = ProtoPreference(ProtocolEnum.WSMAN)

@property
def not_implemented():
    print("===== not implemented ====")


if platform.system() == "Windows":
    myshare = FileOnShare(remote =nshare,
        mount_point='Z:\\', isFolder=True,
        creds = UserCredentials(nsharename, nsharepass))
    updshare = myshare
else:
    myshare = FileOnShare(remote =nshare,
        mount_point='/tst', isFolder=True,
        creds = UserCredentials(nsharename, nsharepass))
    updshare = myshare

sd = sdkinfra()
sd.importPath()

t1 = time.time()

dprint("Driver SDK", "1.03 Connect to " + ipaddr)
idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr, creds, protopref)
if idrac is None:
        print ("Error: Not found a device driver for: " + ipaddr)
        exit()
else:
        print("Connected to " + ipaddr)

dprint("Driver SDK", "5.04 Export SCP")
scp_file = myshare.new_file('fact_%ip_%Y%m%d_%H%M%S.xml')
msg = idrac.config_mgr.scp_export(scp_file, method=ExportMethodEnum.Clone)
print(PrettyPrint.prettify_json(msg))

if msg['Status'] == "Success":
    print("Saved to file :" + msg['file'])
else:
    print("Operation Failed with Message :" + msg['Message'])

dprint("Driver SDK", "5.04 Export SCP Async")
scp_file = myshare.new_file('fact_%ip_%Y%m%d_%H%M%S.xml')
msg = idrac.config_mgr.scp_export(scp_file, job_wait=False)
print(PrettyPrint.prettify_json(msg))
if msg['Status'] == 'Success':
        print("Saving to file :" + msg['file'])
        jobid = msg['Job']['JobId']
        retVal = idrac.job_mgr.job_wait(jobid, show_progress=True)
        if msg['Status'] == "Success":
            print("Successfully saved file!")
        else:
            print("Job Failed with Message :" + msg['Message'])
else:
        print("Operation Failed with Message :" + msg['Message'])
