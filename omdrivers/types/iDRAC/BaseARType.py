import json
import re
from omsdk.sdkcenum import TypeHelper, EnumWrapper
import os

class BaseARType(object):

    def __init__(self, mode):
        if mode == 'create':
            self.my_create()
        elif mode == 'modify':
            self.my_modify()
        elif mode == 'delete':
            self.my_delete()

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError('Invalid attribute ' + name)

    def __setattr__(self, name, value):
            #if isinstance(value, str):
            #    value = TypeHelper.convert_to_enum(value, entype)
            #if TypeHelper.belongs_to(entype, value):
            #    self.__dict__[name] = value
        self.__dict__[name] = value
        return
        raise AttributeError('Invalid attribute ' + name)

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

    def printx(self):
        for i in self.Properties:
            print('self.' + i + "=" + str(self.__getattr__(i)))
