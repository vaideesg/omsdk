import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class iBaseSecurityApi(object):

    def __init__(self, entity):
        self.entity = entity