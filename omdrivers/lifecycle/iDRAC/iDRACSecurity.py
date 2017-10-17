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
import os
import re
import time
import xml.etree.ElementTree as ET
import base64

from enum import Enum
from datetime import datetime
from omsdk.sdkdevice import iDeviceRegistry, iDeviceDriver, iDeviceDiscovery
from omsdk.http.sdkwsman import WsManProtocol
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkproto import PWSMAN, PREDFISH, PSNMP
from omsdk.sdkfile import FileOnShare, Share
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkconfig import ConfigFactory
from omsdk.lifecycle.sdksecurityapi import iBaseSecurityApi
from omsdk.lifecycle.sdkentry import ConfigEntries, RowStatus
from omsdk.sdktime import SchTimer, TIME_NOW
from omdrivers.enums.iDRAC.iDRACEnums import *

import sys
import tempfile
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

class iDRACSecurity(iBaseSecurityApi):
    def __init__(self, entity):
        if PY2:
            super(iDRACSecurity, self).__init__(entity)
        else:
            super().__init__(entity)
        self._job_mgr = entity.job_mgr
        self._config_mgr = entity.config_mgr

    # SSL Export/Import
    def export_ssl_certificate(self, ssl_cert_type=SSLCertTypeEnum.CA_Cert, export_file=None):
        ssl_cert_data = self.entity._export_ssl_certificate(ssl_cert_type=ssl_cert_type)

        logger.info("Writing SSL Certificate to file : {0} : ".format(export_file))
        if export_file is not None:
            if ssl_cert_data["Status"] == "Success":
                # Write the SSL Certificate Data to file
                try:
                    with open(export_file, 'w+') as f:
                        f.write(ssl_cert_data["Data"]["ExportSSLCertificate_OUTPUT"]["CertificateFile"])
                    logger.info("Successfully Export SSL Certificate to file")
                except IOError as e:
                    logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            else:
                logger.error("Export SSL Certificate to file failed : {0}".format(ssl_cert_data["Message"]))

        return ssl_cert_data

    def import_ssl_certificate(self, ssl_cert_file=None, ssl_cert_type=SSLCertTypeEnum.CA_Cert, passphrase=""):
        if ssl_cert_file is not None:
            try:
                # Reading SSL Certificate file
                logger.info("Reading SSL Certificate from file : {0} : ".format(ssl_cert_file))
                with open(ssl_cert_file, 'rb') as f:
                    file_data = f.read()

                #Encode data to Base64
                cert_data = bytearray(base64.b64encode(file_data))

                for i in range(0, len(cert_data) + 77, 77):
                    cert_data[i:i] = '\n'.encode()

                ssl_cert_data = self.entity._import_ssl_certificate(ssl_cert_file=cert_data.decode(), ssl_cert_type=ssl_cert_type,
                                                pass_phrase=passphrase)
                logger.info("Successfully Export SSL Certificate to file")
            except IOError as e:
                logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        else:
            ssl_cert_data = { "Status": "Failed",  "Message": "No certificate file or a bad certificate file" \
                              "given for import"}
            logger.error("No Certificate File available to import.")
        return ssl_cert_data
