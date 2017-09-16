import os
import sys
import glob
import socket
import time
import gzip
import shutil
import logging
import gzip
import hashlib
import base64
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkcenum import EnumWrapper, TypeHelper

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    from httplib import HTTPConnection
if PY3:
    from http.client import HTTPConnection

logger = logging.getLogger(__name__)

DownloadProtocolEnum = EnumWrapper('DPE', {
   "HTTP" : 'HTTP',
   "FTP" : 'FTP',
   "NoOp" : 'NoOp',
   'HashCheck' : 'HashCheck',
}).enum_type


class FtpCredentials:
    def __init__(self, user='anonymous', password='anonymous@'):
        self.user = user
        self.password = password

class DownloadHelper:
    def __init__(self, site, protocol = DownloadProtocolEnum.HTTP, creds=None):
        self.protocol = protocol
        self.creds = creds
        self.site = site
        self.conn = None
        self.connect()

    def connect(self):
        try :
            if self.conn:
                return True
            if self.protocol == DownloadProtocolEnum.HTTP:
                self.conn = HTTPConnection(self.site)
            elif self.protocol == DownloadProtocolEnum.FTP:
                if self.creds is None: self.creds = FtpCredentials()
                self.conn = FTP(self.site, timeout=60)
                self.conn.login(self.creds.user, self.creds.password)
            elif self.protocol == DownloadProtocolEnum.NoOp:
                self.conn = 'Connected'
            elif self.protocol == DownloadProtocolEnum.HashCheck:
                self.conn = 'Connected'
            return True
        except socket.error as e:
            self.conn = None
            logger.debug("ERROR: Connection failed: " + str(e))
            return False
        except socket.gaierror as e:
            self.conn = None
            logger.debug("ERROR: Connection failed: " + str(e))
            return False

    def disconnect(self):
        try:
            if not self.conn:
                return True
            if self.protocol == DownloadProtocolEnum.HTTP:
                self.conn.close()
            elif self.protocol == DownloadProtocolEnum.FTP:
                self.conn.quit()
            self.conn = None
            return True
        except socket.timeout:
            logger.debug('ERROR:: socket timedout')
            return False
        except Exception as err:
            logger.debug('ERROR:: ' + str(err))
            return False

    def _download_file(self, fname, lfile):
        try:
            if not self.connect():
                return False
            if self.protocol == DownloadProtocolEnum.HTTP:
                self.conn.request('GET', '/' + fname)
                response = self.conn.getresponse()
                with open(lfile, 'wb') as f:
                    f.write(response.read())
            elif self.protocol == DownloadProtocolEnum.FTP:
                f = open(lfile, 'wb')
                self.conn.retrbinary('RETR '+ fname, f.write)
                f.close()
            elif self.protocol == DownloadProtocolEnum.HashCheck:
                if os.path.exists(lfile) and os.path.isfile(lfile):
                    print("{0} {1}".format(self.get_hashMD5(lfile), lfile))
                else:
                    print("{0:32} {1}".format('Does not exist', lfile))
            else:
                print('Downloading :' + fname)
                print('         to :' + lfile)
            return True
        except Exception as ex:
            print(str(ex))
            logger.debug("File Download failed:" + str(ex))
            return False
        return True

    def _create_dir(self, lfolder, *rfname):
        nfolder = os.path.join(lfolder, *rfname)
        if not os.path.exists(nfolder):
            try:
                os.makedirs(nfolder)
            except Exception as ex:
                logger.debug("Cannot create directory : " + str(ex))
                return False
        elif not os.path.isdir(nfolder):
            logger.debug("cannot create directory, file exists: " + nfolder)
            return False
        return True

    def get_hashMD5(self, filename):
        md5 = hashlib.md5()
        with open(filename,'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''): 
                md5.update(chunk)
        return md5.hexdigest()

    def download_newerfiles(self, flist, lfolder = "."):
        counter = { 'success' : 0, 'failed' : 0 }

        if not self._create_dir(lfolder):
            counter['failed'] = len(flist)
            counter['Message'] = 'Local folder not present'
            print("local folder is not present")
            return counter

        for scomponent in flist:
            rfile = scomponent
            if isinstance(scomponent, dict):
                rfile = scomponent['path']
                md5hash = scomponent['hashMD5']
            else:
                rfile = scomponent
                md5hash = ''
            lfile = os.path.join(lfolder, *rfile.split('/'))
            if os.path.exists(lfile) and os.path.isfile(lfile):
                file_md5hash = self.get_hashMD5(lfile)
                if file_md5hash == md5hash:
                    logger.debug("HashMD5 for " + lfile + " is same as catalog")
                    if self.protocol == DownloadProtocolEnum.HashCheck:
                        print("{0:32} {1}".format('Same', lfile))
                    continue
                logger.debug("HashMD5 for " + lfile + " is different")
                logger.debug("File HashMD5={0}, expected HashMD5={1}".\
                             format(file_md5hash, md5hash))
            else:
                logger.debug(lfile + " does not exist")
            logger.debug('Downloading ' + rfile + " to " + lfile)
            if not self._create_dir(os.path.dirname(lfile)):
                counter['failed'] += 1
                continue
            if self._download_file(rfile, lfile):
                counter['success'] += 1
            else:
                counter['failed'] += 1
        return counter

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
