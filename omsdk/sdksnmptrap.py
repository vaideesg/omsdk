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
#from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
#from pysnmp.carrier.asynsock.dgram import udp, udp6
#from pyasn1.codec.ber import encoder
#from pysnmp.proto import api
from pysnmp.hlapi import *

            #<Event AgentID="RACLOG" Category="Audit" Severity="Informational" Timestamp="2017-11-29T00:43:42-0600" Sequence="5523">
            #<Message>Virtual Console session created.</Message>
            #<MessageID>VME0007</MessageID>
            #<FQDD>iDRAC.Embedded.1</FQDD>
            #</Event>
test_run = [
    {
        'MessageID' : 'VME0007',
        'Message' : 'Virtual Console session created.',
        'FQDD' : 'iDRAC.Embedded.1',
        'MessageArgs.Arg' : [ ],
        'Host' : '100.96.45.246'
    },
    {
        'MessageID' : 'VME0001',
        'Message' : 'Virtual Console session started.',
        'FQDD' : 'iDRAC.Embedded.1',
        'MessageArgs.Arg' : [ ],
        'Host' : '100.96.45.246'
    },
    {
        'MessageID' : 'VME0005',
        'Message' : 'Virtual Console session exited.',
        'FQDD' : 'iDRAC.Embedded.1',
        'MessageArgs.Arg' : [ ],
        'Host' : '10.96.45.246'
    },
    {
        'MessageID' : 'input'
    },
    {
        'MessageID' : 'VME0005',
        'Message' : 'Virtual Console session exited.',
        'FQDD' : 'iDRAC.Embedded.1',
        'MessageArgs.Arg' : [ ],
        'Host' : '100.96.45.246'
    },
    {
        'MessageID' : 'input'
    },
    {
        'MessageID' : 'VME0007',
        'Message' : 'Virtual Console session created.',
        'FQDD' : 'iDRAC.Embedded.1',
        'MessageArgs.Arg' : [ ],
        'Host' : '100.96.45.246'
    },
]

for message in test_run:
  print(message)
  if message['MessageID'] == 'input':
        m = input()
        continue
  errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget(('localhost', 162)),
        ContextData(),
        'trap',
        NotificationType(
            ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.2.1.2089')
        ).addVarBinds(
            ObjectType(ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.1.1.0'),
                       OctetString(message['MessageID'])),
            ObjectType(ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.1.2.0'),
                       OctetString(message['Message'])),
            ObjectType(ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.1.6.0'),
                       OctetString(message['FQDD'])),
            ObjectType(ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.1.8.0'),
                       OctetString(",".join(message['MessageArgs.Arg']))),
            ObjectType(ObjectIdentity('1.3.6.1.4.1.674.10892.5.3.1.9.0'),
                       OctetString(message['Host']))
        )
    )
  )
  if errorIndication:
    print(errorIndication)
