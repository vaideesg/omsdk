import os
import sys
import re
import tempfile
import glob
import json
import logging
from enum import Enum
from datetime import datetime
from omsdk.sdkprint import MyEncoder, PrettyPrint
from omsdk.sdkenum import DeviceGroupFilter
from omsdk.sdkcenum import EnumWrapper,TypeHelper

import platform

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY2UC = (sys.version_info < (3,0,0))

logger = logging.getLogger(__name__)
# idrac.get_share_type_mapped():
#   { ShareType.NFS : 0, ShareType.CIFS : 2, ShareType.VFLASH : 4 }
#   { IPAddressTypeEnum.IPv4 : 1, IPAddressTypeEnum.IPv6 : 2,  }
# f10.get_share_type_mapped():
#   { ShareType.TFTP : 3, ShareType.FTP : 4, ShareType.SCP : 5 }
#   { IPAddressTypeEnum.IPv4 : 1, IPAddressTypeEnum.IPv6 : 2, IPAddressTypeEnum.DNS : 16 }


class Share(object):
    ShareType = EnumWrapper('ShareType', {'NFS':0, 'CIFS':2, 'TFTP' : 3, 'FTP' : 4, 'SCP': 5}).enum_type
    LocalFolderType = EnumWrapper('LocalFolderType', {'Windows':-1, 'Linux':-2}).enum_type
    vFlashType = EnumWrapper('vFlashType', {'VFLASH' : 4}).enum_type
    IPAddressTypeEnum = EnumWrapper('IPAD', { 'Invalid' : 0, 'IPv4' : 1, 'IPv6': 2, 'DNS' : 16}).enum_type

    _ShareSpec = {
        ShareType.CIFS : {
            'share_file' : re.compile('\\\\\\\\([^\\\\]+)[\\\\](.+)[\\\\]([^\\\\]+)$'),
            'share' : re.compile('\\\\\\\\([^\\\\]+)[\\\\](.+)'),
            'path_sep' : '\\',
            'path_start' : '\\\\',
            'ipsep' : '\\',
            'type' : ShareType.CIFS,
        },
        ShareType.NFS : {
            'share_file' : re.compile("([^/]+):/(.+)/([^/]+)$"),
            'share' : re.compile("([^/]+):/(.+)"),
            'path_sep' : '/',
            'rpath_sep' : '/',
            'ipsep' : ':',
            'type' : ShareType.NFS,
        },
        ShareType.SCP : {
            'share_file' : re.compile("scp:([^/]+):/(.+)/([^/]+)$"),
            'share' : re.compile("scp:([^/]+):/(.+)"),
            'path_sep' : '/',
            'fsep' : ':',
            'ipsep' : ':',
            'rpath_sep' : '/',
            'type' : ShareType.SCP,
            'prefix' : 'scp',
        },
        ShareType.FTP : {
            'share_file' : re.compile("ftp:([^/]+):/(.+)/([^/]+)$"),
            'share' : re.compile("ftp:([^/]+):/(.+)"),
            'path_sep' : '/',
            'fsep' : ':',
            'ipsep' : ':',
            'rpath_sep' : '/',
            'type' : ShareType.FTP,
            'prefix' : 'ftp',
        },
        ShareType.TFTP : {
            'share_file' : re.compile("tftp:([^/]+):/(.+)/([^/]+)$"),
            'share' : re.compile("tftp:([^/]+):/(.+)"),
            'path_sep' : '/',
            'fsep' : ':',
            'ipsep' : ':',
            'rpath_sep' : '/',
            'type' : ShareType.TFTP,
            'prefix' : 'tftp',
        },
        LocalFolderType.Windows : {
            'share' : re.compile('^[A-Za-z]:.+$'),
            'path_sep' : '\\',
            'type' : LocalFolderType.Windows,
        },
        LocalFolderType.Linux : {
            'share' : re.compile("^[^\\\\:]+$"),
            'path_sep' : '/',
            'type' : LocalFolderType.Linux,
        },
    }

    IPv4Address = re.compile("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")

    TemplateSpec = re.compile(".*%[A-Za-z].*")

class _PathObject(object):
    def __init__(self, share_type, isFolder, ipaddr, *args):
        self.share_type = share_type
        self.ipaddr = ipaddr
        self.isFolder = isFolder
        self.iptype = Share.IPAddressTypeEnum.Invalid
        if ipaddr:
            if Share.IPv4Address.match(self.ipaddr):
                self.iptype = Share.IPAddressTypeEnum.IPv4
            else:
                self.iptype = Share.IPAddressTypeEnum.IPv6

        self.paths = [path for path in args \
                         if path is not None and len(path.strip()) > 0]
        if self.share_type in Share._ShareSpec:
            psep = Share._ShareSpec[self.share_type]['path_sep']
            path_repl_char = '\\'
            path_repl_regex = '[\\\\]+$'
            if self.share_type in [Share.ShareType.CIFS, Share.LocalFolderType.Windows]:
                path_repl_char = '/'
                path_repl_regex = '/+$'
            self.paths = [i.replace(path_repl_char, psep) for i in self.paths]
            self.paths = [re.sub('[\\\\/]+$', '', i) for i in self.paths]
            self.full_path = self._get_full_path(self.paths)
            self.mountable_path = self._get_full_path([self.paths[0]])
            shpath = self._get_share_path("", self.paths)
            if self.isFolder:
                self.share_name = shpath
                self.file_name = ""
                self.share_path = self.full_path
            else:
                shpatharr = shpath.split(psep)
                self.share_name = psep.join(shpatharr[0:-1])
                self.file_name = shpatharr[-1]
                self.share_path = psep.join(self.full_path.split(psep)[0:-1])
        else:
            if len(args) <= 0: args = [""]
            self.mountable_path = args[0]
            self.full_path = args[0]
            self.share_name = args[0]
            self.file_name = args[0]
            self.share_path = args[0]

    def _get_share_path(self, fname, paths):
        comma = ''
        for path_comp in paths:
            if path_comp and len(path_comp.strip()) > 0:
                fname += comma + path_comp 
                comma = Share._ShareSpec[self.share_type]['path_sep']
        return fname


    def _get_full_path(self, paths):
        fname = ""

        if self.share_type in [Share.vFlashType.VFLASH]:
            return self.paths[0]

        # protocol_prefix scp, tftp, ftp
        if 'prefix' in Share._ShareSpec[self.share_type]:
            fname += Share._ShareSpec[self.share_type]['prefix']

        if 'fsep' in Share._ShareSpec[self.share_type]:
            fname += Share._ShareSpec[self.share_type]['fsep']

        if 'path_start' in Share._ShareSpec[self.share_type]:
            fname += Share._ShareSpec[self.share_type]['path_start']

        if 'ipsep' in Share._ShareSpec[self.share_type]:
            fname += self.ipaddr + Share._ShareSpec[self.share_type]['ipsep']

        if 'rpath_sep' in Share._ShareSpec[self.share_type]:
            fname += Share._ShareSpec[self.share_type]['rpath_sep']

        return self._get_share_path(fname, paths)

    def get_full_path_with(self, npaths):
        if not isinstance(npaths, list):
            npaths = [npaths]
        return self._get_full_path(self.paths + npaths)

    def printx(self, sname):
        print("Share (" + str(self.share_type) + "): " + str(self.share_name))
        if self.ipaddr and len(self.ipaddr) > 0:
            print("  " + sname + " IPAddress " + str(self.ipaddr))
            print("  " + sname + " IPType " + str(self.iptype))
        if self.file_name and len(self.file_name) > 0:
            print("  " + sname + " Filename " + str(self.file_name))
        print("  " + sname + " Full Path " + str(self.full_path))
        print("  " + sname + " Mountable Path " + str(self.mountable_path))
        print("  " + sname + " Share Path " + str(self.share_path))

class RemotePath(_PathObject):
    def __init__(self, share_type, isFolder, ipaddr, *args):
        if PY2:
            super(RemotePath, self).__init__(share_type, isFolder, ipaddr, *args)
        else:
            super().__init__(share_type, isFolder, ipaddr, *args)

class LocalPath(_PathObject):
    def __init__(self, share_type, isFolder, *args):
        if PY2:
            super(LocalPath, self).__init__(share_type, isFolder, None, *args)
        else:
            super().__init__(share_type, isFolder, None, *args)

class vFlash(_PathObject):
    def __init__(self):
        if PY2:
            super(vFlash, self).__init__(Share.vFlashType.VFLASH, False, None, "vFlash")
        else:
            super().__init__(Share.vFlashType.VFLASH, False, None, "vFlash")

class InvalidPath(_PathObject):
    def __init__(self):
        if PY2:
            super(InvalidPath, self).__init__(None, False, None, "<invalid>")
        else:
            super().__init__(None, False, None, "<invalid>")

class FileOnShare(Share):

    def json_encode(self):
        return {
            'share_type': str(self.share_type),
            'share_name': str(self.share_name),
            'ipaddr': str(self.ipaddr),
            'creds.username': str(self.creds.username),
            'creds.password': str(self.creds.password),
            'full_path': str(self.full_path),
        }

    def _get_path_object(self, stype_enum, remote_path, common_path, isFolder):
        filename = None
        if remote_path.endswith('/') or remote_path.endswith('\\'):
            if common_path is None:
                isFolder = True
        if not isFolder:
            for pspec in stype_enum:
                if pspec not in Share._ShareSpec:
                    continue
                if 'share_file' not in Share._ShareSpec[pspec]:
                    continue
                cfgtype = Share._ShareSpec[pspec]['share_file'].match(remote_path)
                if not cfgtype: continue
                share_type = pspec
                if len(cfgtype.groups()) > 1:
                    (ipaddr, rshare, filename) = [i for i in cfgtype.groups()]
                    return RemotePath(share_type, isFolder, ipaddr, rshare, common_path, filename)
                return LocalPath(share_type, isFolder, remote_path, common_path, filename)
        
        for pspec in stype_enum:
            if pspec not in Share._ShareSpec:
                continue
            cfgtype = Share._ShareSpec[pspec]['share'].match(remote_path)
            if not cfgtype: continue
            share_type = pspec
            if len(cfgtype.groups()) > 1:
                (ipaddr, rshare) = [i for i in cfgtype.groups()]
                return RemotePath(share_type, isFolder, ipaddr, rshare, common_path)
            return LocalPath(share_type, isFolder, remote_path, common_path)

        return InvalidPath()

    def __init__(self, remote, mount_point = None, common_path = None, isFolder=False, creds = None, fd=None):
        if PY2:
            super(FileOnShare, self).__init__()
        else:
            super().__init__()

        self.creds = creds
        self.isFolder = isFolder

        if PY2UC:
            if type(remote) == unicode:
                remote = remote.encode('ascii', 'ignore')
            if type(mount_point) == unicode:
                mount_point = mount_point.encode('ascii', 'ignore')
            if type(common_path) == unicode:
                common_path = common_path.encode('ascii', 'ignore')

        if remote == "vFlash":
            self.remote = vFlash()
        else:
            self.remote = self._get_path_object(Share.ShareType, remote, common_path, isFolder)
        if mount_point and mount_point == "vFlash":
            self.mount_point = vFlash()
        elif mount_point:
            self.mount_point = self._get_path_object(Share.LocalFolderType, mount_point, common_path, isFolder)
        else:
            self.mount_point = None
        self.mounted = False
        self.fd = fd
        self.valid = False
        self.is_template = False
        if Share.TemplateSpec.match(self.remote_full_path) is not None:
            self.is_template = True


    def isConnected(self, drive, remote = None):
        if platform.system() != "Windows":
            return True
        maps = self.mapdetails(drive)
        status = False
        if 'Status' in maps:
            status = (maps['Status'] == 'OK')
        if 'Remote name' in maps:
            if not remote:
                return status
            elif (maps['Remote name'] == remote):
                return status
        return False

    def isMapped(self, drive, remote = None):
        if platform.system() != "Windows":
            return True
        maps = self.mapdetails(drive)
        if 'Remote name' in maps:
            if not remote:
                return True
            elif (maps['Remote name'] == remote):
                return True
        return False

    def mapdetails(self, drive):
        if platform.system() != "Windows":
            return {}
        if len(drive) == 1:
            drive = drive + ':'
        if len(drive) > 2:
            drive = drive[0:2]
        try :
            (fd, fonshare) = tempfile.mkstemp(prefix='n', suffix='.out')
            #Kludge: Windows associates the fonshare with the fd
            # and keeps the file in open state.
            # As a result, os.system() fails to write to this openfile
            # so we attach a suffix "1" to file and create it.
            os.system("net use " + drive + " > " + fonshare + "1 2>&1")
            mapinfo = {}
            with open(fonshare + "1", "r") as netout:
                for line in netout:
                    if 'could not be found' in line:
                        mapinfo['cmd_status'] = 'Failed'
                    if 'success' in line:
                        mapinfo['cmd_status'] = 'Success'
                    field = re.search('^(.+)\s\s+(.+)$', line)
                    if field:
                        mapinfo[field.group(1).strip()] = field.group(2).strip()
        except Exception as ex:
            logger.debug("Tempfile creation failed: " + str(ex))

        try:
            os.close(fd)
        except Exception as ex:
            logger.debug(str(ex))

        try:
            os.remove(fonshare)
        except Exception as ex:
            logger.debug(str(ex))

        return mapinfo

    def mount(self):
        if self.mounted:
            return True
        if self.mount_point is None or self.remote is None:
            return False
        if self.isConnected(self.mount_point.mountable_path,
                            self.remote.mountable_path):
            self.mounted = True
            return self.mounted

        if platform.system() == "Windows":
            logger.debug("net use /d " + self.mount_point.mountable_path)
            err = os.system("net use /d " + self.mount_point.mountable_path + " >nul 2>&1")
            logger.debug("net use /d returned : " + str(err) + ". Ignoring!")
            logger.debug("net use " + self.mount_point.mountable_path +
              " " + self.remote.mountable_path + 
              " /user:" + self.creds.username + " " + self.creds.password)
            err = os.system("net use " + self.mount_point.mountable_path + 
              " " + self.remote.mountable_path + 
              " /user:" + self.creds.username + " " + self.creds.password + " >nul 2>&1")
            if err == 0:
                self.mounted = True
                logger.debug("net use succeeded!")
            else:
                self.mounted = False
                logger.debug("net use failed with err code:" + str(err))
        if platform.system() == "Linux":
            self.mounted = True
        return self.mounted

    @property
    def IsValid(self):
        if self.valid:
            return True
        if not self.mount():
            return False
        fonshare = self.mkstemp(prefix='scp', suffix='.xml')
        if not fonshare:
            return False
        fonshare.dispose()
        self.valid = True
        return True

    def mkstemp(self, suffix, prefix, text=True):
        if not self.mount_point:
            return None

        if not self.isFolder:
            return None

        psep = ''
        if 'path_sep' in Share._ShareSpec[self.mount_point.share_type]:
            psep = Share._ShareSpec[self.mount_point.share_type]['path_sep']
        try:
            (fd, fname) = tempfile.mkstemp(prefix=prefix, suffix=suffix,
                        dir=self.mount_point.share_path, text=text)
        except Exception as ex:
            logger.debug("Failed to create temp file: " +str(ex))
            return None
        common_path = fname.replace(self.mount_point.mountable_path + psep, '')

        #Kludge: Windows associates the fonshare with the fd
        # and keeps the file in open state.
        # As a result, os.system() fails to write to this openfile
        # so we attach a suffix "1" to file and create it.
        return FileOnShare(remote = self.remote.mountable_path,
            mount_point = self.mount_point.mountable_path + psep,
            common_path = common_path + "1", fd = fd,
            isFolder = False, creds = self.creds)

    def format(self, **kwargs):

        if not self.is_template:
            return self
        if self.mount_point is None and self.remote is None:
            return self
        mp_mountable_path = None
        folder = None
        if self.mount_point:
            mp_mountable_path = self.mount_point.mountable_path
            folder = self.mount_point
        r_mountable_path = None
        if self.remote:
            r_mountable_path = self.remote.mountable_path
            if not folder:
                folder = self.remote

        fname = folder.full_path
        for arg in kwargs:
            fname = re.sub("%"+arg, kwargs[arg], fname)
        try:
            fname = datetime.strftime(datetime.now(), fname)
        except Exception as ex:
            logger.debug(str(ex))
        psep = ''
        if 'path_sep' in Share._ShareSpec[folder.share_type]:
            psep = Share._ShareSpec[folder.share_type]['path_sep']
        common_path = fname.replace(folder.mountable_path + psep, '')

        if mp_mountable_path:
            mp_mountable_path += psep

        return FileOnShare(remote = r_mountable_path,
            mount_point = mp_mountable_path,
            common_path = common_path, fd = None,
            isFolder = self.isFolder, creds = self.creds)

    def new_file(self, *args):

        if not self.isFolder:
            return None

        if self.mount_point is None and self.remote is None:
            return self
        mp_mountable_path = None
        folder = None
        if self.mount_point:
            mp_mountable_path = self.mount_point.mountable_path
            folder = self.mount_point
        r_mountable_path = None
        if self.remote:
            r_mountable_path = self.remote.mountable_path
            if not folder:
                folder = self.remote

        fname = folder.full_path
        psep = ''
        if 'path_sep' in Share._ShareSpec[folder.share_type]:
            psep = Share._ShareSpec[folder.share_type]['path_sep']
            for arg in args:
                fname = fname + psep + arg
        common_path = fname.replace(folder.mountable_path + psep, '')

        if mp_mountable_path:
            mp_mountable_path += psep

        return FileOnShare(remote = r_mountable_path,
            mount_point = mp_mountable_path,
            common_path = common_path, fd = None,
            isFolder = False, creds = self.creds)

    def makedirs(self, *args):

        if not self.isFolder:
            return False
        if self.mount_point is None:
            return False
        if not 'path_sep' in Share._ShareSpec[self.mount_point.share_type]:
            return False
        if not self.IsValid:
            return False

        fname = self.mount_point.full_path
        psep = Share._ShareSpec[self.mount_point.share_type]['path_sep']
        for t in args:
            fname += psep + t
        try :
            if os.path.exists(fname) and os.path.isdir(fname):
                return True

            os.makedirs(fname)
            return True
        except Exception as ex:
            logger.debug("makedirs(): Failed to create folder: " +str(ex))
            return False

    @property
    def IsTemp(self):
        return (self.fd is not None)

    def dispose(self):
        try :
            os.close(self.fd)
        except Exception as ex:
            logger.debug(str(ex))

        try :
            if os.path.exists(self.mount_point.full_path):
                os.remove(self.mount_point.full_path)
        except Exception as ex:
            logger.debug(str(ex))

        # Windows Kludge: Remove the file without 1 suffix
        try :
            if os.path.exists(self.mount_point.full_path[0:-1]):
                os.remove(self.mount_point.full_path[0:-1])
        except Exception as ex:
            logger.debug(str(ex))
    
    @property
    def remote_share_type(self):
       return self.remote.share_type

    @property
    def remote_ipaddr(self):
       return self.remote.ipaddr

    @property
    def remote_iptype(self):
       return self.remote.iptype

    @property
    def remote_full_path(self):
       return self.remote.full_path

    def __str__(self):
       return self.remote.full_path

    @property
    def remote_share_name(self):
       return self.remote.share_name

    @property
    def remote_file_name(self):
       return self.remote.file_name

    def addcreds(self, creds):
        self.creds = creds
        return self

    def printx(self):
        if self.remote:
            self.remote.printx("Remote")
        if self.mount_point:
            self.mount_point.printx("Mount")
        if self.creds:
            print("   Username " + self.creds.username)
            print("   Password " + self.creds.password)
        print("   Template " + str(self.is_template))

class cfgprocessor:
	UNGROUPED = "<ungrouped>"
	def __init__(self):
		self.comment = re.compile('^[ \t]*#')
		self.emptyline = re.compile('^[ \t]*$')
		self.defineline = re.compile('^[ \t]*define[ \t]+(hostgroup|command|host|service)[ \t]+{[ \t]*')
		self.token = re.compile('^[ \t]*([a-zA-Z_][a-zA-Z_0-9]*)[ \t]+([^ \t].*)[ \t]*')
		self.finalline = re.compile('^[ \t]*}[ \t]*$')
		self.reset()

	def reset(self):
		self.datasets = {}
		self.hosts = {}
		self.hostgroup = {}
		self.topology = {}
		self.topology["DeviceGroups"] = {}
		self.devmap = {}
		self.hostgroup[self.UNGROUPED] = []

	def process(self, file1):
		with open(file1, "r") as cfg:
			mytype = ""
			fields = {}
			for line in cfg:
				if (self.comment.match(line.rstrip('\n'))): continue
				if (self.emptyline.match(line.rstrip('\n'))): continue
				cfgtype = self.defineline.match(line.rstrip('\n'))
				if not cfgtype is None:
					if (len(fields) > 0):
						if not "register" in fields:
							n = mytype + "-none"
						else:
							n = mytype + "-" + fields["register"]
						if not n in self.datasets:
							self.datasets[n] = []
						self.datasets[n].append(fields)
						fields = {}
					mytype = cfgtype.group(1)
					continue
				tokentype = self.token.match(line.rstrip('\n'))
				if not tokentype is None:
					fields[tokentype.group(1)] = tokentype.group(2)
					continue
				if (self.finalline.match(line.rstrip('\n'))): continue
				logger.debug("notsure>>" + line.rstrip('\n'))
			if (len(fields) > 0):
				if not "register" in fields:
					n = mytype + "-none"
				else:
					n = mytype + "-" + fields["register"]
				if not n in self.datasets:
					self.datasets[n] = []
				self.datasets[n].append(fields)
		return self
	
	def printx(self):
		logger.debug("====")
		for i in self.datasets:
			logger.debug("=====" + i + "=======")
			logger.debug(PrettyPrint.prettify_json(self.datasets[i]))
			logger.debug("=====================")
		logger.debug("====")
		return self

	def hostit(self):
		#self.svcnames = {}
		#for i in self.datasets:
		#	logger.debug("=====" + i + "=======")
		#for host in self.datasets["service-0"]:
		#	if 'use' in host:
		#		self.svcnames[host['name']] = host['use']
		#	else:
		#		self.svcnames[host['name']] = "<unknown>"
		#for host in self.datasets["host-0"]:
		#	if 'use' in host:
		#		self.hstnames[host['name']] = host['use']
		#	else:
		#		self.hstnames[host['name']] = "<unknown>"

		dgroup = DeviceGroupFilter("Dell.*")
		if "hostgroup-none" in self.datasets:
			for hgroup in self.datasets["hostgroup-none"]:
				if "hostgroup_name" in hgroup:
					if dgroup.isMatch(hgroup["hostgroup_name"]):
						self.hostgroup[hgroup["hostgroup_name"]] = []
						continue
				if "alias" in hgroup:
					if dgroup.isMatch(hgroup["alias"]):
						self.hostgroup[hgroup["hostgroup_name"]] = []
						continue

		if "host-1" in self.datasets:
			for host in self.datasets["host-1"]:
				ipaddr = ""
				svctag = None

				if 'hostgroups' in host:
					if not host['hostgroups'] in self.hostgroup:
						self.hostgroup[host['hostgroups']] = []

				if 'address' in host:
					ipaddr = host['address']
					if not ipaddr in self.hosts:
						self.hosts[ipaddr] = host['host_name']
					if 'hostgroups' in host:
						self.hostgroup[host['hostgroups']].append(ipaddr)
					else:
						self.hostgroup[self.UNGROUPED].append(ipaddr)

				if '_servicetag' in host:
					svctag = host['_servicetag']
					self.devmap[svctag] = {}
					self.devmap[svctag]["doc.prop"] = {}
					self.devmap[svctag]["doc.prop"]["ipaddr"] = ipaddr

					# host['use'] ==> host-0 / host-0['use'] ==> host-0
					# host['alias'], host['display_name'] ==> DNSName
					# host['notes'] => Protocol selected: WSMAN, SNMP
					# host['action_url'] => http://<ipaddress>
					# host['_servicetag'] => servicetag
					# host['_xiwizard'] => MonitoringWizard
			for hgroup in self.hostgroup:
				tst = { }
				tst["Name"] = hgroup
				tst["ID"] = hgroup
				tst["Description"] = hgroup
				tst["Devices"] = self.hostgroup[hgroup]
				tst["DevicesCount"] = len(self.hostgroup[hgroup])
				self.topology["DeviceGroups"][hgroup] = tst
		return self
