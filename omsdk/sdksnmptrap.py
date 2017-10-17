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
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import encoder
from pysnmp.proto import api

# Protocol version to use
pMod = api.protoModules[api.protoVersion1]
#pMod = api.protoModules[api.protoVersion2c]

# Build PDU
trapPDU =  pMod.TrapPDU()
pMod.apiTrapPDU.setDefaults(trapPDU)

# Traps have quite different semantics across proto versions
if pMod == api.protoModules[api.protoVersion1]:
    pMod.apiTrapPDU.setEnterprise(trapPDU, (1,3,6,1,4,1,20408,4,1,1,2))
    pMod.apiTrapPDU.setGenericTrap(trapPDU, 'coldStart')

# Build message
trapMsg = pMod.Message()
pMod.apiMessage.setDefaults(trapMsg)
pMod.apiMessage.setCommunity(trapMsg, 'public')
pMod.apiMessage.setPDU(trapMsg, trapPDU)

transportDispatcher = AsynsockDispatcher()

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openClientMode()
    )
transportDispatcher.sendMessage(
    encoder.encode(trapMsg), udp.domainName, ('localhost', 162)
    )

# UDP/IPv6
transportDispatcher.registerTransport(
    udp6.domainName, udp6.Udp6SocketTransport().openClientMode()
)
transportDispatcher.sendMessage(
    encoder.encode(trapMsg), udp6.domainName, ('::1', 162)
)

# Dispatcher will finish as all scheduled messages are sent
transportDispatcher.runDispatcher()

transportDispatcher.closeDispatcher()
