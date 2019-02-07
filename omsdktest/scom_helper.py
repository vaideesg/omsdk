import sys
import os
import json
sys.path.append(os.getcwd())
import threading
import time
import traceback
from multiprocessing import Pool
import logging

counter = 1
from sys import stdout, path
from omsdk.sdkcreds import CredentialStore
from omsdk.sdkprint import PrettyPrint
from omsdk.sdkinfra import sdkinfra
from omsdk.sdkgroup import TopologyBuilder
from omsdk.sdkstore import DeviceStore
from omsdk.sdkvisitor import SDKHealthVisitor

import sys
import logging
from omsdk.logging.Logger import LogManager, LoggerConfigTypeEnum

LogManager.setup_logging()

logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def dprint(module, msg):
    global counter
    print("")
    print("=-=-=-=-=-==============================================-=-=-=-=-=")
    print("=-=-=-=-=-= "+str(counter)+ ". "+module + ": " + msg+ "=-=-=-=-=-=")
    counter = counter + 1

sd = sdkinfra()
sd.importPath()
#logging.basicConfig(level=logging.DEBUG)


dprint("Driver SDK", "Connecting to device")

class Results:
    def __init__(self):
        self.npass = 0
        self.nfailed = 0
        self.passlock = threading.Lock()
        self.faillock = threading.Lock()
    def passed(self, obj):
        with self.passlock:
            self.npass = self.npass + 1
    def failed(self, obj):
        with self.faillock:
            self.nfailed = self.nfailed + 1
    def printx(self):
        print("Number Passed: " + str(self.npass))
        print("Number Failed: " + str(self.nfailed))

def do_detailed():
    self.creds = creds

class ListProc:
    NumThreads=30
    def __init__(self, sd, devlist, credstore, store, tbuild,mode):
        self.devlist = devlist
        self.credstore = credstore
        self.sd = sd
        self.store = store
        self.tbuild = tbuild
        self.mode = mode

    def detailed(self):
        return self._process(self._detailed)

    def _process(self, func):
        self.threadlist = []
        P = int(len(self.devlist)/self.NumThreads)
        if P <= 0:
            P = 1
        iplist = [x for x in self.devlist]
        th_iplist = [iplist[i:i+P] for i in range(0,len(iplist),P)]
        print("Number of threads: " + str(len(th_iplist)))
        print("Number of devices/thread: " + str(len(th_iplist[0])))
        counter = 0
        results = Results()
        for i in th_iplist:
            counter=counter +1
            thr = threading.Thread(name=str(counter), \
                          target=func, args=(i,counter,results,))
            #thr = multiprocessing.Process(target=func, args=(i,counter,results,))
            self.threadlist.append(thr)
        for thr in self.threadlist:
            thr.start()
        for t in self.threadlist:
            t.join()
        results.printx()
        return self


    def _detailed(self, th_iplist, c, results):
        t1 = time.time()
        for ipaddr in th_iplist:
            try:
                creds = self.devlist[ipaddr]
                print("=== Connecting to " + ipaddr + " using " + creds+" ====")
                #idrac = sd.get_driver(sd.driver_enum.iDRAC, ipaddr,
                #           self.credstore.get_creds(creds))
                idrac = sd.find_driver(ipaddr,
                           self.credstore.get_creds(creds))
                if idrac is None:
                    print ("Error: Not found a device driver for: " + ipaddr)
                    continue

                idracTopoInfo = idrac._get_topology_info()
                updateGroupsNeeded = self.store.has_topology_info_changes(idrac)
                if updateGroupsNeeded and idracTopoInfo:
                    idracTopoInfo.create_static_groups(self.tbuild)
                    idracTopoInfo.create_groups(self.tbuild)
                    idracTopoInfo.create_assoc(self.tbuild)
                if mode == "detailed":
                    idrac.get_entityjson()
                #SDKHealthVisitor(idrac).visitAll().printx()
                self.store.store_entity(idrac)
                idrac.disconnect()
                results.passed(idrac)
            except Exception as e:
                traceback.print_exc()
                results.failed(e)
        print("Time for " + str(c) + " thread = " + str(time.time()-t1))


class Helper:
    def __init__(self, devlist, credstore, mode):
        store = DeviceStore('.', 'Store')
        tbuild = TopologyBuilder(store)
        tbuild.load()
        l =ListProc(sd, devlist, credstore, store, tbuild, mode)
        l.detailed()
        tbuild.store()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python -m omsdktest.scom_helper devlist creds scalable|detailed")
        exit(1)
    if not os.path.exists(sys.argv[1]) or os.path.isdir(sys.argv[1]):
        print(sys.argv[1] + " does not exist!")
        print("Usage: python -m {0} <jsonfile> [creds]".format(sys.argv[0]))
        exit(1)
    gen_spec = {}
    credstore = CredentialStore()
    mode = 'scalable'
    with open(sys.argv[1]) as enum_data:
        devlist = json.load(enum_data)
    if len(sys.argv) > 2:
        if not os.path.exists(sys.argv[2]) or os.path.isdir(sys.argv[2]):
            print(sys.argv[2] + " does not exist!")
            print("Usage: python -m {0} <jsonfile> [creds]".format(sys.argv[0]))
            exit(1)
        credstore.load_file(sys.argv[2])
    if len(sys.argv) > 3:
        mode = sys.argv[3]
    if mode not in ['scalable', 'detailed']:
        print('invalid mode: ' + mode)
        print("Usage: python -m {0} <jsonfile> [creds]".format(sys.argv[0]))
        exit(1)

    prep_list = {}
    if isinstance(devlist, list):
        prep_list = dict([(ip, 'default') for ip in devlist])

    else:
        for cred in devlist:
            if not credstore.get_creds(cred):
                print("Credentials not found: " + cred)
                continue
            prep_list.update(dict([(ip, cred) for ip in devlist[cred]]))
    #print(PrettyPrint.prettify_json(prep_list))
        
    Helper(prep_list, credstore, mode)
