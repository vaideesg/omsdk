from argparse import ArgumentParser
from omsdk.sdkfile import LocalFile
from omsdk.sdkcenum import TypeHelper
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omsdk.catalog.sdkhttpsrc import DownloadProtocolEnum
from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
from omsdk.omlog.Logger import LogManager, LoggerConfigTypeEnum
import sys
import logging

#LogManager.setup_logging()
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

def RepoBuilder(arglist):
    parser = ArgumentParser(description='Local Repository Builder')
    parser.add_argument('-C', '--catalog', 
        action="store", dest="catalog", nargs='?',
        default='Catalog', type=str,
        help="Name of the Catalog file that contains the info about needed DUPs")
    parser.add_argument('-f', '--folder', 
        action="store", dest="folder", type=str,
        help="folder from where repository is built")
    parser.add_argument('-c', '--components',
        action="store", dest="component", nargs='+',
        help="components for which the DUPs are requested.")
    parser.add_argument('-s', '--site', 
        action="store", dest="site", type=str, nargs='?',
        default='downloads.dell.com',
        help="models for which the DUPs are requested.")
    parser.add_argument('-p', '--protocol', 
        action="store", dest="protocol", nargs='?',
        default='HTTP', choices=['HTTP', 'FTP', 'NoOp', 'HashCheck'],
        help="models for which the DUPs are requested.")

    options = parser.parse_args(arglist)
    if not options.component:
        options.component = []

    if options.folder is None:
        print("Folder must be provided")
        return -1

    options.protocol = TypeHelper.convert_to_enum(options.protocol,
                            DownloadProtocolEnum)

    updshare = LocalFile(local = options.folder, isFolder=True)
    if not updshare.IsValid:
        print("Folder is not writable!")
        return -2

    print("Configuring Update Share...")
    UpdateManager.configure(updshare, site=options.site,
            protocol=options.protocol)
    print("Updating Catalog from downloads.dell.com...")
    UpdateManager.update_catalog()
    print("Building Repository Catalog ....")
    UpdateHelper.build_repo(options.catalog, True, *options.component)
    print("Downloading DUPs ...")
    UpdateManager.update_cache(options.catalog)

if __name__ == "__main__":
    RepoBuilder(sys.argv[1:])
