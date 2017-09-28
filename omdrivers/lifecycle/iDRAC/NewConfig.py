import os
from omdrivers.lifecycle.iDRAC.SCPParsers import XMLParser
from omdrivers.enums.iDRAC.iDRAC import *
from omsdk.sdkcenum import TypeHelper
from omsdk.typemgr.Formatters import *
from omsdk.typemgr.TypeState import *

TLSOptions = TLSProtocol_WebServerTypes
class SCPSimulator(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def _load_scp(self):
        if self.idrac._sysconfig is not None:
            return { 'Status' : 'Success' }

        self.idrac._sysconfig = self.idrac.xmlp.parse_scp('dd\\test.xml')
        self.idrac._sysconfig.commit()
        return { 'Status' : 'Success' }

    def apply_changes(self, reboot=False):
        self.idrac.xmlp.save_scp('', self._sysconfig)
        

class SCPReal(object):

    def _load_scp(self, idrac):
        if idrac._sysconfig is not None:
            return { 'Status' : 'Success' }

        if not idrac.liason_share:
            return { 'Status' : 'Failed',
                     'Message' : 'Configuration Liason Share not registered.' }

        msg = idrac.scp_export(tempshare)
        logger.debug(PrettyPrint.prettify_json(msg))
        if msg['Status'] == 'Success':
            self.load_scp(tempshare, False)
        tempshare.dispose()
        return msg

    def apply_changes(self, reboot=False):
        tempshare = self.liason_share
        if not self._sysconfig.is_changed():
            return {'Status' : 'Success',
                    'Message' : 'Configuration is up-to-date'}

        with open(tempshare, "w") as f:
            f.write(self.xmlp.save_scp('', self._sysconfig))

        msg = self.scp_import(tempshare, reboot=reboot)
        if msg['Status'] == 'Success':
            self._sysconfig.commit()
        else:
            self._sysconfig.reject()
        if reboot:
            reboot()
        tempshare.dispose()
        return msg

class Config:

    def __init__(self):
        self.liason_share = 'one.xml'
        self._sysconfig = None
        self.xmlp = XMLParser(os.path.join('omdrivers\\iDRAC\\Config\\iDRAC.comp_spec'))
        self.scp = SCPSimulator(self)
        self.scp._load_scp()

    def firm_up(self):
        self._sysconfig.RAID.RAIDresetConfig = False
        self._sysconfig.VirtualDisk.RAIDaction = None

    # Enabling APIs
    def apply_changes(self, reboot=False):
        self.xmlp.save_scp('', self._sysconfig)
        msg= { 'Status' : 'Success' }

        if reboot and self._sysconfig.reboot_required():
            print("Rebooting....")
        elif not reboot and self._sysconfig.reboot_required():
            print("Reboot required - but not told to....")
        if msg['Status'] == 'Success':
            self._sysconfig.commit()
        else:
            self._sysconfig.reject()
        return msg

    def change_boot_mode(self, mode):
        self._sysconfig.BIOS.BootMode = mode
        return self.apply_changes(reboot = True)

    def bios_reset_to_defaults(self):
        self._sysconfig.LifecycleController.LCAttributes.BIOSRTDRequested_LCAttributes = BIOSRTDRequested_LCAttributes.T_True
        return self.apply_changes(reboot = True)


    @property
    def BootMode(self):
        return self._sysconfig.BIOS.BootMode

    # Configure APIs
    @property
    def CSIOR(self):
        return self._sysconfig.LifecycleController.LCAttributes.CollectSystemInventoryOnRestart_LCAttributes

    def enable_csior(self):
        self.CSIOR.set_value(CollectSystemInventoryOnRestart_LCAttributesTypes.Enabled)
        return self.apply_changes(reboot = True)

    def disable_csior(self):
        self.CSIOR.set_value(CollectSystemInventoryOnRestart_LCAttributesTypes.Disabled)
        return self.apply_changes(reboot = True)

    @property
    def Location(self):
        return self._sysconfig.System.ServerTopology

    @property
    def iDRAC_NIC(self):
        return self._sysconfig.iDRAC.NIC

    @property
    def iDRAC_IPv4Static(self):
        return self._sysconfig.iDRAC.IPv4Static

    @property
    def iDRAC_IPv6Static(self):
        return self._sysconfig.iDRAC.IPv4Static

    @property
    def TLSProtocol(self):
        return self._sysconfig.iDRAC.WebServer.TLSProtocol_WebServer

    @property
    def SSLEncryptionBits(self):
        return self._sysconfig.iDRAC.WebServer.SSLEncryptionBitLength_WebServer


    #############################################
    ##  SNMP Trap Destinations
    #############################################
    @property
    def SNMPTrapDestination(self):
        return self._sysconfig.iDRAC.SNMPAlert

    def get_trap_destination(self, trap_dest_host):
        return self._sysconfig.iDRAC.SNMPAlert.find_first(Destination_SNMPAlert = trap_dest_host)

    def add_trap_destination(self, trap_dest_host, username = None):
        self._sysconfig.iDRAC.SNMPAlert.new(Destination_SNMPAlert =trap_dest_host, SNMPv3Username_SNMPAlert =username)
        return self.apply_changes(reboot = False)

    def remove_trap_destination(self, trap_dest_host):
        self._sysconfig.iDRAC.SNMPAlert.remove(Destination_SNMPAlert =trap_dest_host)
        return self.apply_changes(reboot = False)

    def disable_trap_destination(self, trap_dest_host):
        entry = self._sysconfig.iDRAC.SNMPAlert.find(trap_dest_host)
        if entry: entry.State_SNMPAlert = StateTypes_SNMPAlert.Disabled
        return self.apply_changes(reboot = False)

    def enable_trap_destination(self, trap_dest_host):
        entry = self._sysconfig.iDRAC.SNMPAlert.find(trap_dest_host)
        if entry: entry.State_SNMPAlert = StateTypes_SNMPAlert.Enabled
        return self.apply_changes(reboot = False)

    #############################################
    ##  End SNMP Trap Destinations
    #############################################

    @property
    def SNMPConfiguration(self):
        return self._sysconfig.iDRAC.SNMP

    @property
    def SyslogServers(self):
        return self._sysconfig.iDRAC.SysLog.Servers.get_value()

    @property
    def SyslogConfig(self):
        return self._sysconfig.iDRAC.SysLog

    def enable_syslog(self):
        if len(self.SyslogServers) > 0:
            self._sysconfig.iDRAC.SysLog.PowerLogEnable_SysLog = PowerLogEnable_SysLogTypes.Enabled
            self._sysconfig.iDRAC.SysLog.SysLogEnable_SysLog = SysLogEnable_SysLogTypes.Enabled
        return self.apply_changes(reboot = False)

    def disable_syslog(self):
        if len(self.SyslogServers) > 0:
            self._sysconfig.iDRAC.SysLog.PowerLogEnable_SysLog = PowerLogEnable_SysLogTypes.Disabled
            self._sysconfig.iDRAC.SysLog.SysLogEnable_SysLog = SysLogEnable_SysLogTypes.Disabled
        return self.apply_changes(reboot = False)

    @property
    def TimeZone(self):
        return self._sysconfig.iDRAC.Time.TimeZone_Time

    @property
    def Time(self):
        return self._sysconfig.iDRAC.Time

    @property
    def NTPServers(self):
        return self._sysconfig.iDRAC.NTPConfigGroup.NTPServers.get_value()

    @property
    def NTPEnabled(self):
        return self._sysconfig.iDRAC.NTPConfigGroup.NTPEnable_NTPConfigGroup

    @property
    def NTPMaxDist(self):
        return self._sysconfig.iDRAC.NTPConfigGroup.NTPMaxDist_NTPConfigGroup

    def enable_ntp(self):
        if len(NTPServers) > 0:
            self._sysconfig.iDRAC.SysLog.NTPEnable_NTPConfigGroup = NTPEnable_NTPConfigGroupTypes.Enabled
        return self.apply_changes(reboot = False)

    def disable_ntp(self):
        self._sysconfig.iDRAC.SysLog.NTPEnable_NTPConfigGroup = NTPEnable_NTPConfigGroupTypes.Disabled
        return self.apply_changes(reboot = False)

    def configure_idrac_dnsname(self, dnsname):
        self._sysconfig.iDRAC.NIC.DNSRacName_NIC = dnsname

    def configure_idrac_ipv4(self, enable_ipv4=True, dhcp_enabled=True):
        m = { True : 'Enabled', False : 'Disabled' }
        self._sysconfig.iDRAC.IPv4.Enable_IPv4 = m[enable_ipv4]
        self._sysconfig.iDRAC.IPv4.DHCPEnable_IPv4 = m[dhcp_enabled]

    def configure_tls(self, tls_protocol = TLSOptions.TLS_1_0_and_Higher, ssl_bits = None):
        self._sysconfig.iDRAC.WebServer.TLSProtocol_WebServer = tls_protocol
        self._sysconfig.iDRAC.WebServer.SSLEncryptionBitLength_WebServer = ssl_bits


    def configure_idrac_ipv4static(self, ipv4_address, ipv4_netmask, ipv4_gateway, dnsarray=None, dnsFromDHCP=False):
        m = { True : 'Enabled', False : 'Disabled' }
        if dnsarray is None: dnsarray = []
        dnsarray.extend(['', ''])
        self._sysconfig.iDRAC.IPv4Static.Address_IPv4Static = ipv4_address
        self._sysconfig.iDRAC.IPv4Static.Netmask_IPv4Static = ipv4_netmask
        self._sysconfig.iDRAC.IPv4Static.Gateway_IPv4Static = ipv4_gateway
        self._sysconfig.iDRAC.IPv4Static.DNS1_IPv4Static = dnsarray[0]
        self._sysconfig.iDRAC.IPv4Static.DNS2_IPv4Static = dnsarray[1]
        self._sysconfig.iDRAC.IPv4Static.DNSFromDHCP_IPv4Static = m[dnsFromDHCP]

    def configure_idrac_ipv4dns(self, dnsarray, dnsFromDHCP=False):
        m = { True : 'Enabled', False : 'Disabled' }
        if dnsarray is None: dnsarray = []
        dnsarray.extend(['', ''])
        self._sysconfig.iDRAC.IPv4Static.DNS1_IPv4Static = dnsarray[0]
        self._sysconfig.iDRAC.IPv4Static.DNS2_IPv4Static = dnsarray[1]
        self._sysconfig.iDRAC.IPv4Static.DNSFromDHCP_IPv4Static = m[dnsFromDHCP]

    def configure_idrac_ipv6static(self, ipv6_address, ipv6_prefixlen = 64, ipv6_gateway="::", dnsarray=None, dnsFromDHCP=False):
        m = { True : 'Enabled', False : 'Disabled' }
        if dnsarray is None: dnsarray = []
        dnsarray.extend(['', ''])
        self._sysconfig.iDRAC.IPv6Static.Address1_IPv6Static = ipv6_address
        self._sysconfig.iDRAC.IPv6Static.PrefixLength_IPv6Static = ipv6_prefixlen
        self._sysconfig.iDRAC.IPv6Static.Gateway_IPv6Static = ipv6_gateway
        self._sysconfig.iDRAC.IPv6Static.DNS1_IPv6Static = dnsarray[0]
        self._sysconfig.iDRAC.IPv6Static.DNS2_IPv6Static = dnsarray[1]
        self._sysconfig.iDRAC.IPv6Static.DNSFromDHCP6_IPv6Static = m[dnsFromDHCP]

    def configure_idrac_ipv6dns(self, dnsarray, dnsFromDHCP=False):
        m = { True : 'Enabled', False : 'Disabled' }
        self._sysconfig.iDRAC.IPv6Static.DNS1_IPv6Static = dnsarray[0]
        self._sysconfig.iDRAC.IPv6Static.DNS2_IPv6Static = dnsarray[1]
        self._sysconfig.iDRAC.IPv6Static.DNSFromDHCP6_IPv6Static = m[dnsFromDHCP]

    def configure_idrac_nic(self, idrac_nic = 'Dedicated', failover=None, auto_negotiate=False, idrac_nic_speed = 1000, auto_dedicated_nic = False):
        m = { True: 'Enabled', False : 'Disabled' }
        if idrac_nic == 'Dedicated':
            failover = None
            auto_dedicated_nic = False
        if idrac_nic == failover:
            return { 'Status' : 'Failed', 'Message' : 'Dedicated and Failover NIC should be different' }
        self._sysconfig.iDRAC.NIC.Selection_NIC = idrac_nic
        self._sysconfig.iDRAC.NIC.Failover_NIC = str(failover)
        self._sysconfig.iDRAC.NIC.Autoneg_NIC = auto_negotiate
        self._sysconfig.iDRAC.NIC.Speed_NIC = idrac_nic_speed
#       self._sysconfig.iDRAC.AutoDedicatedNIC_NIC = m[auto_dedicated_nic],

    def disable_idracnic_vlan(self):
        self._sysconfig.iDRAC.NIC.VLanEnable_NIC = 'Disabled'

    def enable_idracnic_vlan(self, vlan_id = 1, vlan_priority = 0):
        self._sysconfig.iDRAC.NIC.VLanID_NIC = vlan_id
        self._sysconfig.iDRAC.NIC.VLanPriority_NIC = vlan_priority
        self._sysconfig.iDRAC.NIC.VLanEnable_NIC = 'Enabled'

    def configure_location(self,loc_datacenter = None, loc_room=None, loc_aisle=None, loc_rack=None, loc_rack_slot =None, loc_chassis=None):
        self._sysconfig.System.ServerTopology.AisleName_ServerTopology = loc_aisle
        self._sysconfig.System.ServerTopology.DataCenterName_ServerTopology = loc_datacenter
        self._sysconfig.System.ServerTopology.RackName_ServerTopology = loc_rack
        self._sysconfig.System.ServerTopology.RackSlot_ServerTopology = loc_rack_slot
        self._sysconfig.System.ServerTopology.RoomName_ServerTopology = loc_room

    #############################################
    ##  Email Alerts
    #############################################
    @property
    def RegisteredEmailAlert(self):
        return self._sysconfig.iDRAC.EmailAlert

    def get_email_alert(self, email_id):
        return self._sysconfig.iDRAC.EmailAlert.find(Address_EmailAlert = email_id)

    def add_email_alert(self, email_id, custom_msg = ""):
        self._sysconfig.iDRAC.EmailAlert.new(Address_EmailAlert = email_id, CustomMsg_EmailAlert = custom_msg)
        return self.apply_changes(reboot = False)

    def remove_email_alert(self, email_id):
        self._sysconfig.iDRAC.EmailAlert.remove(Address_EmailAlert = email_id)
        return self.apply_changes(reboot = False)

    def disable_email_alert(self, email_id):
        entry = self._sysconfig.iDRAC.EmailAlert.find(Address_EmailAlert = email_id)
        if entry: entry.State_EmailAlert = StateTypes_EmailAlert.Disabled
        return self.apply_changes(reboot = False)

    def enable_email_alert(self, email_id):
        entry = self._sysconfig.iDRAC.EmailAlert.find(Address_EmailAlert = email_id)
        if entry: entry.State_EmailAlert = StateTypes_EmailAlert.Enabled
        return self.apply_changes(reboot = False)

    def change_email_alert(self, email_id, custom_msg):
        entry = self._sysconfig.iDRAC.EmailAlert.find(Address_EmailAlert = email_id)
        if entry: entry.CustomMsg_EmailAlert = custom_msg
        return self.apply_changes(reboot = False)

    #############################################
    ##  End Email Alerts
    #############################################

    def _replicate_ctree(self, obj):
        if isinstance(obj, list):
            return [self._replicate_ctree(i) for i in obj]
        elif isinstance(obj, dict):
            return dict([ (x, self._replicate_ctree(obj[x])) for x in obj])
        else:
            return obj

    def _init_raid_tree(self):
        if self._raid_tree:
            return self._raid_tree

        self.entity.get_partial_entityjson(
              self.entity.ComponentEnum.Controller,
              self.entity.ComponentEnum.Enclosure,
              self.entity.ComponentEnum.VirtualDisk,
              self.entity.ComponentEnum.PhysicalDisk
        )
        raid_tree = self.entity.ContainmentTree
        self._raid_tree = self._replicate_ctree(raid_tree)
        rjson = self._raid_tree["Storage"]
        if not "Controller" in rjson:
            logger.debug("No Controllers!")
            return False

        logger.debug("Containment Tree from device:")
        logger.debug(PrettyPrint.prettify_json(raid_tree['Storage']))

        healthy_cntl_list = {}
        if 'Controller' in self.entity.entityjson:
            for cnt in self.entity.entityjson['Controller']:
                if cnt['PrimaryStatus'] in ['1', '0']:
                    healthy_cntl_list[cnt['FQDD']] = cnt['PrimaryStatus']

        healthy_enc_list = {}
        if 'Enclosure' in self.entity.entityjson:
            for enc in self.entity.entityjson['Enclosure']:
                if enc['PrimaryStatus'] in ['1', '0']:
                    healthy_enc_list[enc['FQDD']] = enc['PrimaryStatus']

        available_pd_list = {}
        if 'PhysicalDisk' in self.entity.entityjson:
            for pd in self.entity.entityjson['PhysicalDisk']:
                if pd['RaidStatus'] in ['1']:
                    available_pd_list[pd['FQDD']] = pd['RaidStatus']

        for controller in rjson['Controller']:
            if isinstance(rjson['Controller'][controller], list):
                continue
            if controller not in healthy_cntl_list:
                rjson['Controller'][controller] = {}
            if 'Enclosure' in rjson['Controller'][controller]:
                encl_list = rjson['Controller'][controller]['Enclosure']
                for encl in encl_list:
                    if encl not in healthy_enc_list:
                        encl_list[encl] = {}
                    if not 'PhysicalDisk' in encl_list[encl]:
                        continue
                    my_list = []
                    for pd in encl_list[encl]['PhysicalDisk']:
                        if pd in available_pd_list:
                            my_list.append(pd)
                    encl_list[encl]['PhysicalDisk'] = my_list

            if 'PhysicalDisk' in rjson['Controller'][controller]:
                my_list = []
                for pd in rjson['Controller'][controller]['PhysicalDisk']:
                    if pd in available_pd_list:
                        my_list.append(pd)
                rjson['Controller'][controller]['PhysicalDisk'] = my_list
        # Controller and Enclosure should be Healthy
        # convert non-raid to raid
        logger.debug("Containment Tree containing healthy/available entries:")
        logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))

    def create_virtual_disk(self, vd_name, span_depth, span_length, raid_type, n_dhs = 0, n_ghs = 0):
        raid_type = TypeHelper.resolve(raid_type)
        self._init_raid_tree()
        config = self.config
        if not "Storage" in self._raid_tree:
            logger.debug("Storage not found in device")
            return { 'Status' : 'Failed',
                     'Message' : 'Storage not found in device' }
        rjson = self._raid_tree["Storage"]
        s_controller = None
        s_enclosure = None
        n_disks = span_length * span_depth
        t_disks = n_disks + n_dhs + n_ghs
        n_cntr = 0
        s_disks = []
        if not "Controller" in rjson:
            logger.debug("No disks left in any Controllers!")
            return { 'Status' : 'Failed',
                     'Message' : 'No controllers found' }

        for controller in rjson['Controller']:
            if isinstance(rjson['Controller'][controller], list):
                continue
            n_cntr = 0
            if 'VirtualDisk' in rjson['Controller'][controller]:
                n_cntr = len(rjson['Controller'][controller]['VirtualDisk'])
                logger.debug("No vds in controller:" + controller)
            if 'PhysicalDisk' in rjson['Controller'][controller]:
                # Direct Attached Disks
                cntrl = rjson['Controller'][controller]
                if len(cntrl['PhysicalDisk']) >= t_disks:
                    s_disks = cntrl['PhysicalDisk'][0:t_disks]
                    s_enclosure = None
                    s_controller = controller
                    break
                else:
                    logger.debug(controller+" no "+str(t_disks)+" disks")
            if 'Enclosure' in rjson['Controller'][controller]:
                encl_list = rjson['Controller'][controller]['Enclosure']
                for encl in encl_list:
                    if not 'PhysicalDisk' in encl_list[encl]:
                        continue
                    if len(encl_list[encl]['PhysicalDisk']) >= t_disks:
                        s_disks = encl_list[encl]['PhysicalDisk'][0:t_disks]
                        s_enclosure = encl
                        s_controller = controller
                        break
                    else:
                        logger.debug(controller+" no "+str(t_disks)+" disks")
            if s_controller:
                break
        if s_controller is None:
            return { 'Status' : 'Failed',
                     'Message' : 'No free disks found' }
        vdfqdd = "Disk.Virtual." + str(n_cntr) + ":" + s_controller
        scp = {}
        scp[s_controller] = {
                config.arspec.RAID.RAIDresetConfig : "False",
                config.arspec.RAID.RAIDforeignConfig : "Clear",
                config.arspec.RAID.RAIDprMode : "Automatic",
                config.arspec.RAID.RAIDccMode : "Normal",
                config.arspec.RAID.RAIDcopybackMode : "On",
                config.arspec.RAID.RAIDEnhancedAutoImportForeignConfig : "Disabled",
                config.arspec.RAID.RAIDrebuildRate : "30",
                config.arspec.RAID.RAIDbgiRate : "30",
                config.arspec.RAID.RAIDreconstructRate : "30",
                vdfqdd :  {
                    config.arspec.RAID.RAIDaction : "Create",
                    config.arspec.RAID.RAIDinitOperation : "None",
                    config.arspec.RAID.DiskCachePolicy : "Default",
                    config.arspec.RAID.RAIDdefaultWritePolicy : "WriteThrough",
                    config.arspec.RAID.RAIDdefaultReadPolicy  :"NoReadAhead",
                    config.arspec.RAID.Name : vd_name,
                    config.arspec.RAID.StripeSize : 128,
                    config.arspec.RAID.SpanDepth : span_depth,
                    config.arspec.RAID.SpanLength : span_length,
                    config.arspec.RAID.RAIDTypes : raid_type,
                    config.arspec.RAID.IncludedPhysicalDiskID : s_disks
                },
        }
        counter = 0
        for disk in s_disks:
            counter += 1
            if counter > (n_disks + n_dhs): state = "Global"
            elif counter > n_disks: state = "Dedicated"
            else: state = "No"
            disk_state = { config.arspec.RAID.RAIDHotSpareStatus : state }
            if s_enclosure:
                if s_enclosure not in scp[s_controller]:
                    scp[s_controller][s_enclosure] = {}
                scp[s_controller][s_enclosure][disk] = disk_state
            else:
                scp[s_controller][disk] = disk_state

        rjson = self._commit_scp(scp, reboot=True)

        if rjson['Status'] == 'Success':
            # if SCP is successful -> update _raid_tree
            updtree = self._raid_tree['Storage']['Controller'][s_controller]
            if 'VirtualDisk' not in updtree:
                updtree['VirtualDisk'] = []
            updtree['VirtualDisk'].append(vdfqdd)
            for disk in s_disks:
                if s_enclosure:
                  updtree['Enclosure'][s_enclosure]['PhysicalDisk'].remove(disk)
                else:
                  updtree['PhysicalDisk'].remove(disk)
            logger.debug("VD Created Successfully. State after creation:")
            logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))
        return rjson

    def get_virtual_disk(self, vd_name):
        self._init_raid_tree()
        if 'VirtualDisk' not in self.entity.entityjson:
            return None
        vdfqdd = None
        for vd in self.entity.entityjson['VirtualDisk']:
            if vd['Name'] == vd_name:
                return vd
        return None

    def delete_virtual_disk(self, vd_name):
        vdselect = self.get_virtual_disk(vd_name)
        if not vdselect:
            return { 'Status' : 'Success', 'Message' : 'No VD found with name "' + vd_name + '"' }
        rjson = self._raid_tree["Storage"]
        if not "Controller" in rjson:
            return { 'Status' : 'Failed', 'Message' : 'Unable to get controller information' }

        scp = {}
        vdfqdd = vdselect['FQDD']
        for controller in rjson['Controller']:
            if isinstance(rjson['Controller'][controller], list):
                continue
            n_cntr = 0
            if not 'VirtualDisk' in rjson['Controller'][controller]:
                continue
            if vdfqdd in rjson['Controller'][controller]['VirtualDisk']:
                scp[controller] = { vdfqdd : { self.config.arspec.RAID.RAIDaction : "Delete" } }

        if len(scp) <= 0:
            return { 'Status' : 'Failed', 'Message' : 'Unable to find the virtual disk information ' }

        rjson = self._commit_scp(scp, reboot=True)

        if rjson['Status'] == 'Success':
            logger.debug("VD Deleted Successfully. State after deletion:")
            # rebuild the raid tree
            del self.entity.entityjson['PhysicalDisk']
            del self.entity.entityjson['VirtualDisk']
            self._raid_tree = None
            self._init_raid_tree()
            logger.debug(PrettyPrint.prettify_json(self._raid_tree['Storage']))
        return rjson

    @property
    def Users(self):
        return self._sysconfig.iDRAC.Users

    def get_user(self, username):
        user = self._sysconfig.iDRAC.Users.find_first(UserName_Users = username)
        if not user:
            print(username + " not found")
        else:
            print(username + " found")
        return user

    def create_user(self, username, password, user_privilege, others=None):
        user_privilege = TypeHelper.resolve(user_privilege)
        self._sysconfig.iDRAC.Users.new(
            UserName_Users =  username,
            Password_Users =   password,
            Privilege_Users =  user_privilege,
            IpmiLanPrivilege_Users = IpmiLanPrivilege_UsersTypes.Administrator,
            IpmiSerialPrivilege_Users = IpmiSerialPrivilege_UsersTypes.Administrator,
            Enable_Users = 'Enabled',
            SolEnable_Users = 'Enabled',
            ProtocolEnable_Users = 'Enabled',
            AuthenticationProtocol_Users = 'SHA',
            PrivacyProtocol_Users = 'AES'
        )

    def change_password(self, username, old_password, new_password):
        user = self.get_user(username)
        if user:
            user.Password_Users = new_password

    def change_privilege(self, username, user_privilege, others=None):
        user = self.get_user(username)
        if user:
            user.Privilege_Users = Privilege_UsersTypes.T_511

    def disable_user(self, username):
        user = self.get_user(username)
        if user:
            user.Enable_Users = 'Disabled'

    def enable_user(self, username):
        user = self.get_user(username)
        if user:
            user.Enable_Users = 'Enabled'

    def delete_user(self, username):
        user = self.get_user(username)
        if user:
            newobj = type(user.get_root())(loading_from_scp=True)
            newobj.commit(True)
            newobj.iDRAC.__dict__['_attribs'] = user.get_root().iDRAC.__dict__['_attribs']
            nuser = newobj.iDRAC.Users.find_or_create(user._index)
            nuser.UserName_Users.__dict__['_state'] = TypeState.Initializing
            nuser.Privilege_Users = Privilege_UsersTypes.T_0
            nuser.IpmiLanPrivilege_Users = IpmiLanPrivilege_UsersTypes.No_Access
            nuser.IpmiSerialPrivilege_Users = IpmiSerialPrivilege_UsersTypes.No_Access
            nuser.Enable_Users ='Disabled'
            nuser.SolEnable_Users ='Disabled'
            nuser.ProtocolEnable_Users ='Disabled'
            self.xmlp.save_scp('', newobj)
            self._sysconfig.iDRAC.Users.remove(UserName_Users = username)
            self.apply_changes()

    def configure_boot_sequence(*boot_devices):
        boot_seq_list = []
        hdd_seq = []
        for bdevice in boot_devices:
            if bdevice == 'CDROM':
                boot_seq_list.append('Optical.SATAEmbedded.E-1')
            elif bdevice == 'NIC':
                for nic in cfg._sysconfig.NIC:
                    if nic.LegacyBootProto not in [LegacyBootProtoTypes.NONE]:
                        boot_seq_list.append(nic._attribs['FQDD'])
            elif bdevice == 'FCHBA':
                for fc in cfg._sysconfig.FCHBA:
                    boot_seq_list.append(fc._FQDD)
            elif bdevice == 'SDCard':
                if cfg._sysconfig.BIOS.InternalSdCardPrimaryCard == 'SdCard1':
                    boot_seq_list.append('Disk.SDInternal.1-1')
            #else:
            #    for controller in cfg._sysconfig.Controller:
            #        vd = idrac.config_mgr.get_virtual_disk(bdevice)
            #        if vd is None:
            #            vd = bdevice
            #        hdd_seq.append(bdevice)
            #        if 'HardDisk.List.1-1' not in boot_seq_list:
            #            boot_seq_list.append('HardDisk.List.1-1')
        if cfg._sysconfig.BIOS.BootMode == BootMode.Uefi:
            cfg._sysconfig.BIOS.UefiBootSeq = ','.join(boot_seq_list)
            cfg._sysconfig.BIOS.UefiHddSeq = ','.join(hdd_seq)
        else:
            cfg._sysconfig.BIOS.BootSeq = ','.join(boot_seq_list)
            cfg._sysconfig.BIOS.HddSeq = ','.join(hdd_seq)

    def print_data(self, obj):
        if obj:
            print(XMLFormatter(True).format_type(obj)._get_str())
        else:
            print('object is null')
