#!/usr/bin/env python3
"""
    Script for modifying stations.
"""
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class ModifyStation(Realm):
    def __init__(self,
                 _ssid="NA",
                 _security="NA",
                 _password="NA",
                 _mac="NA",
                 _host=None,
                 _port=None,
                 _station_list=None,
                 _enable_flags=None,
                 _disable_flags=None,
                 _number_template="00000",
                 _radio=None,
                 _proxy_str=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _dhcp=True):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.mac = _mac
        self.station_list = _station_list
        self.enable_flags = _enable_flags
        self.disable_flags = _disable_flags
        self.radio = _radio
        self.timeout = 120
        self.number_template = _number_template
        self.debug = _debug_on
        self.dhcp = _dhcp
        self.station_profile = self.new_station_profile()
        self.station_profile.station_names = self.station_list
        self.station_profile.ssid = self.ssid
        self.station_profile.security = self.security
        self.station_profile.ssid_pass = self.password
        self.station_profile.mac = self.mac
        self.station_profile.dhcp = self.dhcp
        self.station_profile.debug = self.debug
        self.station_profile.desired_add_sta_flags = self.enable_flags
        self.station_profile.desired_add_sta_flags_mask = self.enable_flags + self.disable_flags

    def set_station(self):
        return self.station_profile.modify(radio=self.radio)


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='modify_station.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Modify stations on a system. Use the enable_flag to create a flag on a station. Turn off a flag with \
         the disable_flag option. A list of available flags are available in the add_station.py file in \
         py-json/LANforge.
            ''',

        description='''\
        modify_station.py
        --------------------
        Command example:
        ./modify_station.py
            --radio wiphy0
            --station 1.1.sta0000
            --security open
            --ssid netgear
            --passwd BLANK
            --enable_flag osen_enable
            --disable_flag ht160_enable
            --debug
        --------------------
        Station flags are currently defined as:
        wpa_enable           | 0x10         # Enable WPA
        custom_conf          | 0x20         # Use Custom wpa_supplicant config file.
        wep_enable           | 0x200        # Use wpa_supplicant configured for WEP encryption.
        wpa2_enable          | 0x400        # Use wpa_supplicant configured for WPA2 encryption.
        ht40_disable         | 0x800        # Disable HT-40 even if hardware and AP support it.
        scan_ssid            | 0x1000       # Enable SCAN-SSID flag in wpa_supplicant.
        passive_scan         | 0x2000       # Use passive scanning (don't send probe requests).
        disable_sgi          | 0x4000       # Disable SGI (Short Guard Interval).
        lf_sta_migrate       | 0x8000       # OK-To-Migrate (Allow station migration between LANforge radios)
        verbose              | 0x10000      # Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs.
        80211u_enable        | 0x20000      # Enable 802.11u (Interworking) feature.
        80211u_auto          | 0x40000      # Enable 802.11u (Interworking) Auto-internetworking feature.  Always enabled currently.
        80211u_gw            | 0x80000      # AP Provides access to internet (802.11u Interworking)
        80211u_additional    | 0x100000     # AP requires additional step for access (802.11u Interworking)
        80211u_e911          | 0x200000     # AP claims emergency services reachable (802.11u Interworking)
        80211u_e911_unauth   | 0x400000     # AP provides Unauthenticated emergency services (802.11u Interworking)
        hs20_enable          | 0x800000     # Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.
        disable_gdaf         | 0x1000000    # AP:  Disable DGAF (used by HotSpot 2.0).
        8021x_radius         | 0x2000000    # Use 802.1x (RADIUS for AP).
        80211r_pmska_cache   | 0x4000000    # Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).
        disable_ht80         | 0x8000000    # Disable HT80 (for AC chipset NICs only)
        ibss_mode            | 0x20000000   # Station should be in IBSS mode.
        osen_enable          | 0x40000000   # Enable OSEN protocol (OSU Server-only Authentication)
        disable_roam         | 0x80000000   # Disable automatic station roaming based on scan results.
        ht160_enable         | 0x100000000  # Enable HT160 mode.
        disable_fast_reauth  | 0x200000000  # Disable fast_reauth option for virtual stations.
        mesh_mode            | 0x400000000  # Station should be in MESH mode.
        power_save_enable    | 0x800000000  # Station should enable power-save.  May not work in all drivers/configurations.
        create_admin_down    | 0x1000000000 # Station should be created admin-down.
        wds-mode             | 0x2000000000 # WDS station (sort of like a lame mesh), not supported on ath10k
        no-supp-op-class-ie  | 0x4000000000 # Do not include supported-oper-class-IE in assoc requests.  May work around AP bugs.
        txo-enable           | 0x8000000000 # Enable/disable tx-offloads, typically managed by set_wifi_txo command
        use-wpa3             | 0x10000000000 # Enable WPA-3 (SAE Personal) mode.
        use-bss-transition   | 0x80000000000 # Enable BSS transition.
        disable-twt          | 0x100000000000 # Disable TWT mode

                    ''')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--enable_flag', help='station flags to add', default=list(), action='append')
    optional.add_argument('--disable_flag', help='station flags to disable', default=list(), action='append')
    optional.add_argument('--station', help='station to modify', required=True, action='append')
    optional.add_argument('--mac', default="NA")

    args = parser.parse_args()

    modify_station = ModifyStation(_host=args.mgr,
                                   _port=args.mgr_port,
                                   _ssid=args.ssid,
                                   _password=args.passwd,
                                   _security=args.security,
                                   _mac=args.mac,
                                   _station_list=args.station,
                                   _radio=args.radio,
                                   _proxy_str=args.proxy,
                                   _enable_flags=args.enable_flag,
                                   _disable_flags=args.disable_flag,
                                   _debug_on=args.debug)
    modify_station.set_station()

    # TODO:  Check return code and exit accordingly


if __name__ == "__main__":
    main()
