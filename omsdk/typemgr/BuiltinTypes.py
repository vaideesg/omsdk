from omsdk.typemgr.FieldType import FieldType

class SuperFieldType(FieldType):
    def __init__(self, *parts):
        super().__init__(None, tuple, 'Attribute', None, None, True)
        self.__dict__['_value'] = parts
        self._composite = True

    def clone(self, parent=None):
        return type(self)(*self.__dict__['_value'])

class CloneableFieldType(FieldType):
    def clone(self, parent=None):
        if isinstance(self, EnumTypeField):
            return type(self)(self._value, entype=self._type, alias=self._alias,
                  parent=parent, volatile=self._volatile,
                  modifyAllowed = self._modifyAllowed, deleteAllowed = self._deleteAllowed)
        else:
            return type(self)(self._value, alias=self._alias,
                  parent=parent, volatile=self._volatile,
                  modifyAllowed = self._modifyAllowed, deleteAllowed = self._deleteAllowed)

class PortField(CloneableFieldType):
    def __init__(self, init_value, alias =None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, int, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

    def my_accept_value(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(str(value) + " should be an integer > 0")
        return True
        
class IntField(CloneableFieldType):
    def __init__(self, init_value, alias =None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, int, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

class BooleanField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, bool, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

class StringField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, str, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

class EnumTypeField(CloneableFieldType):
    def __init__(self, init_value, entype, alias=None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

class IPv4AddressField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)

class IPv6AddressField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False, modifyAllowed=True, deleteAllowed=True):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile, modifyAllowed, deleteAllowed)
