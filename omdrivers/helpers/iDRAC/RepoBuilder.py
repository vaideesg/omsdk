#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan
#
from argparse import ArgumentParser
from omsdk.sdkfile import LocalFile
from omsdk.sdkcenum import TypeHelper
from omsdk.catalog.sdkupdatemgr import UpdateManager
from omsdk.catalog.sdkhttpsrc import DownloadProtocolEnum
from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
from omsdk.omlogs.Logger import LogManager, LoggerConfigTypeEnum
import sys
import logging

#LogManager.setup_logging()
logger = logging.getLogger(__name__)

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
    parser.add_argument('-v', '--verbose', 
        action="store_true", help="verbose mode")
    parser.add_argument('-D', '--download-dups', 
        action="store_true", dest="dld_dups", help="download DUPs")
    parser.add_argument('-l', '--download-catalog', 
        action="store_true", dest="dld_catalog", help="download catalog")
    parser.add_argument('-b', '--build-catalog', 
        action="store_true", dest="build_catalog", help="build catalog")
    parser.add_argument('-i', '--download-index', 
        action="store_true", dest="dld_index", help="build index")

    options = parser.parse_args(arglist)
    if not options.component:
        options.component = []

    if options.folder is None:
        print("Folder must be provided")
        return -1

    if options.verbose is None:
        options.verbose = False

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not options.dld_dups and not options.build_catalog and \
       not options.dld_catalog:
        options.dld_catalog = True
        options.build_catalog = True
        options.dld_dups = True

    options.protocol = TypeHelper.convert_to_enum(options.protocol,
                            DownloadProtocolEnum)

    updshare = LocalFile(local = options.folder, isFolder=True)
    if not updshare.IsValid:
        print("Folder is not writable!")
        return -2

    if options.protocol != DownloadProtocolEnum.HashCheck:
        print("Configuring Update Share...")
    UpdateManager.configure(updshare, site=options.site,
            protocol=options.protocol)

    if options.dld_catalog:
        if options.protocol != DownloadProtocolEnum.HashCheck:
            print("Updating Catalog from downloads.dell.com...")
        UpdateManager.update_catalog()
    if options.build_catalog:
        if options.protocol != DownloadProtocolEnum.HashCheck:
            print("Building Repository Catalog ....")
            UpdateHelper.build_repo(options.catalog, True, *options.component)
    if options.dld_index:
        if options.protocol != DownloadProtocolEnum.HashCheck:
            print("Updating index from downloads.dell.com...")
        UpdateManager.update_index()

    if options.dld_dups:
        if options.protocol != DownloadProtocolEnum.HashCheck:
            print("Downloading DUPs ...")
        UpdateManager.update_cache(options.catalog)

if __name__ == "__main__":
    RepoBuilder(sys.argv[1:])
