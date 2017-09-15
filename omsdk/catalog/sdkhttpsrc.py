import os
import sys
import glob
import socket
import time
import gzip
import shutil
import logging
import gzip
from omsdk.sdkprint import PrettyPrint

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    from httplib import HTTPConnection
if PY3:
    from http.client import HTTPConnection

logger = logging.getLogger(__name__)

class HttpHelper:
    def __init__(self, site):
        try :
            self.http = HTTPConnection(site)
        except socket.error as e:
            self.http = None
            logger.debug("ERROR: Connection failed: " + str(e))
            return
        except socket.gaierror as e:
            self.http = None
            logger.debug("ERROR: Connection failed: " + str(e))
            return

    def close(self):
        try:
            if self.http:
                self.http.close()
            self.http = None
        except socket.timeout:
            logger.debug('ERROR:: socket timedout')
        except Exception as err:
            logger.debug('ERROR:: ' + str(err))

    def list_files_to_download(self, flist, lfolder="."):
        dlist = [fname for fname in flist ]
        return dlist

    def download_file(self, fname, lfname):
        try:
            if not self.http:
                return False
            logger.debug('Downloading ' + fname + " to " + lfname)
            self.http.request('GET', '/' + fname)
            response = self.http.getresponse()
            with open(lfname, 'wb') as f:
                f.write(response.read())

        except Exception as ex:
            logger.debug("File Download failed:" + str(ex))
            return False
        return True

    def _download_files(self, fname, lfolder):
        rfname = fname.split('/')
        lfile = os.path.join(lfolder, *rfname)
        if len(rfname) > 1:
            nfolder = os.path.join(lfolder, *rfname[0:-1])
            if not os.path.exists(nfolder):
                try:
                    os.makedirs(nfolder)
                except Exception as ex:
                    logger.debug("Cannot create directory : " + str(ex))
                    return False
            elif not os.path.isdir(nfolder):
                logger.debug("cannot create directory, file exists: " + nfolder)
                return False
        return self.download_file(fname, lfile)

    def download_file_to_folder(self, fname, lfolder = "."):
        if not os.path.exists(lfolder) or not os.path.isdir(lfolder):
            logger.debug("Need a folder name")
            return False
        return self._download_files(fname, lfolder)


    def download_files(self, flist, lfolder = "."):
        counter = { 'success' : 0, 'failed' : 0 }
        for fname in flist:
            if self.download_file_to_folder(fname, lfolder):
                counter['success'] += 1
            else:
                counter['failed'] += 1
        return counter

    def download_newerfiles(self, flist, lfolder = "."):
        flist = self.list_files_to_download(flist, lfolder)
        return self.download_files(flist, lfolder)

    def unzip_file(self, lfname, tfname=None):
        if not tfname:
            tfname = lfname.rsplit('.gz',1)[0]
        f_in = gzip.open(lfname, 'rb')
        try:
            with open(tfname, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        finally:
            f_in.close()
        return True
