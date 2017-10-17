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
