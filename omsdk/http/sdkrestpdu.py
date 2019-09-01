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
import subprocess
import io
from xml.dom.minidom import parse
import xml.dom.minidom
import json
import re
import uuid
import sys
import xml.etree.ElementTree as ET

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class RestRequest:
    envAttrs = {
       'xmlns:enc' : 'http://www.w3.org/2003/05/soap-encoding',
       'xmlns:env': 'http://www.w3.org/2003/05/soap-envelope',
       'xmlns:tns' : 'http://schemas.microsoft.com/wmx/2005/06',
       # xmlns:a = xmlns:wsa
       'xmlns:a': 'http://schemas.xmlsoap.org/ws/2004/08/addressing',
       'xmlns:wse' : 'http://schemas.xmlsoap.org/ws/2004/08/eventing',
       # xmlns:n = xmlns:wsen
       'xmlns:n': 'http://schemas.xmlsoap.org/ws/2004/09/enumeration',
       # xmlns:w = xmlns:wsman
       'xmlns:w': 'http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd',
       # xmlns:b = xmlns:wsmb
       'xmlns:b': 'http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd',
       'xmlns:wsmid':'http://schemas.dmtf.org/wbem/wsman/identity/1/wsmanidentity.xsd',
       # xmlns:x = xmlns:wxf
       'xmlns:x': 'http://schemas.xmlsoap.org/ws/2004/09/transfer',
       'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema',
       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
       'xmlns:p': 'http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd',
    }

    def __init__(self):
        self.root = {}
        self.selector = None

    def enumerate(self, to, ruri, selectors, envSize = 512000, mid= None, opTimeout = 60):
        return self

    def set_header(self, to, ruri, action, envSize = 512000, mid= None, opTimeout = 60):
        return self

    def add_selectors(self, selectors):
        return self

    def add_body(self, ruri, action, args):
        self.root = { }
        sample = {
            "ExportFormat" : "XML",
            "ShareParameters" : {
                "Target" : "ALL",
                "IPAddress" : "10.9.9.9",
                "ShareName" : "sammba",
                "ShareType" : 0,
                "UserName"  : "root",
                "Password"  : "password",
                "FileName"  : "/root/file.xml",
            }
        }
        for i in args:
            self.root[i] = str(args[i])
        return self

    def add_error(self, ex):
        self.root = {
            "Body" : {
                "ClientFault" : {
                    "Reason" : {
                        "Text" : str(ex)
                    }
                }
            }
        }
        return self

    def identify(self):
        return self

    def get_text(self):
        return json.dumps(self.root)


class RestResponse:
    def __init__(self):
        pass

    def strip_ns(self, s, stripNS):
        return (re.sub(".*:", "", s) if stripNS else s)

    def execute_str(self, value, stripNS = True):
        return json.loads(value)

    def get_message(self, fault):
        msg = None
        while fault != None and msg == None:
            if not isinstance(fault, dict):
                msg = fault
            elif "Message" in fault:
                if isinstance(fault["Message"], dict):
                    fault = fault["Message"]
                else:
                    msg = fault["Message"]
            elif "WSManFault" in fault:
                fault = fault["WSManFault"]
            else:
                for field in fault:
                    if field.startswith("Fault"):
                        m = self.get_message(fault[field])
                        if not m is None:
                            msg = m
                            break
                    elif field == "Text":
                        msg = fault[field]
        return msg
