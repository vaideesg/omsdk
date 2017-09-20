from omsdk.sdkcenum import EnumWrapper
import logging

logger = logging.getLogger(__name__)

BusProtocolTypes = EnumWrapper("BusProtocolTypes", {
    "PCIe" : "PCIe",
}).enum_type

BusProtocolVersionTypes = EnumWrapper("BusProtocolVersionTypes", {
    "T_2_0" : "2.0",
    "T_2_1" : "2.1",
    "T_3_0" : "3.0",
    "T_3_1" : "3.1",
    "Unknown" : "Unknown",
}).enum_type

CapableSpeedTypes = EnumWrapper("CapableSpeedTypes", {
    "T_2_5_GT_s" : "2.5 GT/s",
    "T_5_0_GT_s" : "5.0 GT/s",
    "T_8_0_GT_s" : "8.0 GT/s",
    "Unknown" : "Unknown",
}).enum_type

CryptographicEraseTypes = EnumWrapper("CryptographicEraseTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

DeviceProtocolTypes = EnumWrapper("DeviceProtocolTypes", {
    "NVMe_1_1" : "NVMe 1.1",
    "Nvme1_0" : "Nvme1.0",
    "Unknown" : "Unknown",
}).enum_type

FailurePredictedTypes = EnumWrapper("FailurePredictedTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

PcieMaxLinkWidthTypes = EnumWrapper("PcieMaxLinkWidthTypes", {
    "Unknown" : "Unknown",
    "x1" : "x1",
    "x2" : "x2",
    "x4" : "x4",
    "x8" : "x8",
}).enum_type

PcieNegotiatedLinkSpeedTypes = EnumWrapper("PcieNegotiatedLinkSpeedTypes", {
    "T_2_5_GT_s" : "2.5 GT/s",
    "T_5_0_GT_s" : "5.0 GT/s",
    "T_8_0_GT_s" : "8.0 GT/s",
    "Unknown" : "Unknown",
}).enum_type

PcieNegotiatedLinkWidthTypes = EnumWrapper("PcieNegotiatedLinkWidthTypes", {
    "Unknown" : "Unknown",
    "x1" : "x1",
    "x2" : "x2",
    "x4" : "x4",
    "x8" : "x8",
}).enum_type

SecureEraseTypes = EnumWrapper("SecureEraseTypes", {
    "No" : "No",
    "Yes" : "Yes",
}).enum_type

SmartStatusTypes = EnumWrapper("SmartStatusTypes", {
    "Disabled" : "Disabled",
    "Enabled" : "Enabled",
}).enum_type

StateTypes = EnumWrapper("StateTypes", {
    "Failed" : "Failed",
    "Not_Ready_Locked" : "Not Ready/Locked",
    "Overheat" : "Overheat",
    "ReadOnly" : "ReadOnly",
    "Ready" : "Ready",
    "Unknown" : "Unknown",
}).enum_type

