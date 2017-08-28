from omsdk.sdkcenum import EnumWrapper

ProtocolEnum = EnumWrapper('ProtocolEnum',  {
        'SNMP' : 1,
        'WSMAN' : 2,
        'REDFISH' : 3,
        'REST' : 4,
        'Other' : 100,
        'Simulator' : 101
    }).enum_type

ProtoMethods = EnumWrapper("FST", {
    "HuntMode" : "HuntMode",
    "MergeMode" : "MergeMode"
}).enum_type

class ProtoPreference:
    def __init__(self, *args):
        self.orig_protocols = []
        for arg in args:
            self.orig_protocols.append(arg)
        self.orig_mode = ProtoMethods.HuntMode
        self.reset()

    def set_mode(self, mode):
        self.mode = mode

    def reset(self):
        self.protocols = []
        self.include_flag = []
        for arg in self.orig_protocols:
            self.protocols.append(arg)
            self.include_flag.append(True)
        self.mode = self.orig_mode

    def add(self, *protoenums):
        for protoenum in protoenums:
            if not protoenum in self.orig_protocols:
                self.orig_protocols.append(protoenum)
                self.protocols.append(protoenum)
                self.include_flag.append(True)

    def clone(self):
        s = ProtoPreference()
        for i in range(0, len(self.protocols)):
            s.protocols.append(self.protocols[i])
            s.include_flag.append(self.include_flag[i])
        s.mode = self.mode
        return s

    def copy(self, source):
        # clean all preferences
        for i in range(0, len(self.protocols)):
            self.include_flag[i] = False

        # set include flag for all those source protocols
        for j in range(0, len(source.protocols)):
            for i in range(0, len(self.protocols)):
                if self.protocols[i] == source.protocols[j]:
                    self.include_flag[i] = source.include_flag[j]

        if not source.mode is None:
            self.mode = source.mode

        return self

    def set_preferred(self, protoenum):
        moveit = []
        for i in range(0, len(self.protocols)):
            if (self.protocols[i] == protoenum):
                moveit.append(i)
        tt2 = []
        tt3 = []
        for i in range(len(moveit), 0, -1):
            tt2.insert(0, self.protocols[moveit[i-1]])
            tt3.insert(0, self.include_flag[moveit[i-1]])
            del self.protocols[moveit[i-1]]
            del self.include_flag[moveit[i-1]]
        self.protocols[0:0] = tt2
        self.include_flag[0:0] = tt3

    def exclude(self, *protoenums):
        for i in range(0, len(self.protocols)):
            for protoenum in protoenums:
                if (self.protocols[i] == protoenum):
                    self.include_flag[i] = False

    def include(self, *protoenums):
        for i in range(0, len(self.protocols)):
            for protoenum in protoenums:
                if (self.protocols[i] == protoenum):
                    self.include_flag[i] = True

    def include_all(self):
        for i in range(0, len(self.protocols)):
            self.include_flag[i] = True

    def include_only(self, *protoenums):
        for i in range(0, len(self.protocols)):
            self.include_flag[i] = False

        for i in range(0, len(self.protocols)):
            for protoenum in protoenums:
                if (self.protocols[i] == protoenum):
                    self.include_flag[i] = True

    def printx(self):
        counter = 0
        for i in range(0, len(self.protocols)):
            counter = counter + 1
            print (str(counter) + " :" + str(self.protocols[i]) + "(" + str(self.include_flag[i]) + ")")

