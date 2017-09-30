import os
import re
import sys
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkcredentials import iBaseCredentialsApi
from omdrivers.enums.iDRAC.iDRACEnums import *
from omdrivers.enums.iDRAC.iDRAC import Privilege_UsersTypes

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False


class iDRACCredsMgmt(iBaseCredentialsApi):
    def __init__(self, entity):
        if PY2:
            super(iDRACCredsMgmt, self).__init__(entity)
        else:
            super().__init__(entity)
        self._job_mgr = entity.job_mgr
        self._config_mgr = entity.config_mgr
        self.eUserPrivilegeEnum = UserPrivilegeEnum

    @property
    def Users(self):
        return self._config_mgr._sysconfig.iDRAC.Users

    #######
    # Creating a user
    # 
    #   user = idrac.user_mgr.Users.new(
    #         user.<attribute_name> = value
    #         user.<attribute_name> = value
    #         user.<attribute_name> = value
    #   )
    #   idrac.user_mgr.Users.new(
    #           UserName_Users = username,
    #           Password_Users = password,
    #           Privilege_Users = Privilege_UsersTypes.Operator,
    #           IpmiLanPrivilege_Users = "Administrator",
    #           IpmiSerialPrivilege_Users = "Administrator",
    #           Enable_Users = "Enabled",
    #           SolEnable_Users = "Enabled",
    #           ProtocolEnable_Users = "Disabled",
    #           AuthenticationProtocol_Users = "SHA",
    #           PrivacyProtocol_Users = "AES"
    #       )
    #
    #   idrac.config_mgr.apply_changes()
    #
    #   Note: for enum types you can give enum or corresponding string value
    #             Privilege_UsersTypes.Administrator or "511"
    #   For details on variable types look at omdrivers.types.iDRAC.iDRAC
    #   and possible values of enum in omdrivers.enums.iDRAC.iDRAC
    #
    #   don't forget to catch for ValueEror and AttributeError exceptions!
    #   You will get that for following reasons:
    #        - Wrong/invalid value provided (enum, string)
    #        - All user entries are exhausted
    #        - Duplicate user entry
    #
    #   Until you do apply_changes, they are not committed.
    #
    #######

    #######
    # Modifying a user
    # 
    #   user = idrac.user_mgr.Users.find_first(UserName_Users = username)
    #
    #   user.<attribute_name> = value
    #   user.<attribute_name> = value
    #   user.<attribute_name> = value
    #
    #   value is None     => treated as no change
    #   value is ''       => treated as equivalent nullifying the object
    #   value is invalid  => ValueError is thrown
    #   idrac.config_mgr.apply_changes()
    #
    #   don't forget to catch for ValueEror and AttributeError exceptions!
    #
    #######

    #######
    # deleting a user
    # 
    #   idrac.user_mgr.iDRAC.Users.remove(UserName_Users = username)
    #   idrac.config_mgr.apply_changes()
    #
    #   don't forget to catch for ValueEror and AttributeError exceptions!
    #
    #######
