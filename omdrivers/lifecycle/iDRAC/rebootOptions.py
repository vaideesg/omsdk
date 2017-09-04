
from omsdk.sdkcenum import EnumWrapper, TypeHelper

ShutdownTypeEnum = EnumWrapper('STE', {
    'Graceful' : 0,
    'Forced' : 1,
    'NoReboot' : 2,
}).enum_type

HostEndPowerStateEnum = EnumWrapper('EPSE', {
    'On' : 1,
    'Off' : 2,
}).enum_type

class RebootOptions(object):
    def __init__(self, time_to_wait = 300, host_state = HostEndPowerStateEnum.On, shutdown_type = ShutdownTypeEnum.Forced):
        self.time_to_wait = time_to_wait
        self.host_state = host_state
        self.shutdown_type = shutdown_type
