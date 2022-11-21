#!/usr/bin/env python3
import sys
import os
import importlib
import time
import datetime
import argparse
# import allure
# from tabulate import tabulate
import csv
from pprint import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")
multicast_profile = importlib.import_module("py-json.multicast_profile")
station_profile = importlib.import_module("py-json.station_profile")
wifi_monitor = importlib.import_module("py-json.wifi_monitor_profile")
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_rpt = cv_test_reports.lanforge_reports

import pyshark as ps

'''
Usage: python3 lf_power_save_test_cases_cisco.py --mgr 192.168.200.229 --ssid Endurance1 --radio wiphy0 
       --upstream_port 1.1.eth1 --monitor_radio wiphy0 
       --report_path /home/mahesh/Desktop/lanforge-scripts/lanforge-scripts/py-scripts
'''


class MulticastPowersaveTraffic(Realm):

    def __init__(self, host, port, ssid, security, password, station_list, min_rate_multi_cast=56,
                 max_rate_multi_cast=56,
                 pdu_size=1000,
                 upstream="1.1.eth1", interface_to_capture=None,
                 prefix="00000", test_duration="5m", report_path="",
                 station_radio="wiphy0", monitor_radio="wiphy0", remote_host_cap_ip=None,
                 output_file_for_cap="",
                 remote_host_cap_interface=None,

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
        self.upstream = upstream
        self.min_rate = min_rate_multi_cast
        self.max_rate = max_rate_multi_cast
        self.output_file = output_file_for_cap
        self.enable_multicast_testing = False
        self.enable_unicast_testing = False
        self.filter = ""
        self.report_dir = report_path
        self.captured_file_name = ""
        self.sta_mac = ""
        self.ap_mac = ""
        self.upstream_mac = ""
        if interface_to_capture is not None:
            self.live_cap_timeout = interface_to_capture
        else:
            self.live_cap_timeout = station_radio
        if remote_host_cap_ip and remote_host_cap_interface is not None:
            self.remote_cap_host = remote_host_cap_ip
            self.remote_cap_interface = remote_host_cap_interface

        self.test_duration = test_duration
        # upload

        self.multi_cast_profile = multicast_profile.MULTICASTProfile(self.host, self.port, local_realm=self)

        self.station_profile = station_profile.StationProfile(self.lfclient_url, local_realm=self, ssid=self.ssid,
                                                              ssid_pass=self.password,
                                                              security=self.security, number_template_=self.prefix,
                                                              mode=0,
                                                              up=True,
                                                              dhcp=True,
                                                              debug_=self.debug)
        self.new_monitor = wifi_monitor.WifiMonitor(self.lfclient_url, local_realm=self, debug_=self.debug)

    def build_station_profile(self):
        print("Station radio..in 108 lanfo-py-scri",self.station_radio)
        self.station_profile.use_security(self.security, ssid=self.ssid, passwd=self.password)
        self.station_profile.set_number_template(self.prefix)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        # self.station_profile.set_command_flag("add_sta", "power_save_enable", 1)
        self.station_profile.create(radio=self.station_radio, sta_names_=self.sta_list)
        self._pass("PASS: Station builds finished")

    def build_monitor(self, channel):
        self.new_monitor.create(resource_=1, channel=channel, radio_=self.monitor_radio, name_="moni0")

    def build_multi_cast_profile(self):
        print("Building multicast endps....")
        self.multi_cast_profile.create_mc_tx("mc_udp", self.upstream, min_rate=self.min_rate, max_rate=self.max_rate)
        self.multi_cast_profile.create_mc_rx("mc_udp", self.sta_list)

    def build_layer3_upload(self):
        self.cx_prof_upload.name_prefix = "UDP_up"
        print("Creating upload cx profile ")
        self.cx_prof_upload.create(endp_type="lf_tcp", side_a=self.station_profile.station_names, side_b=self.upstream,
                                   sleep_time=.05)

    def build_layer3_download(self):
        self.cx_prof_download.name_prefix = "TCP_down"
        print("Creating download cx profile")
        self.cx_prof_download.create(endp_type="lf_tcp", side_a=self.station_profile.station_names,
                                     side_b=self.upstream,
                                     sleep_time=.05)

        # channel = self.json_get("/port/1/%s/%s/"%(1,"wiphy0"))
        # rint("The channel name is...")

        # station_channel = self.json_get("/port/1/%s/%s")
        # pprint.pprint(station_channel)

    def get_channel(self):
        self.station_profile.admin_up()
        # self.new_monitor.set_flag()
        # print(self.station_profile.station_names)
        print("Querying for channel from station created to create monitor interface on that particular channel")
        if self.wait_for_ip(self.station_profile.station_names):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            exit(1)
        channel_info = self.json_get(f"port/1/1/{self.sta_list[0]}?fields=channel")
        print(channel_info)
        if channel_info is not None:
            if 'interfaces' in channel_info:
                for item in channel_info['interfaces']:
                    for k, v in item.items():
                        print("sta_name %s" % v['alias'])
                        print("mac      %s" % v['mac'])
                        print("ap       %s\n" % v['ap'])
            elif 'interface' in channel_info:
                print("channel %s" % channel_info['interface']['channel'])
                self.station_profile.admin_down()
                time.sleep(0.5)
        return int(channel_info['interface']['channel'])

    def get_captured_file_and_location(self):
        return self.captured_file_name, self.report_dir, self.filter

    def start(self):

        print("station profile got admin up")
        self.station_profile.admin_up()
        # self.new_monitor.set_flag()
        # print(self.station_profile.station_names)
        if self.wait_for_ip(self.station_profile.station_names):
            self._pass("All stations got IPs")
            print("Stations received ip")
        else:
            self._fail("Stations failed to get IPs")
            print("Stations didn't received ip")
            # allure.attach(name="FAILED", body="Stations didn't connected to AP")
            exit(1)

        if self.enable_multicast_testing:
            print("started multicast traffic")
            self.multi_cast_profile.start_mc()
        elif self.enable_unicast_testing:
            print("started unicast traffic")
            self.start_layer3()

        # print station + MAC, AP
        temp = []
        for station in self.station_profile.station_names:
            temp.append(self.name_to_eid(station)[2])
        port_info = self.json_get("port/1/1/%s?fields=alias,ap,mac" % ','.join(temp))
        print("port_info.........", port_info)
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
                self.filter = "wlan.addr==" + port_info['interface']['mac'] + " || " + "wlan.addr==" + \
                              port_info['interface']['ap']
                self.ap_mac = str(port_info['interface']['ap'])
                self.sta_mac = str(port_info['interface']['mac'])
                # allure.attach(name="AP MAC", body=str(port_info['interface']['ap']))
                # allure.attach(name="Station MAC", body=str(port_info['interface']['mac']))
                print("filter=", self.filter)
            else:
                print('interfaces and interface not in port_mgr_response')
                exit(1)
        temp_1 = []
        temp_1.append(self.name_to_eid(self.upstream)[2])
        upstream_info = self.json_get("port/1/1/%s?fields=alias,mac" % ','.join(temp_1))
        print("upstream_info.........", upstream_info)
        if upstream_info is not None:
            if 'interfaces' in upstream_info:
                for item in upstream_info['interfaces']:
                    for k, v in item.items():
                        print("upstream_name %s" % v['alias'])
                        print("mac      %s" % v['mac'])
            elif 'interface' in upstream_info:
                print("sta_name %s" % upstream_info['interface']['alias'])
                print("mac      %s" % upstream_info['interface']['mac'])
                self.upstream_mac = str(upstream_info['interface']['mac'])
                # allure.attach(name="Upstream Port MAC", body=str(upstream_info['interface']['mac']))
            else:
                print('interfaces and interface not in port_mgr_upstream_response')
                exit(1)

    '''
    def capture_live_pcap(self):
        try:a8:93:4a:6f:ce:3b
            self.live_pcap = ps.LiveCapture(interface=self.live_pcap_interface, output_file=self.output_file)
            self.live_pcap.sniff(timeout=300)
        except ValueError:
            raise "Capture Error"
        return self.live_pcap

    def capture_remote_pcap(self):
        try:
            self.remote_pcap = ps.RemoteCapture(remote_host=self.remote_cap_host,
                                                remote_interface=self.remote_cap_interface)
        except ValueError:
            raise "Host error"
        return self.remote_pcap
    '''

    def verify_dtim_multicast_pcap(self, pcap_file, apply_filter=None):
        self.ap_mac = "10:F9:20:FD:E2:0B"
        self.sta_mac = "7c:50:79:01:14:38"
        self.upstream_mac = "9c:69:b4:60:ab:5a"
        self.pcap_file = self.report_dir + "/" + pcap_file
        if apply_filter is not None:
            self.apply_filter = apply_filter
            # allure.attach(name="Filter", body=str(self.apply_filter))
        try:
            self.pcap = ps.FileCapture(input_file=self.pcap_file, display_filter=self.apply_filter)
        except Exception as error:
            raise error
        check_mcast_val = False
        qos_null_frame_val = False
        end_result = False
        filename = self.report_dir + "/" + pcap_file.split('.')[0] + ".csv"
        table_headers = ["Packet Number", "Description", "Pass/Fail"]
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile, lineterminator='\r')

            # writing the fields
            csvwriter.writerow(table_headers)
        pwr_mgt_val = []
        for pkt in self.pcap:  # traversing through all packets one by one
            table_values = []
            if str(pkt.wlan.fc_type_subtype) == "0x002c":
                if str(pkt.wlan.fc_pwrmgt) == '1':
                   qos_null_frame_val = True
                elif str(pkt.wlan.fc_pwrmgt) == '0':
                    qos_null_frame_val = False
                pwr_mgt_val.append(str(pkt.wlan.fc_pwrmgt))
            if qos_null_frame_val:
                if 'wlan.mgt' in pkt and str(pkt.wlan.fc_type_subtype) == "0x0008":
                    dtim_multicast_bit = pkt['wlan.mgt'].get_field_value('wlan_tim_bmapctl_multicast',
                                                                         raw=True)  # reading Multicast bit to verify whether it is set or not
                    frame_num = str(pkt.number)
                    print(f"PACKET NUMBER : {frame_num}, dtim_multicast_bit : {dtim_multicast_bit}")
                    if dtim_multicast_bit == "1":  # verifying whether multicast bit is set i.e True
                        dtim_count = pkt['wlan.mgt'].get_field_value('wlan_tim_dtim_count',
                                                                     raw=True)  # here i'm checking the dtim count of the frame to which MUlticast bit which is set
                        print(f"PACKET NUMBER : {frame_num}, dtim_count : {dtim_count}")
                        if dtim_count == "00":
                            print("dtim_multicast_bit_frame_num :", frame_num)
                            check_mcast_val = True
                            continue  # if dtim count is zero im going for next packet to verify whether multicast frame is transmitted or not
                    else:
                        continue

                elif str(pkt.wlan.fc_type_subtype) == "0x0020" and check_mcast_val:
                    frame_type = pkt[
                        'wlan'].DATA_LAYER  # here i'm verifying the type of frame to identify multicast packet right after beacon.
                    # print("TRANSMITTER ADDRESS..", str(pkt.wlan.ta))
                    # print("SOURCE ADDRESS..",str(pkt.wlan.sa))
                    print("AP MAC", self.ap_mac)
                    # if (str(pkt.wlan.ta).upper() == self.ap_mac) and ((str(pkt.wlan.sa).lower() == str(
                    #         self.sta_mac).lower()) or (str(pkt.wlan.sa).lower() == str(
                    #     self.upstream_mac).lower())):  # if it is data packet it checks for power mgt bit and verify multicast frames are transmitted

                    if (str(pkt.wlan.ta).upper() == self.ap_mac):
                        pwr_mgt_bit = pkt['wlan'].get_field_value('fc_pwrmgt', raw=True)
                        receiver_addr_mcast = str(pkt.wlan.ra)
                        threshold_time_for_mcast_to_transmit = 5
                        mcast_frame_num = str(pkt.number)
                        if receiver_addr_mcast.split(':')[0][-1] == '1':  # check to know multicast or unicast packet
                            print(f"Expected Multi cast frame number right after beacon : {mcast_frame_num}")
                            time_delta_from_prev_frame_in_sec = str(pkt.frame_info.time_delta_displayed)
                            time_delta_from_prev_frame_in_millisec = round(
                                float(time_delta_from_prev_frame_in_sec) * 1000)
                            print("time_delta_from_prev_frame_in_microsec :", time_delta_from_prev_frame_in_sec)
                            print("time_delta_from_prev_frame_in_millisec :",
                                  str(time_delta_from_prev_frame_in_millisec) + "" + 'ms')
                            print(
                                f"PASSED:Multicast bit set in receiver address,receiver_addr_mcast : {receiver_addr_mcast}, PACKET NUMBER:{mcast_frame_num}")
                            # allure.attach(name="Multicast packet frame number", body=str(
                            #     f"PASSED:Multicast bit set in receiver address,receiver_addr_mcast : {receiver_addr_mcast}, PACKET NUMBER:{mcast_frame_num}"))

                            if time_delta_from_prev_frame_in_millisec < threshold_time_for_mcast_to_transmit:
                                print(
                                    f"PASSED:Frame transmitted in less than {threshold_time_for_mcast_to_transmit} milli seconds, PACKET NUMBER:{mcast_frame_num}")

                                # allure.attach(name="PASSED", body=str(
                                #     f"PASSED:Frame transmitted in less than {threshold_time_for_mcast_to_transmit} milli seconds, PACKET NUMBER:{mcast_frame_num}"))

                                # check_mcast_val = False

                                # if pwr_mgt_val is not None:
                                #     if pwr_mgt_val[-1] == "1":
                                #         print(f"FAILED:Multicast Packet transmitted when station in powersave mode , Packet Number:{mcast_frame_num}")
                                #         allure.attach(name="FAILED",body=str(f"FAILED:Multicast Packet transmitted when station in powersave mode , Packet Number:{mcast_frame_num}"))
                                #         print(f"PASSED:Multicast Traffic Transmitted, Packet Number:{mcast_frame_num}")
                                # else:
                                #     continue
                                # continue

                            else:
                                print(
                                    f"FAILED:Packet transmitted in more than {threshold_time_for_mcast_to_transmit} milli seconds, PACKET NUMBER:{mcast_frame_num}")
                                # allure.attach(name="ERROR", body=str(
                                #     f"FAILED:Packet transmitted in more than {threshold_time_for_mcast_to_transmit} milli seconds, PACKET NUMBER:{mcast_frame_num}"))
                                table_values.append(str(mcast_frame_num))
                                table_values.append(
                                    f"Packet transmitted in more than {threshold_time_for_mcast_to_transmit} milli seconds")
                                table_values.append("Fail")

                            if str(pkt.wlan.fc_moredata) == "0":
                                check_mcast_val = False
                            elif str(pkt.wlan.fc_moredata) == "1":
                                check_mcast_val = True

                            # tabulate(table_values, table_headers, tablefmt="fancy_grid")

                        elif receiver_addr_mcast == "ff:ff:ff:ff:ff:ff":
                            print(
                                f"PACKET NUMBER : {str(pkt.number)}, PASSED:broadcast packet transmitted with multicast bit set in previous beacon")
                        else:
                            print(
                                f"ERROR:Multicast bit is not set in receiver address,receiver_addr_mcast : {receiver_addr_mcast},PACKET NUMBER:{mcast_frame_num}")
                            end_result = True

                            # allure.attach(name="Failed", body=str(
                            #     f"ERROR:Multicast bit is not set in receiver address,receiver_addr_mcast : {receiver_addr_mcast},PACKET NUMBER:{mcast_frame_num}"))
                            table_values.append(str(mcast_frame_num))
                            table_values.append("Multicast bit is not set in receiver address")
                            table_values.append("Fail")

                        if str(pkt.wlan.fc_moredata) == "0":
                            check_mcast_val = False
                        elif str(pkt.wlan.fc_moredata) == "1":
                            check_mcast_val = True
                            # tabulate(table_values, table_headers, tablefmt="fancy_grid")
                    else:
                        continue
                        # check_mcast_val = False

                else:
                    if str(pkt.wlan.fc_type_subtype) == "0x0020":
                        receiver_addr_mcast = str(pkt.wlan.ra)
                        rcv_addr = "ff:ff:ff:ff:ff:ff"
                        if (receiver_addr_mcast.split(':')[0][-1] == '1') and (
                                (str(pkt.wlan.sa).lower() == str(self.sta_mac).lower()) or (
                                str(pkt.wlan.sa).lower() == str(self.upstream_mac).lower())):
                            print(f"PACKET NUMBER : {str(pkt.number)}, FAILED:unexpected multicast packet")
                            # allure.attach(name="Failed", body=str(
                            #     f"PACKET NUMBER : {str(pkt.number)}, FAILED:unexpected multicast  packet without previous beacon"))
                            end_result = True
                            table_values.append(str(pkt.number))
                            table_values.append("unexpected multicast packet")
                            table_values.append("Fail")

                        if receiver_addr_mcast == rcv_addr and pkt.wlan.ta == self.ap_mac:
                            print(
                                f"PACKET NUMBER : {str(pkt.number)}, FAILED:Unexpected broadcast packet without multicast bit set in previous beacon")
                            # allure.attach(name="Failed", body=str(
                            #     f"PACKET NUMBER : {str(pkt.number)}, FAILED:Unexpected broadcast packet without multicast bit set in previous beacon"))
                            end_result = True
                            table_values.append(str(pkt.number))
                            table_values.append("Unexpected broadcast packet without multicast bit set in previous beacon")
                            table_values.append("Fail")

                # table_data=tabulate(table_values, table_headers, tablefmt="fancy_grid")
                # print(table_data)
                print("table_values...",table_values)
                if len(table_values):
                    print("IN CSV WRITE..", str(pkt.number))
                    with open(filename, 'a') as csvfile:
                        # creating a csv writer object
                        csvwriter = csv.writer(csvfile, lineterminator='\n')

                        # writing the fields
                        # csvwriter.writerow(table_headers)

                        # writing the data rows

                        csvwriter.writerow(table_values)
        print(filename)
        # allure.attach.file(source=self.pcap_file, name="pcap_file", attachment_type=allure.attachment_type.PCAP)
        # allure.attach.file(source=filename, name="Test Validation info", attachment_type=allure.attachment_type.CSV)
        return end_result

    def start_station_profile(self):
        self.station_profile.admin_up()

    def stop_station_profile(self):
        self.station_profile.admin_down()

    def stop_monitor(self):
        # switch off new monitor
        self.new_monitor.admin_down()

    def start_multicast(self):
        self.multi_cast_profile.start_mc()

    def start_layer3(self):
        # self.cx_prof_upload.start_cx()
        self.cx_prof_download.start_cx()

    def stop_multi_cast(self):
        self.multi_cast_profile.stop_mc()

    def stop_layer3(self):
        # self.cx_prof_upload.stop_cx()
        self.cx_prof_download.stop_cx()

    def cleanup_station_profile(self):
        self.station_profile.cleanup(desired_stations=self.sta_list)

    def cleanup_layer3(self):
        self.cx_prof_download.cleanup()
        self.cx_prof_upload.cleanup()

    def cleanup_monitor(self):
        self.new_monitor.cleanup()

    def cleanup_multicast(self):
        self.multi_cast_profile.cleanup()

    def multicast_testing(self, cleanup=True):
        self.enable_multicast_testing = True
        self.station_profile.cleanup(desired_stations=self.sta_list)
        self.station_profile.local_realm.remove_all_cxs(remove_all_endpoints=True)
        self.build_station_profile()  # function to build station profile
        # channel_info = self.get_channel()
        # self.build_monitor(channel_info)  # function to create monitor
        self.build_multi_cast_profile()  # function to build multi_cast_profile

        self.start()  # function to start sniff by admin up station and /
        # starting the multicast traffic for some duration
        if cleanup:
            self.multicast_testing_stop_and_cleanup()

    def multicast_testing_stop_and_cleanup(self):
        self.new_monitor.admin_down()
        self.stop_multi_cast()
        self.station_profile.admin_down()

        self.new_monitor.cleanup()
        self.cleanup_multicast()
        self.station_profile.cleanup(desired_stations=self.sta_list)

    def unicast_testing(self):
        self.enable_unicast_testing = True
        self.build_station_profile()  # function to build station profile
        self.build_monitor()  # function to create monitor
        # self.build_layer3_upload()
        self.build_layer3_download()  # function to build unicast download traffic

        self.start()  # function to start sniff by admin up station followed by /
        # starting the unicast traffic with desired pdu size for some duration

        self.new_monitor.admin_down()
        # self.cx_prof_upload.stop_cx()
        self.cx_prof_download.stop_cx()
        self.station_profile.admin_down()

        self.new_monitor.cleanup()
        self.cx_prof_download.cleanup()
        # self.cx_prof_upload.cleanup()
        self.station_profile.cleanup(desired_stations=self.sta_list)


def main():
    # Realm.create_basic_argparse defined in lanforge-scripts/py-json/LANforge/lfcli_base.py
    parser = Realm.create_basic_argparse(
        prog='lf_power_save_test_cases_cisco.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        lf_power_save_test_cases_cisco.py

            ''',
        description='''\
Example of creating traffic on an l3 connection
        ''')

    parser.add_argument('--monitor_radio', help="--monitor_radio radio to be used in monitor creation",
                        default="wiphy1")
    parser.add_argument('--report_path', help="desired path to save your pcap file fetched from lanforge through ssh",
                        default="/home/mahesh/Desktop/lanforge-scripts/lanforge-scripts/py-scripts")
    parser.add_argument('--mcast_min_rate', help="value for multicast minimum rate in kbps", type=int, default=9000)
    parser.add_argument('--mcast_max_rate', help="value for multicast maximum rate in kbps", type=int, default=128000)

    parser.add_argument('--test_duration', help='duration of the test eg: 30s, 2m, 4h', default="5m")

    parser.add_argument('--pdu_size', help="pdu size in bytes", type=int, default=1400)

    args = parser.parse_args()

    lfjson_host = args.mgr
    lfjson_port = 8080
    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_stations)-1, padding_number_=10000)
    ip_powersave_test = MulticastPowersaveTraffic(lfjson_host, lfjson_port, ssid=args.ssid,
                                                  security=args.security,
                                                  password=args.passwd, station_list=station_list,
                                                  min_rate_multi_cast=args.mcast_min_rate,
                                                  max_rate_multi_cast=args.mcast_max_rate,
                                                  pdu_size=args.pdu_size,
                                                  station_radio=args.radio,
                                                  upstream=args.upstream_port,
                                                  monitor_radio=args.monitor_radio,
                                                  test_duration=args.test_duration,
                                                  interface_to_capture=None,
                                                  _debug_on=args.debug, remote_host_cap_ip=None,
                                                  remote_host_cap_interface=None,
                                                  report_path=args.report_path,
                                                  output_file_for_cap="/home/lanforge",
                                                  _exit_on_error=True, _exit_on_fail=True)

    ip_powersave_test.multicast_testing(cleanup=False)  # function to run multicast test
    # ip_powersave_test.unicast_testing()   # function to run unicast test

    # captured_file_name, local_dir, filter = ip_powersave_test.get_captured_file_and_location()  # function returns captured_file_name along \
    # with location of local directory where the \
    # captured file is pulled

    # below function should be executed along with multicast_testing or unicast_testing if we wish to disect captured file.
    # ip_powersave_test.verify_dtim_multicast_pcap(local_dir + '/' + captured_file_name,
    #                                             apply_filter=filter)

    # below function can be run solely without calling above functions to disect multicast packets \
    # if we have ready packet captured file to test dtim_multicast

    # apply_filter = "wlan.addr==10:F9:20:FD:E2:0E || wlan.addr==04:f0:21:a3:8f:69||wlan.addr==7c:50:79:6d:8c:b6||wlan.addr==7c:50:79:26:6b:3c||wlan.addr==a8:93:4a:6f:ce:3b")

    # ip_powersave_test.verify_dtim_multicast_pcap("powersave_4clients_5ghz.pcapng",
    #                                               apply_filter="wlan.addr == 10:F9:20:FD:E2:0B || wlan.addr==7c:50:79:01:14:38")


if __name__ == "__main__":
    main()
