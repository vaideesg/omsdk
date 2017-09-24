from omsdk.sdkcenum import EnumWrapper, TypeHelper

TypeState = EnumWrapper('TMS', { 
    'UnInitialized' : 'UnInitialized',
    'Initializing' : 'Initializing',
    'Committed' : 'Committed',
    'Changing' : 'Changing',
}).enum_type

