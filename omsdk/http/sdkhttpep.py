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
import io
import logging
import traceback
import json
from enum import Enum

import xml.etree.ElementTree as ET

import requests
import requests.adapters
import requests.exceptions
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import SNIMissingWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
from omsdk.sdkcenum import EnumWrapper, TypeHelper
import logging


AuthenticationTypeMap = {
    'Basic' : 1
}
AuthenticationType = EnumWrapper('AT', AuthenticationTypeMap).enum_type


class HttpEndPointOptions(object):
    def __init__(self):
        self.connection_timeout = 10 # establish a connection
        self.read_timeout = 50 # how long to wait for response from client
        self.max_retries = 1
        self.skip_ca_check = True
        self.skip_cn_check = True
        self.verify_ssl = None
        self.authentication = AuthenticationType.Basic
        self.port = 443

class HttpEndPointProtocolException(Exception):
    pass

class HttpEndPointTransportException(Exception):
    pass

class HttpEndPointProtocolAuthException(Exception):
    pass

class HttpEndPoint(object):
    def __init__(self, ipaddr, creds, pOptions, headers = {}):
        self.ipaddr = ipaddr
        self.creds = creds
        self.pOptions = pOptions
        self.session = None
        self.headers = headers
        self._logger = logging.getLogger(__name__)
        url_form = "https://{0}:{1}/wsman"
        if ':' in self.ipaddr:
            url_form = "https://[{0}]:{1}/wsman"
        self.endpoint = url_form.format(self.ipaddr, self.pOptions.port)

    def reset(self):
        if not self.session is None:
            self.session.close()
            self.session = None

    def reconnect(self):
        self.reset()
        return self.connect()

    def connect(self):
        if self.session:
            return True
        self._logger.debug("Attempting a connection to device")
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        requests.packages.urllib3.disable_warnings(SNIMissingWarning)
        if not self.pOptions.verify_ssl:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.adapter = requests.adapters.HTTPAdapter(
                pool_connections = 1,
                max_retries = self.pOptions.max_retries)
        self.session = requests.Session()
        self.session.auth = None
        if self.pOptions.authentication == AuthenticationType.Basic:
            self.session.auth = requests.auth.HTTPBasicAuth(self.creds.username,
                                                    self.creds.password)
        self.session.headers.update(self.headers)
        self.session.mount("https", self.adapter)
        self._logger.debug("Connection to device: complete")
        return True

    def ship_payload(self, payload):

        self._logger.debug("Begin doing HTTP POST with SOAP message")

        if self.session:
        # Prepare the http request
            self._logger.debug("Begin preparing POST request with payload:\n%s", payload)
            try:
                request = requests.Request('POST', self.endpoint, data=str(payload))
                prepared_request = self.session.prepare_request(request)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Finished preparing POST request")

            # Submit the http request
            self._logger.debug("Begin submitting POST request")
            try:
                response = self.session.send(prepared_request, verify=self.pOptions.verify_ssl,
                    timeout=(self.pOptions.connection_timeout, self.pOptions.read_timeout))
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                error_message = "HTTP connection error"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                self._logger.exception(error_message)
                raise HttpEndPointTransportException(error_message)
            else:
                self._logger.debug("Finished submitting POST request")

            # now check response for errors
            self._logger.debug("Begin checking POST response")
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                error_message = (
                    "DRAC WSMAN endpoint returned HTTP code '{}' Reason '{}'"
                    ).format(response.status_code, response.reason)
                # response.content
                #self._logger.exception(error_message)
                if response.status_code == 401:
                    raise HttpEndPointProtocolAuthException(error_message)
                else:
                    raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Received non-error HTTP response")
            finally:
                self._logger.debug("Finished checking POST response")

            # make sure its a string
            reply = response.content # Avoid unicode difficulties
            self._logger.debug("Received SOAP reply:\n%s", reply)

        # return it
        return reply
