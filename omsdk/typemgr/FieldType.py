from enum import Enum

# private
#
# def __init__(self, init_value, typename, fname, alias, volatile=False)
#     def __init__(self, mode)
# def __eq__, __ne__, __lt__, __le__, __gt__, __ge__
# def __getattr__, __delattr__, __setattr__
# def _start_tracking(self)
# def _stop_tracking(self)
#
# protected:
#
# def my_accept_value(self, value):
#
# public:
# def is_changed(self)
# def freeze(self)
# def unfreeze(self)
# def json_encode(self)
# def printx(self, print_everything=False)

# def format(self, formatter, everything = False)

class FieldType(object):

    def __init__(self, init_value, typename, fname, alias, parent=None, volatile=False):
        self.__dict__['_freeze'] = False
        self.__dict__['_track'] = False

        self.__dict__['_orig_value'] = init_value
        self.__dict__['_type']  = typename
        self.__dict__['_alias'] = alias
        self.__dict__['_volatile'] = volatile
        self.__dict__['_fname'] = fname
        self.__dict__['_parent'] = parent
        self._value = init_value

    def __getattr__(self, name):
        if name in self.__dict__ and name not in ['_orig_value', '_track']:
            return self.__dict__[name]
        raise AttributeError('Invalid attribute ' + name)

    def __setattr__(self, name, value):
        # Do not allow access to internal variables
        if name in ['_orig_value', '_track']:
            raise AttributeError('Invalid attribute ' + name)

        # Freeze mode - don't allow any updates
        if '_freeze' in self.__dict__ and self.__dict__['_freeze']:
            raise ValueError('object in freeze mode')

        if name in ['_parent']:
            self.__dict__[name] = value
            return

        # Validate value and convert it if needed
        valid = False
        msg = None
        if value is None:
            self.__dict__[name] = value
            valid = True
        # value belongs to the expected type
        elif isinstance(value, self._type):
            self.__dict__[name] = value
            valid = True
        elif isinstance(value, str):
            # expected value is int
            if self._type == int:
                value = int(value)
                valid = True
            # expected value is bool
            if self._type == bool:
                value = bool(value)
                valid = True
            # expected value is enumeration
            elif self._type == Enum:
                value = TypeHelper.convert_to_enum(value, self._type)
                if value is not None:
                    valid = True
                else:
                    msg = str(value) + " is not " + str(self._type)
            else:
                msg = str(value) + " cannot be converted to " + str(self._type)
        elif type(self) == type(value):
            value = value._value
            valid = True
        else:
            msg = "No type conversion found for '" + str(value) + "'. "\
                  "Expected " + str(self._type.__name__) + ". Got " +\
                  type(value).__name__

        if valid and not self.my_accept_value(value):
            msg = "Subclass returned failure"
            valid = False

        # if invalid, raise ValueError exception
        if not valid:
            raise ValueError(msg)

        # modify the value
        self.__dict__[name] = value

        # if not in tracking mode, then treat the value as original
        if not self.__dict__['_track'] and name == '_value':
            self.__dict__['_orig_value'] = value

    def __delattr__(self, name):
        # Do not allow access to internal variables
        if name in ['_orig_value', '_track', '_freeze', '_type', '_value', '_volatile']:
            raise AttributeError('Invalid attribute ' + name)

        # Freeze mode - don't allow any updates
        if '_freeze' in self.__dict__ and self.__dict__['_freeze']:
            raise AttributeError('object in freeze mode')

        if name in self.__dict__:
            del self.__dict__[name]

    def my_accept_value(self, value):
        return True

    def is_changed(self):
        return self._changed

    def fix_changed(self):
        return self._changed

    @property
    def _changed(self):
        return self._value != self.__dict__['_orig_value']

    def has_value(self):
        return self._value != None

    def copy(self, other, commit = False):
        if isinstance(other, type(self)):
            return self._copy(other)
        return False

    def _copy(self, other):
        self._value = other._value
        return True

    def commit(self):
        return self._commit()

    def _commit(self):
        self.__dict__['_orig_value'] = self._value 
        return True

    def reject(self):
        return self._reject()

    def _reject(self):
        self._value = self.__dict__['_orig_value'] 
        return True

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self._value is None and other._value is None:
                return False
            return self._value < other._value
        elif isinstance(other, self._type):
            if self._value is None and other is None:
                return False
            return self._value < other
        return False

    def __le__(self, other):
        if isinstance(other, type(self)):
            if self._value is None and other._value is None:
                return True
            return self._value <= other._value
        elif isinstance(other, self._type):
            if self._value is None and other is None:
                return True
            return self._value <= other
        return False

    def __gt__(self, other):
        if isinstance(other, type(self)):
            if self._value is None and other._value is None:
                return False
            return self._value > other._value
        elif isinstance(other, self._type):
            if self._value is None and other is None:
                return False
            return self._value > other
        return False

    def __ge__(self, other):
        if isinstance(other, type(self)):
            if self._value is None and other._value is None:
                return True
            return self._value >= other._value
        elif isinstance(other, self._type):
            if self._value is None and other is None:
                return True
            return self._value >= other
        return False

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._value == other._value
        elif isinstance(other, self._type):
            return self._value == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def _start_tracking(self):
        self.__dict__['_track'] = True

    def _stop_tracking(self):
        self.__dict__['_track'] = False

    def freeze(self):
        self.__dict__['_freeze'] = True

    def unfreeze(self):
        self.__dict__['_freeze'] = False

    def json_encode(self):
        return self._value

    def printx(self):
        print(str(type(self._value))+"<>"+str(self._type)+"::"+str(self._value))
