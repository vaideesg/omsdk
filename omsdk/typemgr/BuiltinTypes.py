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
        return type(self)(self._value, self._alias, parent, self._volatile)

class PortField(CloneableFieldType):
    def __init__(self, init_value, alias =None, parent=None, volatile=False):
        super().__init__(init_value, int, 'Attribute', alias, parent, volatile)

    def my_accept_value(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(str(value) + " should be an integer > 0")
        return True
        
class IntField(CloneableFieldType):
    def __init__(self, init_value, alias =None, parent=None, volatile=False):
        super().__init__(init_value, int, 'Attribute', alias, parent, volatile)

class BooleanField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False):
        super().__init__(init_value, bool, 'Attribute', alias, parent, volatile)

class StringField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False):
        super().__init__(init_value, str, 'Attribute', alias, parent, volatile)

class EnumTypeField(CloneableFieldType):
    def __init__(self, init_value, entype, alias=None, parent=None, volatile=False):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile)

class IPv4AddressField(CloneableFieldType):
    def __init__(self, init_value, entype, alias=None, parent=None, volatile=False):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile)

class IPv6AddressField(CloneableFieldType):
    def __init__(self, init_value, entype, alias=None, parent=None, volatile=False):
        super().__init__(init_value, entype, 'Attribute', alias, parent, volatile)
