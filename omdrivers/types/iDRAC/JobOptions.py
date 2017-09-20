
import logging

DEFAULT_INTERVAL = 2*60 # seconds
class JobOptions(object):
    def __init__(self, job_wait = False, wait_interval = DEFAULT_INTERVAL):
        self.job_wait = job_wait
        if wait_interval <= 0:
            logging.warning("Job wait interval is negative. Setting default")
            wait_interval = DEFAULT_INTERVAL
        self.wait_interval = wait_interval

