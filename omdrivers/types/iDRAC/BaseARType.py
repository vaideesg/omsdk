import json
import re
from omsdk.sdkcenum import TypeHelper, EnumWrapper
import os

class BaseARType(object):

    def __init__(self, mode):
        self.__dict__['_origs'] = {}
        self.__dict__['_track'] = False
        if mode == 'create':
            self.my_create()
        elif mode == 'modify':
            self.my_modify()
        elif mode == 'delete':
            self.my_delete()
        self.__dict__['_track'] = True

    def __getattr__(self, name):
        if name in self.__dict__ and name not in ['_origs', '_track']:
            return self.__dict__[name]
        raise AttributeError('Invalid attribute ' + name)

    def _enumize(self, value, entype):
        if isinstance(value, str):
            value = TypeHelper.convert_to_enum(value, entype)
        if TypeHelper.belongs_to(entype, value):
            return value
        raise AttributeError('Invalid value for type :' + value)

    def __setattr__(self, name, value):
        if name in ['_origs', '_edits', '_track']:
            raise AttributeError('Invalid attribute ' + name)
        self.__dict__[name] = value
        if not self.__dict__['_track']:
            # Initializing Mode
            self.__dict__['_origs'][name] = value

    def _delattr__(self, name):
        if name in self.__dict__:
            del self.__dict__[name]

    def my_create(self):
        pass

    def my_modify(self):
        pass

    def my_delete(self):
        pass

    @property
    def Properties(self):
        return sorted([i for i in self.__dict__ if not i.startswith('_')])

    def printx(self, changed=False):
        for i in self.Properties:
            status = ''
            if self.__dict__[i] != self.__dict__['_origs'][i]:
                status = '[changed]'
            if changed and status != '':
                print('self.{0} = {1} {2}'.format(i, self.__dict__[i], status))
