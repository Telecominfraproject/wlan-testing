""" This script will create one station at a time and generate downstream traffic at 5Mbps  then again create next station create layer3 and will continue doing same until Ap stops admiting client
    This script can be used for for client admission test for particular AP

    arguements = >python3 load_21.py -hst 192.168.200.13 -s Nikita -pwd [BLANK] -sec open -rad wiphy1 --num_sta 60
    -Nikita Yadav
    -date: 23-02-2021
"""
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


class LoadLayer3(Realm):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd, security, radio, num_sta, name_prefix="L3", upstream="eth2"):

        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.paswd = paswd
        self.security = security
        self.radio = radio
        self.num_sta = num_sta

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
        self.cx_profile.side_a_min_bps = 5000000
        self.cx_profile.side_a_max_bps = 5000000
        self.cx_profile.side_b_min_bps = 0
        self.cx_profile.side_b_max_bps = 0

    def precleanup(self):
        num_sta = self.num_sta
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)
        self.cx_profile.cleanup_prefix()

        for sta in station_list:
            self.local_realm.rm_port(sta, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=station_list,
                                           debug=self.local_realm.debug)
        time.sleep(1)

    def build(self, sta_name):
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.local_realm.debug)
        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip([sta_name]):
            self.local_realm._pass("All stations got IPs", print_=True)

            self.cx_profile.create(endp_type="lf_udp", side_a=self.upstream, side_b=[sta_name],
                                   sleep_time=0)
            self.cx_profile.start_cx()

            return 1
        else:
            self.local_realm._fail("Stations failed to get IPs", print_=True)
            return 0

    def start(self):
        num_sta = self.num_sta
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)

        for i in station_list:
            # self.build(i)
            if self.build(i) == 0:
                print("station not created")
                break
            else:
                print("station created")

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
        self.cx_profile.stop_cx()


def main():
    parser = argparse.ArgumentParser(
        prog="test_client_admission.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Client Admission Test Script")
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected')
    parser.add_argument('-num_sta', '--num_sta', type=int, help='provide number of stations you want to create', default=60)
    # parser.add_argument()
    args = parser.parse_args()

    obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                     security=args.security, radio=args.radio, num_sta=args.num_sta)
    obj.precleanup()

    obj.start()


if __name__ == '__main__':
    main()
