#!/usr/bin/env python3
"""
    Script for creating a variable number of VAPs.
"""
import sys
import os
import importlib
import argparse
import pprint
import logging

logger = logging.getLogger(__name__)
if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


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
                 _proxy_str=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _dhcp=True):
        super().__init__(_host, _port, debug_=_debug_on)
        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.vap_list = _vap_list
        self.resource = _resource
        if _vap_flags is None:
            self.vap_flags = [
                "wpa2_enable",
                "80211u_enable",
                "create_admin_down"]
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
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.dhcp = self.dhcp
        self.vap_profile.mode = self.mode
        self.vap_profile.desired_add_vap_flags = self.vap_flags + \
            ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.vap_profile.desired_add_vap_flags_mask = self.vap_flags + \
            ["wpa2_enable", "80211u_enable", "create_admin_down"]
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

    def build(self):
        # Build VAPs
        self.vap_profile.use_security(
            self.security, self.ssid, passwd=self.password)

        logger.info("Creating VAPs")
        # TODO:  Add cmd line arguments to control the various options of the VAP profile.
        if self.vap_profile.create(resource=self.resource,
                                radio=self.radio,
                                channel=self.channel,
                                up=True,
                                debug=self.debug,
                                use_ht40=True,
                                use_ht80=True,
                                use_ht160=False,
                                suppress_related_commands_=True,
                                use_radius=False,
                                hs20_enable=False):
            self._pass("PASS: VAP build finished")
            return True
        else:
            self._fail("VAP profile creation failed.")
            return False


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
    optional.add_argument(
        '--num_vaps',
        help='Number of VAPs to Create',
        required=False,
        default=1)
    optional.add_argument(
        '--vap_flag',
        help='VAP flags to add',
        required=False,
        default=None,
        action='append')
    optional.add_argument(
        '--mac',
        help='Custom mac address',
        default="xx:xx:xx:xx:*:xx")
    optional.add_argument('--mode', default='0') # 0 means auto  # TODO:  Add help for other available modes.
    optional.add_argument('--channel', default=36)
    optional.add_argument('--country_code', default=0)
    optional.add_argument('--resource', default=1)
    optional.add_argument('--start_id', default=0)
    optional.add_argument('--vap_suffix', default=None, help='The numeric suffix, like the 005 in vap005')
    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    # if args.debug:
    #    pprint.pprint(args)
    #    time.sleep(5)
    if args.radio is None:
        raise ValueError("--radio required")

    num_vap = int(args.num_vaps)

    vap_list = LFUtils.port_name_series(prefix="vap",
                                        start_id=int(args.start_id),
                                        end_id=num_vap - 1,
                                        padding_number=10000,
                                        radio=args.radio)
    # print(args.passwd)
    # print(args.ssid)

    create_vaps = []
    if args.vap_suffix is None:
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
                                   _proxy_str=args.proxy,
                                   _debug_on=args.debug)
            logger.info('Creating VAP')
            if create_vap.build():
                create_vap._pass("VAP %s created." % (vap))
            else:
                create_vap._fail("VAP %s was not created." % (vap))
            create_vaps.append(create_vap)
    else:
        vap_name = "vap" + args.vap_suffix
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
                               _proxy_str=args.proxy,
                               _debug_on=args.debug)
        logger.info('Creating VAP')
        if create_vap.build():
            create_vap._pass("VAP %s created." % (vap))
        else:
            create_vap._fail("VAP %s was not created." % (vap))
        create_vaps.append(create_vap)

    # TODO:  Add logic to clean up vap, unless --noclean option is specified.
    # TODO:  Set radio back to previous channel.

    any_failed = False
    for v in create_vaps:
        if not v.passes():
            any_failed = True
        v.print_pass_fail()

    if any_failed:
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
