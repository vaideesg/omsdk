from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.TypeState import TypeState,TypeBase

# private
#
# >>def __init__(self, mode, fname, alias, parent=None, volatile=False)
# def __init__(self, clsname, min_index=1, max_index=2)
#
# def __eq__, __ne__, __lt__, __le__, __gt__, __ge__
# def __str__, __repr__
#
# protected:
#
# def my_accept_value(self, value):
#
# public:
#
# def new(self, **kwargs):
# def find(self, **kwargs):
# def find_first(self, **kwargs):
# def remove(self, **kwargs):
#
# def is_changed(self)
# def copy(self, other, commit= False)
# def commit(self)
# def reject(self)
# def freeze(self)
# def unfreeze(self)
#
# def get_root(self)

class ArrayType(TypeBase):
    def __init__(self, clsname, parent=None, min_index=1, max_index=2, loading_from_scp=False):
        self._alias = None
        self._fname = clsname.__name__
        self._volatile = False
        self._parent = parent
        self._composite = False
        self._index = 1
        self._loading_from_scp = loading_from_scp
        #self._modifyAllowed = True

        self._cls = clsname
        self._entries = []

        self._indexes_free = [i for i in range(min_index, max_index+1)]
        self._keys = {}

        self._freeze = False

        # Special case for Array. Empty Array is still valid
        self.__dict__['_orig_value'] = []
        self.__dict__['_state'] = TypeState.Committed

    # State APIs:
    def is_changed(self):
        return self._state in [TypeState.Initializing, TypeState.Changing]

    def _copy_state(self, source, dest):
        # from _entries to _orig_entries
        toadd = []
        for i in source:
            if i not in dest:
                toadd.append(i)

        toremove = []
        for i in dest:
            if i not in source:
                toremove.append(i)

        for i in toremove:
            dest.remove(i)

        for i in toadd:
            dest.append(i)

        return True

    def _values_changed(self, source, dest):
        source_idx = []
        for entry in source:
            source_idx.append(str(entry.Key))
        for entry in dest:
            if str(entry.Key) not in source_idx:
                return False
            source_idx.remove(str(entry.Key))
        return (len(source_idx) <= 0)

    def values_deleted(self):
        source_idx = []
        dest_idx = []
        for entry in self._entries:
            source_idx.append(str(entry.Key))
        for entry in self.__dict__['_orig_value']:
            if str(entry.Key) not in source_idx:
                dest_idx.append(str(entry.Key))
                continue
            source_idx.remove(str(entry.Key))
        return dest_idx

    # State : to Committed
    # allowed even during freeze
    def commit(self, loading_from_scp = False):
        if self.is_changed():
            if not self._composite:
                self._copy_state(source = self._entries,
                                 dest = self.__dict__['_orig_value'])
                self.__dict__['_orig_value'] = \
                    sorted(self.__dict__['_orig_value'], key = lambda entry: entry.Index)
                # update _keys
                for entry in self._entries:
                    entry.commit(loading_from_scp)
            if loading_from_scp:
                self.__dict__['_state'] = TypeState.Precommit
            else:
                self.__dict__['_state'] = TypeState.Committed
        return True

    # State : to Committed
    # allowed even during freeze
    def reject(self):
        if self.is_changed():
            if not self._composite:
                if '_orig_value' not in self.__dict__:
                    for i in self._entries:
                        del self._entries
                else:
                    self._copy_state(source = self.__dict__['_orig_value'],
                                 dest = self._entries)
                    for entry in self._entries:
                        entry.reject()
                    self._indexes_free = [i for i in \
                                 range(min_index, max_index+1)]
                    for i in self._entries:
                        self._indexes_free.remove(i.Index)
                        self._keys[str(i.Key)] = i
                self.__dict__['_state'] = TypeState.Committed
        return True

    # Does not have children - so not implemented
    def child_state_changed(self, child, child_state):
        if child_state in [TypeState.Initializing, TypeState.Precommit, TypeState.Changing]:
            if self._state == TypeState.UnInitialized:
                self.__dict__['_state'] = TypeState.Initializing
            elif self._state == TypeState.Committed:
                self.__dict__['_state'] = TypeState.Changing
        if self.is_changed() and self._parent:
            self._parent.child_state_changed(self, self._state)

    # what to do?
    def parent_state_changed(self, new_state):
        not_implemented

    # Object APIs
    def copy(self, other):
        if other is None or not isinstance(other, type(self)):
            return False
        for i in other._entries:
            if i not in self._entries:
                self._entries[i] = other._entries[i].clone(parent=self)
            elif not self._entries[i]._volatile:
                self._entries[i].copy(other._entries[i])
        return True

    # Freeze APIs
    def freeze(self):
        self._freeze = True
        for i in self._entries:
            self.__dict__[i].freeze()

    # Freeze APIs
    def unfreeze(self):
        self.__dict__['_freeze'] = False
        for i in self._entries:
            self.__dict__[i].unfreeze()

    # Freeze APIs
    def is_frozen(self):
        return self.__dict__['_freeze']

    def get_root(self):
        if self._parent is None:
            return self
        return self._parent.get_root()


    def my_accept_value(self, value):
        return True

    # State APIs:
    def is_changed(self):
        return self._state in [TypeState.Initializing, TypeState.Precommit, TypeState.Changing]

    def new(self, index=None, **kwargs):
        if len(self._indexes_free) <= 0:
            raise AttributeError('no more entries in array')
        entry = self._cls(parent=self, loading_from_scp=self._loading_from_scp)
        for i in kwargs:
            entry.__setattr__(i, kwargs[i])
        if index is None and entry.Key is None:
            raise ValueError('key not provided')
        if entry.Key and str(entry.Key) in self._keys:
            raise ValueError(self._cls.__name__ +" key " + str(entry.Key) +' already exists')
            
        if index is None:
            index = self._indexes_free[0]
        else:
            index = int(index)
        entry._set_index(index)
        self._indexes_free.remove(index)
        self._entries.append(entry)
        self._sort()

        # set state!
        if self._state in [TypeState.UnInitialized, TypeState.Initializing]:
            self.__dict__['_state'] = TypeState.Initializing
        elif self._state in [TypeState.Committed, TypeState.Changing]:
            if self._values_changed(self._entries, self.__dict__['_orig_value']):
                self.__dict__['_state'] = TypeState.Committed
            else:
                self.__dict__['_state'] = TypeState.Changing
        else:
            print("Should not come here")

        if self.is_changed() and self._parent:
            self._parent.child_state_changed(self, self._state)
        return entry

    def _clear_duplicates(self):
        keys = {}
        toremove = []
        for entry in self._entries:
            if entry.Key is None:
                #print("Removing none key: " + str(entry._index) + " in " + self._cls.__name__)
                toremove.append(entry)
            strkey = str(entry.Key)
            if strkey in ["", "()"]:
                #print("Removing emptykey: " + str(entry._index) + " in " + self._cls.__name__)
                toremove.append(entry)
            elif strkey in keys:
                #print("ERROR: Duplicate Entry found: " + strkey + " in " + self._cls.__name__)
                toremove.append(entry)
            keys[strkey] = entry

        for entry in toremove:
            self._entries.remove(entry)
            self._indexes_free.append(entry.Index)
            if str(entry.Key) in self._keys:
                del self._keys[str(entry.Key)]
        self._sort()

    # returns a list
    def find(self, **kwargs):
        return self._find(True, **kwargs)

    # returns the first entry
    def find_first(self, **kwargs):
        entries = self._find(False, **kwargs)
        if len(entries) > 0:
            return entries[0]
        return None

    def find_or_create(self, index):
        if isinstance(index, str):
            index = int(index)
        for entry in self._entries:
            if entry._index == index:
                return entry
        return self.new(index)

    def remove(self, **kwargs):
        entries = self._find(True, **kwargs)
        for i in entries:
            self._entries.remove(i)
            self._indexes_free.append(i.Index)
            del self._keys[str(i.Key)]
        self._sort()

        if self._state in [TypeState.UnInitialized, TypeState.Precommit, TypeState.Initializing]:
            self.__dict__['_state'] = TypeState.Initializing
        elif self._state in [TypeState.Committed, TypeState.Changing]:
            if self._values_changed(self._entries, self.__dict__['_orig_value']):
                self.__dict__['_state'] = TypeState.Committed
            else:
                self.__dict__['_state'] = TypeState.Changing
        else:
            print("Should not come here")

        if self.is_changed() and self._parent:
            self._parent.child_state_changed(self, self._state)
        return entries

    def _sort(self):
        self._indexes_free = sorted(self._indexes_free)
        self._entries = sorted(self._entries, key = lambda entry: entry.Index)

    def _find(self, all_entries = True, **kwargs):
        output = []
        for entry in self._entries:
            found = True
            for field in kwargs:
                if entry.__dict__[field]._value != kwargs[field]:
                    found = False
                    break
            if found:
                output.append(entry)
                if not all_entries: break
        return output

    def _find(self, all_entries = True, **kwargs):
        output = []
        for entry in self._entries:
            found = True
            for field in kwargs:
                if entry.__dict__[field]._value != kwargs[field]:
                    found = False
                    break
            if found:
                output.append(entry)
                if not all_entries: break
        return output

    @property
    def Properties(self):
        return self._entries
