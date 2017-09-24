from omsdk.typemgr.ClassType import ClassType

# private
#
# >>def __init__(self, mode, fname, alias, parent=None, volatile=False)
# def __init__(self, clsname, min_index=1, max_index=2)
# def __getattr__
# def __delattr__
# def __setattr__
# def _start_tracking(self)
# def _stop_tracking(self)
# def _copy(self, other)
# def _commit(self)
# def _reject(self)
# @_changed
#
# def __eq__, __ne__, __lt__, __le__, __gt__, __ge__
# def __str__, __repr__
#
# def _duplicate_tree(self, obj, parent)
# def _set_index(self, index=1)
#
# protected:
#
# def my_accept_value(self, value):
#
# public:
# def Properties(self)
#
# def new(self, **kwargs):
# def find(self, **kwargs):
# def find_first(self, **kwargs):
# def remove(self, **kwargs):
#
# def is_changed(self)
# def fix_changed(self)
# def copy(self, other, commit= False)
# def commit(self)
# def reject(self)
# def freeze(self)
# def unfreeze(self)
#
# def get_root(self)

class ArrayType(object):
    def __init__(self, clsname, parent=None, min_index=1, max_index=2):
        self.cls = clsname
        self._fname = clsname.__name__
        self._entries = []
        self._indexes_free = [i for i in range(min_index, max_index+1)]
        self.keys = {}
        self.__dict__['_freeze'] = False
        self.__dict__['_removed'] = []
        self.__dict__['_track'] = False
        #self.__dict__['_alias'] = alias
        #self.__dict__['_volatile'] = volatile
        #self.__dict__['_fname'] = fname
        self.__dict__['_changed'] = False
        self.__dict__['_parent'] = parent
        self.__dict__['_super_field'] = False
        self.__dict__['_orig_entries'] = []
        self._start_tracking()

    def _start_tracking(self):
        self.__dict__['_track'] = True
        for entry in self._entries:
            entry._start_tracking()

    def _stop_tracking(self):
        self.__dict__['_track'] = False
        for entry in self._entries:
            entry._stop_tracking()

    def copy(self, other, commit = False):
        if not self._copy(other):
            return False
        if commit: self.commit()
        return True

    def _copy(self, other):
        if other is None or not isinstance(other, type(self)):
            return False
        for entry in self._entries:
            # TODO: check if this key is present in copy
            pass
        return True

    def get_root(self):
        if self._parent is None:
            return self
        return self._parent.get_root()

    def commit(self):
        self._stop_tracking()
        self._commit()
        self._start_tracking()
        return True

    def _commit(self):
        # from _entries to _orig_entries
        toadd = []
        for i in self._entries:
            if i not in self._orig_entries:
                toadd.append(i)

        toremove = []
        for i in self._orig_entries:
            if i not in self._entries:
                toremove.append(i)

        for i in toremove:
            self._orig_entries.remove(i)

        for i in toadd:
            self._orig_entries.append(i)
        self._orig_entries = sorted(self._orig_entries, key = lambda entry: entry.Index)

        for entry in self._entries:
            entry._commit()
        return True

    def reject(self):
        self._stop_tracking()
        self._reject()
        self._start_tracking()
        return True

    def _reject(self):
        # from _orig_entries to _entries
        toremove = []
        for i in self._entries:
            if i not in self._orig_entries:
                toremove.append(i)

        toadd = []
        for i in self._orig_entries:
            if i not in self._entries:
                toadd.append(i)

        for i in toremove:
            self._entries.remove(i)
            self._indexes_free.append(i.Index)
            del self.keys[str(i.Key)]

        for i in toadd:
            self._entries.append(i)
            self._indexes_free.remove(i.Index)
            self.keys[str(i.Key)] = i

        self._entries = sorted(self._entries, key = lambda entry: entry.Index)

        for entry in self._entries:
            entry._reject()
        return True

    def my_accept_value(self, value):
        return True

    def fix_changed(self):
        self._changed = False
        print(str(len(self._orig_entries)) + "!=" + str(len(self._entries)))
        if len(self._orig_entries) != len(self._entries):
            self._changed = True
        for entry in self._entries:
            if entry.fix_changed():
                self._changed = True
        return self._changed

    def is_changed(self):
        return self._changed

    def freeze(self):
        self._freeze = True
        for entry in self._entries:
            entry.freeze()

    def unfreeze(self):
        self._freeze = False
        for entry in self._entries:
            entry.unfreeze()

    @property
    def Properties(self):
        return self._entries

    def new(self, **kwargs):
        if len(self._indexes_free) <= 0:
            raise AttributeError('no more entries in array')
        entry = self.cls(mode = 'create', parent=self)
        for i in kwargs:
            entry.__dict__[i]._value = kwargs[i]
        if entry.Key is None:
            raise ValueError('key not provided')
        if str(entry.Key) in self.keys:
            raise ValueError('duplicate entry provided')

        index = self._indexes_free[0]
        self._indexes_free.remove(index)
        entry._set_index(index)
        self._entries.append(entry)
        self.keys[str(entry.Key)] = (index, entry)
        self._sort()
        if not self._track:
            self._orig_entries.append(entry)
        return entry

    # returns a list
    def find(self, **kwargs):
        return self._find(True, **kwargs)

    # returns the first entry
    def find_first(self, **kwargs):
        entries = self._find(False, **kwargs)
        if len(entries) > 0:
            return entries
        return None

    def remove(self, **kwargs):
        entries = self._find(True, **kwargs)
        for i in entries:
            self._entries.remove(i)
            self._indexes_free.append(i.Index)
            del self.keys[str(i.Key)]
        self._sort()
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
