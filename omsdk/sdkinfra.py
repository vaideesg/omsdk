import os
import imp
import sys, glob
from omsdk.sdkprint import LogMan, eprint
from omsdk.sdkcenum import EnumWrapper,TypeHelper

class sdkinfra:
    def __init__(self):
        self.drivers = {}
        self.disc_modules = {}
        self.driver_names = {}
    
    def load_from_file(self, filepath):
        mod_name = None
        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        LogMan.debug("Loading " + filepath + "...")
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)
        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)
        return { "name" : mod_name, "module" : py_mod }
    
    def importPath(self, srcdir = None):
        oldpaths = sys.path
        if not srcdir is None:
            oldpaths = [srcdir]
        counter = 0
        paths = []
        for k in oldpaths:
            if not k in paths:
                paths.append(k)

        for psrcdir in paths:
            pypath = os.path.join(psrcdir, 'omdrivers', '__DellDrivers__.py')
            pyglobpath = os.path.join(psrcdir, 'omdrivers', '*.py')
            pydrivers = os.path.join(psrcdir, 'omdrivers')
            if not os.path.exists(pypath):
                continue
            fl = glob.glob(pyglobpath)
            for i in range(len(fl)):
                if fl[i].endswith("__.py"):
                    continue
                counter = counter + 1
                LogMan.debug("Loading: " + str(counter) + "::" + fl[i])
                module_loaded = self.load_from_file(fl[i])
                self.drivers[module_loaded["name"]] = module_loaded["module"]
                self.driver_names[module_loaded["name"]] = module_loaded["name"]
                discClass = getattr(module_loaded["module"], module_loaded["name"])
                self.disc_modules[module_loaded["name"]] = discClass(pydrivers)
                aliases = self.disc_modules[module_loaded["name"]].my_aliases()
                mname = module_loaded["name"]
                for alias in aliases:
                    self.disc_modules[alias] = self.disc_modules[mname]
                    self.drivers[alias] = self.drivers[mname]
                    self.driver_names[alias] = self.driver_names[mname]

        self.driver_enum = EnumWrapper("Driver", self.driver_names).enum_type
    
    def find_driver(self, ipaddr, creds, protopref = None, pOptions = None):
        for mod in self.disc_modules:
            if str(mod) == "FileList":
                continue
            drv = self._create_driver(mod, ipaddr, creds, protopref, pOptions)
            if drv:
                return drv
        return None

    # Return:
    #    None - if driver not found, not classifed
    #    instance of iBaseEntity  - if device of the proper type
    def get_driver(self, driver_en, ipaddr, creds, protopref = None, pOptions = None):
        mod = TypeHelper.resolve(driver_en)
        LogMan.debug("get_driver(): Asking for " + mod)
        return self._create_driver(mod, ipaddr, creds, protopref, pOptions)

    def _create_driver(self, mod, ipaddr, creds, protopref, pOptions):
        LogMan.debug("get_driver(): Asking for " + mod)
        if not mod in self.disc_modules:
            # TODO: Change this to exception
            print(mod + " not found!")
            return None
        try:
            LogMan.debug(mod + " driver found!")
            drv = self.disc_modules[mod].is_entitytype(self, ipaddr, creds, protopref, mod, pOptions)
            return drv
        except AttributeError as attrerror:
            print(mod + " is not device or console")
            print(attrerror)
            return None

    def _driver(self, driver_en):
        mod = TypeHelper.resolve(driver_en)
        LogMan.debug("_driver(): Asking for " + mod)
        if not mod in self.disc_modules:
            # TODO: Change this to exception
            print(mod + " not found!")
            return None
        try:
            LogMan.debug(mod + " driver found!")
            drv = self.disc_modules[mod]._get(self)
            return drv
        except AttributeError as attrerror:
            print(mod + " is not device or console")
            print(attrerror)
            return None
