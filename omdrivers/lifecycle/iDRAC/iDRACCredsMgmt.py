import os
import re
import sys
from omsdk.sdkcreds import UserCredentials
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.lifecycle.sdkcredentials import iBaseCredentialsApi

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    from pysnmp.hlapi import *
    from pysnmp.smi import *
    PySnmpPresent = True
except ImportError:
    PySnmpPresent = False

UserPrivilegeEnum = EnumWrapper("UserPrivilegeEnum", {
    "Administrator" : 511,
    "Operator" : 499,
    "ReadOnly" : 1,
    "NoPrivilege" : 0,
    }).enum_type

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
        return self._config_mgr._get_scp_component('Users')

    def create_user(self, username, password, user_privilege, others=None):
        (uid, retobj, msg) = self._config_mgr._find_empty_slot('Users', username)
        if retobj is None: return msg

        user_privilege = TypeHelper.resolve(user_privilege)
        config = self._config_mgr.config
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  {
                config.arspec.iDRAC.UserName_Users :  (uid, username),
                config.arspec.iDRAC.Password_Users :  (uid, password),
                config.arspec.iDRAC.Privilege_Users : (uid, user_privilege),
                config.arspec.iDRAC.IpmiLanPrivilege_Users : (uid, 'Administrator'),
                config.arspec.iDRAC.IpmiSerialPrivilege_Users : (uid, 'Administrator'),
                config.arspec.iDRAC.Enable_Users : (uid, 'Enabled'),
                config.arspec.iDRAC.SolEnable_Users : (uid, 'Enabled'),
                config.arspec.iDRAC.ProtocolEnable_Users : (uid, 'Enabled'),
                config.arspec.iDRAC.AuthenticationProtocol_Users : (uid, 'SHA'),
                config.arspec.iDRAC.PrivacyProtocol_Users : (uid, 'AES'),
            })

    def change_password(self, username, old_password, new_password):
        (uid, retobj, msg) = self._config_mgr._find_existing_slot('Users', username)
        if retobj is None: return msg

        config = self._config_mgr.config
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  { config.arspec.iDRAC.Password_Users : (uid, new_password), })

    def change_privilege(self, username, user_privilege, others=None):
        (uid, retobj, msg) = self._config_mgr._find_existing_slot('Users', username)
        if retobj is None: return msg

        config = self._config_mgr.config
        user_privilege = TypeHelper.resolve(user_privilege)
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  { config.arspec.iDRAC.Privilege_Users : (uid, user_privilege), })

    def disable_user(self, username):
        (uid, retobj, msg) = self._config_mgr._find_existing_slot('Users', username)
        if retobj is None: return msg

        config = self._config_mgr.config
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  { config.arspec.iDRAC.Enable_Users :  (uid, 'Disabled'), })

    def enable_user(self, username):
        (uid, retobj, msg) = self._config_mgr._find_existing_slot('Users', username)
        if retobj is None: return msg

        config = self._config_mgr.config
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  { config.arspec.iDRAC.Enable_Users :  (uid, 'Enabled'), })

    def delete_user(self, username):
        (uid, retobj, msg) = self._config_mgr._find_existing_slot('Users', username)
        if retobj is None: return msg

        config = self._config_mgr.config
        return self._config_mgr._configure_field_using_scp(
            component = "iDRAC.Embedded.1",
            fmap =  {
                config.arspec.iDRAC.UserName_Users :  (uid, ''),
                config.arspec.iDRAC.Password_Users :  (uid, ''),
                config.arspec.iDRAC.Privilege_Users : (uid, ''),
                config.arspec.iDRAC.IpmiLanPrivilege_Users : (uid, ''),
                config.arspec.iDRAC.IpmiSerialPrivilege_Users : (uid, ''),
                config.arspec.iDRAC.Enable_Users : (uid, 'Disabled'),
                config.arspec.iDRAC.SolEnable_Users : (uid, 'Disabled'),
                config.arspec.iDRAC.ProtocolEnable_Users : (uid, 'Disabled'),
                config.arspec.iDRAC.AuthenticationProtocol_Users : (uid, 'SHA'),
                config.arspec.iDRAC.PrivacyProtocol_Users : (uid, 'AES'),
            })

