#!/usr/bin/env python3
"""
    Script for modifying VAPs.
"""
import sys
import os
import importlib
import argparse
import logging
from pprint import pformat


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

logger = logging.getLogger(__name__)

class ModifyVAP(Realm):
    def __init__(self,
                 _ssid="NA",
                 _security="NA",
                 _password="NA",
                 _mac="NA",
                 _host=None,
                 _port=None,
                 _vap_list=None,
                 _enable_flags=None,
                 _disable_flags=None,
                 _number_template="00000",
                 _radio=None,
                 _proxy_str=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _dhcp=True):
        super().__init__(lfclient_host=_host,
                         lfclient_port=_port,
                         debug_=_debug_on)

        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.mac = _mac
        self.vap_list = _vap_list
        self.enable_flags = _enable_flags
        self.disable_flags = _disable_flags
        self.radio = _radio
        self.timeout = 120
        self.number_template = _number_template
        self.debug = _debug_on
        self.dhcp = _dhcp
        self.vap_profile = self.new_vap_profile()
        shelf, resource, port, *nil = self.name_to_eid(eid=self.vap_list, debug=self.debug)
        self.vap_profile.resource = resource      
        self.vap_profile.shelf = shelf
        self.vap_profile.add_vap_data["resource"] = resource      
        self.vap_profile.add_vap_data["shelf"] = shelf
        self.vap_profile.vap_name = port
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.mac = self.mac
        self.vap_profile.dhcp = self.dhcp
        self.vap_profile.debug = self.debug
        self.vap_profile.desired_add_vap_flags = self.enable_flags
        self.vap_profile.desired_add_vap_flags_mask = self.enable_flags + self.disable_flags

    def set_vap(self):
        return self.vap_profile.modify(radio=self.radio)


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='modify_vap.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Modify VAPs on a system. Use the enable_flag to create a flag on a VAP. Turn off a flag with \
         the disable_flag option. A list of available flags are available in the add_vap.py file in \
         py-json/LANforge.
            ''',

        description='''\
        modify_vap.py
        --------------------
        Command example:
        ./modify_vap.py
            --radio wiphy0
            --vap 1.1.vap0000
            --security open
            --ssid netgear
            --passwd BLANK
            --enable_flag osen_enable
            --disable_flag ht160_enable
            --debug
        --------------------
        AP flags are currently defined as:

enable_wpa           | 0x10            # Enable WPA
hostapd_config       | 0x20            # Use Custom hostapd config file.
enable_80211d        | 0x40            # Enable 802.11D to broadcast country-code & channels in VAPs
short_preamble       | 0x80            # Allow short-preamble
pri_sec_ch_enable    | 0x100           # Enable Primary/Secondary channel switch.
wep_enable           | 0x200           # Enable WEP Encryption
wpa2_enable          | 0x400           # Enable WPA2 Encryption
disable_ht40         | 0x800           # Disable HT-40 (will use HT-20 if available).
verbose              | 0x10000         # Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs.
80211u_enable        | 0x20000         # Enable 802.11u (Interworking) feature.
80211u_auto          | 0x40000         # Enable 802.11u (Interworking) Auto-internetworking feature.  Always enabled currently.
80211u_gw            | 0x80000         # AP Provides access to internet (802.11u Interworking)
80211u_additional    | 0x100000        # AP requires additional step for access (802.11u Interworking)
80211u_e911          | 0x200000        # AP claims emergency services reachable (802.11u Interworking)
80211u_e911_unauth   | 0x400000        # AP provides Unauthenticated emergency services (802.11u Interworking)
hs20_enable          | 0x800000        # Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.
disable_dgaf         | 0x1000000       # AP Disable DGAF (used by HotSpot 2.0).
8021x_radius         | 0x2000000       # Use 802.1x (RADIUS for AP).
80211r_pmska_cache   | 0x4000000       # Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).
disable_ht80         | 0x8000000       # Disable HT80 (for AC chipset NICs only)
80211h_enable        | 0x10000000      # Enable 802.11h (needed for running on DFS channels)  Requires 802.11d.
osen_enable          | 0x40000000      # Enable OSEN protocol (OSU Server-only Authentication)
ht160_enable         | 0x100000000     # Enable HT160 mode.
create_admin_down    | 0x1000000000    # Station should be created admin-down.
use-wpa3             | 0x10000000000   # Enable WPA-3 (SAE Personal) mode.
use-bss-load         | 0x20000000000   # Enable BSS Load IE in Beacons and Probe Responses (.11e).
use-rrm-report       | 0x40000000000   # Enable Radio measurements IE in beacon and probe responses.
use-bss-transition   | 0x80000000000   # Enable BSS transition.

                    ''')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--enable_flag', help='VAP flags to add', default=list(), action='append')
    optional.add_argument('--disable_flag', help='VAP flags to disable', default=list(), action='append')
    optional.add_argument('--vap', help='VAP to modify', required=True)
    optional.add_argument('--mac', default="NA")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if (args.log_level):
        logger_config.set_level(level=args.log_level)
        
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()


    modify_vap = ModifyVAP(_host=args.mgr,
                           _port=args.mgr_port,
                           _ssid=args.ssid,
                           _password=args.passwd,
                           _security=args.security,
                           _mac=args.mac,
                           _vap_list=args.vap,
                           _enable_flags=args.enable_flag,
                           _disable_flags=args.disable_flag,
                           _radio=args.radio,
                           _proxy_str=args.proxy,
                           _debug_on=args.debug)
    json_response = modify_vap.set_vap()
    logger.info("modify_vap.set_vap ")


if __name__ == "__main__":
    main()
