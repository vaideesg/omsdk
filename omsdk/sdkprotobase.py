from enum import Enum
from omsdk.sdkcreds import ProtocolCredentialsFactory, CredentialsEnum
from datetime import datetime
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkcenum import TypeHelper

import sys
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)


class ProtocolBase(object):
    def operation(self, protocmds, cmdname, *args):
        pass


    def _build_ops(self, protocmds, cmdname, *args):
        toargs = {}
        if not "Parameters" in protocmds[cmdname]:
            logger.debug("no parameters")
        elif len(protocmds[cmdname]["Parameters"]) != len(args):
            logger.debug("Too many args")
            return { 'Status' : 'Failed', 'Message' : 'Client Side: Too many arguments' }
        else:
            counter = 0
            for (var, arg, field, val, dest) in protocmds[cmdname]["Parameters"]:
                if (args[counter] is None):
                    myval = ""
                else:
                    args_fixed = args[counter]
                    if PY2 and (val == str and type(args_fixed) == unicode):
                        args_fixed = args_fixed.encode('ascii', 'ignore')
                    if not TypeHelper.belongs_to(val, args_fixed):
                            return { 'Status' : 'Failed', 'Message' : 'Client Side: Argument ' + str(counter) + " got " + str(type(args_fixed))+ "! Must be: " + val.__name__ }
                    try :
                        if (val == datetime) and args_fixed.year == 1970:
                            myval = "TIME_NOW"
                        elif (val == datetime):
                            myval = datetime.strftime(args_fixed, "%Y%m%d%H%M%S")
                        else:
                            myval = TypeHelper.resolve(args_fixed.value)
                    except Exception as ex:
                        myval = args_fixed
                toargs[var] = myval
                if dest != None:
                    toargs[var] = dest(toargs[var])
                logger.debug(var + "<=>" + str(toargs[var]))
                counter = counter + 1
        return { 'Status' : 'Success', 'retval' : toargs }
