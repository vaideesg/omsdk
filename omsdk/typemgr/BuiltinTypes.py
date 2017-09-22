from omsdk.typemgr.FieldType import FieldType

class CloneableFieldType(FieldType):
    def clone(self, parent=None):
        return type(self)(self._value, self._alias, parent, self._volatile)

class PortField(CloneableFieldType):
    def __init__(self, init_value, alias =None, parent=None, volatile=False):
        super().__init__(init_value, int, 'Attribute', alias, volatile)

    def my_accept_value(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(str(value) + " should be an integer > 0")
        return True

class BooleanField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False):
        super().__init__(init_value, bool, 'Attribute', alias, volatile)

class StringField(CloneableFieldType):
    def __init__(self, init_value, alias=None, parent=None, volatile=False):
        super().__init__(init_value, str, 'Attribute', alias, volatile)

class EnumTypeField(CloneableFieldType):
    def __init__(self, init_value, entype, alias=None, parent=None, volatile=False):
        super().__init__(init_value, entype, 'Attribute', alias, volatile)

