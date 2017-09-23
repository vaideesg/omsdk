from omsdk.typemgr.ClassType import ClassType

class CloneableClassType(ClassType):

    def duplicate_parent(self):
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
            new_list.append(type(parent)('custom', new_list[-1]))
            if new_list[-2]:
                new_list[-2].__dict__[field] = new_list[-1]
        return (new_list[1], parent_list[-1][1])

    def duplicate(self, parent=None):
        if parent is None:
            (parent, field) = self.duplicate_parent()
        obj = type(self)(self._mode, parent)
        self._duplicate_tree(obj, parent)
        if parent:
            parent.__dict__[field] = obj
        obj._start_tracking()
        return obj
