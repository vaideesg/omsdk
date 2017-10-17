#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan
#
from omsdk.version.sdkversion import PY2UC
import io

if PY2UC:
    import codecs

class UnicodeHelper(object):
    @staticmethod
    def is_string(ustring):
        return isinstance(ustring, str) or \
               (PY2UC and isinstance(ustring, unicode))

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
