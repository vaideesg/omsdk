from omsdk.catalog.pdkcatalog import DellPDKCatalog
from omsdk.catalog.updaterepo import UpdateRepo
from omsdk.sdkfile import FileOnShare
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkftp import FtpHelper, FtpCredentials
from omsdk.sdkprint import LogMan
import json
import threading
import os

class UpdateManager(object):

    _update_store = None
    _update_store_lock = threading.Lock()
    @staticmethod
    def configure(update_share):
        if not update_share.IsValid:
            print("Update Share is not valid")
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
    def add_models(ids):
        if UpdateManager._update_store:
            catscope = UpdateManager._update_store.cache
            for model in ids:
                catscope.add_model_to_scope(model)
            catscope.save()
            return { 'Status' : 'Success' }
        return { 'Status' : 'Failed', 'Message' : 'Update Manager is not initialized' }

    @staticmethod
    def add_devices(devices):
        if UpdateManager._update_store:
            catscope = UpdateManager._update_store.cache
            if not isinstance(devices, list):
                devices = [devices]
            for device in devices:
                catscope.add_device_to_scope(device)
            catscope.save()
            return { 'Status' : 'Success' }
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
        self.update_share.makedirs("_master")
        self.master_share = self.update_share.new_file("_master", ".\\Catalog.xml")
        self.cache_share = self.update_share.new_file(".\\StoreCatalog.xml")
        self.cache = CatalogScoper(self.master_share, self.cache_share)

    def scoped_to_components(self, catscope, model, swidentity, compfqdd):
        if catscope is None:
            temp_share = self.update_share.mkstemp(prefix='upd', suffix='.xml')
            catscope = CatalogScoper(self.cache_share, temp_share)
        catscope.add_to_scope(model, swidentity, *compfqdd)
        catscope.save()
        return catscope

    def scoped_to_device(self, catscope, model, swidentity):
        if catscope is None:
            temp_share = self.update_share.mkstemp(prefix='upd', suffix='.xml')
            catscope = CatalogScoper(self.cache_share, temp_share)
        catscope.add_to_scope(model, swidentity)
        catscope.save()
        return catscope

    def scoped_to_model(self, catscope, model):
        if catscope is None:
            temp_share = self.update_share.mkstemp(prefix='upd', suffix='.xml')
            catscope = CatalogScoper(self.cache_share, temp_share)
        catscope.add_model_to_scope(model)
        catscope.save()
        return catscope

    def update_catalog(self):
        folder = self.cache.master_share.mount_point.share_path
        ftp = FtpHelper('ftp.dell.com', FtpCredentials())
        c = 'Catalog.xml.gz'
        retval = ftp.download_newerfiles([c], folder)
        LogMan.debug("Download Success = {0}, Failed = {1}".format(retval['success'], retval['failed']))
        if retval['failed'] == 0 and ftp.unzip_file(os.path.join(folder, c)):
            retval['Status'] = 'Success'
        else:
            print("Unable to download and extract " + c)
            retval['Status'] = 'Failed'
        ftp.close()
        return retval

    def update_cache(self):
        files_to_dld = self.cache.rcache.UpdateFilePaths
        ftp = FtpHelper('ftp.dell.com', FtpCredentials())
        retval = ftp.download_newerfiles(files_to_dld, self.update_share.mount_point.full_path)
        LogMan.debug("Download Success = {0}, Failed = {1}".format(retval['success'], retval['failed']))
        if retval['failed'] == 0:
            retval['Status'] = 'Success'
        else:
            retval['Status'] = 'Failed'
        ftp.close()
        return retval

class CatalogScoper(object):

    def __init__(self, master_share, cache_share):
        self.master_share = master_share
        self.cache_share = cache_share
        self.cache_lock = threading.Lock()
        LogMan.debug("master:" + self.master_share.mount_point.full_path)
        self.cmaster = DellPDKCatalog(self.master_share.mount_point.full_path)

        LogMan.debug("cache:" + self.cache_share.mount_point.share_path)
        LogMan.debug("cache:" + self.cache_share.mount_point.file_name)
        self.rcache = UpdateRepo(self.cache_share.mount_point.share_path,
                            catalog=self.cache_share.mount_point.file_name,
                            source=self.cmaster, mkdirs=True)


    def add_model_to_scope(self, model):
        count = 0
        with self.cache_lock:
            count = self.rcache.filter_by_model(model)
        return count

    def add_device_to_scope(self, device):
        if hasattr(device, 'update_mgr'):
            if hasattr(device.update_mgr, 'catalog_scoped_to_device'):
                device.update_mgr.catalog_scoped_to_device(self)

    def add_to_scope(self, model, swidentity, *components):
        count = 0
        with self.cache_lock:
            comps = [i for i in components]
            count = self.rcache.filter_by_component(model,
                            swidentity, compfqdd=comps)
        return count

    def save(self):
        with self.cache_lock:
            self.rcache.store()

    def dispose(self):
        with self.cache_lock:
            if self.cache_share.IsTemp:
                LogMan.debug("Temporary cache")
                self.cache_share.dispose()
            else:
                LogMan.debug("Not a temporary cache")

