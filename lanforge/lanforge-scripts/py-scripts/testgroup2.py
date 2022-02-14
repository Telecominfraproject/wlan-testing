#!/usr/bin/env python3
"""
    This script will create a variable number of layer3 stations each with their own set of cross-connects and endpoints.

    Use './create_l3.py --help' to see command line usage and options
"""
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
TestGroupProfile = realm.TestGroupProfile


class TestGroup2(Realm):
    def __init__(self,
                 ssid, security, password, sta_list, name_prefix, upstream, radio,
                 host="localhost",
                 port=8080,
                 mode=0,
                 ap=None,
                 side_a_min_rate=56,
                 side_a_max_rate=0,
                 side_b_min_rate=56,
                 side_b_max_rate=0,
                 number_template="00000",
                 use_ht160=False,
                 group_name=None,
                 list_groups=None,
                 tg_action=None,
                 cx_action=None,
                 add_cx_list=None,
                 rm_cx_list=None,
                 show_group=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port)
        if rm_cx_list is None:
            rm_cx_list = []
        if add_cx_list is None:
            add_cx_list = []
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.mode = mode
        self.ap = ap
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l3_cx_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.use_ht160 = use_ht160
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)
        # self.station_list= LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=2, padding_number_=10000, radio='wiphy0') #Make radio a user defined variable from terminal.

        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        self.tg_action = tg_action
        self.cx_action = cx_action
        self.list_groups = list_groups
        self.show_group = show_group
        self.tg_profile = self.new_test_group_profile()
        if not group_name and not list_groups and (tg_action or cx_action or add_cx_list or rm_cx_list or show_group):
            raise ValueError("Group name must be set if manipulating test groups")
        else:
            self.tg_profile.group_name = group_name

        if add_cx_list is not None and len(add_cx_list) == 1 and ',' in add_cx_list[0]:
            self.add_cx_list = add_cx_list[0].split(',')
        else:
            self.add_cx_list = add_cx_list

        if rm_cx_list and len(rm_cx_list) == 1 and ',' in rm_cx_list[0]:
            self.rm_cx_list = rm_cx_list[0].split(',')
        else:
            self.rm_cx_list = rm_cx_list

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.rm_port(sta, check_exists=True)

    def build(self):

        self.station_profile.use_security(self.security,
                                          self.ssid,
                                          self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio,
                                    sta_names_=self.sta_list,
                                    debug=self.debug)
        self.cx_profile.create(endp_type="lf_udp",
                               side_a=self.station_profile.station_names,
                               side_b=self.upstream,
                               sleep_time=0)
        self.add_cx_list = self.cx_profile.get_cx_names()
        self._pass("PASS: Station build finished")

    def do_cx_action(self):
        if self.cx_action == 'start':
            print("Starting %s" % self.tg_profile.group_name)
            self.tg_profile.start_group()
        elif self.cx_action == 'stop':
            print("Stopping %s" % self.tg_profile.group_name)
            self.tg_profile.stop_group()
        elif self.cx_action == 'quiesce':
            print("Quiescing %s" % self.tg_profile.group_name)
            self.tg_profile.quiesce_group()

    def do_tg_action(self):
        if self.tg_action == 'add':
            print("Creating %s" % self.tg_profile.group_name)
            self.tg_profile.create_group()
        if self.tg_action == 'del':
            print("Removing %s" % self.tg_profile.group_name)
            if self.tg_profile.check_group_exists():
                self.tg_profile.rm_group()
            else:
                print("%s not found, no action taken" % self.tg_profile.group_name)

    def show_info(self):
        time.sleep(.5)
        if self.list_groups:
            tg_list = self.tg_profile.list_groups()
            if len(tg_list) > 0:
                print("Current Test Groups: ")
                for group in tg_list:
                    print(group)
            else:
                print("No test groups found")
        if self.show_group:
            cx_list = self.tg_profile.list_cxs()
            if len(cx_list) > 0:
                print("Showing cxs in %s" % self.tg_profile.group_name)
                for cx in cx_list:
                    print(cx)
            else:
                print("No cxs found in %s" % self.tg_profile.group_name)

    def update_cxs(self):
        if len(self.add_cx_list) > 0:
            print("Adding cxs %s to %s" % (', '.join(self.add_cx_list), self.tg_profile.group_name))
            for cx in self.add_cx_list:
                self.tg_profile.add_cx(cx)
                self.tg_profile.cx_list.append(cx)
        if len(self.rm_cx_list) > 0:
            print("Removing cxs %s from %s" % (', '.join(self.rm_cx_list), self.tg_profile.group_name))
            for cx in self.rm_cx_list:
                self.tg_profile.rm_cx(cx)
                if cx in self.tg_profile.cx_list:
                    self.tg_profile.cx_list.remove(cx)


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='testgroup2.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Create stations to test connection and traffic on VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open) and then add them to a test group
            ''',

        description='''\
testgroup2.py:
--------------------
Generic command layout:

python3 ./testgroup2.py
    --upstream_port eth1
    --radio wiphy0
    --num_stations 32
    --security {open|wep|wpa|wpa2|wpa3} \\
    --mode   1
        {"auto"   : "0",
        "a"      : "1",
        "b"      : "2",
        "g"      : "3",
        "abg"    : "4",
        "abgn"   : "5",
        "bgn"    : "6",
        "bg"     : "7",
        "abgnAC" : "8",
        "anAC"   : "9",
        "an"     : "10",
        "bgnAC"  : "11",
        "abgnAX" : "12",
        "bgnAX"  : "13",
    --ssid netgear
    --password admin123
    --a_min 1000
    --b_min 1000
    --ap "00:0e:8e:78:e1:76"
    --group_name group0
    --add_group
    --debug
    
    ./testgroup2.py --num_stations 4 --ssid lanforge --passwd password --security wpa2 --radio wiphy0 --group_name group0 --add_group

            ''')

    required_args = None
    for group in parser._action_groups:
        if group.title == "required arguments":
            required_args = group
            break
    if required_args is not None:
        required_args.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
        required_args.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
        required_args.add_argument('--group_name', help='specify the name of the test group to use', default=None)

    optional_args = None
    for group in parser._action_groups:
        if group.title == "optional arguments":
            optional_args = group
            break
    if optional_args is not None:
        optional_args.add_argument('--mode', help='Used to force mode of stations')
        optional_args.add_argument('--ap', help='Used to force a connection to a particular AP')

    tg_group = parser.add_mutually_exclusive_group()
    tg_group.add_argument('--add_group', help='add new test group', action='store_true', default=False)
    tg_group.add_argument('--del_group', help='delete test group', action='store_true', default=False)
    parser.add_argument('--show_group', help='show connections in current test group', action='store_true',
                        default=False)

    cx_group = parser.add_mutually_exclusive_group()
    cx_group.add_argument('--start_group', help='start all cxs in chosen test group', default=None)
    cx_group.add_argument('--stop_group', help='stop all cxs in chosen test group', default=None)
    cx_group.add_argument('--quiesce_group', help='quiesce all cxs in chosen test groups', default=None)

    parser.add_argument('--add_cx', help='add cx to chosen test group', nargs='*', default=[])
    parser.add_argument('--remove_cx', help='remove cx from chosen test group', nargs='*', default=[])
    args = parser.parse_args()

    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_sta = int(args.num_stations)

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1, padding_number_=10000,
                                          radio=args.radio)

    tg_action = None
    cx_action = None

    if args.add_group:
        tg_action = 'add'
    elif args.del_group:
        tg_action = 'del'

    if args.start_group:
        cx_action = 'start'
    elif args.stop_group:
        cx_action = 'stop'
    elif args.quiesce_group:
        cx_action = 'quiesce'

    ip_var_test = TestGroup2(host=args.mgr,
                             port=args.mgr_port,
                             number_template="0000",
                             sta_list=station_list,
                             name_prefix="VT-",
                             upstream=args.upstream_port,
                             ssid=args.ssid,
                             password=args.passwd,
                             radio=args.radio,
                             security=args.security,
                             use_ht160=False,
                             side_a_min_rate=args.a_min,
                             side_b_min_rate=args.b_min,
                             mode=args.mode,
                             ap=args.ap,
                             group_name=args.group_name,
                             tg_action=tg_action,
                             cx_action=cx_action,
                             _debug_on=args.debug)

    ip_var_test.pre_cleanup()
    ip_var_test.build()
    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        ip_var_test.exit_fail()
    ip_var_test.do_tg_action()
    ip_var_test.update_cxs()
    ip_var_test.do_cx_action()
    time.sleep(5)
    ip_var_test.show_info()
    print('Creates %s stations and connections' % num_sta)


if __name__ == "__main__":
    main()
