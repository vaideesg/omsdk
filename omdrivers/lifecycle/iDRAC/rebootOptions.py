

class RebootOptions(object):
    def __init__(self, time_to_wait = 300, host_state = 1, shutdown_type = 1):
        self.time_to_wait = time_to_wait
        self.host_state = host_state
        self.shutdown_type = shutdown_type
