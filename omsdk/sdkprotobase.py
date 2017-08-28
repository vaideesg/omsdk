from enum import Enum
from omsdk.sdkcreds import ProtocolCredentialsFactory, CredentialsEnum
from datetime import datetime
from omsdk.sdkprint import pretty, LogMan
from omsdk.sdkcenum import TypeHelper

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class ProtocolBase(object):
    def operation(self, protocmds, cmdname, *args):
        pass


    def _build_ops(self, protocmds, cmdname, *args):
        toargs = {}
        if not "Parameters" in protocmds[cmdname]:
            print("no parameters")
        elif len(protocmds[cmdname]["Parameters"]) != len(args):
            print("Too many args")
            return { 'Status' : 'Failed', 'Message' : 'Client Side: Too many arguments' }
        else:
            counter = 0
            for (var, arg, field, val, dest) in protocmds[cmdname]["Parameters"]:
                if (args[counter] is None):
                    myval = ""
                else:
                    if not TypeHelper.belongs_to(val, args[counter]):
                            return { 'Status' : 'Failed', 'Message' : 'Client Side: Argument ' + str(counter) + " got " + str(type(args[counter]))+ "! Must be: " + val.__name__ }
                    try :
                        if (val == datetime) and args[counter].year == 1970:
                            myval = "TIME_NOW"
                        elif (val == datetime):
                            myval = datetime.strftime(args[counter], "%Y%m%d%H%M%S")
                        else:
                            myval = TypeHelper.resolve(args[counter].value)
                    except Exception as ex:
                        myval = args[counter]
                toargs[var] = myval
                if dest != None:
                    toargs[var] = dest(toargs[var])
                LogMan.debug(var + "<=>" + str(toargs[var]))
                counter = counter + 1
        return { 'Status' : 'Success', 'retval' : toargs }
