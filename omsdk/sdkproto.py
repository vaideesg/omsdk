from enum import Enum
from omsdk.sdkcreds import ProtocolCredentialsFactory, CredentialsEnum
from omsdk.sdksnmp import SNMPProtocol, EntityMibConvertor
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkunits import UnitsFactory
from omsdk.sdkentitymib import EntityCompEnum, EntitySNMPViews, EntityComponentTree
from omsdk.simulator.devicesim import Simulator
import json
import re
import os
import logging
import sys

from omsdk.http.sdkwsmanbase import WsManOptions
from omsdk.http.sdkwsman import WsManProtocol


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class ProtocolOptions(object):
    def __init__(self, enid):
        self.enid = enid
        self.options = {}

class WSMANOptions(ProtocolOptions):
    def __init__(self):
        if PY2:
            super(WSMANOptions, self).__init__(ProtocolEnum.WSMAN)
        else:
            super().__init__(ProtocolEnum.WSMAN)

class ProtocolOptionsFactory:
    def __init__(self):
        self.pOptions = {}

    def _tostr(self):
        mystr = ""
        for i in self.pOptions:
            mystr = mystr + str(self.pOptions[i]) + ";"
        return mystr

    def __str__(self):
        return self._tostr()

    def __repr__(self):
        return self._tostr()

    def add(self, pOptions):
        if isinstance(pOptions, ProtocolOptions):
            self.pOptions[pOptions.enid] = pOptions
        return self

    def get(self, pEnum):
        if creden in self.pOptions:
            return self.pOptions[pEnum]
        return None

class SNMPOptions(ProtocolOptions):
    def __init__(self):
        if PY2:
            super(SNMPOptions, self).__init__(ProtocolEnum.SNMP)
        else:
            super().__init__(ProtocolEnum.SNMP)

class ProtocolWrapper(object):
    def __init__(self, enumid):
        self.enumid = enumid
        self.selectors = {}
        self.views = {}
        self.compmap = {}
        self.cmds = {}
        self.classifier = {}
        self.view_fieldspec = {}
        self.proto = None
        self.creds = None

    def get_name(self):
        return TypeHelper.resolve(self.enumid)

    def __str__(self):
        return "proto(" + str(self.enumid) + ")"

    def __repr__(self):
        return "proto(" + str(self.enumid) + ")"

    def p(self):
        logger.debug("selected protocol is " + self.enumid.name)

    def connect(self, ipaddr, creds, pOptions):
        self.ipaddr = ipaddr
        self.creds = None
        for supported_cred in self.supported_creds:
            if isinstance(creds, ProtocolCredentialsFactory):
                self.creds = creds.get(supported_cred)
            elif TypeHelper.resolve(creds.enid) == TypeHelper.resolve(supported_cred):
                self.creds = creds
            else:
                logger.debug("Invalid credentials provided!")
        if self.creds is None:
            return False

        logger.debug("Connecting to " + ipaddr + " using " + str(self.creds))
        if Simulator.is_simulating():
            return Simulator.simulator_connect(self.ipaddr, self.enumid, self)
        # no options for me!
        if not pOptions or not pOptions.get(self.enumid):
            pOptions = None
        
        return self.my_connect(ipaddr, self.creds, pOptions)

    def disconnect(self):
        not_implemented

    def my_connect(self, ipaddr, creds, pOptions):
        not_implemented

    def _apply_spec(self, rjson, en):
        for i in self.view_fieldspec[en]:
            if (not i in rjson) or (rjson[i] == "Not Available"):
                continue
            if 'Type' in self.view_fieldspec[en][i]:
                orig_value = rjson[i]
                if rjson[i]:
                    units_spec = {
                        'Type' : self.view_fieldspec[en][i]['Type'],
                        'InUnits' : self.view_fieldspec[en][i]['InUnits'],
                        'Value' : float(rjson[i])
                    }
                    if 'OutUnits' in self.view_fieldspec[en][i]:
                        units_spec['OutUnits'] =  \
                            self.view_fieldspec[en][i]['OutUnits']
                    if 'Metrics' in self.view_fieldspec[en][i]:
                        units_spec['Metrics'] =  \
                            self.view_fieldspec[en][i]['Metrics']
                    rjson[i] = UnitsFactory.Convert(units_spec)
                logger.debug("orig_value: " + str(orig_value) + ", " +\
                             "new_value: " + str(rjson[i]))
            if 'Lookup' in self.view_fieldspec[en][i]:
                orig_value = rjson[i]
                if 'Values' in self.view_fieldspec[en][i] and \
                   orig_value in self.view_fieldspec[en][i]['Values']:
                    rjson[i] = self.view_fieldspec[en][i]['Values'][orig_value]
                logger.debug("orig_value: " + str(orig_value) + ", " +\
                             "new_value: " + str(rjson[i]))
            if 'Rename' in self.view_fieldspec[en][i]:
                orig_value = rjson[i]
                del rjson[i]
                rjson[self.view_fieldspec[en][i]['Rename']] = orig_value

            if 'CopyTo' in self.view_fieldspec[en][i]:
                orig_value = rjson[i]
                rjson[self.view_fieldspec[en][i]['CopyTo']] = orig_value

            if 'UnitModify' in self.view_fieldspec[en][i]:
                # logger.debug("Modifying UNit for ",i)
                unit_spec = self.view_fieldspec[en][i]
                unit_name = unit_spec['UnitName']
                unit_str = 'Units'
                if unit_name in unit_spec:
                    unit_val = rjson[unit_name]
                    unit_map = unit_spec[unit_name]
                    if unit_val in unit_map:
                        unit_str = unit_map[unit_val]
                rjson[i] = UnitsFactory.append_sensors_unit(rjson[i], rjson[unit_spec['UnitModify']], unit_str)

            if 'UnitScale' in self.view_fieldspec[en][i]:
                # logger.debug("Scaling UNit for ",i)
                unit_spec = self.view_fieldspec[en][i]
                rjson[i] = UnitsFactory.append_sensors_unit(rjson[i], unit_spec['UnitScale'], unit_spec['UnitAppend'])

            if 'Macedit' in self.view_fieldspec[en][i]:
                s = rjson[i]
                rjson[i] = str(':'.join([s[j]+s[j+1] for j in range(2,14,2)]))

    def enumerate_view(self, index, bTrue):
        return self._enumerate_view(index, self.views, bTrue)

    def _enumerate_view(self, index, views, bTrue):
        if not index in views:
            logger.debug("WARN: no " + str(index) + " for " + str(self.enumid))
            return { 'Status' : 'Success', 'Message' : 'Not supported' }
        clsName = TypeHelper.resolve(index)
        logger.debug("Collecting " + clsName + " ... via " + str(self.enumid) + "..." )
        if Simulator.is_simulating():
            retval = Simulator.simulate_proto(self.ipaddr, self.enumid, clsName)
        else:
            retval = self.proto.enumerate(clsName, views[index], self.selectors, True)
            if Simulator.is_recording():
                Simulator.record_proto(self.ipaddr,self.enumid, clsName, retval)
        if not 'Data' in retval or retval['Data'] is None:
            return retval
        if index in self.classifier:
            for attr in self.classifier[index]:
                if not clsName in retval['Data']:
                    return {
                        'Status' : 'Failed',
                        'Message': clsName + ' instance is not found!'
                    }
                if not attr in retval['Data'][clsName]:
                    return {
                        'Status' : 'Failed',
                        'Message': 'Classifier attribute not found!'
                    }
                if not re.search(self.classifier[index][attr],
                           retval['Data'][clsName][attr]):
                    return {
                        'Status' : 'Failed',
                        'Message': 'Classifier did not match!'
                    }

        for en in self.view_fieldspec:
            if en != index:
                continue
            for retobj in retval['Data']:
                if isinstance(retval['Data'][retobj], dict):
                    self._apply_spec(retval['Data'][retobj], en)
                else:                        
                    for i in retval['Data'][retobj]:
                        self._apply_spec(i, en)
        return retval

    def complete(self, sdkbase):
        return True

    def operation(self, cmdname, **kwargs):
        argvals = {}
        counter = 1
        fcmd = self.cmds[cmdname]
        for name, value in kwargs.items():
            logger.debug(str(counter) + ":"+ str(name) + "=" + str(value))
            counter = counter + 1
            if not name in fcmd["Args"]:
                str_err = name + " argument is invalid!"
                logger.debug(str_err)
                return { 'Status' : 'Failed', 'Message' : str_err }
            argtype = fcmd["Args"][name]
            if not TypeHelper.belongs_to(argtype, value):
                str_err = name + " argument is invalid type! "
                str_err = str_err + "Expected "+ str(argtype) + ". "
                str_err = str_err + "But got "+ str(type(value))
                str_err = str_err + "But got "+ str(value)
                logger.debug(str_err)
                return { 'Status' : 'Failed', 'Message' : str_err }
            argvals[name] = value
    
        for name in fcmd["Args"]:
            if not name in argvals:
                str_err = name + " argument is empty!"
                logger.debug(str_err)
                return { 'Status' : 'Failed', 'Message' : str_err }
        paramlist = []
        for (pname, argname, field, ftype, dest) in fcmd["Parameters"]:
            if field is None:
                argval = argvals[argname]
            else:
                argval = getattr(argvals[argname], field)
            paramlist.append(argval)

        logger.debug(PrettyPrint.prettify_json(paramlist))
    
        if Simulator.is_simulating():
            str_out = cmdname + "("
            comma = ""
            for i in paramlist:
                str_out = str_out + comma + type(i).__name__ + str(i)
            comma = ","
            str_out = str_out + ")"
            logger.debug(str_out)
            rjson= { 'Status' : 'Success' }
        else:
            rjson = self.proto.operation(self.cmds, cmdname, *paramlist)
        rjson['retval' ] = True
        if not 'Message' in rjson:
            rjson['Message'] = 'none'
        return rjson

    def opget(self, index, selector):
        if not index in self.views:
            logger.debug("WARN: no " + str(index) + " for " + str(self.enumid))
            return { 'Status' : 'Success', 'Message' : 'Not supported' }
        clsName = TypeHelper.resolve(index)
        logger.debug("Collecting " + clsName + " ... via " + str(self.enumid) + "..." )
        if Simulator.is_simulating():
            retval = Simulator.simulate_proto(self.ipaddr, self.enumid, clsName)
        else:
            retval = self.proto.opget(self.views[index], clsName, selector)
            if Simulator.is_recording():
                Simulator.record_proto(self.ipaddr,self.enumid, clsName, retval)
        if not 'Data' in retval or retval['Data'] is None:
            return retval

        counter = 0
        for i in retval['Data']:
            counter = counter + 1
            retval['Data'][clsName] = retval['Data'][i]
            del retval['Data'][i]
            if counter <= 1: 
                break
        return retval

    def isOpSupported(self, fname, **kwargs):
        return fname in self.cmds

class PWSMAN(ProtocolWrapper):
    def __init__(self, selectors, views, compmap, cmds, view_fieldspec = {}):
        if PY2:
            super(PWSMAN, self).__init__(ProtocolEnum.WSMAN)
        else:
            super().__init__(ProtocolEnum.WSMAN)
        self.selectors = selectors
        self.views = views
        self.view_fieldspec = view_fieldspec
        self.compmap = compmap
        self.cmds = cmds
        self.supported_creds = [ CredentialsEnum.User ]

    def clone(self):
        return PWSMAN(self.selectors, self.views, self.compmap, self.cmds, self.view_fieldspec)

    def my_connect(self, ipaddr, creds, pOptions):
        if pOptions:
            logger.debug("Using wsman options!")
        self.proto = WsManProtocol(ipaddr, creds, WsManOptions())
        if self.proto is None:
            return False

        return True

    def disconnect(self):
        if self.proto:
            self.proto.reset(True)


class PSNMP(ProtocolWrapper):
    def __init__(self, views, classifier, view_fieldspec = {}, cmds = {}):
        if PY2:
            super(PSNMP, self).__init__(ProtocolEnum.SNMP)
        else:
            super().__init__(ProtocolEnum.SNMP)
        self.selectors = {}
        self.views = views
        self.view_fieldspec = view_fieldspec
        self.classifier = classifier
        self.cmds = cmds
        self.supported_creds = [ CredentialsEnum.SNMPv1_v2c ]
        self.supports_entity_mib = False
        self.emib_mgr = EntityMibConvertor()

    def clone(self):
        return PSNMP(self.views, self.classifier, self.view_fieldspec, self.cmds)

    def my_connect(self, ipaddr, creds, pOptions):
        if pOptions:
            logger.debug("Using snmp options!")
        self.proto = SNMPProtocol(ipaddr, creds.community, creds.writeCommunity)
        if self.proto is None:
            return False
        return True

    def disconnect(self):
        return True

    def complete(self, sdkbase):
        if not sdkbase.supports_entity_mib:
            return True
        sdkbase.emib_json = self._enumerate_view(EntityCompEnum.Entity, EntitySNMPViews, True)
        if not "Data" in sdkbase.emib_json:
            return False
        if not "Entity" in sdkbase.emib_json['Data']:
            return False
        self.emib_mgr.build_entity_json(sdkbase.emib_json['Data'], sdkbase.entityjson)

class PREST(ProtocolWrapper):
    def __init__(self, views, cmds):
        if PY2:
            super(PREST, self).__init__(ProtocolEnum.REST)
        else:
            super().__init__(ProtocolEnum.REST)
        self.selectors = {}
        self.views = views
        self.cmds = cmds
        self.supported_creds = [ CredentialsEnum.User ]

    def my_connect(self, ipaddr, creds, pOptions):
        return False

    def clone(self):
        return PREST(self.views, self.cmds)

class PREDFISH(ProtocolWrapper):
    def __init__(self, views, cmds):
        if PY2:
            super(PREDFISH, self).__init__(ProtocolEnum.REDFISH)
        else:
            super().__init__(ProtocolEnum.REDFISH)
        self.selectors = {}
        self.views = views
        self.cmds = cmds
        self.supported_creds = [ CredentialsEnum.User ]

    def my_connect(self, ipaddr, creds, pOptions):
        return False

    def clone(self):
        return PREDFISH(self.views, self.cmds)

class PCONSOLE(ProtocolWrapper):
    def __init__(self, obj):
        if PY2:
            super(PCONSOLE, self).__init__(ProtocolEnum.Other)
        else:
            super().__init__(ProtocolEnum.Other)
        self.cmds = { "cmd" : 1 }
        self.obj = obj

    def clone(self):
        return PCONSOLE(self.obj)

    def connect(self, ipaddr, creds):
        self.obj.my_connect()

class ProtocolFactoryIterator:
    def __init__(self, proto):
        self.protocol_factory = proto
        self.current = 0
        self.high = self.protocol_factory.count()

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.current >= self.high:
            raise StopIteration
        else:
            for i in range(self.current, self.high):
                self.current += 1
                if self.protocol_factory.pref.include_flag[self.current - 1]:
                    break
            if i >= self.high:
                raise StopIteration
            return self.protocol_factory.protos[self.current - 1]

class ProtocolFactory(object):
    def __init__(self):
        self.protos = []
        self.ctree = None
        self.sspec = None
        self.pref = ProtoPreference()
        self.classifier = set([])

    def clone(self):
        pFactory = ProtocolFactory()
        for i in self.protos:
            pFactory.protos.append(i.clone())
        pFactory.pref = self.pref.clone()
        pFactory.ctree = self.ctree
        pFactory.sspec = self.sspec
        pFactory.classifier = self.classifier
        return pFactory

    def __iter__(self):
        return ProtocolFactoryIterator(self)

    def add(self, protocol):
        self.protos.append(protocol)
        self.pref.add(protocol.enumid)

    def copy(self, source):
        self.pref.copy(source)
        for i in range(len(source.protocols)-1, -1, -1):
            self._set_preferred_proto(source.protocols[i])

    def _set_preferred_proto(self, protoenum):
        moveit = []
        for i in range(0, len(self.pref.protocols)):
            if (self.pref.protocols[i] == protoenum):
                moveit.append(i)
        tt1 = []
        tt2 = []
        tt3 = []
        for i in range(len(moveit), 0, -1):
            tt1.insert(0, self.protos[moveit[i-1]])
            tt2.insert(0, self.pref.protocols[moveit[i-1]])
            tt3.insert(0, self.pref.include_flag[moveit[i-1]])
            del self.protos[moveit[i-1]]
            del self.pref.protocols[moveit[i-1]]
            del self.pref.include_flag[moveit[i-1]]
        self.protos[0:0] = tt1
        self.pref.protocols[0:0] = tt2
        self.pref.include_flag[0:0] = tt3

    def get(self, i):
        if i < len(self.protos):
            return self.protos[i]
        return None

    def count(self):
        return len(self.protos)

    def addCTree(self, ctree):
        self.ctree = ctree

    def addSubsystemSpec(self, sspec):
        self.sspec = sspec

    def addClassifier(self, classifier):
        self.classifier = set(classifier)

    def printx(self):
        for i in self.protos:
            logger.debug(i)
        self.pref.printx()
