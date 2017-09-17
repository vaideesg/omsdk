import os
import sys
import glob
import socket
import time
import gzip
import shutil
import logging
import hashlib
import base64
import json
from datetime import datetime
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

DownloadedFileStatusEnum = EnumWrapper('DFSE', {
   "NotExists" : 'NotExists',
   "Same" : 'Same',
   "Present" : 'Present',
   "Different" : 'Different',
   "RemoteIsNew" : 'RemoteIsNew',
   "RemoteIsOld" : 'RemoteIsOld',
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

    def _convert_date_to_iso(self, date):
        if date is None: date = '1971-01-01T01:01:01Z',
        try :
            return datetime.strptime(date,"%a, %d %b %Y %H:%M:%S %Z")
        except Exception as ex:
            logger.debug(str(ex))
        try :
            return datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
        except Exception as ex:
            logger.debug(str(ex))
        return date

    def _validate_file_metadata(self, rfile, file_metadata, rfile_metadata):
        if 'dateTime' not in rfile:
            rfile['dateTime'] = rfile_metadata['dateTime']
        if 'size' not in rfile:
            rfile['size'] = rfile_metadata['size']
        rtime = self._convert_date_to_iso(rfile['dateTime'])
        ltime = self._convert_date_to_iso(file_metadata['dateTime'])
        if rfile['size'] == file_metadata['size'] and rtime == ltime:
            return DownloadedFileStatusEnum.Same
        if rfile['size'] != file_metadata['size']:
            return DownloadedFileStatusEnum.Different
        if rtime > ltime:
            return DownloadedFileStatusEnum.RemoteIsNew
        return DownloadedFileStatusEnum.RemoteIsOld

    def _get_hashMD5(self, filename):
        md5 = hashlib.md5()
        with open(filename,'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def _validate_file(self, rfile, lfile):
        if not os.path.exists(lfile) or not os.path.isfile(lfile):
            logger.debug(lfile + " does not exist")
            return DownloadedFileStatusEnum.NotExists

        if rfile['hashMD5'] is None:
            logger.debug(lfile + " exists. But no hashMD5 given.")
            return DownloadedFileStatusEnum.Present

        file_md5hash = self._get_hashMD5(lfile)
        if file_md5hash == rfile['hashMD5']:
            logger.debug("HashMD5 for " + lfile + " matches with catalog")
            return DownloadedFileStatusEnum.Same
        logger.debug("HashMD5 for " + lfile + " is different")
        logger.debug("File HashMD5={0}, expected HashMD5={1}".\
                             format(file_md5hash, rfile['hashMD5']))
        return DownloadedFileStatusEnum.Different



    def _download_file(self, rfile, lfile):
        try:
            fstatus =self._validate_file(rfile, lfile)
            if fstatus in [DownloadedFileStatusEnum.Same]:
                logger.debug(rfile['path'] + " is as expected!")
                if self.protocol == DownloadProtocolEnum.HashCheck:
                   print("{0:16} {1}".format(TypeHelper.resolve(fstatus),lfile))
                return True
            logger.debug('Downloading ' + rfile['path'] + " to " + lfile)
            if not self.connect():
                return False
            if not self._create_dir(os.path.dirname(lfile)):
                return False
            if self.protocol == DownloadProtocolEnum.HTTP:
                file_metadata = {
                    'dateTime' :  '1971-01-01T01:01:01Z',
                    'size' : 0
                }
                try:
                    if os.path.isfile(lfile + ".Metadata"):
                        with open(lfile + ".Metadata", "r") as f1:
                            file_metadata = json.load(f1)
                        logger.debug(json.dumps(file_metadata, sort_keys=True,
                            indent=4, separators=(',', ': ')))
                except Exception as ex:
                    logger.debug("Error opening metadata file:" + str(ex))

                self.conn.request('GET', '/' + rfile['path'])
                response = self.conn.getresponse()
                rfile_metadata = {}
                rfile_metadata['size'] = int(response.getheader('Content-Length'))
                rfile_metadata['dateTime'] = response.getheader('Last-Modified')
                for header in ['Content-Type', 'Server', 'Date']:
                    rfile_metadata[header] = response.getheader(header)
                fstatus =self._validate_file_metadata(rfile, file_metadata,
                                                      rfile_metadata)
                logger.debug("_validate_file_metadat() returned" + str(fstatus))
                if fstatus not in [DownloadedFileStatusEnum.RemoteIsNew,
                            DownloadedFileStatusEnum.Different ]:
                    response.close()
                    return True
                with open(lfile + ".Metadata", "w") as f1:
                    f1.write(json.dumps(rfile_metadata, sort_keys=True,
                            indent=4, separators=(',', ': ')))
                with open(lfile, 'wb') as f:
                    f.write(response.read())
                fstatus = self._validate_file(rfile, lfile)
                logger.debug("_validate_file() returned" + str(fstatus))
                return (fstatus in [DownloadedFileStatusEnum.Same,
                                   DownloadedFileStatusEnum.Present])
            elif self.protocol == DownloadProtocolEnum.FTP:
                f = open(lfile, 'wb')
                self.conn.retrbinary('RETR '+ rfile['path'], f.write)
                f.close()
            elif self.protocol == DownloadProtocolEnum.HashCheck:
                if os.path.exists(lfile) and os.path.isfile(lfile):
                    print("{0:16} {1}".format(TypeHelper.resolve(fstatus), lfile))
                else:
                    print("{0:16} {1}".format('Does not exist', lfile))
            else:
                print('Downloading :' + rfile['path'])
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

    def download_newerfiles(self, flist, lfolder = "."):
        counter = { 'success' : 0, 'failed' : 0 }

        if not self._create_dir(lfolder):
            counter['failed'] = len(flist)
            counter['Message'] = 'Local folder not present'
            print("local folder is not present")
            return counter

        for rfile in flist:
            if not isinstance(rfile, dict):
                rfile = { 'path' : rfile, 'hashMD5' : None }
            lfile = os.path.join(lfolder, *rfile['path'].split('/'))
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
