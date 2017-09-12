import os
import re
import time
import xml.etree.ElementTree as ET
from enum import Enum
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdklogapi import iBaseLogApi
import sys
import logging


logger = logging.getLogger(__name__)
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False

from omdrivers.enums.iDRAC.iDRACEnums import *

class iDRACLogs(iBaseLogApi):
    def __init__(self, entity):
        if PY2:
            super(iDRACLogs, self).__init__(entity, iDRACLogsEnum)
        else:
            super().__init__(entity, iDRACLogsEnum)
        self._job_mgr = entity.job_mgr

    def clear_sel_logs(self):
        if hasattr(self, 'SELLog') and "SELLog" not in self.SELLog:
            del self.SELLog
        return self.entity._clear_sel_log()

    def get_sel_logs(self):
        if not hasattr(self, 'SELLog') or "SELLog" not in self.SELLog:
            self.SELLog = {}
            self.entity._get_entries(self.SELLog, iDRACLogsEnum)
        return self.SELLog

    def get_logs_for_last_job(self):
        if self.entity.cfactory == None:
            logger.debug("Protocol not initialized!")
            return {}
        if self._job_mgr.last_job is None:
            return [{ "Sequence" : "-1", "MessageID" : "None", "Message": "No jobid provided"} ]

        return self.get_logs_for_job(self._job_mgr.last_job)

    def lclog_export(self, myshare):
        rjson = self.lclog_export_async(myshare)
        return self._job_mgr._job_wait(rjson['file'], rjson, False)

    def lclog_export_async(self, myshare):
        share = myshare.format(ip = self.entity.ipaddr)
        rjson = self.entity._log_export(share = share, creds = myshare.creds)
        rjson['file'] = str(share)
        return rjson

    def get_logs_for_job(self, jobid):
        if self.entity.cfactory == None:
            logger.debug("Protocol not initialized!")
            return {}
        if not self.liason_share:
            logger.debug("Configuration Liason Share not registered!")
            return { }

        tempshare = self.liason_share.mkstemp(prefix='logs', suffix='.xml')
        rjson = self.entity._log_export(share = tempshare, creds = tempshare.creds)
        rjson['file'] = str(tempshare)
        rjson = self._job_mgr._job_wait(rjson['file'], rjson, False)

        if rjson['Status'] != 'Success':
            logger.debug("ERROR: cannot get logs. Failed with message: " + rjson['Message'])
            tempshare.dispose()
            return {}

        logger.debug("Log file saved to " + rjson['file'])

        try :
            domtree = ET.ElementTree(file = tempshare.mount_point.full_path)
            logs = []
            startlogging = False
            for logent in domtree.getroot().getchildren():
                logentry = {}
                for (attrname, attrvalue) in logent.items():
                    logentry[attrname] = attrvalue
                for field in logent.getchildren():
                    if field.tag == "MessageArgs":
                        cntr = 0
                        for arg in field.getchildren():
                            logentry["MessageArgs."+arg.tag+"."+str(cntr)] = arg.text
                            cntr = cntr + 1
                    logentry[field.tag] = field.text
                if startlogging:
                    logs.append(logentry)
                if re.match("JCP.*", logentry["MessageID"]):
                    if logentry["MessageArgs.Arg.0"] != jobid:
                        continue
                    if logentry["MessageID"] == "JCP027":
                        startlogging = True
                        logs.append(logentry)
                    else:
                        startlogging = False
        except Exception as ex:
            logger.debug("ERROR: " + str(ex))
        tempshare.dispose()
        return logs
