import os
import re
import time
import xml.etree.ElementTree as ET
from enum import Enum
from datetime import datetime
from omsdk.sdkdevice import iDeviceRegistry, iDeviceDriver, iDeviceDiscovery
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkproto import PWSMAN,PREDFISH, PSNMP
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkconfig import ConfigFactory
from omsdk.lifecycle.sdkconfigapi import iBaseConfigApi
from omsdk.lifecycle.sdkentry import ConfigEntries, RowStatus
from omsdk.sdktime import SchTimer, TIME_NOW
from omdrivers.lifecycle.iDRAC.rebootOptions import RebootOptions
from omdrivers.enums.iDRAC.iDRACEnums import *
import sys
import logging
import tempfile

logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False

iDRACConfigCompSpec = {
    "LifecycleController" : {
        "pattern" : "LifecycleController.Embedded.1",
        "registry" : "iDRAC",
        "groups" : ["LCAttributes"]
    },
    "System" : {
        "pattern" : "System.Embedded.1",
        "registry" : "iDRAC",
        "groups" : [
            "LCD",
            "ThermalConfig",
            "QuickSync", 
            "ServerPwr", 
            "ServerTopology", 
            "ServerOS"
        ]
    },
    "iDRAC" : {
        "pattern" : "iDRAC.Embedded.1",
        "registry" : "iDRAC",
        "firmware_pattern" : "(iDRAC|OSCollector|USC)\..*",
        "excl_groups" : [
            "LCD",
            "ThermalConfig",
            "QuickSync", 
            "ServerPwr", 
            "ServerTopology", 
            "ServerOS"
        ]
    },
    "FC" : {
        "pattern" : "FC\.Slot\..*",
        "firmware_pattern" : "FC\.Slot\..*",
        "registry" : "FCHBA",
        "nogroup" : True
    },
    "NIC" : {
        "pattern" : "NIC\..*",
        "firmware_pattern" : "NIC\..*",
        "registry" : "NIC",
        "nogroup" : True
    },
    "Controller" : {
        "pattern" : "^RAID\.*",
        "firmware_pattern" : "^RAID\.*",
        "registry" : "RAID",
        "groups" : [ "Controller" ],
        "nogroup" : True
    },
    "Enclosure" : {
        "pattern" : "^[^:]+:RAID\..*",
        "firmware_pattern" : "^[^:]+:RAID\..*",
        "registry" : "RAID",
        "groups" : [ "Enclosure" ],
        "nogroup" : True
    },
    "PhysicalDisk" : {
        "pattern" : "^Disk.*",
        "firmware_pattern" : "^Disk.*",
        "registry" : "RAID",
        "groups" : [ "PhysicalDisk" ],
        "nogroup" : True
    },
    "VirtualDisk" : {
        "pattern" : "Disk\.Virtual\..*",
        "registry" : "RAID",
        "groups" : [ "VirtualDisk" ],
        "nogroup" : True
    },
    "BIOS" : {
        "pattern" : "BIOS\..*",
        "firmware_pattern" : "BIOS\..*",
        "registry" : "BIOS",
        "groups" : [  ],
        "nogroup" : True
    },
    "DriverPack" : {
        "firmware_pattern" : "DriverPack\..*",
        "registry" : None,
        "groups" : [  ],
        "nogroup" : True
    },
    "PowerSupply" : {
        "firmware_pattern" : "(PSU)\..*",
        "registry" : None,
        "groups" : [  ],
        "nogroup" : True
    },
    "Diags" : {
        "firmware_pattern" : "(Diagnostics)\..*",
        "registry" : None,
        "groups" : [  ],
        "nogroup" : True
    },
    "CPLD" : {
        "firmware_pattern" : "CPLD\..*",
        "registry" : None,
        "groups" : [  ],
        "nogroup" : True
    },
    "CMC" : {
        "firmware_pattern" : "CMC\..*",
        "registry" : None,
        "groups" : [  ],
        "nogroup" : True
    },
}


iDRACWsManCmds = {
    ###### LC Services
    "_lc_status" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "GetRemoteServicesAPIStatus",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Return" : {},
        "Parameters" : []
    },

    "_export_tsr" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ExportTechSupportReport",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #RackHD("DataSelectorArrayIn",  None, None, type("0"), None), # 0
        ]
    },
    #######
    ## Server Profiles
    #######
    "_sp_restore": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "RestoreImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "passphrase" : str,
            "image" : str
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ('Passphrase', "passphrase", None, type("passphrase"), None),
                ("ImageName", "image", None, type("imagename"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },
    "_sp_backup": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "BackupImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "passphrase" : str,
            "image" : str
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ('Passphrase', "passphrase", None, type("passphrase"), None),
                ("ImageName", "image", None, type("imagename"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },
     #   IPAddress, ShareName, ShareType, Passphrase, ImageName, Username, Password, Workgroup, ScheduledStartTime (TIME_NOW or yyyymmddhhmmss), UntilTime 
     #   Returns JobID (return value == 4096)
     #   ShareTypeEnum = (0 = NFS, 2 = CIFS, VFLASH= 4 )
     #   ScheduledStartTime (TIME_NOW or yyyymmddhhmmss)
     #   UntilTime  (yyyymmddhhmmss)
    "_factory_export": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ExportFactoryConfiguration",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
    },
    "_inventory_export": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ExportHWInventory",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
    },
    #######
    ##  Server Configuration Profile
    #######
    "_scp_export": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ExportSystemConfiguration",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #RackHD("TimeToWait", "wait", None, type(300), None),
                #RackHD("EndHostPowerState", "power", None, type(1), None), #1
                #RackHD("Target", "target", None, type(1), None), #1
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },
    "_scp_import": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ImportSystemConfiguration",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },
    "_scp_import_with_reboot": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ImportSystemConfiguration",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum,
            "reboot_options" : RebootOptions
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ("TimeToWait", "reboot_options", "time_to_wait", type(300), None),
                ("EndHostPowerState", "reboot_options", "host_state", HostEndPowerStateEnum, None),
                ("ShutdownType", "reboot_options", "shutdown_type", ShutdownTypeEnum, None)
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },

    ###### LC Log
    "_log_export": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ExportLCLog",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
     },
    "_clear_sel_log": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SELRecordLog",
        "Action" :  "ClearLog",
        "SelectorSet" : {
            "w:Selector" : [
           ] },
        "Args" : {},
        "Parameters" : []
        # return 0 - completed with no error; 1 - not supported; 2 - error
     },
    ###### LC Log

    # Manage Power in Server
    "_change_power_state" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_CSPowerManagementService",
        "Action" :  "RequestPowerStateChange",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_CSPowerManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'pwrmgtsvc:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "state" : PowerStateEnum,
        },
        "Return" : {
        },
        "Parameters" : [
            ('PowerState', "state", None, PowerStateEnum, None)
        ]
    },
    # Set/Apply Attributes; no scp
    "_jobq_setup" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_JobService",
        "Action" :  "SetupJobQueue",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_JobService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'JobService' },
                { '@Name': 'SystemName', '#text': 'Idrac' }
           ] },
        "Args" : {
            "jobs" : list,
            "startat" : SchTimer
        },
        "Return" : {
        },
        "Parameters" : [
            ('JobArray', "jobs", None, list, None),
            ('StartTimeInterval', "startat", "time", datetime, None),
            #('UntilTime', 'startat', 'until', datetime, None)
        ]
    },
    "_jobq_delete" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_JobService",
        "Action" :  "DeleteJobQueue",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_JobService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'JobService' },
                { '@Name': 'SystemName', '#text': 'Idrac' }
           ] },
        "Args" : {
            "jobid" : type("JID"),
        },
        "Return" : {
        },
        "Parameters" : [
            ('JobID', "jobid", None, type("jobid"), None)
        ]
    },
    "_power_boot" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_ComputerSystem",
        "Action" :  "RequestStateChange",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SoftwareInstallationService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'SoftwareUpdate' },
                { '@Name': 'SystemName', '#text': 'IDRAC:ID' }
        ] },
        "Args": {
            "state" : PowerBootEnum
        },
        "Parameters" : [
            ('RequestedState', PowerBootEnum)
        ]
    },
    "_reboot_job" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareInstallationService",
        "Action" :  "CreateRebootJob",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SoftwareInstallationService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'SoftwareUpdate' },
                { '@Name': 'SystemName', '#text': 'IDRAC:ID' }
        ] },
        "Args": {
            "reboot" : RebootJobType
        },
        "Parameters" : [
            ('RebootJobType', 'reboot', None, RebootJobType, None)
        ]
    },

    ###### ISO
    "_boot_from_flash": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "BootToISOFromVFlash",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_boot_to_disk": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "BootToHD",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_boot_to_pxe": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "BootToPXE",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_boot_to_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "BootToISO",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_boot_to_network_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "BootToNetworkISO",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('ImageName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #RackHD("ExposeDiration",  "duration", None, type("0"), None),
        ]
    },


    "_detach_drivers": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DetachDrivers",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []

     },
    "_detach_iso_from_vflash": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DetachISOFromVFlash",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_detach_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DetachISOImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_delete_iso_from_vflash": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DetachISOFromVFlash",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_get_driver_pack_info": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "GetDriverPackInfo",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_get_host_mac_info": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "GetHostMACInfo",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_disconnect_network_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DisconnectNetworkISOImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_connect_network_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "ConnectNetworkISOImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('ImageName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #RackHD("HashType",  "hashType", None, type(""), None),
                #RackHD("HashValue",  "hashValue", None, type(""), None),
        ]
    },
    "_download_iso": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DownloadISOImage",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('ImageName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
    },
    "_download_iso_flash": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_OSDeploymentService",
        "Action" :  "DownloadISOToVFlash",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_OSDeploymentService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:OSDeploymentService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('ImageName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime)
        ]
    },
    ##############
    ##### Update Management
    ##############
    "_install_from_uri": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareInstallationService",
        "Action" :  "InstallFromURI",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SoftwareInstallationService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'SoftwareUpdate' },
                { '@Name': 'SystemName', '#text': 'IDRAC:ID' }
        ] },
        "Args" : {
            "uri" : str,
            "target" : str,
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('URI', "uri", None, type("tftp://share/dup or cifs://user:pass@ipaddr/dup"), None),
                ("Target", "target", None, type("iDRAC.Embedded.1"), None),
        ]
        # Do reboot after install_from_uri
     },
    "_update_get_repolist": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareInstallationService",
        "Action" :  "GetRepoBasedUpdateList",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SoftwareInstallationService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'SoftwareUpdate' },
                { '@Name': 'SystemName', '#text': 'IDRAC:ID' }
           ] },
        "Args" : {},
        "Parameters" : []
     },
    "_update_repo": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareInstallationService",
        "Action" :  "InstallFromRepository",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SoftwareInstallationService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'SoftwareUpdate' },
                { '@Name': 'SystemName', '#text': 'IDRAC:ID' }
        ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "catalog" : str,
            "apply" : int,
            "reboot" : str 
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ("CatalogFile", "catalog", None, type("Catalog.xml"), None),
                ("ApplyUpdate", "apply", None, type(0), None), # 0 - report, 1 - apply
                ("RebootNeeded", "reboot", None, type("TRUE"), None),
                #("ProxyPort", "proxy", 'port', type(100), None),
                #("ProxyType", "proxy", 'type', type("1"), None),
                #("ProxySupport", "proxy", 'support', type("3"), None), # 1-off, 2-user default proxy 3-passed in params
                #("ProxyUName",  "proxy_creds", 'username', type("user"), None),
                #("ProxyPasswd",  "proxy_creds", 'password', type("password"), None),
        ]
     },
    ##############
    ##### End Update Management
    ##############
     # Blink LED
    "_blink_led" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SystemManagementService",
        "Action" :  "IdentifyChassis",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_SystemManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:SystemManagementService' },
                { '@Name': 'SystemName', '#text': 'srv:system' }
           ] },
        "Args" : {
            "state" : BlinkLEDEnum,
            "duration" : type(0), # seconds
        },
        "Return" : {
        },
        "Parameters" : [
            ('IdentifyState', "state", None, BlinkLEDEnum, None),
            ('DurationLimit', "duration", None, type(0), None)
        ]
    },

    "_change_bios_password" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_BIOSService",
        "Action" :  "ChangePassword",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_BIOSService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:BIOSService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "target" : type("BIOS.Setup.1-1"), # name of BIOS
            "password_type" : BIOSPasswordTypeEnum,
            "old_password" : type("old"),
            "new_password" : type("new"),
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "target", None, type(0), None),
            ('PasswordType', "password_type", None, BIOSPasswordTypeEnum, None),
            ('OldPassword', "old_password", None, type(0), None),
            ('NewPassword', "new_password", None, type(0), None),
        ]
    },

    "_lc_wipe": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "LCWipe",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
        },
        "Return" : {
        },
        "Parameters" : [
        ]
     },
    "_clear_provisioning_server": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "ClearProvisioningServer",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : { },
        "Return" : { },
        "Parameters" : [ ]
     },
    "_reinitiate_dhs": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService",
        "Action" :  "LCWipe",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LCService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LCService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "server" : type("provserver.host.com"), # name of PSErver
            "reset" : type(True), # name of PSErver
            "auto_discover" : type("1"), # 1 - Off, 2- Now, 3 - NextBoot
        },
        "Return" : {
        },
        "Parameters" : [
            ('ProvisioningServer', "server", None, type("s"), None),
            ('ResetToFactoryDefaults', "reset", None, type(True), None),
            ('PerformAutoDiscovery', "auto_discover", None, type("1"), None),
        ]
     },

    ##############
    ##### License Management
    ##############

    "_delete_license" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "DeleteLicense",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "id" : type("EntitlementID"), # name of PSErver
            "fqdd" : type("fqdd_of_device"), # name of PSErver
            "options" : LicenseApiOptionsEnum
        },
        "Return" : {
        },
        "Parameters" : [
            ('EntitlementID', "id", None, type(""), None),
            ('FQDD', "fqdd", None, type(""), None),
            ('DeleteOptions', "options", None, LicenseApiOptionsEnum, None),
        ]
    },
    "_replace_license" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ReplaceLicense",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "id" : type("EntitlementID"), # name of PSErver
            "fqdd" : type("fqdd_of_device"), # name of PSErver
            "options" : LicenseApiOptionsEnum,
            "file" : type("file"),
        },
        "Return" : {
        },
        "Parameters" : [
            ('EntitlementID', "id", None, type(""), None),
            ('FQDD', "fqdd", None, type(""), None),
            ('ReplaceOptions', "options", None, LicenseApiOptionsEnum, None),
            ('LicenseFile', "file", None, type(""), None),
        ]
    },
    "_import_license" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ImportLicense",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "fqdd" : type("fqdd_of_device"), # name of PSErver
            "options" : LicenseApiOptionsEnum,
            "file" : str,
        },
        "Return" : {
        },
        "Parameters" : [
            ('FQDD', "fqdd", None, type(""), None),
            ('ImportOptions', "options", None, LicenseApiOptionsEnum, None),
            ('LicenseFile', "file", None, str, None),
        ]
    },
    "_export_device_license_share": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ExportLicenseByDeviceToNetworkShare",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "fqdd" : type("iDRAC.Embedded.1")
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ("FQDD",  "fqdd", None, type("id"), None),
        ]
    },
    "_export_license_share": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ExportLicenseToNetworkShare",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "id" : type("0")
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ("EntitlementID",  "id", None, type("id"), None),
        ]
    },
    "_export_license": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ExportLicense",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "id" : type("0")
        },
        "Return" : {
        },
        "Parameters" : [
                ("EntitlementID",  "id", None, type("id"), None),
        ]
    },
    "_export_device_license": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ExportLicense",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "fqdd" : type("0")
        },
        "Return" : {
        },
        "Parameters" : [
                ("FQDD",  "fqdd", None, type("id"), None),
        ]
    },
    "_license_bits": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ShowLicenseBits",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
        },
        "Return" : {
        },
        "Parameters" : [
        ]
    },
    "_import_license_share": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_LicenseManagementService",
        "Action" :  "ImportLicenseFromNetworkShare",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_LicenseManagementService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_SPComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:LicenseManagementService:1' },
                { '@Name': 'SystemName', '#text': 'systemmc' }
           ] },
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "name" : type("0"),
            "fqdd" : type("0"),
            "options" : LicenseApiOptionsEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('IPAddress', "share", 'remote_ipaddr', type("10.20.40.50"), None),
                ('ShareName', "share", 'remote_share_name', type("\\test"), None),
                ('ShareType', "share", 'remote_share_type', Share.ShareType, None),
                ('FileName',  "share", 'remote_file_name', type("filename"), None),
                ("Username",  "creds", 'username', type("user"), None),
                ("Password",  "creds", 'password', type("password"), None),
                ("LicenseName",  "name", None, type("name"), None),
                ("FQDD",  "fqdd", None, type("name"), None),
                ("ImportOptions",  "options", None, LicenseApiOptionsEnum, None),
        ]
    },
    ##############
    ##### End License Management
    ##############

    "_reset_to_factory": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "iDRACResetCfg",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "preserve" : ResetToFactoryPreserveEnum,
            "force" : ResetForceEnum
        },
        "Return" : {
        },
        "Parameters" : [
                ("Preserve",  "preserve", None, ResetToFactoryPreserveEnum, None),
                ("Force",  "force", None, ResetForceEnum, None),
        ]
    },
    "_reset_idrac": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "iDRACReset",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "force" : ResetForceEnum
        },
        "Return" : {
        },
        "Parameters" : [
                ("Force",  "force", None, ResetForceEnum, None),
        ]
    },

    ###### Drive Functions
    "_create_raid_config_job" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "CreateTargetedConfigJob",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "virtual_disk" : str,
            "reboot" : RebootJobType
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "virtual_disk", None, str, None),
            ('RebootJobType', "reboot", None, RebootJobType, None),
            # out RebootRequired 
            # out - 0 -NoError, 1-NotSupported, 2-Error
        ]
    },
    "_delete_raid" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "DeleteVirtualDisk",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "virtual_disk" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "virtual_disk", None, str, None),
            # out RebootRequired 
            # out - 0 -NoError, 1-NotSupported, 2-Error
        ]
    },
    "_lock_raid" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "LockVirtualDisk",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "virtual_disk" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "virtual_disk", None, str, None),
            # out RebootRequired [0=No, 1=Yes]
        ]
    },
    "_remove_all_raids" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "ResetConfig",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "controller" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "controller", None, str, None),
            # out RebootRequired [0=No, 1=Yes]
        ]
    },
    "_secure_erase_raid" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "SecureErase",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "virtual_disk" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "virtual_disk", None, str, None),
            # out RebootRequired [0=No, 1=Yes]
        ]
    },
    "_blink_drive" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "BlinkTarget",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "target" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "target", None, str, None),
        ]
    },
    "_unblink_drive" : {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_RAIDService",
        "Action" :  "UnBlinkTarget",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_RAIDService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:RAIDService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "target" : str
        },
        "Return" : {
        },
        "Parameters" : [
            ('Target', "target", None, str, None),
        ]
    },
    ###########
    # WSMAN Streaming
    ###########
    "_clear_transfer_session": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "ClearTransferSession",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "fileop" : type(1), # 1-DeleteImport, 2-DeleteExport, 3=Both
            "filetype" : type(1), # 0-All,1=SCP,2=LCLog,3=Inventory,4=Factory
                                  # 5-TSR, 6-CrashVideoLog, 7=Diags, 8=LCFullLg
        },
        "Return" : {
        },
        "Parameters" : [
                ("FileOperation",  "fileop", None, int, None),
                ("FileType",  "filetype", None, int, None),
        ]
    },
    "_import_data": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "ImportData",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "encoding" : type(1), # 1=text, 2=base64
            "chunksize" : type(1), # size of chunk data
            "filetype" : type(1), # 1 -scp, 2-fwimage
            "filename" : type(""), # nameoffile
            "sid" : type(1), #64-bit number
            "crc" : type(""), #64-bit number
#CRC of entire import filemd5 checksum algorithm is used for CRC calulation, its value is 128 bytes
            "size" : type(1), #64-bit number sizeoffile
            "dptor" : type(1), #1=StartofTransmit, 2=NormalTransit, 3=End
            "payload" : type(""), 

        },
        "Return" : {
            "SessionID" : 'SessionID'
        },
        "Parameters" : [
                ("ChunkSize", "chunksize", None, ResetForceEnum, None),
                ("FileType", "filetype", None, ResetForceEnum, None),
                ("ImportFileName", "filename", None, ResetForceEnum, None),
                ("InSessionID", "sid", None, ResetForceEnum, None),
                ("CRC", "crc", None, ResetForceEnum, None),
                ("FileSize", "size", None, ResetForceEnum, None),
                ("TxfrDescriptor", "dptor", None, ResetForceEnum, None),
                ("PayLoad", "payload", None, ResetForceEnum, None),
                ("PayLoadEncoding", "encoding", None, ResetForceEnum, None),
        ]
    },
    "_export_data": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "ExportData",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "offset" : type(1), # file offset - 64-bit no
            "size" : type(1), #64-bit number sizeoffile
            "filetype" : type(1), # 1 -scp, 2-lclog, 3-inv, 4-fact, 5-tsr
                                  # 6-boot video, 7-diags, 8-lclog, 9-crashvide
            "sid" : type(1), #64-bit number
            "chunksize" : type(1), # size of chunk data
            "filename" : type(""), # nameoffile


        },
        "Return" : {
            "crc" : type(""), #64-bit number
#CRC of entire import filemd5 checksum algorithm is used for CRC calulation, its value is 128 bytes
            "sid" : type(""), #sessionid
            "fsize" : type(1), # filesize
            "payload" : type(""), 
            "dptor" : type(1), #1=StartofTransmit, 2=NormalTransit, 3=End
            "encoding" : type(1), # Encoding
            "chunksize" : type(1), # size of chunk

        },
        "Parameters" : [
                ("FileOffset", "offset", None, int, None),
                ("TxDataSize", "size", None, int, None),
                ("FileType", "filetype", None, int, None),
                ("InSessionID", "sid", None, int, None),
                ("InChunkSize", "chunksize", None, int, None),
                ("ExportFileName", "filename", None, str, None),
        ]
    },
    ###########
    # SSL Certificate Import and Export
    ###########

    "_import_ssl_certificate": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "ImportSSLCertificate",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "ssl_cert_file" : str,
            "ssl_cert_type"   :  SSLCertTypeEnum,
            "pass_phrase"        :   str
        },
        "Return" : {
        },
        "Parameters" : [
                ("SSLCertificateFile", "ssl_cert_file", None, str, None),
                ("CertificateType", "ssl_cert_type", None, SSLCertTypeEnum, None),
                ("Passphrase", "pass_phrase", None, str, None)
        ]
    },

    "_export_ssl_certificate": {
        "ResourceURI" : "http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_iDRACCardService",
        "Action" :  "ExportSSLCertificate",
        "SelectorSet" : {
            "w:Selector" : [
                { '@Name': 'CreationClassName', '#text': 'DCIM_iDRACCardService' },
                { '@Name': 'SystemCreationClassName', '#text': 'DCIM_ComputerSystem' },
                { '@Name': 'Name', '#text': 'DCIM:iDRACCardService' },
                { '@Name': 'SystemName', '#text': 'DCIM:ComputerSystem' }
           ] },
        "Args" : {
            "ssl_cert_type"   :  SSLCertTypeEnum,
        },
        "Return" : {
        },
        "Parameters" : [
                ("SSLCertType", "ssl_cert_type", None, SSLCertTypeEnum, None)
        ]
    }
}

iDRACRedfishCmds = {
    "_scp_export": {
        "ResourceURI" : "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager",
        "Action" :  "ExportSystemConfiguration",
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('ShareParameters/IPAddress', "share", "remote_ipaddr", type("10.20.40.50"), None),
                ('ShareParameters/ShareName', "share", "remote_share_name", type("\\test"), None),
                ('ShareParameters/ShareType', "share", "remote_share_type", Share.ShareType, None),
                ('ShareParameters/FileName', "share", "remote_file_name", type("filename"), None),
                ('ShareParameters/Username', "creds", "username", type("user"), None),
                ('ShareParameters/Password', "creds", "password", type("password"), None),
                ('ShareParameters/Target', "target", None, SCPTargetEnum, None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime),
                ('ExportFormat', "format_file", None, ExportFormatEnum, None),
        ]
     },
    "_scp_import": {
        "ResourceURI" : "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager",
        "Action" :  "ImportSystemConfiguration",
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [
                ('ShareParameters/IPAddress', "share", "remote_ipaddr", type("10.20.40.50"), None),
                ('ShareParameters/ShareName', "share", "remote_share_name", type("\\test"), None),
                ('ShareParameters/ShareType', "share", "remote_share_type", Share.ShareType, None),
                ('ShareParameters/FileName', "share", "remote_file_name", type("filename"), None),
                ('ShareParameters/Username', "creds", "username", type("user"), None),
                ('ShareParameters/Password', "creds", "password", type("password"), None),
                ('ShareParameters/Target', "target", None, SCPTargetEnum, None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime),
                ('ExportFormat', "format_file", None, ExportFormatEnum, None),
        ]
     },
    "_scp_import_preview": {
        "ResourceURI" : "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager",
        "Action" :  "ImportSystemConfigurationPreview",
        "Args" : {
            "share" : FileOnShare,
            "creds" : UserCredentials,
            "target" : SCPTargetEnum,
            "format_file" : ExportFormatEnum
        },
        "Return" : {
            "File" : "file"
        },
        "Parameters" : [ ('ShareParameters', 'IPAddress', type("10.20.40.50")),
                ('ShareParameters/IPAddress', "share", "remote_ipaddr", type("10.20.40.50"), None),
                ('ShareParameters/ShareName', "share", "remote_share_name", type("\\test"), None),
                ('ShareParameters/ShareType', "share", "remote_share_type", Share.ShareType, None),
                ('ShareParameters/FileName', "share", "remote_file_name", type("filename"), None),
                ('ShareParameters/Username', "creds", "username", type("user"), None),
                ('ShareParameters/Password', "creds", "password", type("password"), None),
                ('ShareParameters/Target', "target", None, SCPTargetEnum, None),
                #("ScheduledStartTime", datetime),
                #("UntilTime", datetime),
                ('ExportFormat', "format_file", None, ExportFormatEnum, None),
        ]
     },
}

class iDRACKeyFieldSpec(object):
    @staticmethod
    def vUserName(vmap):
        if not 'UserName' in vmap:
            return RowStatus.Partial
        username = vmap['UserName']
        retval = RowStatus.Row_With_Invalid_Key
        if (username is not None and len(username.strip()) > 0):
            retval = RowStatus.Row_With_Valid_Key
        return retval

    @staticmethod
    def vAlertDestination(vmap):
        if not 'Destination' in vmap:
            return RowStatus.Partial
        destentry = vmap['Destination']
        retval = RowStatus.Row_With_Invalid_Key
        if (destentry is not None and len(destentry.strip()) > 0 and \
                destentry not in ["::", '0.0.0.0']):
            retval = RowStatus.Row_With_Valid_Key
        return retval

    @staticmethod
    def vEmailAddress(vmap):
        if not 'Address' in vmap:
            return RowStatus.Partial
        destentry = vmap['Address']
        retval = RowStatus.Row_With_Invalid_Key
        if (destentry is not None and len(destentry.strip()) > 0):
            retval = RowStatus.Row_With_Valid_Key
        return retval

iDRACConfigKeyFields = {
    "Users"      : {
        "Pattern" : 'Users.(\d+)#(.+)',
        "Key" : 'UserName',
        "Validate" : iDRACKeyFieldSpec.vUserName
    },
    "SNMPAlert"  : {
        "Pattern" : 'SNMPAlert.(\d+)#(.+)',
        "Key" : 'Destination',
        "Validate" : iDRACKeyFieldSpec.vAlertDestination
    },
    "EmailAlert" : {
        "Pattern" : 'EmailAlert.(\d+)#(.+)',
        "Key" : 'Address',
        "Validate" : iDRACKeyFieldSpec.vEmailAddress
    },
}

class iDRACConfig(iBaseConfigApi):
    def __init__(self, entity):
        if PY2:
            super(iDRACConfig, self).__init__(entity)
        else:
            super().__init__(entity)
        self._job_mgr = entity.job_mgr
        self.config = ConfigFactory.get_config(entity.config_dir, iDRACConfigCompSpec)
        self.entity.configCompSpec = iDRACConfigCompSpec
        self.entity.eResetToFactoryPreserveEnum = ResetToFactoryPreserveEnum
        self.entity.eResetForceEnum = ResetForceEnum
        self.entity.eBIOSPasswordTypeEnum = BIOSPasswordTypeEnum
        self.entity.eConfigStateEnum = ConfigStateEnum
        self.entity.eBootModeEnum = BootModeEnum
        self.entity.eRAIDLevelsEnum = RAIDLevelsEnum
        self.liason_share = None
        self._config_entries = ConfigEntries(iDRACConfigKeyFields)
        self._raid_tree = None

    def set_liason_share(self, myshare):
        if not isinstance(myshare, FileOnShare):
            logger.debug("should be an instance of FileOnShare")
            return False
        if not myshare.IsValid:
            logger.debug("Share is not valid, please retry!!")
            logger.debug("You can only perform readonly operations!")
            #return False
        self.liason_share = myshare
        return True

    # Enabling APIs
    def _commit_scp(self, record, reboot=False):
        if not self.liason_share:
            return { 'Status' : 'Failed',
                     'Message' : 'Configuration Liason Share not registered.' }

        tempshare = self.liason_share.mkstemp(prefix='scp', suffix='.xml')

        with open(tempshare.local_full_path, "w") as f:
            f.write(self.config.format_scp(record))
        msg = self.scp_import(tempshare, reboot=reboot)
        if msg['Status'] == 'Success':
            self._config_entries.process(tempshare.local_full_path, True)
        tempshare.dispose()
        return msg

    def _load_scp(self):
        if self._config_entries.loaded:
            return { 'Status' : 'Success' }
        if not self.liason_share:
            return { 'Status' : 'Failed',
                     'Message' : 'Configuration Liason Share not registered.' }

        tempshare = self.liason_share.mkstemp(prefix='scp', suffix='.xml')
        msg = self.scp_export(tempshare)
        logger.debug(PrettyPrint.prettify_json(msg))
        if msg['Status'] == 'Success':
            self._config_entries.process(tempshare.local_full_path, False)
        tempshare.dispose()
        return msg

    def _configure_field_using_scp(self, component, fmap, reboot_needed = False):
        config = self.config
        lc_config = { component : fmap }
        rjson = self._commit_scp(lc_config, reboot_needed)
        return rjson

    def _modify_field_using_scp(self, component, modify_map, reboot_needed = False):
        fmap = {}
        if not isinstance(modify_map, list):
            modify_map = [ modify_map ]
        for (fname, new_value, current) in modify_map:
            new_value = TypeHelper.resolve(new_value)
            if new_value and new_value != TypeHelper.resolve(current):
                fmap[ fname ] = new_value
        if len(fmap) <= 0:
            return { 'Status' : 'Success', 'Message' : 'No changes required!' }
        return self._configure_field_using_scp(component, fmap, reboot_needed)

    def _comp_to_fqdd(self, fqdd_list, comp, default=None):
        retVal = []
        if not comp in self.entity.configCompSpec:
            return retVal
        for i in fqdd_list:
            if 'firmware_pattern' in self.entity.configCompSpec[comp]:
                fpattern = self.entity.configCompSpec[comp]['firmware_pattern']
                if re.match(fpattern, i):
                    retVal.append(i)
        if len(retVal) <= 0 and default:
            retVal = default
        return retVal

    def _fqdd_to_comp(self, fqdd_list):
        retVal = []
        for i in fqdd_list:
            found= False
            for comp in self.entity.configCompSpec:
                if 'firmware_pattern' in self.entity.configCompSpec[comp]:
                    fpattern = self.entity.configCompSpec[comp]['firmware_pattern']
                    if re.match(fpattern, i):
                        retVal.append(comp)
                        found = True
                        break
            if not found:
                retVal.append(i)
        return set(retVal)

    def _find_empty_slot(self, component, field):
        self._load_scp()
        msg = self._config_entries.check_and_get_empty_slot(component, field)
        if msg['Status'] != 'Success':
            return (-1, None, msg)
        return (msg['retval'], str(msg['retval']), msg)

    def _find_existing_slot(self, component, field):
        self._load_scp()
        msg = self._config_entries.find_existing(component, field)
        if msg['Status'] != 'Success':
            return (-1, None, msg)
        return (msg['retval']['_slot'], msg['retval'], msg)

    def _get_scp_component(self, comp):
        self._load_scp()
        return self._config_entries.get_component(comp)

    def _get_scp_comp_field(self, comp, field):
        self._load_scp()
        return self._config_entries.get_comp_field(comp, field)

    def _get_scp_comp_field_as_array(self, comp, group, fields):
        self._load_scp()
        array = []
        if not isinstance(fields, list):
            fields = [fields]
        for i in fields:
            entry = self._get_scp_comp_field(comp, group + i)
            if entry: array.append(entry)
        return array

    @property
    def LCReady(self):
        rjson = self.entity._lc_status()
        status = self.entity._get_field_from_action(rjson, "Data", "GetRemoteServicesAPIStatus_OUTPUT", "Status")
        return (status and status in ["0"])


    @property
    def ServerStatus(self):
        rjson = self.entity._lc_status()
        status = self.entity._get_field_from_action(rjson, "Data", "GetRemoteServicesAPIStatus_OUTPUT", "ServerStatus")
        return (status and status not in ["6","7","8", "9"])
   
    @property
    def LCStatus(self):
        rjson = self.entity._lc_status()
        states = {
            "0" : "Ready",
            "1" : "Not Initialized",
            "2" : "Reloading Data",
            "3" : "Disabled",
            "4" : "In Recovery",
            "5" : "In Use",
            "U" : "Unknown",
        }
        status = self.entity._get_field_from_action(rjson, "Data", "GetRemoteServicesAPIStatus_OUTPUT", "LCStatus")

        if not status or (status not in states):
            status = "U"
        return states[status]

    # LC Status
    def lc_status(self):
        return self.entity._lc_status()

    def wait_till_lc_ready(self, timeout=100):
        sleep_time = 10 #seconds
        ncntr = round(interval/sleep_time)
        for i in range(0, ncntr+1):
            if self.LCReady:
                return True
            time.sleep(sleep_time)
        return False

    # Blink LED
    def blink_led(self, ledenum, duration = None):
        return self.entity._blink_led(state = ledenum, duration = duration)

    # Decommission: Wipe off all data
    def lc_wipe(self):
        return self.entity._lc_wipe()

    # BIOS Change Password
    def change_bios_password(self, passtype, old_password, new_password):
        return self.entity._change_bios_password(target="BIOS.Setup.1-1", 
                 passtype=passtype, old_password=old_password, new_password=new_password)

    @property
    def BootMode(self):
        bmode = self._get_scp_comp_field('BIOS.Setup.1-1','BootMode')
        if bmode and bmode.lower() == 'bios':
            return BootModeEnum.Bios
        elif bmode and bmode.lower() == 'uefi':
            return BootModeEnum.Uefi
        else:
            return BootModeEnum.Unknown

    def change_boot_mode(self, mode):
        return self._modify_field_using_scp(
                    component = "BIOS.Setup.1-1",
                    modify_map = (self.config.arspec.BIOS.BootMode, mode, self.BootMode),
                    reboot_needed = True)

    # Power Management and Reboot
    def change_power(self, penum):
        return self.entity._change_power_state(state = penum)

    def power_boot(self, power_boot_enum):
        return self.entity._power_boot(state = power_boot_enum)

    # Reset to Factory Defaults
    def reset_to_factory(self, preserve_config = ResetToFactoryPreserveEnum.ResetExceptNICAndUsers, force=ResetForceEnum.Graceful):
        return self.entity._reset_to_factory(preserve = preserve_config, force=force)

    def bios_reset_to_defaults(self):
        return self._configure_field_using_scp(
                    component = "LifecycleController.Embedded.1",
                    fmap = { self.config.arspec.iDRAC.BIOSRTDRequested_LCAttributes : 'True'},
                    reboot_needed = True)

    # Reset iDRAC
    def reset_idrac(self, force=ResetForceEnum.Graceful):
        return self.entity._reset_idrac(force=force)

    # Auto Discovery APIs
    def clear_provisioning_server(self):
        return self.entity._clear_provisioning_server()

    def reinitiate_dhs(self):
        return self.entity._renitiate_dhs()
    # End Auto Discovery APIs

    # Configure APIs
    @property
    def CSIOR(self):
        csior = self._get_scp_comp_field("LifecycleController.Embedded.1",
                    "LCAttributes.1#CollectSystemInventoryOnRestart")
        return TypeHelper.convert_to_enum(csior, ConfigStateEnum,
                    ConfigStateEnum.Unknown)

    def enable_csior(self):
        csior_fname = self.config.arspec.iDRAC.CollectSystemInventoryOnRestart_LCAttributes
        return self._modify_field_using_scp(
                    component = "LifecycleController.Embedded.1",
                    modify_map = (csior_fname, 'Enabled', self.CSIOR))

    def disable_csior(self):
        csior_fname = self.config.arspec.iDRAC.CollectSystemInventoryOnRestart_LCAttributes
        return self._modify_field_using_scp(
                    component = "LifecycleController.Embedded.1",
                    modify_map = (csior_fname, 'Disabled', self.CSIOR))

    @property
    def Location(self):
        return {
            'DataCenter' : self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#DataCenterName'),
            'Room'       : self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#RoomName'),
            'Aisle'      : self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#AisleName'),
            'Rack'       : self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#RackName'),
            'RackSlot'   : self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#RackSlot'),
            'ChassisName': self._get_scp_comp_field('System.Embedded.1', 'ServerTopology.1#ChassisName')
        }

    def configure_location(self, datacenter = None, loc_room=None, loc_aisle=None, loc_rack=None, loc_rack_slot =None, loc_chassis=None):
        loc = self.Location
        if not datacenter:  datacenter = loc['DataCenter']
        if not loc_room:  loc_room = loc['Room']
        if not loc_aisle:  loc_aisle = loc['Aisle']
        if not loc_rack:  loc_rack = loc['Rack']
        if not loc_rackslot:  loc_rackslot = loc['RackSlot']
        if not loc_chassis:  loc_chassis = loc['ChassisName']
        return self._modify_field_using_scp(
            component = "System.Embedded.1",
            modify_map = [
                (self.config.arspec.iDRAC.DataCenterName_ServerTopology, loc_datacenter, loc['DataCenter'])
                (self.config.arspec.iDRAC.RoomName_ServerTopology, loc_room, loc['Room'])
                (self.config.arspec.iDRAC.AisleName_ServerTopology, loc_aisle, loc['Aisle'])
                (self.config.arspec.iDRAC.RackName_ServerTopology, loc_rack, loc['Rack'])
                (self.config.arspec.iDRAC.RackSlot_ServerTopology, loc_rack_slot, loc['RackSlot'])
                (self.config.arspec.iDRAC.ChassisName_ServerTopology, loc_chassis, loc['ChassisName'])
            ])

    def configure_idrac_dnsname(self, dnsname):
        return self._configure_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    fmap = { self.config.arspec.iDRAC.DNSRacName_NIC : dnsname })

    def configure_idrac_ipv4(self, enable_ipv4=True, dhcp_enabled=True):
        m = { True : 'Enabled', False : 'Disabled' }
        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap = {
                self.config.arspec.iDRAC.Enable_IPv4 : m[enable_ipv4],
                self.config.arspec.iDRAC.DHCPEnable_IPv4 : m[dhcp_enabled],
            })

    @property
    def TLSProtocol(self):
        tls = self._get_scp_comp_field('iDRAC.Embedded.1', 'WebServer.1#TLSProtocol')
        return TypeHelper.convert_to_enum(tls, TLSOptions)

    @property
    def SSLEncryptionBits(self):
        ssl = self._get_scp_comp_field('iDRAC.Embedded.1', 'WebServer.1#SSLEncryptionBitLength')
        return TypeHelper.convert_to_enum(ssl, SSLBits)

    def configure_tls(self, tls_protocol = TLSOptions.TLS_1_1, ssl_bits = None):
        return self._modify_field_using_scp(component = "iDRAC.Embedded.1", 
            modify_map = [
                (self.config.arspec.iDRAC.TLSProtocol_WebServer, tls_protocol, self.TLSProtocol),
                (self.config.arspec.iDRAC.SSLEncryptionBitLength_WebServer, ssl_bits, self.SSLEncryptionBits) ])

    def _clean_dnsarray(self, dnsarray, defdns):
        if not dnsarray:
            dnsarray = [defdns, defdns]
        elif not isinstance(dnsarray, list):
            dnsarray = [dnsarray, defdns]
        elif len(dnsarray) < 2:
            dnsarray = [dnsarray[0], defdns]
        elif len(dnsarray) > 2:
            dnsarray[2:] = []
        return dnsarray

    def configure_idrac_ipv4static(self, ipv4_address, ipv4_netmask, ipv4_gateway, dnsarray=None, dnsFromDHCP=False):
        fieldmap = { True : 'Enabled', False : 'Disabled' }
        dnsarray = self._clean_dnsarray(dnsarray, "0.0.0.0")
        return self._configure_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    fmap = {
                        self.config.arspec.iDRAC.Address_IPv4Static : ipv4_address,
                        self.config.arspec.iDRAC.Netmask_IPv4Static : ipv4_netmask,
                        self.config.arspec.iDRAC.Gateway_IPv4Static : ipv4_gateway,
                        self.config.arspec.iDRAC.DNS1_IPv4Static : dnsarray[0],
                        self.config.arspec.iDRAC.DNS2_IPv4Static : dnsarray[1],
                        self.config.arspec.iDRAC.DNSFromDHCP_IPv4Static : fieldmap[dnsFromDHCP],
                    })

    def configure_idrac_ipv4dns(self, dnsarray, dnsFromDHCP=False):
        fieldmap = { True : 'Enabled', False : 'Disabled' }
        dnsarray = self._clean_dnsarray(dnsarray, "0.0.0.0")
        return self._configure_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    fmap = {
                        self.config.arspec.iDRAC.DNS1_IPv4Static : dnsarray[0],
                        self.config.arspec.iDRAC.DNS2_IPv4Static : dnsarray[1],
                        self.config.arspec.iDRAC.DNSFromDHCP_IPv4Static : fieldmap[dnsFromDHCP],
                    })

    def configure_idrac_ipv6static(self, ipv6_address, ipv6_prefixlen = 64, ipv6_gateway="::", dnsarray=None, dnsFromDHCP=False):
        fieldmap = { True : 'Enabled', False : 'Disabled' }
        dnsarray = self._clean_dnsarray(dnsarray, "::")
        return self._configure_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    fmap = {
                        self.config.arspec.iDRAC.Address1_IPv6Static : ipv6_address,
                        self.config.arspec.iDRAC.PrefixLength_IPv6Static : ipv6_prefixlen,
                        self.config.arspec.iDRAC.Gateway_IPv6Static : ipv6_gateway,
                        self.config.arspec.iDRAC.DNS1_IPv6Static : dnsarray[0],
                        self.config.arspec.iDRAC.DNS2_IPv6Static : dnsarray[1],
                        self.config.arspec.iDRAC.DNSFromDHCP6_IPv6Static : fieldmap[dnsFromDHCP],
                    })

    def configure_idrac_ipv6dns(self, dnsarray, dnsFromDHCP=False):
        fieldmap = { True : 'Enabled', False : 'Disabled' }
        dnsarray = self._clean_dnsarray(dnsarray, "::")
        return self._configure_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    fmap = {
                        self.config.arspec.iDRAC.DNS1_IPv6Static : dnsarray[0],
                        self.config.arspec.iDRAC.DNS2_IPv6Static : dnsarray[1],
                        self.config.arspec.iDRAC.DNSFromDHCP6_IPv6Static : fieldmap[dnsFromDHCP],
                    })

    # idrac_nic = 'Dedicated', LOM1, LOM2, LOM3, LOM4
    # failover = None, LOM1, LOM2, LOM3, LOM4, All LOMs
    def configure_idrac_nic(self, idrac_nic = 'Dedicated', failover=None, auto_negotiate=False, idrac_nic_speed = 1000, auto_dedicated_nic = False):
        m = { True: 'Enabled', False : 'Disabled' }

        if idrac_nic == 'Dedicated':
            failover = None
            auto_dedicated_nic = False
        if idrac_nic == failover:
            return { 'Status' : 'Failed', 'Message' : 'Dedicated and Failover NIC should be different' }
        return self._configure_field_using_scp(
            component = "System.Embedded.1",
            fmap= {
              self.config.arspec.iDRAC.Selection_NIC : idrac_nic,
              self.config.arspec.iDRAC.Failover_NIC : str(failover),
              self.config.arspec.iDRAC.Autoneg_NIC : auto_negotiate,
              self.config.arspec.iDRAC.Speed_NIC : idrac_nic_speed,
#              self.config.arspec.iDRAC.AutoDedicatedNIC_NIC : m[auto_dedicated_nic],
            })

    def disable_idracnic_vlan(self):
        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.VLanEnable_NIC : 'Disabled',
            })

    def enable_idracnic_vlan(self, vlan_id = 1, vlan_priority = 0):
        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.VLanEnable_NIC : 'Enabled',
                self.config.arspec.iDRAC.VLanID_NIC : vlan_id,
                self.config.arspec.iDRAC.VLanPriority_NIC : vlan_priority,
            })


    #############################################
    ##  SNMP Trap Destinations
    #############################################
    @property
    def SNMPTrapDestination(self):
        return self._get_scp_component('SNMPAlert')

    def get_trap_destination(self, trap_dest_host):
        (uid, retobj, msg) = self._find_existing_slot('SNMPAlert', trap_dest_host)
        return retobj

    def add_trap_destination(self, trap_dest_host, username = None):
        (uid, retobj, msg) = self._find_empty_slot('SNMPAlert', trap_dest_host)
        if retobj is None: return msg
        if username is None: username = ""

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Destination_SNMPAlert : (uid, trap_dest_host),
                self.config.arspec.iDRAC.State_SNMPAlert : (uid, 'Enabled'),
                self.config.arspec.iDRAC.SNMPv3Username_SNMPAlert : (uid, username),
            })
    def remove_trap_destination(self, trap_dest_host):
        (uid, retobj, msg) = self._find_existing_slot('SNMPAlert', trap_dest_host)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Destination_SNMPAlert : (uid, ''),
                self.config.arspec.iDRAC.State_SNMPAlert : (uid, 'Disabled'),
                self.config.arspec.iDRAC.SNMPv3Username_SNMPAlert : (uid, ''),
            })
    def disable_trap_destination(self, trap_dest_host):
        (uid, retobj, msg) = self._find_existing_slot('SNMPAlert', trap_dest_host)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= { self.config.arspec.iDRAC.State_SNMPAlert:(uid, 'Disabled')})

    def enable_trap_destination(self, trap_dest_host):
        (uid, retobj, msg) = self._find_existing_slot('SNMPAlert', trap_dest_host)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= { self.config.arspec.iDRAC.State_SNMPAlert :(uid, 'Enabled')})

    #############################################
    ##  End SNMP Trap Destinations
    #############################################

    @property
    def SNMPConfiguration(self):
        return {
            'SNMPEnabled'    : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#AgentEnable'),
            'SNMPCommunity'  : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#AgentCommunity'),
            'SNMPPort'       : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#DiscoveryPort'),
            'SNMPTrapFormat' : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#TrapFormat'),
            'SNMPTrapPort'   : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#AlertPort'),
            'SNMPVersions'   : self._get_scp_comp_field('iDRAC.Embedded.1', 'SNMP.1#SNMPProtocol')
        }

    def enable_snmp(self, community, snmp_port = None, trap_port = None, trap_format = None, protocols = None):
        snmpcfg = self.SNMPConfiguration
        if not snmp_port: snmp_port = snmpcfg['SNMPPort']
        if not community: community = snmpcfg['SNMPCommunity']
        if not trap_port: community = snmpcfg['SNMPTrapPort']
        if not trap_format: community = snmpcfg['SNMPTrapFormat']
        if not protocols: community = snmpcfg['SNMPVersions']
        trap_format = TypeHelper.resolve(trap_format)
        protocols = TypeHelper.resolve(protocols)
        return self._modify_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    modify_map = [
                        (self.config.arspec.iDRAC.AgentEnable_SNMP, 'Enabled', snmpcfg['SNMPEnabled']),
                        (self.config.arspec.iDRAC.AgentCommunity_SNMP, community, snmpcfg['SNMPCommunity']),
                        (self.config.arspec.iDRAC.TrapFormat_SNMP, trap_format, snmpcfg['SNMPTrapFormat']),
                        (self.config.arspec.iDRAC.SNMPProtocol_SNMP, protocols, snmpcfg['SNMPVersions']),
                        (self.config.arspec.iDRAC.DiscoveryPort_SNMP, str(snmp_port), snmpcfg['SNMPPort']),
                        (self.config.arspec.iDRAC.AlertPort_SNMP, str(trap_port), snmpcfg['SNMPTrapPort'])])

    def disable_snmp(self):
        snmpcfg = self.SNMPConfig
        return self._modify_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    modify_map = (self.config.arspec.iDRAC.AgentEnable_SNMP, 'Disabled', snmpcfg['SNMPEnabled']))

    @property
    def SyslogServers(self):
        return self._get_scp_comp_field_as_array('iDRAC.Embedded.1',
                  'SysLog.1#', ['Server1', 'Server2', 'Server3'])

    @property
    def SyslogConfig(self):
        return {
            'SyslogEnable' : self._get_scp_comp_field('iDRAC.Embedded.1', 'SysLog.1#SysLogEnable'),
            'SyslogPort' : self._get_scp_comp_field('iDRAC.Embedded.1', 'SysLog.1#Port'),
            'Servers' : self.SyslogServers,
            'PowerLogEnable' : self._get_scp_comp_field('iDRAC.Embedded.1', 'SysLog.1#PowerLogEnable'),
            'PowerLogInterval' : self._get_scp_comp_field('iDRAC.Embedded.1', 'SysLog.1#PowerLogInterval')
        }

    def enable_syslog(self, syslog_port = 514, powerlog_interval = 0, server1="", server2="", server3=""):
        syslog = self.SyslogConfig
        powerlog_enable = 'Enabled'
        if powerlog_interval <= 0:
            powerlog_interval = 0
            powerlog_enable = 'Disabled'
        syslog['Servers'].extend([' ', ' ', ' '])
        return self._modify_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    modify_map = [
                        (self.config.arspec.iDRAC.SysLogEnable_SysLog, 'Enabled', syslog['SyslogEnable']),
                        (self.config.arspec.iDRAC.Port_SysLog, syslog_port, syslog['SyslogPort']),
                        (self.config.arspec.iDRAC.Server1_SysLog, server1, syslog['Servers'][0]),
                        (self.config.arspec.iDRAC.Server2_SysLog, server2, syslog['Servers'][1]),
                        (self.config.arspec.iDRAC.Server3_SysLog, server3, syslog['Servers'][2]),
                        (self.config.arspec.iDRAC.PowerLogEnable_SysLog, powerlog_enable, syslog['PowerLogEnable']),
                        (self.config.arspec.iDRAC.PowerLogInterval_SysLog, powerlog_interval, syslog['PowerLogInterval'])])

    def disable_syslog(self):
        syslog = self.SyslogConfig
        return self._modify_field_using_scp(
            component = "iDRAC.Embedded.1",
            modify_map = [
                (self.config.arspec.iDRAC.SysLogEnable_SysLog, 'Disabled', syslog['SyslogEnable']),
                (self.config.arspec.iDRAC.PowerLogEnable_SysLog, 'Disabled', syslog['PowerLogEnable']) ])

    @property
    def TimeZone(self):
        return self._get_scp_comp_field('iDRAC.Embedded.1', 'Time.1#Timezone')

    @property
    def NTPServers(self):
        return self._get_scp_comp_field_as_array('iDRAC.Embedded.1',
                  'NTPConfigGroup.1#', ['NTP1', 'NTP2', 'NTP3'])

    @property
    def NTPEnabled(self):
        ntp = self._get_scp_comp_field('iDRAC.Embedded.1', 'NTPConfigGroup.1#NTPEnable')
        if ntp and ntp.lower() == 'enabled':
            return True
        return False

    @property
    def NTPMaxDist(self):
        ntp = self._get_scp_comp_field('iDRAC.Embedded.1', 'NTPConfigGroup.1#NTPMaxDist')
        if ntp: return int(ntp)
        return 0

    def configure_time_zone(self, tz="CST6CDT", dst_offset = 0, tz_offset = 0):
        return self._modify_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    modify_map = [
                        (self.config.arspec.iDRAC.Timezone_Time, tz, self.TimeZone),
                        (self.config.arspec.iDRAC.DayLightOffset_Time, 0, 0),
                        (self.config.arspec.iDRAC.TimeZoneOffset_Time, 0, 0) ])

    def enable_ntp(self, ntp_port = 514, powerlog_interval = 0, server1="", server2="", server3=""):
        ntp_server = self.NTPServers
        ntp_server.extend([' ', ' ', ' '])
        return self._modify_field_using_scp(
                    component = "iDRAC.Embedded.1",
                    modify_map = [
                        (self.config.arspec.iDRAC.NTPEnable_NTPConfigGroup, 'Enabled', self.NTPEnabled),
                        (self.config.arspec.iDRAC.NTPMaxDist_NTPConfigGroup, ntp_port, self.NTPMaxDist),
                        (self.config.arspec.iDRAC.NTP1_NTPConfigGroup, server1, ntp_server[0]),
                        (self.config.arspec.iDRAC.NTP2_NTPConfigGroup, server2, ntp_server[1]),
                        (self.config.arspec.iDRAC.NTP3_NTPConfigGroup, server3, ntp_server[2]) ])

    def disable_ntp(self):
        syslog = self.SyslogConfig
        return self._modify_field_using_scp(
            component = "iDRAC.Embedded.1",
            modify_map = [
                (self.config.arspec.iDRAC.SysLogEnable_NTPConfigGroup, 'Disabled', self.NTPEnabled)
            ])


    #############################################
    ##  Email Alerts
    #############################################
    @property
    def RegisteredEmailAlert(self):
        return self._get_scp_component('EmailAlerts')

    def add_email_alert(self, email_id, custom_msg = ""):
        (uid, retobj, msg) = self._find_empty_slot('EmailAlert', email_id)
        if retobj is None: return msg

        if custom_msg is None: custom_msg = ""

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Address_EmailAlert : (uid, email_id),
                self.config.arspec.iDRAC.Enable_EmailAlert : (uid, 'Enabled'),
                self.config.arspec.iDRAC.CustomMsg_EmailAlert : (uid, custom_msg),
            })
    def delete_email_alert(self, email_id):
        (uid, retobj, msg) = self._find_existing_slot('EmailAlert', email_id)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Address_EmailAlert : (uid, ''),
                self.config.arspec.iDRAC.Enable_EmailAlert : (uid, 'Disabled'),
                self.config.arspec.iDRAC.CustomMsg_EmailAlert : (uid, ''),
            })
    def disable_email_alert(self, email_id):
        (uid, retobj, msg) = self._find_existing_slot('EmailAlert', email_id)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Enable_EmailAlert : (uid, 'Disabled'),
            })
    def enable_email_alert(self, email_id):
        (uid, retobj, msg) = self._find_existing_slot('EmailAlert', email_id)
        if retobj is None: return msg

        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.Enable_EmailAlert : (uid, 'Enabled'),
            })

    def change_email_alert(self, email_id, custom_msg = ""):
        (uid, retobj, msg) = self._find_existing_slot('EmailAlert', email_id)
        if retobj is None: return msg
        if custom_msg is None: custom_msg = ""
        return self._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.CustomMsg_EmailAlert:(uid, custom_msg),
            })

    #############################################
    ##  End Email Alerts
    #############################################

    def configure_part_update(self, part_fw_update, part_config_update):
        return self._configure_field_using_scp(
            component = "LifecycleController.Embedded.1",
            fmap= {
                self.config.arspec.iDRAC.PartFirmwareUpdate_LCAttributes : part_fw_update,
                self.config.arspec.iDRAC.PartConfigurationUpdate_LCAttributes : part_config_update,
            })

    def _replicate_ctree(self, obj):
        if isinstance(obj, list):
            return [self._replicate_ctree(i) for i in obj]
        elif isinstance(obj, dict):
            return dict([ (x, self._replicate_ctree(obj[x])) for x in obj])
        else:
            return obj

    def _init_raid_tree(self):
        if self._raid_tree:
            return self._raid_tree

        self.entity.get_partial_entityjson(
              self.entity.ComponentEnum.Controller,
              self.entity.ComponentEnum.Enclosure,
              self.entity.ComponentEnum.VirtualDisk,
              self.entity.ComponentEnum.PhysicalDisk
        )
        raid_tree = self.entity.ContainmentTree
        self._raid_tree = self._replicate_ctree(raid_tree)
        rjson = self._raid_tree["Storage"]
        if not "Controller" in rjson:
            logger.debug("No Controllers!")
            return False

        logger.debug("Containment Tree from device:")
        logger.debug(PrettyPrint.prettify_json(raid_tree['Storage']))

        healthy_cntl_list = {}
        if 'Controller' in self.entity.entityjson:
            for cnt in self.entity.entityjson['Controller']:
                if cnt['PrimaryStatus'] in ['1', '0']:
                    healthy_cntl_list[cnt['FQDD']] = cnt['PrimaryStatus']

        healthy_enc_list = {}
        if 'Enclosure' in self.entity.entityjson:
            for enc in self.entity.entityjson['Enclosure']:
                if enc['PrimaryStatus'] in ['1', '0']:
                    healthy_enc_list[cnt['FQDD']] = enc['PrimaryStatus']

        available_pd_list = {}
        if 'PhysicalDisk' in self.entity.entityjson:
            for pd in self.entity.entityjson['PhysicalDisk']:
                if pd['RaidStatus'] in ['1']:
                    available_pd_list[pd['FQDD']] = pd['RaidStatus']

        for controller in rjson['Controller']:
            if isinstance(rjson['Controller'][controller], list):
                continue
            if controller not in healthy_cntl_list:
                rjson['Controller'][controller] = {}
            if 'Enclosure' in rjson['Controller'][controller]:
                encl_list = rjson['Controller'][controller]['Enclosure']
                for encl in encl_list:
                    if encl not in healthy_enc_list:
                        encl_list[encl] = {}
                    if not 'PhysicalDisk' in encl_list[encl]:
                        continue
                    my_list = []
                    for pd in encl_list[encl]['PhysicalDisk']:
                        if pd in available_pd_list:
                            my_list.append(encl_list[encl]['PhysicalDisk'])
                    encl_list[encl]['PhysicalDisk'] = my_list

            if 'PhysicalDisk' in rjson['Controller'][controller]:
                my_list = []
                for pd in rjson['Controller'][controller]['PhysicalDisk']:
                    if pd in available_pd_list:
                        my_list.append(pd)
                rjson['Controller'][controller]['PhysicalDisk'] = my_list
        # Controller and Enclosure should be Healthy
        # convert non-raid to raid
        logger.debug("Containment Tree containing healthy/available entries:")
        logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))

    def create_virtual_disk(self, vd_name, span_depth, span_length, raid_type, n_dhs = 0):
        raid_type = TypeHelper.resolve(raid_type)
        self._init_raid_tree()
        config = self.config
        if not "Storage" in self._raid_tree:
            logger.debug("Storage not found in device")
            return False
        rjson = self._raid_tree["Storage"]
        s_controller = None
        s_enclosure = None
        n_disks = span_length * span_depth
        t_disks = n_disks + n_dhs
        n_cntr = 0
        s_disks = []
        if not "Controller" in rjson:
            logger.debug("No disks left in any Controllers!")
            return None

        for controller in rjson['Controller']:
            if isinstance(rjson['Controller'][controller], list):
                continue
            n_cntr = 0
            if 'VirtualDisk' in rjson['Controller'][controller]:
                n_cntr = len(rjson['Controller'][controller]['VirtualDisk'])
                logger.debug("No vds in controller:" + controller)
            if 'PhysicalDisk' in rjson['Controller'][controller]:
                # Direct Attached Disks
                cntrl = rjson['Controller'][controller]
                if len(cntrl['PhysicalDisk']) >= t_disks:
                    s_disks = cntrl['PhysicalDisk'][0:t_disks]
                    s_enclosure = None
                    s_controller = controller
                    break
                else:
                    logger.debug(controller+" no "+str(t_disks)+" disks")
            if 'Enclosure' in rjson['Controller'][controller]:
                encl_list = rjson['Controller'][controller]['Enclosure']
                for encl in encl_list:
                    if not 'PhysicalDisk' in encl_list[encl]:
                        continue
                    if len(encl_list[encl]['PhysicalDisk']) >= t_disks:
                        s_disks = encl_list[encl]['PhysicalDisk'][0:t_disks]
                        s_enclosure = encl
                        s_controller = controller
                        break
                    else:
                        logger.debug(controller+" no "+str(t_disks)+" disks")
            if s_controller:
                break
        if s_controller is None:
            logger.debug("No sufficient disks found!")
            return False
        vdfqdd = "Disk.Virtual." + str(n_cntr) + ":" + s_controller
        scp = {}
        scp[s_controller] = {
                config.arspec.RAID.RAIDresetConfig : "False",
                config.arspec.RAID.RAIDforeignConfig : "Clear",
                config.arspec.RAID.RAIDprMode : "Automatic",
                config.arspec.RAID.RAIDccMode : "Normal",
                config.arspec.RAID.RAIDcopybackMode : "On",
                config.arspec.RAID.RAIDEnhancedAutoImportForeignConfig : "Disabled",
                config.arspec.RAID.RAIDrebuildRate : "30",
                config.arspec.RAID.RAIDbgiRate : "30",
                config.arspec.RAID.RAIDreconstructRate : "30",
                vdfqdd :  {
                    config.arspec.RAID.RAIDaction : "Create",
                    config.arspec.RAID.RAIDinitOperation : "None",
                    config.arspec.RAID.DiskCachePolicy : "Default",
                    config.arspec.RAID.RAIDdefaultWritePolicy : "WriteThrough",
                    config.arspec.RAID.RAIDdefaultReadPolicy  :"NoReadAhead",
                    config.arspec.RAID.Name : vd_name,
                    config.arspec.RAID.StripeSize : 128,
                    config.arspec.RAID.SpanDepth : span_depth,
                    config.arspec.RAID.SpanLength : span_length,
                    config.arspec.RAID.RAIDTypes : raid_type,
                    config.arspec.RAID.IncludedPhysicalDiskID : s_disks
                },
        }
        counter = 0
        for disk in s_disks:
            counter += 1
            if counter >= (n_disks + n_dhs): state = "Global"
            elif counter >= n_disks: state = "Dedicated"
            else: state = "No"
            disk_state = { config.arspec.RAID.RAIDHotSpareStatus : state }
            if s_enclosure:
                scp[s_controller][s_enclosure][disk] = disk_state
            else:
                scp[s_controller][disk] = disk_state

        rjson = self._commit_scp(scp, reboot=True)

        if rjson['Status'] == 'Success':
            # if SCP is successful -> update _raid_tree
            updtree = self._raid_tree['Storage']['Controller'][s_controller]
            if 'VirtualDisk' not in updtree:
                updtree['VirtualDisk'] = []
            updtree['VirtualDisk'].append(vdfqdd)
            for disk in s_disks:
                if s_enclosure:
                  updtree['Enclosure'][s_enclosure]['PhysicalDisk'].remove(disk)
                else:
                  updtree['PhysicalDisk'].remove(disk)
            logger.debug("VD Created Successfully. State after creation:")
            logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))
        return rjson

    def get_virtual_disk(self, vd_name):
        self._init_raid_tree()
        if 'VirtualDisk' not in self.entity.entityjson:
            return { 'Status' : 'Success', 'Message' : 'No VDs in Server' }
        vdfqdd = None
        for vd in self.entity.entityjson['VirtualDisk']:
            if vd['Name'] == vd_name:
                return vd
        return None

    def delete_virtual_disk(self, vd_name):
        vdselect = self.get_virtual_disk(vd_name)
        if not vdselect:
            return { 'Status' : 'Success', 'Message' : 'No VD found with name "' + vd_name + '"' }
        vdfqdd = vdselect['FQDD']
        rjson = self.entity._delete_raid(virtual_disk = vdfqdd)
        if rjson['Status'] in [ 'Error', "Failed"]: return rjson
        rjson = self.entity._create_raid_config_job(virtual_disk = vdfqdd,
                reboot=RebootJobType.GracefulRebootWithForcedShutdown)
        if rjson['Status'] == 'Success':
            logger.debug("VD Deleted Successfully. State after deletion:")
            # rebuild the raid tree
            del self.entity.entityjson['PhysicalDisk']
            del self.entity.entityjson['VirtualDisk']
            self._raid_tree = None
            self._init_raid_tree()
            logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))

        rjson['file'] = 'delete_raid'
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def lock_virtual_disk(self, vd_name):
        vdselect = self.get_virtual_disk(vd_name)
        if not vdselect:
            return { 'Status' : 'Failed', 'Message' : 'No VD found with name "' + vd_name + '"' }
        vdfqdd = vdselect['FQDD']
        rjson = self.entity._lock_raid(virtual_disk = vdfqdd)
        if rjson['Status'] in [ 'Error', "Failed"]: return rjson
        rjson = self.entity._create_raid_config_job(virtual_disk = vd_name, reboot=RebootJobType.GracefulRebootWithForcedShutdown)
        rjson['file'] = 'lock_raid'
        return self._job_mgr._job_wait(rjson['file'], rjson)

    # Tech Service Report Export
    def export_tsr_async(self, tsr_store_path):
        return self.export_tsr(tsr_store_path, job_wait = False)

    def export_tsr(self, tsr_store_path, job_wait = True):
        share = tsr_store_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._export_tsr(share = share, creds = tsr_store_path.creds)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    # Server Configuration Profile Export/Import
    def scp_import(self, scp_share_path, components=SCPTargetEnum.ALL, format_file=ExportFormatEnum.XML, reboot=False, job_wait = True):
        share = scp_share_path.format(ip = self.entity.ipaddr)
        if reboot:
            rjson = self.entity._scp_import_with_reboot(share = share, creds = scp_share_path.creds,
                      target=components, format_file=format_file, reboot_options = RebootOptions())
        else:
            rjson = self.entity._scp_import(share = share, creds = scp_share_path.creds,
                      target=components, format_file=format_file)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    def scp_export(self, scp_share_path, components=SCPTargetEnum.ALL, format_file=ExportFormatEnum.XML, job_wait = True):
        share = scp_share_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._scp_export(share = share, creds = scp_share_path.creds, target=components, format_file=format_file)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    # Server Profile Backup/Restore
    def sp_backup(self, sp_share_path, passphrase, sp_image_name, job_wait = True):
        share = sp_share_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._sp_backup(share = share, creds = sp_share_path.creds, passphrase = passphrase, image=sp_image_name)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    def sp_restore(self, sp_share_path, passphrase, sp_image_name, job_wait = True):
        share = sp_share_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._sp_restore(share = share, creds = sp_share_path.creds, passphrase = passphrase, image=sp_image_name)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    # Factory Details Export
    def factory_export(self, factory_details_path, job_wait = True):
        share = factory_details_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._factory_export(share = share, creds = factory_details_path.creds)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    # Hardware Inventory Export
    def inventory_export(self, inventory_details_path, job_wait = True):
        share = inventory_details_path.format(ip = self.entity.ipaddr)
        rjson = self.entity._inventory_export(share = share, creds = inventory_details_path.creds)
        rjson['file'] = str(share)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    # Drive APIs
    # target is FQDD of the drive
    def blink_drive(self, target):
        rjson = self.entity._blink_drive(target)
        rjson['file'] = target
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def unblink_drive(self, target):
        rjson = self.entity._unblink_drive(target)
        rjson['file'] = target
        return self._job_mgr._job_wait(rjson['file'], rjson)

    # OS Deployment APIs
    def detach_iso(self):
        rjson = self.entity._detach_iso()
        return rjson

    def detach_iso_from_vflash(self):
        rjson = self.entity._detach_iso_from_vflash()
        rjson['file'] = 'detach_iso_from_vflash'
        return rjson

    def delete_iso_from_vflash(self):
        rjson = self.entity._delete_iso_from_vflash()
        rjson['file'] = 'delete_iso_from_vflash'
        return rjson

    def boot_to_network_iso(self, network_iso_image, job_wait = True):
        rjson = self.entity._boot_to_network_iso(share = network_iso_image,
                      creds = network_iso_image.creds)
        rjson['file'] = str(network_iso_image)
        if job_wait:
            rjson = self._job_mgr._job_wait(rjson['file'], rjson)
        return rjson

    def boot_to_disk(self):
        rjson = self.entity._boot_to_disk()
        rjson['file'] = 'boot_to_disk'
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def boot_to_iso(self):
        rjson = self.entity._boot_to_iso()
        rjson['file'] = 'boot_to_iso'
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def boot_to_pxe(self):
        rjson = self.entity._boot_to_pxe()
        rjson['file'] = 'boot_to_pxe'
        return self._job_mgr._job_wait(rjson['file'], rjson)

    @property
    def DriverPackInfo(self):
        return self.entity._get_driver_pack_info()

    @property
    def HostMacInfo(self):
        return self.entity._get_host_mac_info()

    def connect_network_iso(self, network_iso_image):
        rjson = self.entity._connect_network_iso(share = network_iso_image, creds = network_iso_image.creds)
        rjson['file'] = str(network_iso_image)
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def download_iso(self, network_iso_image):
        rjson = self.entity._download_iso(share = network_iso_image, creds = network_iso_image.creds)
        rjson['file'] = str(network_iso_image)
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def download_iso_flash(self, network_iso_image):
        share = network_iso_image.format(ip = self.entity.ipaddr)
        rjson = self.entity._download_iso_flash(share = network_iso_image, creds = network_iso_image.creds)
        rjson['file'] = str(network_iso_image)
        return self._job_mgr._job_wait(rjson['file'], rjson)

    def disconnect_network_iso(self):
        return self.entity._disconnect_network_iso()

    def detach_drivers(self):
        return self.entity._detach_drivers()
