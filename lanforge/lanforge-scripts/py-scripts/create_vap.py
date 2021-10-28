#!/usr/bin/env python3
"""
    Script for creating a variable number of VAPs.
"""
import sys
import os
import importlib
import argparse
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class CreateVAP(Realm):
    def __init__(self,
                 _ssid=None,
                 _security=None,
                 _password=None,
                 _mac=None,
                 _host=None,
                 _port=None,
                 _vap_list=None,
                 _resource=None,
                 _vap_flags=None,
                 _mode=None,
                 _number_template="00000",
                 _radio=None,
                 _channel=36,
                 _country_code=0,
                 _nss=False,
                 _bridge=False,
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
        self.vap_list = _vap_list
        self.resource = _resource
        if _vap_flags is None:
            self.vap_flags = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        else:
            self.vap_flags = _vap_flags
        self.mode = _mode
        self.radio = _radio
        self.channel = _channel
        self.country_code = _country_code
        self.timeout = 120
        self.number_template = _number_template
        self.debug = _debug_on
        self.dhcp = _dhcp
        self.bridge = _bridge
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.dhcp = self.dhcp
        self.vap_profile.mode = self.mode
        self.vap_profile.desired_add_vap_flags = self.vap_flags + ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.vap_profile.desired_add_vap_flags_mask = self.vap_flags + ["wpa2_enable", "80211u_enable", "create_admin_down"]
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

    def build(self):
        # Build VAPs
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)

        print("Creating VAPs")
        self.vap_profile.create(resource = self.resource,
                                radio = self.radio,
                                channel = self.channel,
                                country=self.country_code,
                                up_ = True,
                                debug = False,
                                use_ht40=True,
                                use_ht80=True,
                                use_ht160=False,
                                suppress_related_commands_ = True,
                                use_radius=False,
                                hs20_enable=False,
                                bridge=self.bridge)
        self._pass("PASS: VAP build finished")


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='create_vap.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Create VAPs
            ''',

        description='''\
        create_vap.py
--------------------
Command example:
./create_vap.py
    --upstream_port eth1
    --radio wiphy0
    --num_vaps 3
    --security open
    --ssid netgear
    --passwd BLANK
    --debug
            ''')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--num_vaps', help='Number of VAPs to Create', required=False, default=1)
    optional.add_argument('--vap_flag', help='VAP flags to add', required=False, default=None, action='append')
    optional.add_argument('--bridge', help='Create a bridge connecting the VAP to a port', required=False, default=False)
    optional.add_argument('--mac', help='Custom mac address', default="xx:xx:xx:xx:*:xx")
    optional.add_argument('--mode', default='AUTO')
    optional.add_argument('--channel', default=36)
    optional.add_argument('--country_code', default=0)
    optional.add_argument('--nss', default=False)
    optional.add_argument('--resource', default=1)
    optional.add_argument('--start_id', default=0)
    optional.add_argument('--vap_name',default=None)
    args = parser.parse_args()
    #if args.debug:
    #    pprint.pprint(args)
    #    time.sleep(5)
    if (args.radio is None):
       raise ValueError("--radio required")

    num_vap = int(args.num_vaps)

    vap_list = LFUtils.port_name_series(prefix="vap",
                           start_id=int(args.start_id),
                           end_id=num_vap-1,
                           padding_number=10000,
                           radio=args.radio)
    #print(args.passwd)
    #print(args.ssid)

    if args.vap_name is None:
        for vap in vap_list:
            create_vap = CreateVAP(_host=args.mgr,
                           _port=args.mgr_port,
                           _ssid=args.ssid,
                           _password=args.passwd,
                           _security=args.security,
                                   _mode=args.mode,
                           _vap_list=vap,
                                   _resource=args.resource,
                                   _vap_flags=args.vap_flag,
                           _radio=args.radio,
                                   _channel=args.channel,
                                   _country_code=args.country_code,
                                   _nss=args.nss,
                           _proxy_str=args.proxy,
                                   _bridge=args.bridge,
                           _debug_on=args.debug)
            print('Creating VAP')

            create_vap.build()
    else:
        vap_name = "vap"+args.vap_name
        create_vap = CreateVAP(_host=args.mgr,
                               _port=args.mgr_port,
                               _ssid=args.ssid,
                               _password=args.passwd,
                               _security=args.security,
                               _mode=args.mode,
                               _vap_list=vap_name,
                               _resource=args.resource,
                               _vap_flags=args.vap_flag,
                               _radio=args.radio,
                               _channel=args.channel,
                               _country_code=args.country_code,
                               _nss=args.nss,
                               _proxy_str=args.proxy,
                               _bridge=args.bridge,
                               _debug_on=args.debug)
        print('Creating VAP')

        create_vap.build()

if __name__ == "__main__":
    main()
