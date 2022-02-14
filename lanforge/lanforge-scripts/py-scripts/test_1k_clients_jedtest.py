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
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class Test1KClients(LFCliBase):
    def __init__(self,
                 upstream,
                 host="localhost",
                 port=8080,
                 side_a_min_rate=0, side_a_max_rate=56000,
                 side_b_min_rate=0, side_b_max_rate=56000,
                 num_sta_=200,
                 test_duration="2d",
                 _debug_on=True,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host,
                         port,
                         _debug=_debug_on,
                         _local_realm=Realm(lfclient_host=host, lfclient_port=port),
                         _exit_on_fail=_exit_on_fail)
        self.ssid_radio_map = {
            '1.1.wiphy0': ("wpa2", "jedway-wpa2-x2048-4-4", "jedway-wpa2-x2048-4-4"),
            '1.1.wiphy1': ("wpa2", "jedway-wpa2-x2048-5-1", "jedway-wpa2-x2048-5-1"),
            '1.1.wiphy2': ("wpa2", "jedway-wpa2-x2048-4-1", "jedway-wpa2-x2048-4-1"),

            '1.2.wiphy0': ("wpa2", "jedway-wpa2-x2048-5-3", "jedway-wpa2-x2048-5-3"),
            '1.2.wiphy1': ("wpa2", "jedway-wpa2-x2048-4-4", "jedway-wpa2-x2048-4-4"),
            '1.2.wiphy2': ("wpa2", "jedway-wpa2-x2048-4-1", "jedway-wpa2-x2048-4-1"),
        }
        if num_sta_ is None:
            raise ValueError("need a number of stations per radio")
        self.num_sta = int(num_sta_)
        self.station_radio_map = {
            # port_name_series(prefix=prefix_, start_id=start_id_, end_id=end_id_, padding_number=padding_number_, radio=radio)
            "1.1.wiphy0": LFUtils.port_name_series(start_id=0, end_id=self.num_sta - 1, padding_number=10000,
                                                   radio="1.1.wiphy0"),
            "1.1.wiphy1": LFUtils.port_name_series(start_id=1000, end_id=1000 + self.num_sta - 1, padding_number=10000,
                                                   radio="1.1.wiphy1"),
            "1.1.wiphy2": LFUtils.port_name_series(start_id=2000, end_id=2000 + self.num_sta - 1, padding_number=10000,
                                                   radio="1.1.wiphy2"),

            "1.2.wiphy0": LFUtils.port_name_series(start_id=3000, end_id=3000 + self.num_sta - 1, padding_number=10000,
                                                   radio="1.2.wiphy0"),
            "1.2.wiphy1": LFUtils.port_name_series(start_id=4000, end_id=4000 + self.num_sta - 1, padding_number=10000,
                                                   radio="1.2.wiphy1"),
            "1.2.wiphy2": LFUtils.port_name_series(start_id=5000, end_id=5000 + self.num_sta - 1, padding_number=10000,
                                                   radio="1.2.wiphy2")
        }
        self.test_duration = test_duration
        self.upstream = upstream
        self.name_prefix = "1k"
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        self.station_profile_map = {}
        # change resource admin_up rate
        self.local_realm.json_post("/cli-json/set_resource", {
            "shelf": 1,
            "resource": all,
            "max_staged_bringup": 30,
            "max_trying_ifup": 15,
            "max_station_bringup": 6
        })

    def build(self):
        for (radio, name_series) in self.station_radio_map.items():
            print("building stations for %s" % radio)
            if (name_series is None) or len(name_series) < 1:
                print("No name series for %s" % radio)
                continue
            station_profile = self.local_realm.new_station_profile()
            station_profile.use_security(self.ssid_radio_map[radio][0],
                                         self.ssid_radio_map[radio][1],
                                         self.ssid_radio_map[radio][2])
            self.station_profile_map[radio] = station_profile

        self._pass("defined %s station profiles" % len(self.station_radio_map))
        for (radio, station_profile) in self.station_profile_map.items():
            station_profile.create(radio=radio,
                                   sta_names_=self.station_radio_map[radio],
                                   dry_run=False,
                                   up_=False,
                                   debug=self.debug,
                                   suppress_related_commands_=True,
                                   use_radius=False,
                                   hs20_enable=False,
                                   sleep_time=.02)
            station_profile.set_command_param("set_port", "report_timer", 1500)
            station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.cx_profile.create(endp_type="lf_udp", side_a=station_profile.station_names, side_b=self.upstream,
                                   sleep_time=0)

        self._pass("built stations on %s radios" % len(self.station_radio_map))

    def __get_rx_values(self):
        cx_list = self.json_get("endp?fields=name,rx+bytes", debug_=self.debug)
        if self.debug:
            print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes' and item in self.cx_profile.created_cx.values():
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    def __compare_vals(self, old_list, new_list):
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

    def start(self):
        print("Bringing stations up...")
        prev_ip_num = 0
        for (radio, station_profile) in self.station_profile_map.items():
            station_profile.admin_up()
            total_num_sta = 6 * self.num_sta
            self.local_realm.wait_for_ip(station_list=self.station_radio_map[radio], debug=self.debug, timeout_sec=30)
            curr_ip_num = self.local_realm.get_curr_num_ips(num_sta_with_ips=prev_ip_num,
                                                            station_list=self.station_radio_map[radio],
                                                            debug=self.debug)
            while (prev_ip_num < curr_ip_num) and (curr_ip_num < total_num_sta):
                self.local_realm.wait_for_ip(station_list=self.station_radio_map[radio], debug=self.debug,
                                             timeout_sec=90)
                prev_ip_num = curr_ip_num
                curr_ip_num = self.local_realm.get_curr_num_ips(num_sta_with_ips=prev_ip_num,
                                                                station_list=self.station_radio_map[radio],
                                                                debug=self.debug)
        if curr_ip_num == total_num_sta:
            self._pass("stations on radio %s up" % radio)
        else:
            self._fail("FAIL: Not all stations on radio %s up" % radio)
            self.exit_fail()

        old_cx_rx_values = self.__get_rx_values()
        self.cx_profile.start_cx()

        passes = 0
        expected_passes = 0
        curr_time = datetime.datetime.now()
        end_time = self.local_realm.parse_time(self.test_duration) + curr_time
        sleep_interval = self.local_realm.parse_time(self.test_duration) // 3

        while curr_time < end_time:

            time.sleep(sleep_interval.total_seconds())

            new_cx_rx_values = self.__get_rx_values()
            if self.debug:
                print(old_cx_rx_values, new_cx_rx_values)
                print("\n-----------------------------------")
                print(curr_time, end_time)
                print("-----------------------------------\n")
            expected_passes += 1
            if self.__compare_vals(old_cx_rx_values, new_cx_rx_values):
                passes += 1
            else:
                self._fail("FAIL: Not all stations increased traffic")
                self.exit_fail()

            old_cx_rx_values = new_cx_rx_values
            curr_time = datetime.datetime.now()

        if passes == expected_passes:
            self._pass("PASS: All tests passed")

    def stop(self):
        self.cx_profile.stop_cx()

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        for (radio, name_series) in self.station_radio_map.items():
            sta_list = self.station_radio_map[radio]
            for sta in sta_list:
                self.local_realm.rm_port(sta, check_exists=True)

    def post_cleanup(self):
        self.cx_profile.cleanup()
        for (radio, name_series) in self.station_radio_map.items():
            sta_list = self.station_radio_map[radio]
            for sta in sta_list:
                self.local_realm.rm_port(sta, check_exists=True)


def main():
    parser = LFCliBase.create_bare_argparse(prog=__file__,
                                            formatter_class=argparse.RawTextHelpFormatter,
                                            epilog='''\
           creates lots of stations across multiple radios.
            ''',
                                            description='''\
        test_1k_clients_jedtest.py:
        --------------------
        Generic command layout:
        python3 ./test_1k_clients_jedtest.py 
            --mgr localhost
            --mgr_port 8080
            --sta_per_radio 300
            --test_duration 3m
            --a_min 1000
            --b_min 1000
            --a_max 0
            --b_max 0
            --debug        '''
                                            )

    required_args = None
    for group in parser._action_groups:
        if group.title == "required arguments":
            required_args = group
            break

    if required_args is not None:
        required_args.add_argument("--sta_per_radio", type=int, help="number of stations per radio")

    optional_args = None
    for group in parser._action_groups:
        if group.title == "optional arguments":
            optional_args = group
            break
    if optional_args is not None:
        optional_args.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=0)
        optional_args.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=0)
        optional_args.add_argument('--a_max', help='--a_min bps rate minimum for side_a', default=256000)
        optional_args.add_argument('--b_max', help='--b_min bps rate minimum for side_b', default=256000)
        optional_args.add_argument('--test_duration', help='--test_duration sets the duration of the test',
                                   default="2m")
        optional_args.add_argument('-u', '--upstream_port',
                                   help='non-station port that generates traffic: <resource>.<port>, e.g: 1.eth1',
                                   default='1.eth1')

    args = parser.parse_args()

    kilo_test = Test1KClients(host=args.mgr,
                              port=args.mgr_port,
                              upstream=args.upstream_port,
                              num_sta_=args.sta_per_radio,
                              side_a_max_rate=args.a_max,
                              side_a_min_rate=args.a_min,
                              side_b_max_rate=args.b_max,
                              side_b_min_rate=args.b_min,
                              _debug_on=args.debug)

    kilo_test.pre_cleanup()
    kilo_test.build()
    if not kilo_test.passes():
        kilo_test.exit_failed()
    kilo_test.start()
    if not kilo_test.passes():
        kilo_test.exit_failed()
    kilo_test.stop()
    if not kilo_test.passes():
        kilo_test.exit_failed()
    time.sleep(60)
    kilo_test.post_cleanup()
    kilo_test.exit_success()


if __name__ == "__main__":
    main()
