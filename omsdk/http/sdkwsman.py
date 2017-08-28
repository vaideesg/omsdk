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
