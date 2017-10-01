import os
import sys
sys.path.append(os.getcwd())
from omdrivers.enums.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.iDRAC import *
from omdrivers.types.iDRAC.SystemConfiguration import *
from omsdk.typemgr.BuiltinTypes import *

FType = True
CType = True
AType = True
def P(msg, expected, actual):
    p = 'Passed==>'
    if expected != actual: p = 'Failed==>'
    print("{3}:: {0} = [expected: {1}] {2}".format(msg, expected, actual, p))

def D(msg, obj, everything = False):
    print('=======' + msg)
    print(obj.ModifiedXML)

if True:
    idrac_system = SNMP(None, loading_from_scp=True)
    idrac_system.AlertPort_SNMP = 184
    idrac_system.TrapFormat_SNMP = TrapFormat_SNMPTypes.SNMPv1
    print("===== 2 attributes")
    print(idrac_system.ModifiedXML)
    idrac_system.commit(True)
    print("===== nothing")
    print(idrac_system.ModifiedXML)

    idrac_system.commit()
    print("===== nothing")
    print(idrac_system.ModifiedXML)


    # Precommit FType
    DVAL = 162
    VAL = 700
    NVAL = 200
    tport = PortField(DVAL, 'SNMPTrapPort')
    tport._value = VAL
    tport.commit(False)
    print(tport == VAL)
    tport._value = NVAL
    print(tport == NVAL)
    tport.reject()
    print(tport == VAL)
    print(tport.__dict__['_orig_value'] == VAL)
    idrac_idrac = iDRAC()
    # Final Test
    idrac_idrac.SNMP.AlertPort_SNMP = 184
    idrac_idrac.SNMP.TrapFormat_SNMP = TrapFormat_SNMPTypes.SNMPv1
    print("=== System.iDRAC.SNMP.162")
    print("=====2 attributes")
    print(idrac_idrac.ModifiedXML)
    print("=====================================")

    idrac_system = SystemConfiguration(loading_from_scp=False)
    print("=====nothing")
    print(idrac_system.ModifiedXML)
    print(idrac_system.iDRAC.SNMP.AlertPort_SNMP == None)
    try:
        idrac_system.iDRAC.copy(idrac_idrac)
        print("Failed: copy ro objects after commit: Failed")
    except Exception as ex:
        print("Passed: do not allow copy of ro objects after commit")
        print(str(ex))
    idrac_system.commit()
    print("===== nothing")
    print(idrac_system.ModifiedXML)
    idrac_system.iDRAC.SNMP.AlertPort_SNMP = 184
    print(idrac_system.iDRAC.SNMP.AlertPort_SNMP == 184)
    idrac_system.commit()
    print(idrac_system.iDRAC.SNMP.AlertPort_SNMP == 184)

    idrac_system.reject() # no rejection as copy committed
    print(idrac_system.iDRAC.SNMP.AlertPort_SNMP == 184)
    print("=== System.iDRAC.SNMP.184 (no rejection as copy committed)")
    print(idrac_system.iDRAC.SNMP.XML)

    tport = PortField(162, 'SNMPTrapPort')
    tfmt = EnumTypeField(None, TrapFormat_SNMPTypes, 'SNMPTrapFormat')
    tfmt._value = "SNMPv1"
    print(tfmt == TrapFormat_SNMPTypes.SNMPv1)
    # Don't allow comparision with string ==> becomes too generic
    try:
        print(tfmt == 'SNMPv1')
        print('Failed')
    except Exception as ex:
        print(str(ex))
        print('Passed')
    # Enum Types
    print(tfmt == TrapFormat_SNMPTypes.SNMPv1)
    print(tfmt != None)
    print("=============")
    tfmt.commit()
    print(tfmt == TrapFormat_SNMPTypes.SNMPv1)
    tfmt._value = None
    print(tfmt == TrapFormat_SNMPTypes.SNMPv1)
    print(tfmt.is_changed() == False)
    tfmt._value = TrapFormat_SNMPTypes.SNMPv2
    print(tfmt != TrapFormat_SNMPTypes.SNMPv1)
    print(tfmt.is_changed() == True)
    tfmt.reject()
    print(tfmt == TrapFormat_SNMPTypes.SNMPv1)
    print(tfmt.is_changed() == False)
    print("=====================================")

    tport._value = 194
    print(tport.is_changed() == True and tport == 194)
    try:
        # assigning a int (same value) to invalid value
        tport._value = -162
        print(False)
    except Exception as s1:
        print(True)
    try:
        tport.reject()
        print(tport._state)
        print(tport.is_changed() == False)
    except Exception as s1:
        # tport has moved to Initialized state. So no ops can be done!
        print(True)
    print(tport._state)
    try:
        tport.commit()
        print(tport.is_changed() == False)
    except Exception as s1:
        # tport has moved to Initialized state. So no ops can be done!
        print(True)
    print(tport._state)
    tport._value = 162
    tport.commit()
    print(tport.is_changed() == False and tport == 162)
    # assigning a string (same value) to value
    tport._value = "162"
    print(tport.is_changed() == False and tport == 162)
    # assigning a string (different value) to value
    tport._value = "181"
    print(tport.is_changed() == True and tport == 181)
    # assigning a int (different value) to value
    tport._value = 191
    print(tport.is_changed() == True and tport == 191)
    # instance of port field
    nport = PortField(171)
    nport.commit()
    try:
        # instance of wrong type
        nport._value = StringField("181")
        print(False)
    except Exception as s1:
        print(True)
    print(nport.is_changed() == False and nport == 171)
    print("=====================================")

    try :
        # freeze the object
        tport.freeze()
        # commits are ok during freeze
        tport.commit()
        # setting should fail!
        tport._value = PortField(141)
        print('Failed')
    except Exception as ex:
        print(tport.is_changed() == False and tport == 191)

    try :
        # freeze the object
        nport = PortField(151)
        # freeze the object
        nport.freeze()
        # rejects are ok during freeze
        nport.reject()
    except Exception as ex:
        print(str(ex))
        print(nport.is_changed() == False and nport == 191)

    try:
        # unfreeze the object
        tport.unfreeze()
        # setting should succeed!
        tport._value = PortField(8711)
        print(tport.is_changed() == True and tport == 8711)
    except Exception as ex:
        print(False)


    print("=====================================")
    s1 = PortField(161)
    print('==== s1 <> s1 ')
    P("s1 == s1",  True , s1 == s1)
    P("s1 != s1",  False, s1 != s1)
    P("s1 >  s1",  False, s1 >  s1)
    P("s1 >= s1",  True , s1 >= s1)
    P("s1 <  s1",  False, s1 <  s1)
    P("s1 <= s1",  True , s1 <= s1)

    s2 = PortField(184)
    print('==== s1.161 <> s2.184 ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", False, s1 >  s2)
    P("s1 >= s2", False, s1 >= s2)
    P("s1 <  s2", True , s1 <  s2)
    P("s1 <= s2", True , s1 <= s2)

    (s2, s1) = (s1, s2)
    print('==== s1.184 <> s2.161 ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", True , s1 >  s2)
    P("s1 >= s2", True , s1 >= s2)
    P("s1 <  s2", False, s1 <  s2)
    P("s1 <= s2", False, s1 <= s2)

    s = SNMP()
    s1 = SNMP()
    s1.AgentCommunity_SNMP = 'public'
    print(s < s1)
    D('after SNMP() -> no changes', s, everything=False)
    D('after SNMP() -> printall', s, everything=True)
    s.reject()
    D('after SNMP() -> reject - no changes', s, everything=False)
    s.TrapFormat_SNMP._value = TrapFormat_SNMPTypes.SNMPv1
    D('after SNMP() -> trapfmt = snmpv1', s, everything=False)
    s.commit()
    D('after SNMP() -> commit - no changes', s, everything=False)
    D('after SNMP() -> printall (contains snmpv1)', s, everything=True)

    try:
        # assigning a int (same value) to invalid value
        s.AlertPort_SNMP = -162
        print(False)
    except Exception as s1:
        print(True)

    # assigning a string (same value) to value
    s.AlertPort_SNMP = "162"
    s.commit()
    D('after SNMP() -> commit - no changes', s, everything=False)
    print(s.is_changed() == False and s.AlertPort_SNMP == 162)
    # assigning a string (different value) to value
    s.AlertPort_SNMP = "181"
    print(s.is_changed() == True and s.AlertPort_SNMP == 181)
    # assigning a int (different value) to value
    s.AlertPort_SNMP = 191
    print(s.is_changed() == True and s.AlertPort_SNMP == 191)
    # instance of port field
    s.AlertPort_SNMP = PortField(171)
    print(s.is_changed() == True and s.AlertPort_SNMP == 171)
    try:
        # instance of wrong type
        s.AlertPort_SNMP = StringField("171")
        print(False)
    except Exception as s1:
        print(True)
    print(s.is_changed() == True and s.AlertPort_SNMP == 171)

    s = SNMP()
    s.AlertPort_SNMP = 184
    s.commit()
    try :
        # freeze the object
        s.freeze()
        # setting should fail!
        s.AlertPort_SNMP._value = PortField(141)
        print('Failed')
    except Exception as ex:
        print(s.is_changed() == False and s.AlertPort_SNMP == 184)
    print("======")
    try:
        # unfreeze the object
        s.unfreeze()
        # setting should succeed!
        s.AlertPort_SNMP = PortField(141)
        print(s.is_changed() == True and s.AlertPort_SNMP == 141)
    except Exception as ex:
        print(False)

    s = SNMP()
    try:
        del s.AlertPort_SNMP
        print( (s.AlertPort_SNMP == 162) == True)
    except Exception as ex:
        print(str(ex))
        print(s.is_changed() == True)
    s.AlertPort_SNMP = PortField(174)
    print(s.is_changed() == True and s.AlertPort_SNMP == 174)
    try:
        s.reject()
        print(s.is_changed() == False and s.AlertPort_SNMP != 162)
    except Exception as ex:
        print(str(ex))
        print(s.is_changed() == False)
        print(s.AlertPort_SNMP == 162)

    # When stop tracking, changes are same as original
    s.AlertPort_SNMP = 1894
    print(s.is_changed() == True and s.AlertPort_SNMP == 1894)
    D('after SNMP() -> port changes', s, everything=False)

    s1 = SNMP()
    s2 = SNMP()
    print('==== def(s1) <> def(s2) ')
    P("s1 == s2", True , s1 == s2)
    P("s1 != s2", False, s1 != s2)
    P("s1 >  s2", False, s1 >  s2)
    P("s1 >= s2", True , s1 >= s2)
    P("s1 <  s2", False, s1 <  s2)
    P("s1 <= s2", True , s1 <= s2)
    s1.AlertPort_SNMP = 162
    s1.commit()
    print('==== s1 <> s1 ')
    P("s1 == s1", True , s1 == s1)
    P("s1 != s1", False, s1 != s1)
    P("s1 >  s1",  False, s1 >  s1)
    P("s1 >= s1",  True , s1 >= s1)
    P("s1 <  s1",  False, s1 <  s1)
    P("s1 <= s1",  True , s1 <= s1)

    s2.AlertPort_SNMP = 162
    s2.commit()
    print('==== s1 <> s2 ')
    P("s1 == s2", True , s1 == s2)
    P("s1 != s2", False, s1 != s2)
    P("s1 >  s2", False, s1 >  s2)
    P("s1 >= s2", True , s1 >= s2)
    P("s1 <  s2", False, s1 <  s2)
    P("s1 <= s2", True , s1 <= s2)

    s2.AlertPort_SNMP = 184
    print('==== s1.161 <> s2.184 ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", False, s1 >  s2)
    P("s1 >= s2", False, s1 >= s2)
    P("s1 <  s2", True , s1 <  s2)
    P("s1 <= s2", True , s1 <= s2)

    s1.AlertPort_SNMP = 184
    s2.AlertPort_SNMP = 161
    print('==== s1.184 <> s2.161 ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", True , s1 >  s2)
    P("s1 >= s2", True , s1 >= s2)
    P("s1 <  s2", False, s1 <  s2)
    P("s1 <= s2", False, s1 <= s2)

    del s1.AlertPort_SNMP
    print('==== s1.None <> s2.161 ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", False, s1 >  s2)
    P("s1 >= s2", False, s1 >= s2)
    P("s1 <  s2", True , s1 <  s2)
    P("s1 <= s2", True , s1 <= s2)

    s1 = SNMP()
    s2 = SNMP()
    del s2.AlertPort_SNMP
    print('==== s1.161 <> s2.None ')
    P("s1 == s2", False, s1 == s2)
    P("s1 != s2", True , s1 != s2)
    P("s1 >  s2", True , s1 >  s2)
    P("s1 >= s2", True , s1 >= s2)
    P("s1 <  s2", False, s1 <  s2)
    P("s1 <= s2", False, s1 <= s2)

if True:

    users = ArrayType(Users, loading_from_scp=True)
    print(users._index_helper.unusable(1))
    users.new(UserName_Users='vaidees')
    print("===== 1 user name")
    print(Users.ModifiedXML)
    users.commit(True)
    print("===== nothing")
    print(Users.ModifiedXML)
    users.commit()
    print("===== nothing")
    print(Users.ModifiedXML)
    entry = users.new(UserName_Users = 'hello')
    print("===== (users.username=hello)")
    print(users.ModifiedXML)
    users.commit()
    print("=== ()")
    print(users.ModifiedXML)
    users.new(UserName_Users = 'ajaya')
    print("===== (ajaya)")
    print(users.ModifiedXML)
    users.reject()
    print("===== ()")
    print(users.ModifiedXML)
    print("=====(hello)")
    print(users.XML)
    users.remove(UserName_Users = 'hello')
    print("===== ()")
    print(users.ModifiedXML)
    print("Expected =[vaidees], Actual=")
    for i in users.values_deleted(): print(i.Json)

    users.reject()
    print("Expected =[], Actual=" + str(users.values_deleted()))
    print("===== ()")
    print(users.ModifiedXML)
    print("=====")
