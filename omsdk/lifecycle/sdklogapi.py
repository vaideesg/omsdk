import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class iBaseLogApi(object):

    def __init__(self, entity, logenum, logtypesen = None):
        self.entity = entity
        self.logenum = logenum
        self.logs_json = {}
        self.logtypesen = logtypesen

    def get_logs(self):
        return self.entity._get_entries(self.logs_json, self.logenum)

    def clear_logs(self):
        pass

