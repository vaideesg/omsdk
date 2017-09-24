from omsdk.sdkcenum import TypeHelper
from omsdk.typemgr.FieldType import FieldType
from omsdk.typemgr.TypeState import TypeState
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# private
#
# def __init__(self, fname, alias, parent=None, volatile=False)
# def __eq__, __ne__, __lt__, __le__, __gt__, __ge__
# def __getattr__
# def __delattr__
# def __setattr__
# def _copy(self, other)
# def _commit(self)
# def _reject(self)
# @_changed
#
# def __str__, __repr__
#
# def _replicate(self, obj, parent)
# def _set_index(self, index=1)
#
# protected:
#
# def my_accept_value(self, value):
#
# public:
# def is_changed(self)
# def fix_changed(self)
# def copy(self, other, commit= False)
# def commit(self)
# def reject(self)
# def freeze(self)
# def unfreeze(self)
# def Properties(self):
#
# def get_root(self)

class ClassType(object):

    def __init__(self, fname, alias, parent = None, volatile=False):
        self._alias = alias
        self._fname = fname
        self._volatile = volatile
        self._parent = parent
        self._composite = False
        self._index = 1
        #self._modifyAllowed = True

        self._freeze = False

        self.__dict__['_state'] = TypeState.UnInitialized

    # Value APIs
    def __getattr__(self, name):
        if name in self.__dict__ and name not in ['_removed']:
            return self.__dict__[name]
        raise AttributeError('Invalid attribute ' + name)

    # Value APIs
    def __setattr__(self, name, value):
        # Do not allow access to internal variables
        if name in ['_removed', '_state']:
            raise AttributeError('Invalid attribute ' + name)

        # Freeze mode: No sets allowed
        if '_freeze' in self.__dict__ and self._freeze:
            raise ValueError('object in freeze mode')

        # allow updates to other fields except _value
        # should we allow updates to  '_type', '_alias', '_fname'?
        if name in [ '_alias', '_fname', '_volatile', '_parent',
                     '_composite', '_index', '_freeze']:
            self.__dict__[name] = value
            return

        # Does it make sense to have create-only attribute!
        # Create-only attribute : No updates allowed
        #if not self._modifyAllowed and \
        #   self._state in [TypeState.Committed, TypeState.Changing]:
        #    raise ValueError('updates not allowed to this object')

        # CompositeClass : sets not allowed in composite classes
        if self._composite:
            raise AttributeError('composite objects cannot be modified')

        # value is None, object was committed; ==> no change
        # value is actually a object!!
        if value is None and \
           self._state in [TypeState.Committed, TypeState.Changing]:
            return 


        if name not in self.__dict__:
            if not (isinstance(value, FieldType) or isinstance(value, ClassType)):
                raise AttributeError(name + ' attribute not found')
            self.__dict__[name] = value
        elif isinstance(self.__dict__[name], FieldType):
            self.__dict__[name]._value = value
        elif isinstance(self.__dict__[name], ClassType):
            not_implemented
        else:
            raise ValueError('value does not belong to FieldType')

        if self._state in [TypeState.UnInitialized, TypeState.Initializing]:
            self.__dict__['_state'] = TypeState.Initializing
        elif self._state in [TypeState.Committed, TypeState.Changing]:
            if self._values_changed(self.__dict__, self.__dict__['_orig_value']):
                self.__dict__['_state'] = TypeState.Committed
            else:
                self.__dict__['_state'] = TypeState.Changing
        else:
            print("Should not come here")

        if self.is_changed() and self._parent:
            self._parent.child_state_changed(self, self._state)

    # Value APIs
    def __delattr__(self, name):
        # Do not allow access to internal variables
        if name in ['_orig_value', '_track', '_freeze', '_type',
                    '_value', '_volatile', '_composite']:
            raise AttributeError('Invalid attribute ' + name)

        # Freeze mode - don't allow any updates
        if '_freeze' in self.__dict__ and self._freeze:
            raise AttributeError('object in freeze mode')

        if name in self.__dict__:
            del self.__dict__[name]

        if self._state in [TypeState.UnInitialized, TypeState.Initializing]:
            self.__dict__['_state'] = TypeState.Initializing
        elif self._state in [TypeState.Committed, TypeState.Changing]:
            if self._values_changed(self.__dict__, self.__dict__['_orig_value']):
                self.__dict__['_state'] = TypeState.Committed
            else:
                self.__dict__['_state'] = TypeState.Changing
        else:
            print("Should not come here")

    # Value APIs
    def my_accept_value(self, value):
        return True

    # State APIs:
    def is_changed(self):
        return self._state in [TypeState.Initializing, TypeState.Changing]

    def _copy_state(self, source, dest):
        for i in source:
            if i.startswith('_'): continue
            if i not in dest:
                dest[i] = source[i]

        for i in dest:
            if i.startswith('_'): continue
            if i not in source: del dest[i]

    def _values_changed(self, source, dest):
        for i in source:
            if i.startswith('_'): continue
            if i not in dest: return False
            if source[i].is_changed(): return False

        for i in dest:
            if i.startswith('_'): continue
            if i not in source: return False
            if dest[i].is_changed(): return False

        return True

    # State : to Committed
    # allowed even during freeze
    def commit(self):
        if self.is_changed():
            if not self._composite:
                if '_orig_value' not in self.__dict__:
                    self.__dict__['_orig_value'] = {}
                self._copy_state(source = self.__dict__,
                                 dest = self.__dict__['_orig_value'])
                for i in self.Properties:
                    self.__dict__[i].commit()
            self.__dict__['_state'] = TypeState.Committed
        return True

    def print_commit(self):
        for i in self.Properties:
            print(i + "<>" + str(self.__dict__[i]._state))

    # State : to Committed
    # allowed even during freeze
    def reject(self):
        print('rejecting....')
        if self.is_changed():
            if not self._composite:
                if '_orig_value' not in self.__dict__:
                    for i in self.Properties:
                        del self.__dict__[i]
                    self.__dict__['_state'] = TypeState.UnInitialized
                else:
                    self._copy_state(source = self.__dict__['_orig_value'],
                                 dest = self.__dict__)
                    self.__dict__['_state'] = TypeState.Committed
                    for i in self.Properties:
                        self.__dict__[i].reject()
        return True

    # Does not have children - so not implemented
    def child_state_changed(self, child, child_state):
        if child_state in [TypeState.Initializing, TypeState.Changing]:
            if self._state == TypeState.UnInitialized:
                self.__dict__['_state'] = TypeState.Initializing
            elif self._state == TypeState.Committed:
                self.__dict__['_state'] = TypeState.Changing

    # what to do?
    def parent_state_changed(self, new_state):
        not_implemented

    # Object APIs
    def copy(self, other):
        if other is None or not isinstance(other, type(self)):
            return False
        for i in other.Properties:
            if i not in self.__dict__:
                self.__dict__[i] = other.__dict__[i].clone(parent=self)
            elif not self.__dict__[i]._volatile:
                self.__dict__[i].copy(other.__dict__[i])
        return True

    # Compare APIs:
    def __lt__(self, other):
        counter = 0
        if isinstance(other, type(self)):
            for i in self.Properties:
                if i not in other.__dict__:
                    counter = counter - 1
                elif self.__dict__[i].__lt__(other.__dict__[i]):
                    counter = counter + 1
                elif self.__dict__[i].__ne__(other.__dict__[i]):
                    counter = counter - 1
            for i in other.Properties:
                if i not in self.__dict__:
                    counter = counter + 1
        return (counter > 0)

    # Compare APIs:
    def __le__(self, other):
        counter = 0
        if isinstance(other, type(self)):
            for i in self.Properties:
                if i not in other.__dict__:
                    counter = counter - 1
                elif self.__dict__[i].__eq__(other.__dict__[i]):
                    continue
                elif self.__dict__[i].__gt__(other.__dict__[i]):
                    counter = counter - 1
            for i in other.Properties:
                if i not in self.__dict__:
                    counter = counter + 1
        return (counter >= 0)

    # Compare APIs:
    def __gt__(self, other):
        counter = 0
        if isinstance(other, type(self)):
            for i in self.Properties:
                if i not in other.__dict__:
                    counter = counter + 1
                elif self.__dict__[i].__gt__(other.__dict__[i]):
                    counter = counter + 1
                elif self.__dict__[i].__ne__(other.__dict__[i]):
                    counter = counter - 1
            for i in other.Properties:
                if i not in self.__dict__:
                    counter = counter - 1
        return (counter > 0)

    # Compare APIs:
    def __ge__(self, other):
        counter = 0
        if isinstance(other, type(self)):
            for i in self.Properties:
                if i not in other.__dict__:
                    counter = counter + 1
                elif self.__dict__[i].__eq__(other.__dict__[i]):
                    continue
                elif self.__dict__[i].__lt__(other.__dict__[i]):
                    counter = counter - 1
            for i in other.Properties:
                if i not in self.__dict__:
                    counter = counter - 1
        return (counter >= 0)

    # Compare APIs:
    def __eq__(self, other):
        if isinstance(other, type(self)):
            for i in self.Properties:
                if i not in other.__dict__ or \
                   self.__dict__[i].__eq__(other.__dict__[i]) is False:
                    return False
            for i in other.Properties:
                if i not in self.__dict__:
                    return False
            return True
        return False

    # Compare APIs:
    def __ne__(self, other):
        return self.__eq__(other) != True

    # Freeze APIs
    def freeze(self):
        self._freeze = True
        for i in self.Properties:
            self.__dict__[i].freeze()

    # Freeze APIs
    def unfreeze(self):
        self.__dict__['_freeze'] = False
        for i in self.Properties:
            self.__dict__[i].unfreeze()

    # Freeze APIs
    def is_frozen(self):
        return self.__dict__['_freeze']

    def _set_index(self, index=1):
        for i in self.Properties:
            self.__dict__[i]._index = index

    def get_root(self):
        if self._parent is None:
            return self
        return self._parent.get_root()

    def _clone_parent(self):
        parent_list = []
        obj = self
        while obj._parent:
            field_name = None
            for prop_name in obj._parent.Properties:
                if obj._parent.__dict__[prop_name] == obj:
                    field_name = prop_name
                    break
            parent_list.insert(0, (obj._parent, field_name))
            obj = obj._parent
        new_list = [ None ]
        for (parent, field) in parent_list:
            new_list.append(type(parent)(new_list[-1]))
            if new_list[-2]:
                new_list[-2].__dict__[field] = new_list[-1]
        return (new_list[1], parent_list[-1][1])

    def clone(self, parent=None):
        if parent is None:
            (parent, field) = self._clone_parent()
        cloneobj = type(self)(parent)
        for i in self.Properties:
            cloneobj.__dict__[i] = self.__dict__[i].clone(parent)
        if parent: parent.__dict__[field] = cloneobj
        return cloneobj

    @property
    def Properties(self):
        return sorted([i for i in self.__dict__ if not i.startswith('_')])

    def _get_fields(self, obj):
        if PY2:
            return {k: v for k,v in obj.iteritems() if not k.startswith('_')}
        if PY3:
            return {k: v for k,v in obj.items() if not k.startswith('_')}

    def json_encode(self):
        return str(self)
