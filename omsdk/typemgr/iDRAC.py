from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.BuiltinTypes import *

class CloneableClassType(ClassType):

    def duplicate_parent(self):
        parent_list = []
        obj = self
        while obj._parent:
            field_name = None
            for prop_name in obj._parent.Properties:
                if obj._parent.__dict__[prop_name] == obj:
                    field_name = prop_name
                    break
            parent_list.insert(0, (obj._parent, field_name))
            obj = obj._parent
        new_list = [ None ]
        for (parent, field) in parent_list:
            new_list.append(type(parent)('custom', new_list[-1]))
            if new_list[-2]:
                new_list[-2].__dict__[field] = new_list[-1]
        return (new_list[1], parent_list[-1][1])

    def duplicate(self, parent=None):
        if parent is None:
            (parent, field) = self.duplicate_parent()
        obj = type(self)(self._mode, parent)
        self._duplicate_tree(obj, parent)
        if parent:
            parent.__dict__[field] = obj
        obj._start_tracking()
        return obj

class SNMP(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, None, 'SNMP', parent)

    def my_create(self):
        self.AgentCommunity_SNMP = StringField(None, 'SNMPCommunity')
        self.DiscoveryPort_SNMP = PortField(161, 'SNMPPort')
        self.AgentEnable_SNMP = \
                EnumTypeField(None, AgentEnable_SNMPTypes, 'SNMPEnabled')
        self.SNMPProtocol_SNMP = \
                EnumTypeField(None, SNMPProtocol_SNMPTypes, 'SNMPVersions')
        self.AlertPort_SNMP = PortField(162, 'SNMPTrapPort')
        self.TrapFormat_SNMP = \
            EnumTypeField(None, TrapFormat_SNMPTypes, 'SNMPTrapFormat')

class NIC(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, None, 'SNMP', parent)

    def my_accept_value(self):
        # Selection_NIC = 'Dedicated', LOM1, LOM2, LOM3, LOM4
        # Failover_NIC = None, LOM1, LOM2, LOM3, LOM4, All LOMs
        if self.Selection_NIC == SelectionTypes.Dedicated:
            self.Failover_NIC = None
            self.AutoDedicatedNIC_NIC = AutoDedicatedNICTypes.Enabled
        if self.Selection_NIC == self.Failover_NIC:
            return False
        return True                

class SysLog(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, None, 'SNMP', parent)

    def my_accept_value(self):
        powerlog_enable = 'Enabled'
        if powerlog_interval <= 0:
            powerlog_interval = 0
            powerlog_enable = 'Disabled'

class Time(CloneableClassType):
    def __init__(self, mode, parent = None):
        super().__init__(mode, None, 'Time', parent)

    # return self._get_scp_comp_field('iDRAC.Embedded.1', 'Time.1#TimeZone')
    # (self.config.arspec.iDRAC.Timezone_Time, tz, self.TimeZone),
    # (self.config.arspec.iDRAC.DayLightOffset_Time, 0, 0),
    # (self.config.arspec.iDRAC.TimeZoneOffset_Time, 0, 0) ])
class iDRAC(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, 'Component', None, parent, False)

    def my_create(self):
        self.SNMP = SNMP(mode='create', parent=self)

class System(CloneableClassType):

    def __init__(self, mode, parent = None):
        super().__init__(mode, 'System', None, parent, False)

    def my_create(self):
        self.iDRAC = iDRAC(mode='create', parent=self)
