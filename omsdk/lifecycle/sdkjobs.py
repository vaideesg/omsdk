import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class iBaseJobApi(object):

    def __init__(self, entity, jobenum):
        self.entity = entity
        self.jobenum = jobenum
        self.reset()

    def reset(self):
        self.last_job = None
        self.jobs_json = {}

    def get_jobs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

    def delete_all_jobs(self):
        pass

    def get_job_details(self, jobid):
        pass

    def get_job_status(self, jobid):
        pass

class iBaseLogApi(object):

    def __init__(self, entity, logenum, logtypesen):
        self.entity = entity
        self.logenum = logenum
        self.logtypesen = logtypesen

    def get_logs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

    def clear_logs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

