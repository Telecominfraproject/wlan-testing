#!/usr/bin/env python3
import sys
import os
import importlib
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
l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")


# Currently, this test can only be applied to UDP connections
class L3PowersaveTraffic(LFCliBase):

    def __init__(self, host, port, ssid, security, password, station_list, side_a_min_rate=56, side_b_min_rate=56,
                 side_a_max_rate=0,
                 side_b_max_rate=0, pdu_size=1000, prefix="00000", test_duration="5m",
                 _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.sta_list = station_list
        self.prefix = prefix
        self.debug = _debug_on
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port, debug_=False)
        # upload
        self.cx_prof_upload = l3_cxprofile.L3CXProfile(self.host, self.port, self.local_realm,
                                                side_a_min_bps=side_a_min_rate, side_b_min_bps=0,
                                                side_a_max_bps=side_a_max_rate, side_b_max_bps=0,
                                                side_a_min_pdu=pdu_size, side_a_max_pdu=pdu_size,
                                                side_b_min_pdu=0, side_b_max_pdu=0, debug_=False)

        # download
        self.cx_prof_download = l3_cxprofile.L3CXProfile(self.host, self.port, self.local_realm,
                                                  side_a_min_bps=0, side_b_min_bps=side_b_min_rate,
                                                  side_a_max_bps=0, side_b_max_bps=side_b_max_rate,
                                                  side_a_min_pdu=0, side_a_max_pdu=0,
                                                  side_b_min_pdu=pdu_size, side_b_max_pdu=pdu_size, debug_=False)
        self.test_duration = test_duration
        self.station_profile = realm.StationProfile(self.lfclient_url, self.local_realm, ssid=self.ssid,
                                                    ssid_pass=self.password,
                                                    security=self.security, number_template_=self.prefix, mode=0,
                                                    up=True,
                                                    dhcp=True,
                                                    debug_=False)
        self.new_monitor = realm.WifiMonitor(self.lfclient_url, self.local_realm, debug_=_debug_on)

    def build(self):
        self.station_profile.use_security("open", ssid=self.ssid, passwd=self.password)
        self.station_profile.set_number_template(self.prefix)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.set_command_flag("add_sta", "power_save_enable", 1)
        # channel = self.json_get("/port/1/%s/%s/"%(1,"wiphy0"))
        # rint("The channel name is...")

        self.new_monitor.create(resource_=1, channel=149, radio_="wiphy1", name_="moni0")
        self.station_profile.create(radio="wiphy0", sta_names_=self.sta_list, debug=False)
        # station_channel = self.json_get("/port/1/%s/%s")
        # pprint.pprint(station_channel)

        self._pass("PASS: Station builds finished")
        self.cx_prof_upload.name_prefix = "UDP_up"
        self.cx_prof_download.name_prefix = "UDP_down"
        print("Creating upload cx profile ")
        self.cx_prof_upload.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b="1.eth1", sleep_time=.05)
        print("Creating download cx profile")
        self.cx_prof_download.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b="1.eth1", sleep_time=.05)

    def __get_rx_values(self):
        cx_list = self.json_get("/endp/list?fields=name,rx+bytes", debug_=False)
        # print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes':
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    def start(self, print_pass=False, print_fail=False):
        # start one test, measure
        # start second test, measure
        cur_time = datetime.datetime.now()
        end_time = self.local_realm.parse_time(self.test_duration) + cur_time
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
        if  self.local_realm.wait_for_ip(self.station_profile.station_names):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            exit(1)
        self.cx_prof_upload.start_cx()
        self.cx_prof_download.start_cx()

        # print station + MAC, AP
        temp = []
        for station in self.station_profile.station_names:
            temp.append(self.local_realm.name_to_eid(station)[2])
        port_info = self.json_get("port/1/1/%s?fields=alias,ap,mac" % ','.join(temp))
        if port_info is not None:
            for item in port_info['interfaces']:
                for k, v in item.items():
                    print("sta_name %s" % v['alias'])
                    print("mac      %s" % v['mac'])
                    print("ap       %s\n" % v['ap'])

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


def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    # station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=4, padding_number_=10000)
    station_list = ["sta0000", "sta0001"]
    ip_powersave_test = L3PowersaveTraffic(lfjson_host, lfjson_port, ssid="jedway-open-149", security="open",
                                           password="[BLANK]", station_list=station_list, side_a_min_rate=2000,
                                           side_b_min_rate=2000, side_a_max_rate=0,
                                           side_b_max_rate=0, prefix="00000", test_duration="30s",
                                           _debug_on=False, _exit_on_error=True, _exit_on_fail=True)
    ip_powersave_test.cleanup()
    ip_powersave_test.build()
    ip_powersave_test.start()
    ip_powersave_test.stop()
    ip_powersave_test.cleanup()


if __name__ == "__main__":
    main()
