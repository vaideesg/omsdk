from omsdk.catalog.pdkcatalog import DellPDKCatalog
from omsdk.catalog.updaterepo import UpdateRepo
from omsdk.sdkftp import FtpHelper, FtpCredentials
from omsdk.catalog.sdkhttpsrc import HttpHelper
from omsdk.sdkprint import PrettyPrint

import threading
import os
import glob
import logging

logger = logging.getLogger(__name__)


class UpdateManager(object):

    _update_store = None
    _update_store_lock = threading.Lock()
    @staticmethod
    def configure(update_share):
        if not update_share.IsValid:
            logger.debug("Update Share is not valid")
            return False
        if UpdateManager._update_store is None:
            with UpdateManager._update_store_lock:
                if UpdateManager._update_store is None:
                    UpdateManager._update_store = _UpdateCacheManager(update_share)
        return (UpdateManager._update_store is not None)

    @staticmethod
    def update_catalog():
        if UpdateManager._update_store:
            return UpdateManager._update_store.update_catalog()
        return { 'Status' : 'Failed', 'Message' : 'Update Manager is not initialized' }

    @staticmethod
    def update_cache():
        if UpdateManager._update_store:
            return UpdateManager._update_store.update_cache()
        return { 'Status' : 'Failed', 'Message' : 'Update Manager is not initialized' }

    @staticmethod
    def get_instance():
        return UpdateManager._update_store

class _UpdateCacheManager(object):

    def __init__(self, update_share):
        self.update_share = update_share
        self.master_share = self.update_share.makedirs("_master")\
                                             .new_file('Catalog.xml')
        self.master= MasterCatalog(self.master_share)

        self.inventory_share = self.update_share.makedirs("_inventory")
        self.cache_catalogs = {}
        catalogs_path = os.path.join(self.update_share.local_full_path, '*.xml')
        for fname in glob.glob(catalogs_path):
            self._initCatalogScoper(fname)

        self._initialize()
        self.UseFtp = False

    def _initCatalogScoper(self, name):
        if name not in self.cache_catalogs:
            self.cache_catalogs[name] = None
        return self.cache_catalogs[name]

    def _initialize(self):
        self.cache_catalogs['Catalog'] = None
        (self.cache_share, self.cache) = self.getCatalogScoper()

    def _randomCatalogScoper(self):
        fname= self.update_share.mkstemp(prefix='upd', suffix='.xml').local_full_path
        self.getCatalogScoper(os.path.basename(fname).replace('.xml', ''))

    def getCatalogScoper(self, name = 'Catalog'):
        if name not in self.cache_catalogs:
            self.cache_catalogs[name] = None

        if not self.cache_catalogs[name]:
            cache_share = self.update_share.new_file(name + '.xml')
            self.cache_catalogs[name] = (cache_share,
                 CatalogScoper(self.master, cache_share))

        return self.cache_catalogs[name]

    def getInventoryShare(self):
        return self.inventory_share

    def _get_helper(self):
        if self.UseFtp:
            conn = FtpHelper('ftp.dell.com', FtpCredentials())
        else:
            conn = HttpHelper('downloads.dell.com')
        return conn

    def update_catalog(self):
        folder = self.master_share.local_folder_path
        c = 'catalog/Catalog.gz'
        conn = self._get_helper()
        retval = conn.download_newerfiles([c], folder)
        logger.debug("Download Success = {0}, Failed = {1}"
                .format(retval['success'], retval['failed']))
        if retval['failed'] == 0 and \
           conn.unzip_file(os.path.join(folder, c),
                          os.path.join(folder, 'Catalog.xml')):
            retval['Status'] = 'Success'
        else:
            logger.debug("Unable to download and extract " + c)
            retval['Status'] = 'Failed'
        conn.close()
        self.master.update()
        self._initialize()
        return retval

    def update_cache(self):
        files_to_dld = self.cache.rcache.UpdateFilePaths
        conn = self._get_helper()
        retval = conn.download_newerfiles(files_to_dld, self.update_share.local_full_path)
        logger.debug("Download Success = {0}, Failed = {1}".format(retval['success'], retval['failed']))
        if retval['failed'] == 0:
            retval['Status'] = 'Success'
        else:
            retval['Status'] = 'Failed'
        conn.close()
        return retval

class MasterCatalog(object):
    def __init__(self, master_share):
        self.master_share = master_share
        self.cache_lock = threading.Lock()
        logger.debug("master:" + self.master_share.local_full_path)
        self.update()

    def update(self):
        self.cmaster = DellPDKCatalog(self.master_share.local_full_path)

class CatalogScoper(object):

    def __init__(self, master_catalog, cache_share):
        self.cache_share = cache_share
        self.cache_lock = threading.Lock()
        self.master_catalog = master_catalog
        logger.debug("cache:" + self.cache_share.local_folder_path)
        logger.debug("cache:" + self.cache_share.local_file_name)
        self.rcache = UpdateRepo(self.cache_share.local_folder_path,
                            catalog=self.cache_share.local_file_name,
                            source=self.master_catalog.cmaster, mkdirs=True)

    def add_to_scope(self, model, swidentity = None, *components):
        count = 0
        with self.cache_lock:
            comps = [i for i in components]
            if len(comps) > 0 and swidentity is None:
                logger.error('Software Identity must be given when scoping updates to components')
            if swidentity:
                count = self.rcache.filter_by_component(model,
                            swidentity, compfqdd=comps)
            else:
                count = self.rcache.filter_by_model(model)
        return count

    def save(self):
        with self.cache_lock:
            self.rcache.store()

    def dispose(self):
        with self.cache_lock:
            if self.cache_share.IsTemp:
                logger.debug("Temporary cache")
                self.cache_share.dispose()
            else:
                logger.debug("Not a temporary cache")
