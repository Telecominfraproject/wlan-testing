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

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class IPV4VariableTime(Realm):
    def __init__(self, ssid, security, password, sta_list, name_prefix, upstream, radio,
                 radio2, host="localhost", port=8080,
                 side_a_min_rate=56, side_a_max_rate=0,
                 side_b_min_rate=56, side_b_max_rate=0,
                 number_template="00000", test_duration="5m", use_ht160=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=host, lfclient_port=port)
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.radio2 = radio2
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l3_cx_profile()
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = "vap0000"
        self.monitor = self.new_wifi_monitor_profile(debug_=_debug_on)

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

    def __get_rx_values(self):
        cx_list = self.json_get("endp?fields=name,rx+bytes", debug_=self.debug)
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
            if passes == expected_passes:
                return True
            else:
                return False
        else:
            return False

    def build(self):

        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)

        self.vap_profile.set_command_flag("add_vap", "use-bss-load", 1)
        self.vap_profile.set_command_flag("add_vap", "use-bss-transition", 1)
        self.vap_profile.create(resource=1, radio="wiphy1", channel=161, up_=True, debug=self.debug,
                                suppress_related_commands_=True)
        self.monitor.create(resource_=1, channel=161, radio_=self.radio2, name_="moni0")
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)
        self._pass("PASS: Station build finished")

    def start(self, print_pass=False, print_fail=False):
        self.station_profile.admin_up()
        self.vap_profile.admin_up(1)
        temp_stas = self.station_profile.station_names.copy()
        temp_stas.append(self.upstream)
        if self.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        cur_time = datetime.datetime.now()
        old_cx_rx_values = self.__get_rx_values()
        end_time = self.parse_time(self.test_duration) + cur_time
        self.cx_profile.start_cx()
        passes = 0
        expected_passes = 0
        curr_mon_name = self.monitor.monitor_name
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d-%H%M%S")
        self.monitor.start_sniff("/home/lanforge/Documents/" + curr_mon_name + "-" + date_time + ".pcap")

        while cur_time < end_time:
            interval_time = cur_time + datetime.timedelta(minutes=1)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                time.sleep(1)

            new_cx_rx_values = self.__get_rx_values()
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
        self.vap_profile.admin_down(1)

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.rm_port(sta, check_exists=True, debug_=self.debug)

    def cleanup(self):
        self.cx_profile.cleanup()
        self.station_profile.cleanup()
        self.vap_profile.cleanup(1)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)


def main():
    parser = Realm.create_basic_argparse(
        prog='test_ipv4_variable_time.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        description='''\
test_ipv4_variable_time.py:
---------------------

Generic command layout:
./test_ipv4_variable_time.py
--upstream_port eth1
--radio wiphy3
--num_stations 4
--ssid jedway-wpa2-x2048-4-1
--passwd jedway-wpa2-x2048-4-1
--security  {wpa2|open|wpa|wpa3}
--a_min 250000
--b_min 260000
--test_duration 2m
--debug
        ''')
    optional = None
    for agroup in parser._action_groups:
        if agroup.title == "optional arguments":
            optional = agroup
    if optional is not None:
        optional.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
        optional.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
        optional.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="5m")
        optional.add_argument('--radio2', help='radio to create monitor on', default='1.wiphy2')

    args = parser.parse_args()
    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1, padding_number_=10000,
                                          radio=args.radio)

    ip_var_test = IPV4VariableTime(host=args.mgr, port=args.mgr_port,
                                   number_template="00",
                                   sta_list=station_list,
                                   name_prefix="VT",
                                   upstream=args.upstream_port,
                                   ssid=args.ssid,
                                   password=args.passwd,
                                   radio=args.radio,
                                   radio2=args.radio2,
                                   security=args.security, test_duration=args.test_duration, use_ht160=False,
                                   side_a_min_rate=args.a_min, side_b_min_rate=args.b_min, _debug_on=args.debug)

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
