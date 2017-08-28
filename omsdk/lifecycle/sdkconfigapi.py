import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class iBaseConfigApi(object):

    def __init__(self, entity):
        self.entity = entity

