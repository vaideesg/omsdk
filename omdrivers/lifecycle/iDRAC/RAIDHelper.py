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

    def Controller_load(self, component, array, ctree, entity):
        return self.my_load(component, array, ctree, entity)

    def Enclosure_load(self, component, array, ctree, entity):
        return self.my_load(component, array, ctree, entity)

    def PhysicalDisk_load(self, component, array, ctree, entity):
        d = self.my_load(component, array, ctree, entity)

    def VirtualDisk_load(self, component, array, ctree, entity):
        return self.my_load(component, array, ctree, entity)

    def my_load(self, component, array, ctree, entity):
        if not component in ctree:
            return False
        count = 0
        for count in range(1, len(entity[component])+1):
            comp = entity[component][count-1]
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
                    self._load_comp(subcomp, entry, subctree, entity)
        return True

    def _load_comp(self, comp, entry, ctree, entity):
        func = getattr(self, comp + '_load')
        return func(comp, entry.__dict__[comp], ctree, entity)

    def load(self, ctree, entity):
        ejson = entity.get_json_device()
        logger.debug(PrettyPrint.prettify_json(ejson))
        self._load_comp('Controller', self, ctree, ejson)
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

    def get_disks(self, span_depth, span_length, n_dhs = 0, n_ghs = 0):
        self._init_storage()
        n_disks = span_length * span_depth + n_dhs + n_ghs
        s_disks = []
        if self.storage.ControllerCount <= 0:
            print("No Healthy Controllers found!")
            return s_disks

        for controller in self.storage.Controller:
            direct_pd_count = controller.PhysicalDisk.Length
            if direct_pd_count >= n_disks:
                s_disks = [i for i in controller.PhysicalDisk]
                return s_disks
            for enclosure in controller.Enclosure:
                encl_pd_count = enclosure.PhysicalDisk.Length
                if encl_pd_count >= n_disks:
                    s_disks = [i for i in enclosure.PhysicalDisk]
                return s_disks
        return s_disks

    def filter_disks(self, n_disks, criteria):
        self._init_storage()
        s_disks = []
        if self.storage.ControllerCount <= 0:
            print("No Healthy Controllers found!")
            return s_disks
        criteria = re.sub('(^|[ \t])disk([^0-9a-zA-Z])','\\1entry\\2',criteria)

        for controller in self.storage.Controller:
            s_disks = controller.PhysicalDisk.find_matching(criteria)
            if len(s_disks) >= n_disks:
                return s_disks[0:n_disks]
            for enclosure in controller.Enclosure:
                s_disks = enclosure.PhysicalDisk.find_matching(criteria)
                return s_disks[0:n_disks]
        return s_disks

    def get_vd_index(self, controller):
        return controller.VirtualDisk.Length+1
