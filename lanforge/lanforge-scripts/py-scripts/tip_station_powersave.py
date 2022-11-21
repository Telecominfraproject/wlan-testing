#!/usr/bin/env python3
import sys
import os
import importlib
import pprint
import time
import datetime
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

'''
This script uses filters from realm's PacketFilter class to filter pcap output for specific packets.
Currently it uses a filter for association packets using wlan.fc.type_subtype<=3. It is also using a filter
for QOS Null packets using wlan.fc.type_subtype==44. Both filters are also looking for the existence of 
either the station MAC or the AP MAC in wlan.addr
These are returned as an array of lines from the output in the format
$subtype $mac_addresses $wlan.fc.pwrmgt
'''
#Currently, this test can only be applied to UDP connections


class TIPStationPowersave(LFCliBase):
    def __init__(self, host, port,
                 ssid=None,
                 security="open",
                 password="[BLANK]",
                 resource_=1,
                 channel_=0,
                 normal_station_list_=None,
                 normal_station_radio_=None,
                 powersave_station_list_=None,
                 powersave_station_radio_=None,
                 monitor_name_=None,
                 monitor_radio_=None,
                 side_a_min_rate_=56000,
                 side_b_min_rate_=56000,
                 side_a_max_rate_=0,
                 side_b_max_rate_=0,
                 pdu_size_=1000,
                 traffic_duration_="5s",
                 pause_duration_="2s",
                 debug_on_=False,
                 exit_on_error_=False,
                 exit_on_fail_=False):
        super().__init__(host, port, _debug=debug_on_, _exit_on_fail=exit_on_fail_)
        self.resource = resource_
        if (channel_ == 0):
            raise ValueError("Please set your radio channel")
        self.channel = channel_
        self.monitor_name = monitor_name_
        self.monitor_radio = monitor_radio_
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.normal_sta_list = normal_station_list_
        self.normal_sta_radio = normal_station_radio_
        self.powersave_sta_list = powersave_station_list_
        self.powersave_sta_radio = powersave_station_radio_
        self.sta_mac_map = {}
        self.debug = debug_on_
        self.packet_filter = realm.PacketFilter()
        self.local_realm = realm.Realm(lfclient_host=self.host,
                                       lfclient_port=self.port,
                                       debug_=self.debug)

        # background traffic
        self.cx_prof_bg = self.local_realm.new_l3_cx_profile()
        self.cx_prof_bg.side_a_min_bps = side_a_min_rate_
        self.cx_prof_bg.side_b_min_bps = side_a_min_rate_
        self.cx_prof_bg.side_a_max_bps = side_a_max_rate_
        self.cx_prof_bg.side_b_max_bps = side_a_min_rate_

        #upload
        self.cx_prof_upload = self.local_realm.new_l3_cx_profile()
        self.cx_prof_upload.side_a_min_bps = side_a_min_rate_
        self.cx_prof_upload.side_b_min_bps = 0
        self.cx_prof_upload.side_a_max_bps = side_a_max_rate_
        self.cx_prof_upload.side_b_max_bps = 0

        self.cx_prof_upload.side_a_min_pdu = pdu_size_
        self.cx_prof_upload.side_a_max_pdu = 0
        self.cx_prof_upload.side_b_min_pdu = pdu_size_
        self.cx_prof_upload.side_b_max_pdu = 0,

        #download
        self.cx_prof_download = self.local_realm.new_l3_cx_profile()
        self.cx_prof_download.side_a_min_bps = 0
        self.cx_prof_download.side_b_min_bps = side_b_min_rate_
        self.cx_prof_download.side_a_max_bps = 0
        self.cx_prof_download.side_b_max_bps = side_b_max_rate_

        self.cx_prof_download.side_a_min_pdu = pdu_size_
        self.cx_prof_download.side_a_max_pdu = 0
        self.cx_prof_download.side_b_min_pdu = pdu_size_
        self.cx_prof_download.side_b_max_pdu = 0

        self.pcap_file = None
        self.test_duration = traffic_duration_
        if isinstance(self.test_duration, int):
            self.test_duration = "%s"%traffic_duration_
        if isinstance(self.test_duration, str):
            self.test_duration = self.local_realm.parse_time(self.test_duration)

        self.pause_duration = pause_duration_
        if isinstance(self.pause_duration, int):
            self.pause_duration = "%s"%pause_duration_
        if isinstance(self.pause_duration, str):
            self.pause_duration = self.local_realm.parse_time(self.pause_duration)

        self.sta_powersave_enabled_profile = self.local_realm.new_station_profile()
        self.sta_powersave_disabled_profile = self.local_realm.new_station_profile()
        self.wifi_monitor_profile = self.local_realm.new_wifi_monitor_profile()

        self.pcap_save_path = "/home/lanforge/lf_reports"

    def build(self):
        self.sta_powersave_disabled_profile.use_security("open", ssid=self.ssid, passwd=self.password)
        self.sta_powersave_disabled_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.sta_powersave_disabled_profile.set_command_param("set_port", "report_timer", 5000)
        self.sta_powersave_disabled_profile.set_command_flag("set_port", "rpt_timer", 1)

        self.sta_powersave_enabled_profile.use_security("open", ssid=self.ssid, passwd=self.password)
        self.sta_powersave_enabled_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.sta_powersave_enabled_profile.set_command_param("set_port", "report_timer", 5000)
        self.sta_powersave_enabled_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.sta_powersave_enabled_profile.set_command_flag("add_sta", "power_save_enable", 1)

        self.wifi_monitor_profile.create(resource_=self.resource,
                                         channel=self.channel,
                                         radio_=self.monitor_radio,
                                         name_=self.monitor_name)

        LFUtils.wait_until_ports_appear(base_url=self.local_realm.lfclient_url,
                                        port_list=[self.monitor_name],
                                        debug=self.debug)
        time.sleep(0.2)
        mon_j = self.json_get("/port/1/%s/%s"%(self.resource, self.monitor_name))
        if ("interface" not in mon_j):
            raise ValueError("No monitor found")

        self.sta_powersave_disabled_profile.create(radio=self.normal_sta_radio,
                                                   sta_names_=self.normal_sta_list,
                                                   debug=self.debug,
                                                   suppress_related_commands_=True)

        self.sta_powersave_enabled_profile.create(radio=self.powersave_sta_radio,
                                                  sta_names_=self.powersave_sta_list,
                                                  debug=self.debug,
                                                  suppress_related_commands_=True)
        temp_sta_map = {}
        for name in  self.powersave_sta_list + self.normal_sta_list:
                temp_sta_map[name]=1
        print("Stations we want:")
        pprint.pprint(temp_sta_map)
        if len(temp_sta_map) < 1:
            self._fail("Misconfigured build(), bye", print_=True)
            exit(1)
        self.local_realm.wait_until_ports_appear(temp_sta_map.keys(), debug=self.debug)

        if len(temp_sta_map) == (len(self.sta_powersave_disabled_profile.station_names) + len(self.sta_powersave_enabled_profile.station_names)):
            self._pass("Stations created", print_=True)
        else:
            print("Stations we see created:")
            pprint.pprint(temp_sta_map)
            self._fail("Not all stations created", print_=True)

        bg_side_a_eids = []
        for port in self.normal_sta_list:
            bg_side_a_eids.append( "%s.%s"%(self.resource, port))

        ul_side_a_eids = []
        for port in self.normal_sta_list:
            ul_side_a_eids.append( "%s.%s"%(self.resource, port))

        dl_side_a_eids = []
        for port in self.normal_sta_list:
            dl_side_a_eids.append( "%s.%s"%(self.resource, port))

        print("Creating background cx profile ")
        self.cx_prof_bg.name_prefix= "udp_bg"
        self.cx_prof_bg.create(endp_type="lf_udp",
                               side_a=bg_side_a_eids,
                               side_b="1.eth1")

        print("Creating upload cx profile ")
        self.cx_prof_upload.name_prefix = "udp_up"
        self.cx_prof_upload.create(endp_type="lf_udp",
                                   side_a=ul_side_a_eids,
                                   side_b="1.eth1")

        print("Creating download cx profile")
        self.cx_prof_download.name_prefix = "udp_down"
        self.cx_prof_download.create(endp_type="lf_udp",
                                     side_a=ul_side_a_eids,
                                     side_b="1.eth1")

        print("Collecting lanforge eth0 IP...")
        eth0_resp = self.json_get("/port/1/%s/eth0?fields=port,alias,ip"%self.resource, debug_=self.debug)
        # would be nice to have a not_found() kind of method
        if (eth0_resp is None) or ("items" in eth0_resp) or ("empty" in eth0_resp) or ("interface" not in eth0_resp):
            self._fail("Unable to query %s.eth0"%self.resource, print_=True)
            exit(1)
        self.eth0_ip = eth0_resp["interface"]["ip"]
        if self.eth0_ip == "0.0.0.0":
            self._fail("eth0 is misconfigured or not our management port", print_=True)
            exit(1)

        self.sta_mac_map = {}


    def __get_rx_values(self):
        cx_list = self.json_get("/endp/list?fields=name,rx+bytes", debug_=False)
        #print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes':
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    def start(self, print_pass=False, print_fail=False):
        """
        This method is intended to start the monitor, the normal station (without powersave),
        and the remaining power save stations. The powersave stations will transmit for tx duration,
        pause, then the AP will pass along upstream traffic. This upstream traffic (download) should
        express a beacon before actually delivering a buffer full of traffic in order to alert the
        station it should wake up for incomming traffic.
        :param print_pass:
        :param print_fail:
        :return:
        """

        #admin up on new monitor
        self.wifi_monitor_profile.admin_up()
        now = datetime.datetime.now()
        test_start = time.time()
        date_time = now.strftime("%Y-%m-%d-%H%M%S")
        curr_mon_name = self.wifi_monitor_profile.monitor_name
        self.pcap_file = "%s/%s-%s.pcap"%(self.pcap_save_path, curr_mon_name, date_time)

        capture_duration = 60 + 4 * (self.test_duration.total_seconds() + self.pause_duration.total_seconds() + 4)
        self.wifi_monitor_profile.start_sniff(self.pcap_file, capture_duration)
        time.sleep(0.05)

        self.sta_powersave_disabled_profile.admin_up()
        self.sta_powersave_enabled_profile.admin_up()

        LFUtils.wait_until_ports_admin_up(base_url=self.local_realm.lfclient_url,
                                          port_list=self.sta_powersave_disabled_profile.station_names + self.sta_powersave_enabled_profile.station_names,
                                          debug=self.debug)
        self.local_realm.wait_for_ip(station_list=self.sta_powersave_disabled_profile.station_names + self.sta_powersave_enabled_profile.station_names)
        time.sleep(2)
        # collect BSSID of AP so we can tshark on it
        temp_stas = []
        for sta in self.sta_powersave_disabled_profile.station_names:
            temp_stas.append(self.local_realm.name_to_eid(sta)[2])
        for sta in self.sta_powersave_enabled_profile.station_names:
            temp_stas.append(self.local_realm.name_to_eid(sta)[2])
        uri = "/port/1/%s/%s?fields=alias,ip,mac,ap"%(
            self.resource,
            ",".join(temp_stas)
        )
        port_info_r = self.json_get(uri)
        # print("="*10, uri, port_info_r, "="*10)
        if (port_info_r is None) or ("empty" in port_info_r):
            self._fail("unable to query for mac addresses", print_=True)
            exit(1)
        self.sta_mac_map = LFUtils.portListToAliasMap(port_info_r)

        self.cx_prof_bg.start_cx()
        print("Upload starts at: %d"%time.time())
        self.cx_prof_upload.start_cx()

        time.sleep(self.test_duration.total_seconds())
        self.cx_prof_upload.stop_cx()
        print("Upload ends at: %d"%time.time())
        time.sleep(float(self.pause_duration.total_seconds()))
        # here is where we should sleep long enough for station to go to sleep
        print("Download begins at: %d"%time.time())
        self.cx_prof_download.start_cx()
        time.sleep(float(self.test_duration.total_seconds()))
        self.cx_prof_download.stop_cx()
        print("Download ends at: %d"%time.time())
        print(" %d " % (time.time() - test_start))


    def stop(self):
        #switch off new monitor
        self.wifi_monitor_profile.admin_down()
        self.cx_prof_bg.stop_cx()
        self.cx_prof_download.stop_cx()
        self.cx_prof_upload.stop_cx()
        self.sta_powersave_enabled_profile.admin_down()
        self.sta_powersave_disabled_profile.admin_down()

        # check for that pcap file
        if self.pcap_file is None:
            self._fail("Did not configure pcap file", print_=True)
            exit(1)
        homepage_url = "http://%s/"%self.eth0_ip
        webpage = LFRequest.plain_get(url_=homepage_url, debug_=True)
        if webpage is None:
            self._fail("Unable to find wepage for LANforge", print_=True)
            exit(1)
        homepage_url="http://%s/lf_reports/"%self.eth0_ip
        webpage = LFRequest.plain_get(url_=homepage_url, debug_=True)
        if webpage is None:
            self._fail("Unable to find /lf_reports/ page", print_=True)
            exit(1)

        pprint.pprint(self.sta_mac_map)
        interesting_macs = {}
        for eid,record in self.sta_mac_map.items():
            interesting_macs[record['alias']] = [record['mac'], record['ap']]

        results = {}
        for station, info in interesting_macs.items():
            if station not in self.normal_sta_list:
                assoc_filter = self.packet_filter.get_filter_wlan_assoc_packets(ap_mac=info[1], sta_mac=info[0])
                null_filter = self.packet_filter.get_filter_wlan_null_packets(ap_mac=info[1], sta_mac=info[0])

                assoc_filter_results = self.packet_filter.run_filter(pcap_file=self.pcap_file, filter=assoc_filter)
                null_filter_results = self.packet_filter.run_filter(pcap_file=self.pcap_file, filter=null_filter)
                results[station] = [assoc_filter_results, null_filter_results]

                # print("\t%s %s" % (station, info[0]))
                # print("\t%s\n" % assoc_filter, assoc_filter_results)
                # print("\t%s\n" % null_filter, null_filter_results, "\n")

        total_fail = 0
        total_pass = 0
        for station,filters in results.items():
            for filter in filters:
                fail_count = 0
                pass_count = 0
                for line in filter:
                    # print(station, "LINE = ", line)
                    line_split = line.rstrip().split('\t')
                    ps_val = line_split[2]
                    if int(ps_val):
                        pass_count += 1
                    else:
                        fail_count += 1
            if fail_count == len(filter) or pass_count < len(filter):
                total_fail += 1
            else:
                total_pass += 1
            # print(len(filter),"%s:%s, %s:%s" % (fail_count, total_fail, total_pass, pass_count))

        print("%d stations had powersave flag set" % total_pass)
        if total_fail >= total_pass:
            self._fail("%d station(s) did not have powersave flag set" % total_fail)

        self._fail("not done writing pcap logic", print_=True)
        exit(1)




    def cleanup(self):
        self.wifi_monitor_profile.cleanup(desired_ports=[self.monitor_name])
        #self.cx_prof_download.cleanup()
        self.local_realm.remove_all_cxs(remove_all_endpoints=True)
        #self.cx_prof_upload.cleanup()
        self.sta_powersave_enabled_profile.cleanup(desired_stations=self.powersave_sta_list)
        self.sta_powersave_disabled_profile.cleanup(desired_stations=self.normal_sta_list)

def main():

    parser = argparse.ArgumentParser(
        prog='tip_station_powersave.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        tip_station_powersave.py

            ''',
        description='''\
This script uses filters from realm's PacketFilter class to filter pcap output for specific packets.
Currently it uses a filter for association packets using wlan.fc.type_subtype<=3. It is also using a filter
for QOS Null packets using wlan.fc.type_subtype==44. Both filters are also looking for the existence of 
either the station MAC or the AP MAC in wlan.addr
These are returned as an array of lines from the output in the format
$subtype $mac_addresses $wlan.fc.pwrmgt

#Currently, this test can only be applied to UDP connections
        ''')
    args = parser.parse_args()        

    lfjson_host = "localhost"
    lfjson_port = 8080
    #station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=4, padding_number_=10000)
    normal_station_list = ["sta1000" ]
    powersave_station_list = ["sta0001","sta0002","sta0003","sta0004"]
    ip_powersave_test = TIPStationPowersave(lfjson_host, lfjson_port,
                                            ssid="jedway-open-149",
                                            password="[BLANK]",
                                            channel_=149,
                                            normal_station_list_=normal_station_list,
                                            normal_station_radio_="wiphy0",
                                            powersave_station_list_=powersave_station_list,
                                            powersave_station_radio_="wiphy0",
                                            monitor_name_="moni0",
                                            monitor_radio_="wiphy1",
                                            side_a_min_rate_=1000000,
                                            side_b_min_rate_=1000000,
                                            traffic_duration_="30s",
                                            pause_duration_="2s",
                                            debug_on_=False,
                                            exit_on_error_=True,
                                            exit_on_fail_=True)
    ip_powersave_test.cleanup()
    ip_powersave_test.build()
    ip_powersave_test.start()
    ip_powersave_test.stop()
    ip_powersave_test.cleanup()

if __name__ == "__main__":
    
    main()

