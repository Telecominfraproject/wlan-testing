#!/usr/bin/env python3
'''
this script creates 1 station on given arguments
how to run - [lanforge@LF4-Node2 py-scripts]$ python3 station_banao.py -hst localhost -s TestAP22 -pwd [BLANK] -sec open -rad wiphy0
'''
import sys
import os
import importlib
import argparse
import time

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class STATION(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd, security, radio, sta_list=None, name_prefix="L3Test", upstream="eth2"):
        super().__init__(lfclient_host, lfclient_port)
        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.paswd = paswd
        self.security = security
        self.radio = radio
        self.sta_list = sta_list
        self.name_prefix = name_prefix
        self.upstream = upstream

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.paswd,
        self.station_profile.security = self.security
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = 1000000
        self.cx_profile.side_a_max_bps = 1000000
        self.cx_profile.side_b_min_bps = 1000000
        self.cx_profile.side_b_max_bps = 1000000


    def precleanup(self, sta_list):
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.local_realm.rm_port(sta, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=sta_list,
                                           debug=self.debug)
        time.sleep(1)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=self.radio)
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)

    def start(self, sta_list):
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        if self.local_realm.wait_for_ip(temp_stas):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.cx_profile.start_cx()


    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
        self.cx_profile.stop_cx()





def main():
    parser = argparse.ArgumentParser(
        prog='station_layer3.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Netgear AP DFS Test Script")
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected')
    #parser.add_argument()
    args = parser.parse_args()
    num_sta = 1
    station_list = LFUtils.port_name_series(prefix="sta",
                                            start_id=0,
                                            end_id=num_sta - 1,
                                            padding_number=10000,
                                            radio=args.radio)
    obj = STATION(lfclient_host= args.host, lfclient_port=8080, ssid=args.ssid , paswd=args.passwd, security=args.security, radio=args.radio, sta_list=station_list)
    obj.precleanup(station_list)
    obj.build()
    obj.start(station_list)

if __name__ == '__main__':
    main()
