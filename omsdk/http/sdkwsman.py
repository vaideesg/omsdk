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
import sys

from omsdk.http.sdkwsmanbase import WsManProtocolBase
from omsdk.http.sdkhttpep import HttpEndPoint, HttpEndPointOptions

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class WsManProtocol(WsManProtocolBase):
    def __init__(self, ipaddr, creds, pOptions):
        if PY2:
            super(WsManProtocol, self).__init__(ipaddr, creds, pOptions)
        else:
            super().__init__(ipaddr, creds, pOptions)
        headers = {
            'Content-Type' : 'application/soap+xml;charset=UTF-8'
        }
        self.proto = HttpEndPoint(ipaddr, creds, pOptions, headers)

    def _proto_connect(self):
        self.proto.connect()

    def _proto_ship_payload(self, payload):
        return self.proto.ship_payload(payload)

    def _proto_endpoint(self):
        return self.proto.endpoint

    def _proto_reset(self):
        return self.proto.reset()
