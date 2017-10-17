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
import json
from omsdk.sdkbase import iBaseRegistry, iBaseDiscovery, iBaseDriver
from omsdk.sdkbase import iBaseTopologyInfo
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


class iDeviceRegistry(iBaseRegistry):
    pass

class iDeviceDiscovery(iBaseDiscovery):
    pass

class iDeviceDriver (iBaseDriver):
    def __str__(self):
        return self.ipaddr

    def __init__(self, registry, protofactory, ipaddr, creds):
        if PY2:
            super(iDeviceDriver, self).__init__(registry, protofactory, ipaddr, creds)
        else:
            super().__init__(registry, protofactory, ipaddr, creds)
        self._request_device_features()
        self.comp_union_spec = None
        self.comp_merge_join_spec = None
        self.comp_misc_join_spec = None
        self.more_details_spec = None

    def get_json_device(self, monitorfilter = None, compScope = None):
        return self._get_json_for_device(self.entityjson, monitorfilter, compScope)

    def _get_field_device(self, compen, field, idx = 0):
        return self._get_field(self.entityjson, compen, field, idx)

    def _get_field_device_for_all(self, compen, field):
        return self._get_field_for_all(self.entityjson, compen, field)

    @property
    def _DeviceKey(self):
        if ('System' in self.entityjson and
            len(self.entityjson['System']) >= 1 and
            'Key' in self.entityjson['System'][0]):
            return self.entityjson['System'][0]['Key']
        return "<invalid_key>"


class iDeviceTopologyInfo(iBaseTopologyInfo):
    def __init__(self, mytype, json):
        if PY2:
            super(iBaseTopologyInfo, self).__init__(mytype, json)
        else:
            super().__init__(mytype, json)

    def my_is_mytype(self, json):
        return ('System' in json 
                and len(json['System']) == 1
                and '_Type' in json['System'][0]
                and json['System'][0]['_Type'] == self.mytype)

    def my_load(self):
        return self.json['System'][0]

