from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.BuiltinTypes import *

class SNMP(ClassType):

    def __init__(self, mode, alias):
        super().__init__(mode, None, alias)
        self._start_tracking()

    def my_create(self):
        self.AgentCommunity_SNMP = StringField(None, 'SNMPCommunity')
        self.AlertPort_SNMP = PortField(162, 'SNMPTrapPort')
        self.DiscoveryPort_SNMP = PortField(161, 'SNMPPort')
        self.AgentEnable_SNMP = \
            EnumTypeField(None, AgentEnable_SNMPTypes, 'SNMPEnabled')
        self.SNMPProtocol_SNMP = \
            EnumTypeField(None, SNMPProtocol_SNMPTypes, 'SNMPVersions')
        self.TrapFormat_SNMP = \
            EnumTypeField(None, TrapFormat_SNMPTypes, 'SNMPTrapFormat', volatile=True)

class iDRAC(ClassType):

    def __init__(self, mode='create'):
        super().__init__(mode, 'Component', None)
        self._start_tracking()

    def my_create(self):
        self.SNMP = SNMP(mode='create', alias='SNMP')

