#!/usr/bin/env python3
"""
NAME: lf_pcap.py

PURPOSE:
Common Library for reading pcap files and check packet information for specific filters

SETUP: This script requires pyshark and tshark to be installed before

EXAMPLE:
see: /py-scritps/lf_pcap_test.py for example

COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
"""
import os
import sys
import argparse
import time
import pyshark as ps
import importlib
from datetime import datetime

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

wifi_monitor = importlib.import_module("py-json.wifi_monitor_profile")
WiFiMonitor = wifi_monitor.WifiMonitor
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_report = cv_test_reports.lanforge_reports


class LfPcap(Realm):
    def __init__(self,
                 host="localhost", port=8080,
                 _read_pcap_file=None,
                 _apply_filter=None,
                 _live_pcap_interface=None,
                 _live_cap_timeout=None,
                 _live_filter=None,
                 _live_remote_cap_host=None,
                 _live_remote_cap_interface=None,
                 _debug_on=False,
                 _pcap_name=None
                 ):
        # super().__init__(lfclient_host=host, lfclient_port=port, debug_=_debug_on)
        self.pcap_name = _pcap_name
        self.host = host,
        self.port = port
        self.debug = _debug_on
        self.pcap = None
        self.live_pcap = None
        self.remote_pcap = None
        self.pcap_file = _read_pcap_file
        self.apply_filter = _apply_filter
        self.live_filter = _live_filter
        self.live_pcap_interface = _live_pcap_interface
        self.live_cap_timeout = _live_cap_timeout
        self.remote_cap_host = _live_remote_cap_host
        self.remote_cap_interface = _live_remote_cap_interface
        # self.wifi_monitor = WiFiMonitor(self.lfclient_url, local_realm=self, debug_=self.debug)

    def read_pcap(self, pcap_file, apply_filter=None):
        self.pcap_file = pcap_file
        if apply_filter is not None:
            self.apply_filter = apply_filter
        try:
            self.pcap = ps.FileCapture(input_file=self.pcap_file, display_filter=self.apply_filter, use_json=False)
        except Exception as error:
            raise error
        return self.pcap

    def read_time(self, pcap_file,
                  filter='(wlan.fc.type_subtype==3 && wlan.tag.number==55) && (wlan.da == 04:f0:21:9f:c1:69)'):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter=filter)
                packet_count = 0
                data = None
                for pkt, s in zip(cap, range(2)):
                    if s == 0:
                        x = pkt.frame_info.time_relative
                        y = float(x)
                        z = round(y, 4)
                        m = z * 1000
                        data = m
                        print(data)
                        packet_count += 1
                    print("Total Packets: ", packet_count)
                    # print(data)
                    if packet_count != 0:
                        return data
                    else:
                        return data
        except ValueError:
            raise "pcap file is required"

    def capture_live_pcap(self):
        try:
            self.live_pcap = ps.LiveCapture(interface=self.live_pcap_interface, output_file='captured.pcap')
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

    def get_packet_info(self, pcap_file, filter='wlan.fc.type_subtype==3 && wlan.tag.number==55'):
        """get packet info from each packet from the pcap file"""
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter=filter)
                packet_count = 0
                data = []
                for pkt in cap:
                    data.append(str(pkt))
                    packet_count += 1
                print("Total Packets: ", packet_count)
                print(data)
                data = "\n".join(data)
                if packet_count != 0:
                    return data
                else:
                    return data
        except ValueError:
            raise "pcap file is required"

    def get_wlan_mgt_status_code(self, pcap_file, filter='wlan.fc.type_subtype==3 && wlan.tag.number==55'):
        """ To get status code of each packet in WLAN MGT Layer """
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter=filter)
                packet_count = 0
                value, data = '', None
                for pkt in cap:
                    # print(pkt)
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_fixed_status_code')
                        if value == '0x0000' or value == '0':
                            data = 'Successful'
                        else:
                            data = 'failed'
                        packet_count += 1
                print("Total Packets: ", packet_count)
                if packet_count == 0:
                    return "empty"
                if packet_count != 0:
                    return data
                else:
                    return data
        except ValueError:
            raise "pcap file is required"

    def check_frame_present(self, pcap_file, filter='(wlan.fixed.category_code == 6)'):
        """ To get status code of each packet in WLAN MGT Layer """
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter=filter)
                packet_count = 0
                value, data = '', None
                for pkt in cap:
                    # print(pkt)
                    if 'wlan.mgt' in pkt:
                        packet_count += 1
                print("Total Packets: ", packet_count)
                if packet_count == 0:
                    return "empty"
                else:
                    return "present"
        except ValueError:
            raise "pcap file is required"

    def check_group_id_mgmt(self, pcap_file):
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                print("Checking for Group ID Management Actions Frame...")
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.mgt && wlan.vht.group_id_management')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_group_id_management')
                        if value is not None:
                            print("Group ID Management: ", value)
                            value = f"Group ID Management: {value}"
                            packet_count += 1
                        if packet_count == 1:
                            break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def check_beamformee_association_request(self, pcap_file):
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformee == 1 &&  '
                                                                       'wlan.fc.type_subtype == 0')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_capabilities_mubeamformee')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if value == 0:
                                value = "MU Beamformee Capable: Not Supported"
                            if value == 1:
                                value = "MU Beamformee Capable: Supported"
                            if packet_count == 1:
                                break
                print(packet_count)
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def check_beamformer_association_response(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformer == 1 &&  '
                                                                       'wlan.fc.type_subtype == 1')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_capabilities_mubeamformer')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if value == 0:
                                value = "MU Beamformer Capable: Not Supported"
                            if value == 1:
                                value = "MU Beamformer Capable: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def check_beamformer_beacon_frame(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformer == 1 && '
                                                                       'wlan.fc.type_subtype == 8')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_capabilities_mubeamformer')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if value == 0:
                                value = "MU Beamformer Capable: Not Supported"
                            if value == 1:
                                value = "MU Beamformer Capable: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required."

    def check_beamformer_probe_response(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformer == 1 && wlan.fc.type_subtype==5')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan' in pkt:
                        value = pkt['wlan'].get_field_value('wlan_vht_capabilities_mubeamformer')
                        if value is not None:
                            print(value)
                            if value == 0:
                                value = "MU Beamformer Capable: Not Supported"
                            if value == 1:
                                value = "MU Beamformer Capable: Supported"
                            packet_count += 1
                            if packet_count == 1:
                                break
                if packet_count >= 1:

                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required."

    def check_he_capability_beacon_frame(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.ext_tag.he_phy_cap.he_su_ppdu_etc_gi == 1 && wlan.fc.type_subtype == 8')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_ext_tag_he_phy_cap_he_su_ppdu_with_1x_he_ltf_08us')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if str(value) == '0':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Not Supported"
                            if str(value) == '1':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required."

    def check_he_capability_probe_request(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.ext_tag.he_phy_cap.he_su_ppdu_etc_gi == 1 && wlan.fc.type_subtype == 4')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_ext_tag_he_phy_cap_he_su_ppdu_etc_gi')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if str(value) == '0':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Not Supported"
                            if str(value) == '1':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required."

    def check_he_capability_probe_response(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.ext_tag.he_phy_cap.he_su_ppdu_etc_gi == 1 && wlan.fc.type_subtype == 5')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_ext_tag_he_phy_cap_he_su_ppdu_with_1x_he_ltf_08us')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if str(value) == '0':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Not Supported"
                            if str(value) == '1':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required."

    def check_he_capability_association_request(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.ext_tag.he_phy_cap.he_su_ppdu_etc_gi == 1 && wlan.fc.type_subtype == 0')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_ext_tag_he_phy_cap_he_su_ppdu_etc_gi')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if str(value) == '0':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Not Supported"
                            if str(value) == '1':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Supported"
                            if packet_count == 1:
                                break
                print(packet_count)
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def check_he_capability_association_response(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.ext_tag.he_phy_cap.he_su_ppdu_etc_gi == 1 && wlan.fc.type_subtype == 1')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_ext_tag_he_phy_cap_he_su_ppdu_etc_gi')
                        if value is not None:
                            print(value)
                            packet_count += 1
                            if str(value) == '0':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Not Supported"
                            if str(value) == '1':
                                value = "HE SU PPDU & HE MU PPDU w 4x HE-LTF & 0.8us GI: Supported"
                            if packet_count == 1:
                                break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def check_he_guard_interval(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='radiotap.he.data_5.gi')
                packet_count = 0
                value = "Packet Not Found"
                for pkt in cap:
                    if 'radiotap' in pkt:
                        value = pkt['radiotap'].get_field_value('he_data_5_gi')
                        if value is not None:
                            print(value)
                            value = f"GI: {str(value)}us"
                            packet_count += 1
                        if packet_count == 1:
                            break
                if packet_count >= 1:
                    return f"{value}"
                else:
                    return f"{value}"
        except ValueError:
            raise "pcap file is required"

    def sniff_packets(self, interface_name="wiphy1", test_name="mu-mimo", channel=-1, sniff_duration=180):
        if test_name is not None:
            self.pcap_name = test_name + ".pcap"
        else:
            self.pcap_name = "capture" + str(datetime.now().strftime("%Y-%m-%d-%H-%M")).replace(':', '-') + ".pcap"
        print('pcap file name: ', self.pcap_name)
        self.wifi_monitor.create(resource_=1, channel=channel, mode="AUTO", radio_=interface_name, name_="moni0")
        self.wifi_monitor.start_sniff(capname=self.pcap_name, duration_sec=sniff_duration)
        for i in range(int(sniff_duration)):
            time.sleep(1)
        self.wifi_monitor.cleanup()
        return self.pcap_name

    def move_pcap(self, current_path="/home/lanforge/", pcap_name=None):
        if current_path is None:
            current_path = "/home/lanforge/"
        if pcap_name is None:
            pcap_name = self.pcap_name
        print('...............Moving pcap to directory............\n', current_path + pcap_name)
        print('++++++', os.getcwd())
        if pcap_name is not None:
            if os.path.exists(current_path+pcap_name):
                lf_report.pull_reports(hostname=self.host, port=22, username="lanforge", password="lanforge", report_location=current_path + pcap_name, report_dir=".")
            else:
                raise FileNotFoundError
        else:
            raise ValueError("pcap_name is Required!")


def main():
    parser = argparse.ArgumentParser(
        prog='lf_pcap.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Common Library for reading pcap files and check packet information for specific filters',
        description='''\
    """
-----------------------
NAME: lf_pcap.py

PURPOSE:
Common Library for reading pcap files and check packet information for specific filters

SETUP:
This script requires pyshark to be installed before,you can install it by running "pip install pyshark"

EXAMPLE:
see: /py-scritps/lf_pcap.py 
---------------------
''')
    parser.add_argument('--pcap_file', '-p', help='provide the pcap file path', dest="pcap_file",  default=None)
    parser.add_argument('--apply_filter', '-f', help='apply the filter you want to', dest='apply_filter', default=None)
    args = parser.parse_args()
    pcap_obj = LfPcap(
        host="192.168.100.131",
        port=8080,
        _read_pcap_file=args.pcap_file,
        _apply_filter=args.apply_filter,
        _live_filter=None,
        _live_pcap_interface=None,
        _live_remote_cap_host=None,
        _live_cap_timeout=None,
        _live_remote_cap_interface=None
    )
    # pcap_obj.check_group_id_mgmt(pcap_file=pcap_obj.pcap_file)
    # pcap_obj.check_beamformer_association_request(pcap_file=pcap_obj.pcap_file)
    # pcap_obj.check_beamformer_association_response(pcap_file=pcap_obj.pcap_file)
    # pcap_obj.check_beamformer_beacon_frame(pcap_file=pcap_obj.pcap_file)
    # pcap_obj.get_wlan_mgt_status_code(pcap_file=pcap_obj.pcap_file)
    # pcap_obj.get_packet_info(pcap_obj.pcap_file)
    pcap_obj.read_time(pcap_file="roam_11r_ota_iteration_0_2022-05-05-22-20.pcap")

if __name__ == "__main__":
    main()
