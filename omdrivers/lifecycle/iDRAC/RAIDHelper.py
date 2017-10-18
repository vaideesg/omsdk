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
from omsdk.sdkinfra import sdkinfra
from omsdk.sdkcreds import UserCredentials
from omsdk.simulator.devicesim import Simulator
from omsdk.sdkprint import PrettyPrint
from omdrivers.types.iDRAC.RAID import *
from omsdk.typemgr.ArrayType import ArrayType,FQDDHelper
import re

import logging

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self, loading_from_scp=True):
        self.Controller = ArrayType(Controller, parent = None, 
                              index_helper=FQDDHelper(),
                              loading_from_scp=loading_from_scp)
        self.inited = False

    @property
    def ControllerCount(self):
        return self.Controller.Length

    def Controller_load(self, component, array, ctree, ejson, entity):
        return self.my_load(component, array, ctree, ejson, entity)

    def Enclosure_load(self, component, array, ctree, ejson, entity):
        return self.my_load(component, array, ctree, ejson, entity)

    def PhysicalDisk_load(self, component, array, ctree, ejson, entity):
        d = self.my_load(component, array, ctree, ejson, entity)

    def VirtualDisk_load(self, component, array, ctree, ejson, entity):
        return self.my_load(component, array, ctree, ejson, entity)

    def my_load(self, component, array, ctree, ejson, entity):
        if not component in ctree:
            return False
        count = 0
        for count in range(1, len(ejson[component])+1):
            comp = ejson[component][count-1]
            for field in ['EncryptionMode']:
                if field in comp:
                    del comp[field]
            for field in ['BlockSize', 'FreeSize', 'Size']:
                if field in comp:
                    try :
                        comp[field] = int(float(comp[field]))
                    except Exception as ex:
                        print(str(ex))
            entry = array.flexible_new(index=count, **comp)
            if comp['FQDD'] not in ctree[component]:
                continue
            if isinstance(ctree[component], list):
                # leaf node
                continue
            subctree = ctree[component][comp['FQDD']]
            for subcomp in subctree:
                if subcomp in entry.__dict__:
                    self._load_comp(subcomp, entry, subctree, ejson, entity)
        return True

    def _load_comp(self, comp, entry, ctree, ejson, entity):
        func = getattr(self, comp + '_load')
        return func(comp, entry.__dict__[comp], ctree, ejson, entity)

    def load(self, ctree, entity):
        ejson = entity.get_json_device()
        logger.debug(PrettyPrint.prettify_json(ejson))
        self._load_comp('Controller', self, ctree, ejson, entity)
        self.Controller.commit()
        self.inited = True

class RAIDHelper:
    def __init__(self, entity):
        self.entity = entity
        self.storage = Storage()
        self._init_storage()

    def _init_storage(self):
        if self.storage.inited:
            return self.storage

        self.entity.get_partial_entityjson(
              self.entity.ComponentEnum.Controller,
              self.entity.ComponentEnum.Enclosure,
              self.entity.ComponentEnum.VirtualDisk,
              self.entity.ComponentEnum.PhysicalDisk
        )
        raid_tree = self.entity.ContainmentTree
        logger.debug(PrettyPrint.prettify_json(raid_tree['Storage']))
        self.storage.load(raid_tree["Storage"], self.entity)
        if self.storage.ControllerCount <= 0:
            logger.debug("No Controllers!")
            return self.storage
        self.storage.Controller.remove(PrimaryStatus = '0')
        for controller in self.storage.Controller:
            controller.Enclosure.remove(PrimaryStatus = '0')
            for encl in controller.Enclosure:
                encl.PhysicalDisk.remove_matching("entry.RaidStatus != 'Ready'")
            controller.PhysicalDisk.remove_matching("entry.RaidStatus != 'Ready'")
        return self.storage

    def compute_disk_count(self, span_depth, span_length, n_dhs, n_ghs):
        return span_length * span_depth + n_dhs + n_ghs

    def get_disks(self, n_disks):
        self._init_storage()
        s_disks = []
        if self.storage.ControllerCount <= 0:
            print("No Healthy Controllers found!")
            return s_disks

        for controller in self.storage.Controller:
            direct_pd_count = controller.PhysicalDisk.Length
            if direct_pd_count >= n_disks:
                s_disks = [i for i in controller.PhysicalDisk]
                return s_disks[0:n_disks]
            for enclosure in controller.Enclosure:
                encl_pd_count = enclosure.PhysicalDisk.Length
                if encl_pd_count >= n_disks:
                    s_disks = [i for i in enclosure.PhysicalDisk]
                return s_disks[0:n_disks]
        return s_disks

    def filter_disks(self, n_disks, criteria):
        self._init_storage()
        s_disks = []
        if self.storage.ControllerCount <= 0:
            print("No Healthy Controllers found!")
            return s_disks
        criteria = re.sub('(^|[^0-9a-zA-Z])disk([^0-9a-zA-Z])','\\1entry\\2',criteria)
        for controller in self.storage.Controller:
            s_disks = controller.PhysicalDisk.find_matching(criteria)
            if len(s_disks) >= n_disks:
                return s_disks[0:n_disks]
            for enclosure in controller.Enclosure:
                s_disks = enclosure.PhysicalDisk.find_matching(criteria)
                return s_disks[0:n_disks]
        return s_disks

    def new_virtual_disk(self, **kwargs):
        sysconfig = self.entity.config_mgr._sysconfig
        for i in ['SpanLength', 'SpanDepth',
                  'NumberDedicatedHotSpare', 'NumberGlobalHotSpare']:
            if i not in kwargs:
                return {
                    'Status' : 'Failed',
                    'Message' : 'Parameter ' + i + ' is missing' }

        ndisks = self.compute_disk_count(kwargs['SpanLength'], kwargs['SpanDepth'],
                               kwargs['NumberDedicatedHotSpare'],
                               kwargs['NumberGlobalHotSpare'])
        if 'PhysicalDiskFilter' in kwargs:
            disks = self.filter_disks(ndisks, kwargs['PhysicalDiskFilter'])
        else:
            disks = self.get_disks(ndisks)
        if len(disks) <= 0:
            logger.debug("No sufficient disks found in Controller!")
            return { 'Status' : 'Failed',
                     'Message' : 'No sufficient disks found in controller!' }
        # Assumption: All disks are part of same enclosure or direct attached!
        controller = None
        enclosure = disks[0]._parent._parent
        if not isinstance(disks[0]._parent._parent, Enclosure):
            enclosure = None
            controller = disks[0]._parent._parent
        else:
            controller = enclosure._parent._parent

        cntrl = sysconfig.Controller.find_first(FQDD = controller.FQDD)
        if cntrl is None:
            logger.debug("No such controller found!")
            return { 'Status' : 'Failed',
                     'Message' : 'No such controller found!' }
        vdindex = cntrl.VirtualDisk.Length + 1
        vdfqdd = "Disk.Virtual.{0}:{1}".format(vdindex, controller.FQDD)
        for i in kwargs:
            if i in cntrl.__dict__:
                cntrl.__dict__[i]._value = kwargs[i]
        vdisk = cntrl.VirtualDisk.new(index = vdindex)
        # pass virtual disk attributes to vdisk
        for i in kwargs:
            if i in vdisk.__dict__:
                vdisk.__dict__[i]._value = kwargs[i]
        vdisk._attribs['FQDD'] = vdfqdd
        vdisk.IncludedPhysicalDiskID = ",".join([i.FQDD._value for i in disks])
        target = cntrl
        if enclosure:
            tgt_encl = cntrl.Enclosure.find_first(FQDD = enclosure.FQDD)
            if tgt_encl is None:
                tgt_encl = cntrl.Enclosure.new(index = cntrl.Enclosure.Length+1)
                tgt_encl._attribs['FQDD'] = enclosure.FQDD
            target = tgt_encl
        counter = 0
        (n_dhs, n_ghs) = (kwargs['NumberDedicatedHotSpare'],
                               kwargs['NumberGlobalHotSpare'])
        for disk in disks:
            counter += 1
            if counter > (ndisks + n_dhs): state = "Global"
            elif counter > ndisks: state = "Dedicated"
            else: state = "No"
            tgt_disk = target.PhysicalDisk.find_first(FQDD = disk.FQDD)
            if tgt_disk is None:
                tgt_disk = target.PhysicalDisk.new(index = target.PhysicalDisk.Length+1)
                tgt_disk._attribs['FQDD'] = disk.FQDD
            tgt_disk.RAIDHotSpareStatus.nullify_value()
            tgt_disk.RAIDHotSpareStatus.commit()
            tgt_disk.RAIDHotSpareStatus = state

        return self.entity.config_mgr.apply_changes(reboot = True)

    def delete_virtual_disk(self, **kwargs):
        vdselect = None
        sysconfig = self.entity.config_mgr._sysconfig
        for controller in sysconfig.Controller:
            vdselect = controller.VirtualDisk.find_first(**kwargs)
            if not vdselect:
                continue
            vdselect.RAIDaction = "Delete"
            msg = self.entity.config_mgr.apply_changes(reboot = True)
            if msg['Status'] == 'Success':
                controller.VirtualDisk._remove_selected([vdselect])
                sysconfig.commit()
            return msg
        return { 'Status' : 'Success',
                 'Message' : 'Unable to find the virtual disk' }

    def find_first_virtual_disk(self, **kwargs):
        vdselect = None
        sysconfig = self.entity.config_mgr._sysconfig
        for controller in sysconfig.Controller:
            vdselect = controller.VirtualDisk.find_first(**kwargs)
            if vdselect:
                break
        return vdselect

    def find_virtual_disk(self, **kwargs):
        vdselect = []
        sysconfig = self.entity.config_mgr._sysconfig
        for controller in sysconfig.Controller:
            vdselect.extend(controller.VirtualDisk.find(**kwargs))
        return vdselect

    def find_matching_virtual_disk(self, criteria):
        vdselect = []
        sysconfig = self.entity.config_mgr._sysconfig
        for controller in sysconfig.Controller:
            vdselect.extend(controller.VirtualDisk.find_matching(criteria))
        return vdselect
