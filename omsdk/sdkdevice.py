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

