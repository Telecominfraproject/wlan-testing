#!/usr/bin/env python3
"""
NAME: lf_pcap.py

PURPOSE:
Common Library for reading pcap files and check packet information for specific filters

SETUP: This script requires pyshark and tshark to be installed before

EXAMPLE:
see: /py-scritps/lf_pcap_test.py for example

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
"""
import argparse
import pyshark as ps


class LfPcap:
    def __init__(self,
                 _read_pcap_file=None,
                 _apply_filter=None,
                 _live_pcap_interface=None,
                 _live_cap_timeout=None,
                 _live_filter=None,
                 _live_remote_cap_host=None,
                 _live_remote_cap_interface=None
                 ):
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

    def read_pcap(self, pcap_file, apply_filter=None):
        self.pcap_file = pcap_file
        if apply_filter is not None:
            self.apply_filter = apply_filter
        try:
            self.pcap = ps.FileCapture(input_file=self.pcap_file, display_filter=self.apply_filter)
        except Exception as error:
            raise error
        return self.pcap

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

    def check_group_id_mgmt(self, pcap_file):
        print("pcap file path:  %s" % pcap_file)
        try:
            if pcap_file is not None:
                print("Checking for Group ID Management Actions Frame...")
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.mgt && wlan.vht.group_id_management')
                packet_count = 0
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_group_id_management')
                        if value is not None:
                            print(value)
                            packet_count += 1
                print(packet_count)
                if packet_count >= 1:
                    return True
                else:
                    return False
        except ValueError:
            raise "pcap file is required"

    def check_beamformer_association_request(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformer == 1 &&  '
                                                                       'wlan.fc.type_subtype==0x000')
                packet_count = 0
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_group_id_management')
                        if value is not None:
                            print(value)
                            packet_count += 1
                print(packet_count)
                if packet_count >= 1:
                    return True
                else:
                    return False
        except ValueError:
            raise "pcap file is required"

    def check_beamformer_association_response(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.vht.capabilities.mubeamformer == 1 &&  '
                                                                       'wlan.fc.type_subtype==0x001')
                packet_count = 0
                for pkt in cap:
                    if 'wlan.mgt' in pkt:
                        value = pkt['wlan.mgt'].get_field_value('wlan_vht_group_id_management')
                        if value is not None:
                            print(value)
                            packet_count += 1
                if packet_count >= 1:
                    return True
                else:
                    return False
        except ValueError:
            raise "pcap file is required"

    def check_beamformer_report_poll(self, pcap_file):
        try:
            if pcap_file is not None:
                cap = self.read_pcap(pcap_file=pcap_file, apply_filter='wlan.fc.type_subtype == 0x0014')
                packet_count = 0
                for pkt in cap:
                    packet_count += 1
                if packet_count >= 1:
                    return True
                else:
                    return False
        except ValueError:
            raise "pcap file is required."


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
see: /py-scritps/lf_pcap_test.py 
---------------------
''')
    parser.add_argument('--pcap_file', '-p', help='provide the pcap file path', dest="pcap_file", required=True)
    parser.add_argument('--apply_filter', '-f', help='apply the filter you want to', dest='apply_filter', default=None)
    args = parser.parse_args()
    pcap_obj = LfPcap(
        _read_pcap_file=args.pcap_file,
        _apply_filter=args.apply_filter,
        _live_filter=None,
        _live_pcap_interface=None,
        _live_remote_cap_host=None,
        _live_cap_timeout=None,
        _live_remote_cap_interface=None
    )
    test = pcap_obj.check_group_id_mgmt(pcap_file=pcap_obj.pcap_file)
    print(test)


if __name__ == "__main__":
    main()
