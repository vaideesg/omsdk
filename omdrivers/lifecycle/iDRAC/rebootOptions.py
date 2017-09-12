from omdrivers.enums.iDRAC.iDRACEnums import *

class RebootOptions(object):
    # time_to_wait is in seconds
    def __init__(self, time_to_wait = 300, host_state = HostEndPowerStateEnum.On, shutdown_type = ShutdownTypeEnum.Forced):
        self.time_to_wait = time_to_wait
        self.host_state = host_state
        self.shutdown_type = shutdown_type
