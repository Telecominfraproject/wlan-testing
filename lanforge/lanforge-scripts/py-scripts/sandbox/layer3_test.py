#!/usr/bin/env python3

# script moved to sandbox 11/11/2021 - needs updates

import sys
import os
import importlib
import argparse
import datetime
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class Layer3Test(Realm):

    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio="wiphy1", sta_prefix="sta", start_id=0, num_sta=2,
                 dut_ssid="lexusdut", dut_security="open", dut_passwd="[BLANK]", upstream="1.1.eth1", name_prefix="L3Test",
                 traffic_type="lf_udp",
                 side_a_min_rate=256000, side_a_max_rate=0,
                 side_b_min_rate=256000, side_b_max_rate=0,
                 session_id="Layer3Test", duration="1m",
                 _debug_on=False, _exit_on_error=False,  _exit_on_fail=False):
        super().__init__(lfclient_host=lfclient_host, lfclient_port=lfclient_port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        self.radio = radio
        self.upstream = upstream
        self.monitor_interval = 1
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.test_duration = duration
        self.num_sta = num_sta
        self.name_prefix = name_prefix
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.session_id = session_id
        self.traffic_type = traffic_type
        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l3_cx_profile()

        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        print("Test is Initialized")


    def precleanup(self):
        print("precleanup started")
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                   end_id_=self.num_sta - 1, padding_number_=10000, radio=self.radio)
        self.cx_profile.cleanup_prefix()
        for sta in self.station_list:
            self.rm_port(sta, check_exists=True)
            time.sleep(1)
        self.cx_profile.cleanup()

        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)
        print("precleanup done")
        pass

    def build(self):
        print("Building Test Configuration")
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template("00")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_list, debug=self.debug)
        self.wait_until_ports_appear(sta_list=self.station_list)
        self.cx_profile.create(endp_type=self.traffic_type, side_a=self.station_profile.station_names,
                               side_b=self.upstream, sleep_time=0)
        print("Test Build done")
        pass

    def start(self, print_pass=False, print_fail=False):
        print("Test is starting")
        self.cx_names =[]
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        temp_stas.append(self.upstream)
        if self.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        self.cx_profile.start_cx()
        try:
            for i in self.cx_profile.get_cx_names():
                self.cx_names.append(i)
                while self.json_get("/cx/" + i).get(i).get('state') != 'Run':
                    continue
        except Exception as e:
            pass
        print("Test Started")
        self.cur_time = datetime.datetime.now()
        self.end_time = self.parse_time(self.test_duration) + self.cur_time
        print(self.end_time-self.cur_time)
        self.start_monitor()
        pass

    def my_monitor(self):
        print("Monitoring Test")
        print(self.end_time - datetime.datetime.now())
        if (datetime.datetime.now() > self.end_time):
            self.stop_monitor()
        for i in self.cx_names:
            self.add_event(message= self.cx_profile.get_cx_report()[i]['bps rx b'], name=self.session_id)
        return self.cx_profile.get_cx_report()

    def stop(self):
        print("Stopping Test")
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()
        pass

    def postcleanup(self):
        self.cx_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)
        print("Test Completed")
        pass

def main():
    # Realm.create_basic_argparse defined in 
    # /py-json/LANforge/lfcli_base.py  
    # args --mgr --mgr_port --upstream_port --num_stations --test_id 
    # --debug --proxy --debugging --debug_log
    # --radio --security --ssid --passwd
    parser = Realm.create_basic_argparse(
        prog="layer3_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="About This Script")

    # Adding More Arguments for custom use
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="1m")
    parser.add_argument('--session_id', help='--session_id is for websocket', default="local")
    parser.add_argument('--num_client', type=int, help='--num_sta is number of stations you want to create', default=2)
    parser.add_argument('--side_a_min_speed', help='--speed you want to monitor traffic with (max is 10G)', default="0M")
    parser.add_argument('--side_b_min_speed', help='--speed you want to monitor traffic with (max is 10G)', default="10M")
    parser.add_argument('--traffic_type', help='--traffic_type is used for traffic type (lf_udp, lf_tcp)', default="lf_udp")
    args = parser.parse_args()
    print(args)

    # Start Test
    obj = Layer3Test(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                     duration=args.test_duration, session_id=args.session_id,
                     traffic_type=args.traffic_type,
                     upstream=args.upstream_port,
                     dut_ssid=args.ssid, dut_passwd=args.passwd, dut_security=args.security, num_sta=args.num_client,
                     side_a_min_rate=args.side_a_min_speed, side_b_min_rate=args.side_b_min_speed, radio=args.radio,_debug_on=args.debug)
    obj.precleanup()
    obj.build()
    obj.start()
    obj.monitor()
    obj.stop()
    obj.postcleanup()

if __name__ == '__main__':
    main()
