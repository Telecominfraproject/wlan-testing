#!/usr/bin/env python3
import sys
import os
import importlib
import time
import datetime
import argparse
from pprint import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")
station_profile = importlib.import_module("py-json.station_profile")
wifi_monitor = importlib.import_module("py-json.wifi_monitor_profile")


# Currently, this test can only be applied to UDP connections
class L3PowersaveTraffic(Realm):

    def __init__(self, host, port, ssid, security, password, station_list, side_a_min_rate=56, side_b_min_rate=56,
                 side_a_max_rate=0,
                 side_b_max_rate=0, pdu_size=1000, prefix="00000", test_duration="5m",
                 station_radio="wiphy0", monitor_radio="wiphy1",
                 _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host=host, lfclient_port=port, debug_=_debug_on)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.sta_list = station_list
        self.prefix = prefix
        self.station_radio = station_radio
        self.monitor_radio = monitor_radio
        self.debug = _debug_on
        # upload
        # self is referring to the Realm which test_l3_powersave_traffic is inheriting.
        self.cx_prof_upload = l3_cxprofile.L3CXProfile(self.host, self.port, local_realm=self,
                                                       side_a_min_bps=side_a_min_rate, side_b_min_bps=0,
                                                       side_a_max_bps=side_a_max_rate, side_b_max_bps=0,
                                                       side_a_min_pdu=pdu_size, side_a_max_pdu=pdu_size,
                                                       side_b_min_pdu=0, side_b_max_pdu=0, debug_=self.debug)

        # download
        self.cx_prof_download = l3_cxprofile.L3CXProfile(self.host, self.port, local_realm=self,
                                                         side_a_min_bps=0, side_b_min_bps=side_b_min_rate,
                                                         side_a_max_bps=0, side_b_max_bps=side_b_max_rate,
                                                         side_a_min_pdu=0, side_a_max_pdu=0,
                                                         side_b_min_pdu=pdu_size, side_b_max_pdu=pdu_size, debug_=self.debug)
        self.test_duration = test_duration
        self.station_profile = station_profile.StationProfile(self.lfclient_url, local_realm=self, ssid=self.ssid,
                                                              ssid_pass=self.password,
                                                              security=self.security, number_template_=self.prefix,
                                                              mode=0,
                                                              up=True,
                                                              dhcp=True,
                                                              debug_=self.debug)
        self.new_monitor = wifi_monitor.WifiMonitor(self.lfclient_url, local_realm=self, debug_=self.debug)

    def build(self):
        self.station_profile.use_security(self.security, ssid=self.ssid, passwd=self.password)
        self.station_profile.set_number_template(self.prefix)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.set_command_flag("add_sta", "power_save_enable", 1)
        # channel = self.json_get("/port/1/%s/%s/"%(1,"wiphy0"))
        # rint("The channel name is...")

        self.new_monitor.create(resource_=1, channel=149, radio_=self.monitor_radio, name_="moni0")
        self.station_profile.create(radio=self.station_radio, sta_names_=self.sta_list)
        # station_channel = self.json_get("/port/1/%s/%s")
        # pprint.pprint(station_channel)

        self._pass("PASS: Station builds finished")
        self.cx_prof_upload.name_prefix = "UDP_up"
        self.cx_prof_download.name_prefix = "UDP_down"
        print("Creating upload cx profile ")
        self.cx_prof_upload.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b="1.eth1",
                                   sleep_time=.05)
        print("Creating download cx profile")
        self.cx_prof_download.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b="1.eth1",
                                     sleep_time=.05)

    def __get_rx_values(self):
        cx_list = self.json_get("/endp/list?fields=name,rx+bytes", debug_=self.debug)
        # print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes':
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    def start(self):
        # start one test, measure
        # start second test, measure
        cur_time = datetime.datetime.now()
        end_time = self.parse_time(self.test_duration) + cur_time
        # admin up on new monitor
        self.new_monitor.admin_up()
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d-%H%M%S")
        curr_mon_name = self.new_monitor.monitor_name
        # ("date and time: ",date_time)
        self.new_monitor.start_sniff("/home/lanforge/Documents/" + curr_mon_name + "-" + date_time + ".pcap")
        # admin up on station

        self.station_profile.admin_up()
        # self.new_monitor.set_flag()
        # print(self.station_profile.station_names)
        if self.wait_for_ip(self.station_profile.station_names):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            exit(1)
        self.cx_prof_upload.start_cx()
        self.cx_prof_download.start_cx()

        # print station + MAC, AP
        temp = []
        for station in self.station_profile.station_names:
            temp.append(self.name_to_eid(station)[2])
        port_info = self.json_get("port/1/1/%s?fields=alias,ap,mac" % ','.join(temp))
        if port_info is not None:
            if 'interfaces' in port_info:
                for item in port_info['interfaces']:
                    for k, v in item.items():
                        print("sta_name %s" % v['alias'])
                        print("mac      %s" % v['mac'])
                        print("ap       %s\n" % v['ap'])
            elif 'interface' in port_info:
                print("sta_name %s" % port_info['interface']['alias'])
                print("mac      %s" % port_info['interface']['mac'])
                print("ap       %s\n" % port_info['interface']['ap'])
            else:
                print('interfaces and interface not in port_mgr_response')
                exit(1)

        while cur_time < end_time:
            # DOUBLE CHECK
            interval_time = cur_time + datetime.timedelta(minutes=1)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                time.sleep(1)

    def stop(self):
        # switch off new monitor
        self.new_monitor.admin_down()
        self.cx_prof_upload.stop_cx()
        self.cx_prof_download.stop_cx()
        self.station_profile.admin_down()

    def cleanup(self):
        self.new_monitor.cleanup()
        self.cx_prof_download.cleanup()
        self.cx_prof_upload.cleanup()
        self.station_profile.cleanup(desired_stations=self.sta_list)
        if self.debug:
            pprint('Current ports: %s' % self.json_get('/ports/'))


def main():
    # Realm.create_basic_argparse defined in lanforge-scripts/py-json/LANforge/lfcli_base.py
    parser = Realm.create_basic_argparse(
        prog='test_l3_powersave_traffic.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        test_l3_powersave_traffic.py

            ''',
        description='''\
Example of creating traffic on an l3 connection
        ''')

    parser.add_argument('--monitor_radio', help="--monitor_radio radio to be used in monitor creation",
                        default="wiphy1")
    args = parser.parse_args()

    lfjson_host = args.mgr
    lfjson_port = 8080
    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=0, padding_number_=10000)
    ip_powersave_test = L3PowersaveTraffic(lfjson_host, lfjson_port, ssid=args.ssid, security=args.security,
                                           password=args.passwd, station_list=station_list, side_a_min_rate=2000,
                                           side_b_min_rate=2000, station_radio=args.radio,
                                           monitor_radio=args.monitor_radio, test_duration="30s", _debug_on=args.debug,
                                           _exit_on_error=True, _exit_on_fail=True)
    ip_powersave_test.cleanup()
    ip_powersave_test.build()
    ip_powersave_test.start()
    ip_powersave_test.stop()
    ip_powersave_test.cleanup()


if __name__ == "__main__":
    main()
