from argparse import ArgumentParser
from omsdk.sdkfile import LocalFile
from omsdk.sdkcenum import TypeHelper
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
from omsdk.sdkinfra import sdkinfra
from omsdk.sdkcreds import UserCredentials
import sys

def CollectInventory(arglist):
    parser = ArgumentParser(description='Inventory Collector')
    parser.add_argument('-u', '--user', 
        action="store", dest="user", type=str, nargs='?',
        default='root', help="Username to use for iDRAC")
    parser.add_argument('-p', '--password', 
        action="store", dest="password", type=str,
        default='calvin', help="Password to use for iDRAC")
    parser.add_argument('-i', '--ipaddress',
        action="store", dest="idrac_ip", nargs='+',
        help="ipaddress of iDRAC")
    parser.add_argument('-f', '--folder', 
        action="store", dest="folder", type=str,
        help="folder from where inventory is serialized")

    options = parser.parse_args(arglist)

    if options.password is None:
        print("password must be provided")
        return -1
    if options.user is None:
        print("user must be provided")
        return -1
    if options.folder is None:
        print("Folder must be provided")
        return -1
    if options.idrac_ip is None or len(options.idrac_ip) <= 0:
        print("iDRAC ip addresses must be provided")
        return -1


    updshare = LocalFile(local = options.folder, isFolder=True)
    if not updshare.IsValid:
        print("Folder is not writable!")
        return -2

    print("Configuring Update Share...")
    UpdateManager.configure(updshare)

    sd = sdkinfra()
    sd.importPath()
    creds = UserCredentials(options.user, options.password)
    for ipaddr in options.idrac_ip:
        try:
            print("Connecting to " + ipaddr + " ... ")
            idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr, creds)
            if idrac:
                print("    ... saving firmware!")
                UpdateHelper.save_firmware_inventory(idrac)
                idrac.disconnect()
            else:
                print("    failed to connect to iDRAC")
        except Exception as ex:
            print(str(ex))

if __name__ == "__main__":
    CollectInventory(sys.argv[1:])
