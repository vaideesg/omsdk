from omsdk.sdkcenum import EnumWrapper, TypeHelper


TypeState = EnumWrapper('TMS', { 
    'UnInitialized' : 'UnInitialized',
    'Initializing' : 'Initializing',
    'Precommit' : 'Precommit',
    'Committed' : 'Committed',
    'Changing' : 'Changing',
}).enum_type

class TypeBase(object):
    def __init__(self):
        pass

