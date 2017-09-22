from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.BuiltinTypes import *

class CloneableClassType(ClassType):

    def duplicate(self, parent=None):
        obj = type(self)(self._mode, parent)
        self._duplicate_tree(obj, parent)
        obj._start_tracking()
        return obj

class SNMP(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, None, 'SNMP', parent)


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

class iDRAC(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, 'Component', None, parent, False)

    def my_create(self):
        self.SNMP = SNMP(mode='create', parent=self)

    def my_custom(self):
        pass
