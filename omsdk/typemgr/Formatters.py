import io
from omsdk.sdkprint import PrettyPrint
from omsdk.typemgr.FieldType import FieldType
from omsdk.typemgr.ClassType import ClassType
from omsdk.typemgr.ArrayType import ArrayType
from omsdk.sdkcenum import TypeHelper

class FormatterTemplate(object):
    def __init__(self, everything):
        self.everything = everything
        self.include_super_field = True
        self.target = None

    def _emit(self, output, value):
        return 0

    def _init(self, output, obj, array=False):
        return None

    def _close(self, output, obj):
        pass

    def _write(self, output, attr_name, value):
        pass

    def _get_str(self):
        return None

    def format_type(self, obj):
        if obj:
            obj.fix_changed()
            self._format_recurse(self.target, obj)
        return self

    def _format_recurse(self, output_obj, obj):
        if isinstance(obj, FieldType):
            return self._emit(output_obj, obj)
        opobj = self._init(output_obj, obj, isinstance(obj, ArrayType))
        props = obj.Properties
        for i in props:
            if isinstance(i, str):
                if not self.everything:
                    if not obj.__dict__[i]._changed:
                        continue
                if obj.__dict__[i]._super_field and \
                   not self.include_super_field:
                    continue
                attr_name = i
                if obj.__dict__[i]._alias is not None:
                    attr_name = obj.__dict__[i]._alias
                if obj._fname is None:
                    attr_name = obj._alias + "." + str(obj.__dict__[i]._index) + "#" + attr_name
                self._write(opobj, attr_name, obj.__dict__[i])
            else:
                if not self.everything:
                    if i._changed:
                        continue
                entry = self._create_array_entry(opobj)
                entry = self._format_recurse(entry, i)
                entry = self._close_array_entry(opobj, entry)
        self._close(opobj, obj)
        return opobj

    def printx(self):
        print(self._get_str())

class JSONFormatter(FormatterTemplate):
    def __init__(self, everything):
        super().__init__(everything)
        self.target = {}

    def _emit(self, output, value):
        return value

    def _init(self, output, obj, array=False):
        data = {}
        if array: data = []
        if obj._fname:
            output[obj._fname] = data
            return output[obj._fname]
        elif obj._alias and isinstance(obj, ClassType):
            output[obj._alias] = data
            return output[obj._alias]
        return output

    def _create_array_entry(self, opobj):
        return {}

    def _close_array_entry(self, opobj, obj):
        opobj.append(obj)
        return {}

    def _write(self, output, attr_name, value):
        output[attr_name] = self._format_recurse(output, value)

    def _get_str(self):
        return PrettyPrint.prettify_json(self.target)

class XMLFormatter(FormatterTemplate):
    def __init__(self, everything):
        super().__init__(everything)
        self.target = io.StringIO()
        self.include_super_field = False

    def _emit(self, output, value):
        val = value.sanitized_value()
        if val: output.write(str(val))
        return 0

    def _init(self, output, obj, array=False):
        if obj._fname:
            output.write('<{0}>\n'.format(obj._fname))
        return output

    def _close(self, output, obj):
        if obj._fname:
            output.write('</{0}>\n'.format(obj._fname))

    def _create_array_entry(self, output):
        return output

    def _close_array_entry(self, opobj, obj):
        return 

    def _write(self, output, attr_name, value):
        if value._fname:
            output.write('<{0} name="{1}">'.  format(value._fname, attr_name))
            if not isinstance(value, FieldType):
                output.write('\n')
        self._format_recurse(output, value)
        if value._fname:
            output.write('</{0}>\n'.format(value._fname))

    def _get_str(self):
        return self.target.getvalue()

class StringFormatter(FormatterTemplate):
    def __init__(self, everything):
        super().__init__(everything)
        self.target = io.StringIO()

    def _emit(self, output, value):
        val = value.sanitized_value()
        if val: output.write(str(val))
        return 0

    def _init(self, output, obj):
        if obj._fname:
            output.write('{0}=['.format(obj._fname))
        return output

    def _close(self, output, obj):
        if obj._fname:
            output.write(']\n'.format(obj._fname))

    def _write(self, output, attr_name, value):
        if value._fname:
            output.write('{1}='.  format(value._fname, attr_name))
        self._format_recurse(output, value)
        if value._fname:
            output.write(','.format(value._fname))

    def _get_str(self):
        return self.target.getvalue()

