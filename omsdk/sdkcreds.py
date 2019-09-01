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
from enum import Enum
from omsdk.sdkcenum import TypeHelper, EnumWrapper
import sys
import json
from omsdk.sdkprint import PrettyPrint
import logging


logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

CredentialsEnum = EnumWrapper('CredentialsEnum', {
    'User' : 'User',
    'SNMPv1_v2c' : 'SNMPv1_v2c',
    'SNMPv3' : 'SNMPv3'
}).enum_type

class iCredentials(object):
    def __init__(self, credsEnum = CredentialsEnum.User):
        self.enid = credsEnum

    def __str__(self):
        return TypeHelper.resolve(self.enid)

    def __repr__(self):
        return TypeHelper.resolve(self.enid)

class Snmpv2Credentials(iCredentials):
    def __init__(self, community, writeCommunity = None):
        if PY2:
            super(Snmpv2Credentials, self).__init__(CredentialsEnum.SNMPv1_v2c)
        else:
            super().__init__(CredentialsEnum.SNMPv1_v2c)
        self.community = community
        self.writeCommunity = writeCommunity
        if self.writeCommunity is None:
            self.writeCommunity = community

    def __str__(self):
        return (TypeHelper.resolve(self.enid) + "(community=" + self.community + ")")

    def __repr__(self):
        return (TypeHelper.resolve(self.enid) + "(community=" + self.community + ")")

class UserCredentials(iCredentials):
    def __init__(self, username, password):
        if PY2:
            super(UserCredentials, self).__init__(CredentialsEnum.User)
        else:
            super().__init__(CredentialsEnum.User)
        self.username = username
        self.password = password

    def __str__(self):
        return (TypeHelper.resolve(self.enid) + "(username=" + str(self.username) + ")")

    def __repr__(self):
        return (TypeHelper.resolve(self.enid) + "(username=" + str(self.username) + ")")

    def json_encode(self):
        return { 'type' : 'UserCredentials', 'username' : self.username }

class ProtocolCredentialsFactory:
    def __init__(self):
        self.creds = {}

    def _tostr(self):
        mystr = ""
        for i in self.creds:
            mystr = mystr + str(self.creds[i]) + ";"
        return mystr

    def __str__(self):
        return self._tostr()

    def __repr__(self):
        return self._tostr()

    def add(self, creds):
        if isinstance(creds, iCredentials):
            self.creds[creds.enid] = creds
        return self

    def get(self, creden):
        if creden in self.creds:
            return self.creds[creden]
        return None

    def json_encode(self):
        retval = {}
        for i in self.creds:
            retval[TypeHelper.resolve(i)] = str(self.creds[i])
        return retval

class CredentialStore:
    DEFAULT_CREDS = {
        "default" : {
            "User" : { "username" : "root", "password" : "password" },
            "SNMPv2" : { "community" : "public" }
        }
    }
    def __init__(self):
        self.creds_store = {}
        self._load(self.DEFAULT_CREDS)


    def load_file(self, filename):
        with open(filename) as creds_data:
            cred_spec = json.load(creds_data)
            self._load(cred_spec)

    def _load(self, cred_spec):
        for cred in cred_spec:
            credfact = ProtocolCredentialsFactory()
            if "User" in cred_spec[cred]:
                credfact.add(UserCredentials(
                        cred_spec[cred]["User"]["username"],
                        cred_spec[cred]["User"]["password"]))
            if "SNMPv2" in cred_spec[cred]:
                credfact.add(Snmpv2Credentials(
                        cred_spec[cred]["SNMPv2"]["community"]))
            self.creds_store[cred] = credfact

    def get_creds(self, cred_name, default=None):
        if cred_name not in self.creds_store:
            if default is None or default not in self.creds_store:
                return None
            cred_name = default
        return self.creds_store[cred_name]

    def printx(self):
        for cred in self.creds_store:
            logger.debug(cred)
            logger.debug(PrettyPrint.prettify_json(self.creds_store[cred]))
