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
from omsdk.catalog.pdkcatalog import DellPDKCatalog
from omsdk.catalog.pdkcatalog import DellPDKIndexCatalog
from omsdk.catalog.updaterepo import UpdateRepo,RepoComparator
from omsdk.catalog.sdkhttpsrc import DownloadHelper,DownloadProtocolEnum
from omsdk.catalog.sdkhttpsrc import SkipDownloadHelper
from omsdk.sdkprint import PrettyPrint

import threading
import os
import glob
import logging
import json

logger = logging.getLogger(__name__)


class UpdateManager(object):

    _update_store = None
    _update_index_store = None
    _update_store_lock = threading.Lock()
    @staticmethod
    def configure(update_share, site = 'downloads.dell.com',
                  protocol = DownloadProtocolEnum.HTTP):
        if not update_share.IsValid:
            logger.debug("Update Share is not valid")
            return False
        if UpdateManager._update_store is None:
            with UpdateManager._update_store_lock:
                if UpdateManager._update_store is None:
                    UpdateManager._update_store = \
                         _UpdateCacheManager(update_share, site, protocol)
        if UpdateManager._update_index_store is None:
            with UpdateManager._update_store_lock:
                if UpdateManager._update_index_store is None:
                    UpdateManager._update_index_store = \
                         _UpdateIndexCacheManager(update_share, site, protocol)
        return (UpdateManager._update_store is not None)

    @staticmethod
    def update_catalog():
        retval = { 'Status' : 'Failed',
                   'Message' : 'Update Manager is not initialized' }
        if UpdateManager._update_store:
            retval.update(UpdateManager._update_store.update_catalog())
        return retval

    @staticmethod
    def update_index():
        retval = { 'Status' : 'Failed',
                   'Message' : 'Update Manager is not initialized' }
        if UpdateManager._update_index_store:
            retval.update(UpdateManager._update_index_store.update_index())
        return retval

    @staticmethod
    def update_cache(catalog = 'Catalog'):
        retval = { 'Status' : 'Failed',
                   'Message' : 'Update Manager is not initialized' }
        if UpdateManager._update_store:
            retval.update(UpdateManager._update_store.update_cache(catalog))
        return retval

    @staticmethod
    def get_instance():
        return UpdateManager._update_store

class _UpdateIndexCacheManager(object):
    def __init__(self, update_share, site, protocol):
        self._update_share = update_share
        self._master_index = update_share.makedirs("_index")\
                                             .new_file('CatalogIndex.xml')
        self._index = None
        self._indexes = {}
        self._masters = {}
        self._conn = DownloadHelper(site = site, protocol = protocol)
        #self._conn = SkipDownloadHelper(site = site, protocol = protocol)

    def update_index(self):
        folder = self._master_index.local_folder_path
        c = 'catalog/CatalogIndex.gz'
        retval = self._conn.download_newerfiles([c], folder)
        logger.debug("Download Success = {0}, Failed = {1}"
                .format(retval['success'], retval['failed']))
        if retval['failed'] == 0:
            retval = self._load_index(retval)
        else:
            logger.debug("Unable to download and extract " + c)
            retval['Status'] = 'Failed'
        self._conn.disconnect()
        return retval

    def _load_index(self, retval = {}):
        retval= {}
        folder = self._master_index.local_folder_path
        c = 'catalog/CatalogIndex.gz'
        if self._conn.unzip_file(os.path.join(folder, c),
                          os.path.join(folder, 'CatalogIndex.xml')):
            retval['Status'] = 'Success'
            self._index = DellPDKIndexCatalog(self._master_index.local_full_path)
            for i in self._index.filter_index():
                self._indexes[i['version']] = i
        else:
            logger.debug("Unable to extract " + c)
            retval['Status'] = 'Failed'
        return retval

    def get_all_json(self, models):
        for version in self._indexes:
            if version not in self._masters:
                if version not in self._indexes:
                    return { 'Status' : 'Failed',
                        'Message' : version + " not found in indexes" }
                m_share = self._update_share.makedirs(version)
                self._masters[version] = _CatalogManager(m_share,
                    self._indexes[version]['path'], self._conn)

            fname = self._masters[version]._scoped_catalog_share.local_full_path
            if not os.path.exists(fname + "_catalog.json"):
                self._masters[version].update_catalog()
                (cshare, scoper) = self._masters[version].getCatalogScoper()
                for model in models:
                    scoper.add_to_scope(model)
                with open(fname + "_catalog.json", "w") as f:
                    f.write(json.dumps(scoper.get_json(), sort_keys=True,
                            indent=4, separators=(',', ': ')))
                    f.flush()

class _CatalogManager(object):

    def __init__(self, update_share, catalog_src, conn):
        self._scoped_catalog_share = update_share
        self._master_share = update_share.makedirs("_master")\
                                             .new_file('Catalog.xml')
        self._master= MasterCatalog(self._master_share)
        self._conn = conn
        self._catalog_src = catalog_src

        self._inventory_share = update_share.makedirs("_inventory")
        self._cache_catalogs = {}

        self._initialize()

    def _initialize(self):
        self._master.load()
        catalogs_path = os.path.join(self._scoped_catalog_share.local_full_path, '*.xml')
        for name in glob.glob(catalogs_path):
            fname = os.path.basename(name).replace('.xml', '')
            if fname not in self._cache_catalogs:
                self._cache_catalogs[fname] = None
        self._cache_catalogs['Catalog'] = None

    def _randomCatalogScoper(self):
        fname= self._scoped_catalog_share.mkstemp(prefix='upd', suffix='.xml').local_full_path
        self.getCatalogScoper(os.path.basename(fname).replace('.xml', ''))

    def getCatalogScoper(self, name = 'Catalog'):
        if name not in self._cache_catalogs:
            self._cache_catalogs[name] = None

        if not self._cache_catalogs[name]:
            cache_share = self._scoped_catalog_share.new_file(name + '.xml')
            self._cache_catalogs[name] = (cache_share,
                 CatalogScoper(self._master, cache_share))

        return self._cache_catalogs[name]

    def getInventoryShare(self):
        return self._inventory_share

    def update_catalog(self):
        folder = self._master_share.local_folder_path
        c = self._catalog_src
        retval = self._conn.download_newerfiles([c], folder)
        logger.debug("Download Success = {0}, Failed = {1}"
                .format(retval['success'], retval['failed']))
        if retval['failed'] == 0 and \
           self._conn.unzip_file(os.path.join(folder, c),
                          os.path.join(folder, 'Catalog.xml')):
            retval['Status'] = 'Success'
        else:
            logger.debug("Unable to download and extract " + c)
            retval['Status'] = 'Failed'
        self._conn.disconnect()
        self._initialize()
        return retval

    def update_cache(self, catalog = 'Catalog'):
        (cache_share, cache) = self.getCatalogScoper(catalog)
        retval = self._conn.download_newerfiles(cache.UpdateFileDetails,
                        self._scoped_catalog_share.local_full_path)
        logger.debug("Download Success = {0}, Failed = {1}".\
                     format(retval['success'], retval['failed']))
        if retval['failed'] == 0:
            retval['Status'] = 'Success'
        else:
            retval['Status'] = 'Failed'
        self._conn.disconnect()
        return retval

class _UpdateCacheManager(_CatalogManager):

    def __init__(self, update_share, site, protocol):
        conn = DownloadHelper(site = site, protocol = protocol)
        super().__init__(update_share, 'catalog/Catalog.gz', conn)

class MasterCatalog(object):
    def __init__(self, master_share):
        self._master_share = master_share
        self.cache_lock = threading.Lock()
        logger.debug("master:" + self._master_share.local_full_path)

    def load(self):
        with self.cache_lock:
            self.cmaster = DellPDKCatalog(self._master_share.local_full_path)

class CatalogScoper(object):

    def __init__(self, master_catalog, cache_share):
        self.ostype = "WIN64"
        self._cache_share = cache_share
        self.cache_lock = threading.Lock()
        self._master_catalog = master_catalog
        logger.debug("cache:" + self._cache_share.local_folder_path)
        logger.debug("cache:" + self._cache_share.local_file_name)
        self._rcache = UpdateRepo(self._cache_share.local_folder_path,
                            catalog=self._cache_share.local_file_name,
                            source=self._master_catalog.cmaster, mkdirs=True)

    @property
    def UpdateFilePaths(self):
        return self._rcache.UpdateFilePaths

    @property
    def UpdateFileDetails(self):
        return self._rcache.UpdateFileDetails

    def add_to_scope(self, model, swidentity = None, *components):
        count = 0
        with self.cache_lock:
            comps = [i for i in components]
            if len(comps) > 0 and swidentity is None:
                logger.error('Software Identity must be given when scoping updates to components')
            if swidentity:
                count = self._rcache.filter_by_component(model,
                            swidentity, self.ostype, compfqdd=comps)
            else:
                count = self._rcache.filter_by_model(model, self.ostype)
        return count

    def compare(self, model, swidentity):
        compare = RepoComparator(swidentity)
        self._rcache.filter_by_component(model, swidentity, self.ostype, compare=compare)
        return compare.final()

    def save(self):
        with self.cache_lock:
            self._rcache.store()

    def get_json(self):
        with self.cache_lock:
            self._rcache.store()
        return self._rcache.get_json()

    def dispose(self):
        with self.cache_lock:
            if self._cache_share.IsTemp:
                logger.debug("Temporary cache")
                self._cache_share.dispose()
            else:
                logger.debug("Not a temporary cache")

