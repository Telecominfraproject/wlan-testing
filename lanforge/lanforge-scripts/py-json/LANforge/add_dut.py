# define list of DUT keys
from enum import Enum
from collections import namedtuple

add_dut_flags = {
    'STA_MODE'      : 0x1,      # (1) DUT acts as Station.,
    'AP_MODE'       : 0x2,      # (2) DUT acts as AP.
    'INACTIVE'      : 0x4,      # (3) Ignore this in ChamberView, etc
    'WEP'           : 0x8,      # Use WEP encryption on all ssids, deprecated, see add_dut_ssid.
    'WPA'           : 0x10,     # Use WPA encryption on all ssids, deprecated, see add_dut_ssid.
    'WPA2'          : 0x20,     # Use WPA2 encryption on all ssids, deprecated, see add_dut_ssid.
    'DHCPD-LAN'     : 0x40,     # Provides DHCP server on LAN port
    'DHCPD-WAN'     : 0x80,     # Provides DHCP server on WAN port
    'WPA3'          : 0x100,    # Use WPA3 encryption on all ssids, deprecated, see add_dut_extras.
    '11r'           : 0x200,    # Use .11r connection logic on all ssids, deprecated, see add_dut_ssid.
    'EAP-TTLS'      : 0x400,    # Use EAP-TTLS connection logic on all ssids, deprecated, see add_dut_ssid.
    'EAP-PEAP'      : 0x800,    # Use EAP-PEAP connection logic on all ssids, deprecated, see add_dut_ssid.
    'NOT-DHCPCD'    : 0x1000,   # Station/edge device that is NOT using DHCP.
     # Otherwise, automation logic assumes it is using dhcp client.'
}
class dut_params(namedtuple("dut_params", "key maxlen"), Enum):
    name            = "name",           48
    flags           = "flags",          256
    img_file        = "img_file",       128
    sw_version      = "sw_version",     40
    hw_version      = "hw_version",     40
    model_num       = "model_num",      40
    serial_num      = "serial_num",     40
    serial_port     = "serial_port",    20
    wan_port        = "wan_port",       40
    lan_port        = "lan_port",       40
    ssid1           = "ssid1",          33
    ssid2           = "ssid2",          33
    ssid3           = "ssid3",          33
    passwd1         = "passwd1",        64
    passwd2         = "passwd2",        64
    passwd3         = "passwd3",        64
    mgt_ip          = "mgt_ip",         40
    api_id          = "api_id",         20
    flags_mask      = "flags_mask",     256
    antenna_count1  = "antenna_count1", 1
    antenna_count2  = "antenna_count2", 1
    antenna_count3  = "antenna_count3", 1
    bssid1          = "bssid1",         18
    bssid2          = "bssid2",         18
    bssid3          = "bssid3",         18
    top_left_x      = "top_left_x",     20
    top_left_y      = "top_left_y",     20
    eap_id          = "eap_id",         64

    def has(name):
        for param in dut_params:
            if name == param.key:
                return True
        return False

    def to_flag(name):
        for param in dut_params:
            # print("checking %s =? %s"%(name, param.key))
            if name == param.key:
                return param
        return None

class dut_flags(namedtuple("dut_flags", "name value"), Enum):
    STA_MODE        = "STA_MODE",          0x1  # (1) DUT acts as Station.
    AP_MODE         = "AP_MODE",           0x2  # (2) DUT acts as AP.
    INACTIVE        = "INACTIVE",          0x4  # (3) Ignore this in ChamberView, etc
    WEP             = "WEP",               0x8  # Use WEP encryption
    WPA             = "WPA",              0x10  # Use WPA encryption
    WPA2            = "WPA2",             0x20  # Use WPA2 encryption
    DHCPD_LAN       = "DHCPD-LAN",        0x40  # Provides DHCP server on LAN port
    DHCPD_WAN       = "DHCPD-WAN",        0x80  # Provides DHCP server on WAN port
    WPA3            = "WPA3",            0x100  # Use WPA3 encryption
    IEEE80211r      = "11r",             0x200  # Use .11r connection logic.
    EAP_TTLS        = "EAP-TTLS",        0x400  # Use EAP-TTLS connection logic.
    EAP_PEAP        = "EAP-PEAP",        0x800  # Use EAP-PEAP connection logic.
    NOT_DHCPCD      = "NOT-DHCPCD",     0x1000  # Station/edge device that is NOT using DHCP.
                                                # Otherwise, automation logic assumes it is using dhcp client.
    def has(name):
        for flag in dut_flags:
            # print("checking %s =? %s"%(name, flag.name))
            if name == flag.name:
                return True
        return False

    def to_flag(name):
        for flag in dut_flags:
            # print("checking %s =? %s"%(name, flag.name))
            if name == flag.name:
                return flag
        return None

#eof