#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import time
import datetime

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class VRTest(LFCliBase):
    def __init__(self, host, port, ssid, security, password, sta_list, name_prefix, upstream, radio,
                 side_a_min_rate=56, side_a_max_rate=0,
                 side_b_min_rate=56, side_b_max_rate=0,
                 upstream_subnets="20.20.20.0/24", upstream_nexthop="20.20.20.1",
                 local_subnets="10.40.0.0/24", local_nexthop="10.40.3.198",
                 rdd_ip="20.20.20.20", rdd_gateway="20.20.20.1", rdd_netmask="255.255.255.0",
                 number_template="00000", test_duration="5m", use_ht160=False, vr_name="vr_test",
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port, debug_=_debug_on)
        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.vr_profile = self.local_realm.new_vr_profile()

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.use_ht160 = use_ht160
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9

        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        self.vr_profile.vr_name = vr_name
        self.upstream_subnets = upstream_subnets
        self.upstream_nexthop = upstream_nexthop
        self.local_subnets = local_subnets
        self.local_nexthop = local_nexthop
        self.rdd_ip = rdd_ip
        self.rdd_gateway = rdd_gateway
        self.rdd_netmask = rdd_netmask

    def __get_rx_values(self):
        cx_list = self.json_get("endp?fields=name,rx+bytes", debug_=self.debug)
        # print(self.cx_profile.created_cx.values())
        # print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes' and item in self.cx_profile.created_cx.values():
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    @staticmethod
    def __compare_vals(old_list, new_list):
        passes = 0
        expected_passes = 0
        if len(old_list) == len(new_list):
            for item, value in old_list.items():
                expected_passes += 1
                if new_list[item] > old_list[item]:
                    passes += 1
                # print(item, new_list[item], old_list[item], passes, expected_passes)

            if passes == expected_passes:
                return True
            else:
                return False
        else:
            return False

    def start(self, print_pass=False, print_fail=False):
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        temp_stas.append(self.upstream)
        if self.local_realm.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        cur_time = datetime.datetime.now()
        old_cx_rx_values = self.__get_rx_values()
        end_time = self.local_realm.parse_time(self.test_duration) + cur_time
        self.cx_profile.start_cx()
        passes = 0
        expected_passes = 0
        while cur_time < end_time:
            interval_time = cur_time + datetime.timedelta(minutes=1)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                time.sleep(1)

            new_cx_rx_values = self.__get_rx_values()
            # print(old_cx_rx_values, new_cx_rx_values)
            # print("\n-----------------------------------")
            # print(cur_time, end_time, cur_time + datetime.timedelta(minutes=1))
            # print("-----------------------------------\n")
            expected_passes += 1
            if self.__compare_vals(old_cx_rx_values, new_cx_rx_values):
                passes += 1
            else:
                self._fail("FAIL: Not all stations increased traffic", print_fail)
                break
            old_cx_rx_values = new_cx_rx_values
            cur_time = datetime.datetime.now()

        if passes == expected_passes:
            self._pass("PASS: All tests passed", print_pass)

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.local_realm.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        upstream_temp = self.local_realm.name_to_eid(self.upstream)
        print("Creating Virtual Router and connections")
        self.vr_profile.create(resource=upstream_temp[1], upstream_port=upstream_temp[2], debug=self.debug,
                               upstream_subnets=self.upstream_subnets, upstream_nexthop=self.upstream_nexthop,
                               local_subnets=self.local_subnets, local_nexthop=self.local_nexthop,
                               rdd_ip=self.rdd_ip, rdd_gateway=self.rdd_gateway, rdd_netmask=self.rdd_netmask,
                               suppress_related_commands_=True)
        print("Creating stations")
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)
        self._pass("PASS: Station build finished")
        exit(1)


def main():
    lfjson_port = 8080

    parser = LFCliBase.create_basic_argparse(
        prog='test_l3_WAN_LAN.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Useful Information:
            1. TBD
            ''',

        description='''\
test_l3_WAN_LAN.py:
--------------------
TBD
        ''')

    parser.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
    parser.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="5m")
    parser.add_argument('--upstream_subnets', help='--upstream_subnets sets the subnets used by the upstream vrcx',
                        default="20.20.20.0/24")
    parser.add_argument('--upstream_nexthop',
                        help='--upstream_nexthop sets the nexthop used by the upstream vrcx, should be rdd gateway',
                        default="20.20.20.1")
    parser.add_argument('--local_subnets', help='--local_subnets sets the subnets used by the rdd vrcx',
                        default="10.40.0.0/24")
    parser.add_argument('--local_nexthop',
                        help='--local_nexthop sets the nexthop used by the upstream vrcx, should be upstream ip',
                        default="10.40.3.198")
    parser.add_argument('--rdd_ip', help='--rdd_ip sets the ip to be used by the rdd', default="20.20.20.20")
    parser.add_argument('--rdd_gateway', help='--rdd_gateway sets the gateway to be used by the rdd',
                        default="20.20.20.1")
    parser.add_argument('--rdd_netmask', help='--rdd_netmask sets the netmask to be used by the rdd',
                        default="255.255.255.0")
    parser.add_argument('--vr_name', help='--vr_name sets the name to be used by the virtual router', default="vr_test")

    args = parser.parse_args()
    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1, padding_number_=10000,
                                          radio=args.radio)

    ip_var_test = VRTest(args.mgr, lfjson_port, number_template="00", sta_list=station_list,
                         name_prefix="VRT",
                         upstream=args.upstream_port,
                         ssid=args.ssid,
                         password=args.passwd,
                         radio=args.radio,
                         security=args.security, test_duration=args.test_duration, use_ht160=False,
                         side_a_min_rate=args.a_min, side_b_min_rate=args.b_min, _debug_on=args.debug,
                         upstream_subnets=args.upstream_subnets, upstream_nexthop=args.upstream_nexthop,
                         local_subnets=args.local_subnets, local_nexthop=args.local_nexthop,
                         rdd_ip=args.rdd_ip, rdd_gateway=args.rdd_gateway,
                         rdd_netmask=args.rdd_netmask, vr_name=args.vr_name)

    ip_var_test.pre_cleanup()
    ip_var_test.build()
    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        exit(1)
    ip_var_test.start(False, False)
    ip_var_test.stop()
    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        exit(1)
    time.sleep(30)
    ip_var_test.cleanup()
    if ip_var_test.passes():
        print("Full test passed, all connections increased rx bytes")


if __name__ == "__main__":
    main()
