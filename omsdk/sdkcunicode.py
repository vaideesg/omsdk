from omsdk.version.sdkversion import PY2UC
import io

if PY2UC:
    import codecs

class UnicodeHelper(object):
    @staticmethod

    def stringize(ustring):
        if PY2UC and isinstance(ustring, unicode):
            ustring = ustring.encode('ascii', 'ignore')
        return ustring

class UnicodeWriter(object):
    def __init__(self, name):
        self.name = name
        self.output = None
        
    def __enter__(self):
        if PY2UC:
            self.output = open(self.name, "w")
            #self.output = codecs.open(self.name, encoding='utf-8', mode='w')
        else:
            self.output = open(self.name, "w")
        return self

    def _write_output(self, line):
        if PY2UC:
            self.output.write(unicode(line))
        else:
            self.output.write(line)
                
    def __exit__(self, type, value, traceback):
        if self.output:
            self.output.close()
        return isinstance(value, TypeError)

class UnicodeStringWriter(object):
    def __init__(self):
        self.output = io.StringIO()
        
    def __enter__(self):
        return self

    def _write_output(self, line):
        if PY2UC:
            self.output.write(unicode(line))
        else:
            self.output.write(line)

    def getvalue(self):
        return self.output.getvalue()

    def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)
