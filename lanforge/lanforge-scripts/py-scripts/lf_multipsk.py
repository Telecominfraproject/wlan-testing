#!/usr/bin/env python3

"""
NAME: lf_multipsk.py

PURPOSE:
        to test the multipsk feature in access point. Multipsk feature states connecting clients using same ssid but different passwords ,
        here we will create two or 3 passwords with different vlan id on single ssid and try to connect client with different passwords.

        NOTE:  This script has a lot of hard-coded values, and will only work in a very particular setup
        like what is used in TIP labs with APs set up for VLANs and LANforge set up to serve DHCP address
        on un-tagged ports as well as tagged 1q vlans.  This script may be improved in the future to be more flexible.

        NOTE:  This script does not create the .1q vlan interfaces, it assumes they already exist before this script
        runs.

DESCRIPTION:
            The script will follow basic functionality as:-
            1- create station on input parameters provided
            2- the input parameters consist of dictionary of passwords,upstream,mac address, number of clients and radio as input
            3- will create layer3 cx for tcp and udp
            3- verify layer3 cx
            4- verify the ip for each station is comming from respective vlan id or not.
example :-
         python3 lf_multipsk.py --mgr localhost  --mgr_port 8802  --ssid "MDU Wi-Fi"  --security wpa2

INCLUDE_IN_README
    -Nikita Yadav
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse
import time
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class MultiPsk(Realm):
    def __init__(self,
                 host=None,
                 port=8080,
                 ssid=None,
                 input=None,
                 security=None,
                 passwd=None,
                 radio=None,
                 num_sta=None,
                 start_id=0,
                 resource=1,
                 sta_prefix="sta",
                 debug_=False,
                 ):
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.lfclient_host = host
        self.lfclient_port = port
        self.ssid = ssid
        self.input = input
        self.security = security
        self.passwd = passwd
        self.radio = radio
        self.num_sta = num_sta
        self.start_id = start_id
        self.resource = resource
        self.sta_prefix = sta_prefix
        self.debug = debug_
        self.station_profile = self.new_station_profile()

    def build(self):
        station_list = []
        for idex, input in enumerate(self.input):
            # print(input)
            if "." in input['upstream']:
                num = input['upstream'].split('.')[1]
                sta_name = "1." + str(self.resource) + ".sta" + str(num)
                # print(sta_name)
                station_list.append(sta_name)
            else:
                station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=self.start_id,
                                                      end_id_=input['num_station'] - 1, padding_number_=100,
                                                      radio=self.radio)
                # implementation for non vlan pending ****
            logger.info("creating stations: %s" % (station_list))
            self.station_profile.use_security(self.security, self.ssid, self.passwd)
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            if self.station_profile.create(radio=self.radio, sta_names_=station_list, debug=self.debug):
                self._pass("Station creation succeeded.")
            else:
                self._fail("Station creation failed.")
                return False

            self.station_profile.admin_up()
            if self.wait_for_ip(station_list, timeout_sec=120):
                self._pass("All stations got IPs")
            else:
                self._fail("Stations failed to get IPs")

            logger.info("create udp endp")
            self.cx_profile_udp = self.new_l3_cx_profile()
            self.cx_profile_udp.side_a_min_bps = 128000
            self.cx_profile_udp.side_b_min_bps = 128000
            self.cx_profile_udp.side_a_min_pdu = 1200
            self.cx_profile_udp.side_b_min_pdu = 1500
            self.cx_profile_udp.report_timer = 1000
            self.cx_profile_udp.name_prefix = "udp"
            port_list = list(self.find_ports_like("%s+" % self.sta_prefix))
            # print("port list", port_list)
            if (port_list is None) or (len(port_list) < 1):
                raise ValueError("Unable to find ports named '%s'+" % self.sta_prefix)
            if self.cx_profile_udp.create(endp_type="lf_udp",
                                          side_a=port_list,
                                          sleep_time=0,
                                          side_b="%d.%s" % (self.resource, input['upstream']),
                                          suppress_related_commands=True):
                self._pass("UDP connections created.")
            else:
                self._fail("UDP connections could not be created.")

            # Create TCP endpoints
            print("create tcp endp")
            self.l3_tcp_profile = self.new_l3_cx_profile()
            self.l3_tcp_profile.side_a_min_bps = 128000
            self.l3_tcp_profile.side_b_min_bps = 56000
            self.l3_tcp_profile.name_prefix = "tcp"
            self.l3_tcp_profile.report_timer = 1000
            if self.l3_tcp_profile.create(endp_type="lf_tcp",
                                          sleep_time=0,
                                          side_a=list(self.find_ports_like("%s+" % self.sta_prefix)),
                                          side_b="%d.%s" % (self.resource, input['upstream']),
                                          suppress_related_commands=True):
                self._pass("TCP connections created.")
            else:
                self._fail("TCP connections not created.")

    def start(self):
        self.cx_profile_udp.start_cx()
        self.l3_tcp_profile.start_cx()

    def monitor_vlan_ip(self):
        # this function gives vlan ip dict eg{'eth2.100': '172.17.0.1'}
        vlan_ips = {}
        for i in self.input:
            # print(i)
            # TODO:  Properly detect if it is a real vlan interface, don't just match on a period in the name.
            if "." in i['upstream']:
                # print(str(i['upstream']) + " is a vlan upstream port")
                logger.info("checking VLAN upstream port: %s ip .." %(i['upstream']))
                data = self.json_get("ports/list?fields=IP")
                for val in data["interfaces"]:
                    for j in val:
                        if "1." + str(self.resource) + "." + str(i['upstream']) == j:
                            ip_upstream = val["1." + str(self.resource) + "." + str(i['upstream'])]['ip']
                            vlan_ips[i['upstream']] = ip_upstream
                            # print(ip_upstream)
                            # print(vlan_ips)
        return vlan_ips
        # {'eth2.100': '172.17.0.1', 'eth2.200': '172.18.0.1'}

    def monitor_non_vlan_ip(self):
        non_vlan_ips = {}
        for i in self.input:
            if "." not in i['upstream']:
                # print(str(i['upstream']) + " is not an vlan upstream port")
                logger.info("checking non-vlan ip ..")
                data = self.json_get("ports/list?fields=IP")
                for val in data["interfaces"]:
                    for j in val:
                        if "1." + str(self.resource) + "." + str(i['upstream']) == j:
                            ip_upstream = val["1." + str(self.resource) + "." + str(i['upstream'])]['ip']
                            non_vlan_ips[i['upstream']] = ip_upstream
                            # print(ip_upstream)
                            # print(non_vlan_ips)
        return non_vlan_ips

    def get_sta_ip(self):
        station_ip = {}
        port_list = list(self.find_ports_like("%s+" % self.sta_prefix))
        # print("port list", port_list)
        # port list ['1.1.sta200', '1.1.sta00', '1.1.sta100']
        for name, id in zip(port_list, self.input):
            # print(name)
            # print(type(name))
            x = id['upstream'].split('.')[1]
            # print(x)

            if name == "1." + str(self.resource) + ".sta" + str(x):
                data = self.json_get("ports/list?fields=IP")
                for i in data["interfaces"]:
                    # print(i)
                    for j in i:
                        if j == name:
                            sta_ip = i[name]['ip']
                            # print(sta_ip)
                            station_ip[id['upstream']] = sta_ip
            # print(station_ip)
            return station_ip

    # TODO:  Take cmd line arg for the 'eth2', and radios, and I guess port_list as well.  Or some
    # other way to not hard-code this.
    def get_sta_ip_for_more_vlan(self):
        input = [{'password': 'lanforge1', 'upstream': 'eth2.100', 'mac': '', 'num_station': 1, 'radio': 'wiphy4'},
                 {'password': 'lanforge2', 'upstream': 'eth2.200', 'mac': '', 'num_station': 1, 'radio': 'wiphy4'},
                 {'password': 'lanforge3', 'upstream': 'eth2', 'mac': '', 'num_station': 1, 'radio': 'wiphy0'}]
        port_list = ['1.1.sta200', '1.1.sta00', '1.1.sta100']
        upstream_list = []
        id_num = []
        station_ip = {}
        for i in input:
            if "." in i['upstream']:
                # print(i['upstream'])
                upstream_list.append(i['upstream'])
                x = i['upstream'].split('.')[1]
                id_num.append(x)

        # print(upstream_list)
        # print(id_num)
        # print(port_list)
        port = []

        for i in port_list:
            # print(i.split(".")[2])
            for num in id_num:
                if i.split(".")[2] == "sta" + str(num):
                    port.append(i)
        sorted_port = sorted(port)

        for name, id in zip(sorted_port, self.input):
            # print(name)
            # print(type(name))
            x = id['upstream'].split('.')[1]
            # print(x)

            if name == "1." + str(self.resource) + ".sta" + str(x):
                data = self.json_get("ports/list?fields=IP")
                for i in data["interfaces"]:
                    # print(i)
                    for j in i:
                        if j == name:
                            sta_ip = i[name]['ip']
                            # print(sta_ip)
                            station_ip[id['upstream']] = sta_ip
        # print(station_ip)
        return station_ip

    def get_non_vlan_sta_ip(self):
        station_nonvlan_ip = {}
        x = ""
        port_list = list(self.find_ports_like("%s+" % self.sta_prefix))
        # print("port list", port_list)
        for id in self.input:
            if "." not in id['upstream']:
                x = id['upstream']
        # print(x)
        for name in port_list:
            if name == "1.1.sta00":
                data = self.json_get("ports/list?fields=IP")
                for i in data["interfaces"]:
                    # print(i)
                    for j in i:
                        if j == name:
                            sta_ip = i[name]['ip']
                            # print(sta_ip)
        station_nonvlan_ip[x] = sta_ip
        return station_nonvlan_ip

    def compare_ip(self):
        vlan_ip = self.monitor_vlan_ip()
        station_ip = self.get_sta_ip()
        # vlan_ip = {'eth2.100': '172.17.0.1', 'eth2.200': '172.18.0.1'}
        # station_ip = {'eth2.100': '172.17.0.237', 'eth2.200': '172.18.100.222'}
        for i, j in zip(vlan_ip, station_ip):
            if i == j:
                x = vlan_ip[i].split('.')
                y = station_ip[j].split('.')
                if x[0] == y[0] and x[1] == y[1]:
                    self._pass("station got ip from vlan")
                    return "Pass"
                else:
                    self._fail("station did not got ip from vlan")
                    return "Fail"

    def compare_nonvlan_ip_nat(self):
        non_vlan_sta_ip = self.get_non_vlan_sta_ip()
        # print(non_vlan_sta_ip)
        for id in self.input:
            if "." not in id['upstream']:
                x = id['upstream']
        # print(non_vlan_sta_ip[x])
        non_vlan = non_vlan_sta_ip[x].split(".")
        # TODO:  This should not be hard-coded, take as cmd line arg input instead.
        if non_vlan[0] == "192" and non_vlan[1] == "168":
            # print("Pass")
            self._pass("NON-VLAN IP in NAT setup is as expected: %s" % non_vlan_sta_ip[x])
            x = 'Pass'
        else:
            self._fail("NON-VLAN IP in NAT set up is NOT as expected: %s" % non_vlan_sta_ip[x])
            x = "Fail"
        return x

    def compare_nonvlan_ip_bridge(self):
        upstream_ip = self.monitor_non_vlan_ip()
        non_vlan_sta_ip = self.get_non_vlan_sta_ip()

        for i, j in zip(upstream_ip, non_vlan_sta_ip):
            # print(i)
            if i == j:
                x = upstream_ip[i].split('.')
                y = non_vlan_sta_ip[j].split('.')
                if x[0] == y[0] and x[1] == y[1]:
                    self._pass("station got ip: %s from upstream: %s" % (non_vlan_sta_ip[j], upstream_ip[i]))
                    result1 = "Pass"
                else:
                    self._fail("station got ip: %s NOT from upstream: %s" % (non_vlan_sta_ip[j], upstream_ip[i]))
                    result1 = "Fail"
        return result1

    def postcleanup(self):
        self.cx_profile_udp.cleanup()
        self.l3_tcp_profile.cleanup()
        self.station_profile.cleanup()
        if LFUtils.wait_until_ports_disappear(base_url=self.lfclient_host, port_list=self.station_profile.station_names,
                                              debug=self.debug):
            self._pass("cleanup: Successfully deleted ports.")
        else:
            self._fail("cleanup: Failed to delete ports.")

        logger.info("post-cleanup completed")


def main():
    parser = Realm.create_basic_argparse(
        prog="lf_multipsk.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="lanforge webpage download Test Script")
    parser.add_argument('--n_vlan', help="type number of vlan using in test eg 1 or 2", default=1)
    parser.add_argument('--mode', help="Mode for lf_multipsk", default=None)
    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    # TODO:  Allow specifying this data on the command line.
    input_data = [{
        "password": args.passwd,
        "upstream": "eth2.100",
        "mac": "",
        "num_station": 1,
        "radio": "wiphy4"
        },
        {
            "password": "lanforge2",
            "upstream": "eth2.200",
            "mac": "",
            "num_station": 1,
            "radio": "wiphy4"
        },
        {
            "password": "lanforge2",
            "upstream": "eth2.300",
            "mac": "",
            "num_station": 1,
            "radio": "wiphy4"
        },
        {
            "password": "lanforge",
            "upstream": "eth2",
            "mac": "",
            "num_station": 1,
            "radio": "wiphy0"
        },

        ]
    multi_obj = MultiPsk(host=args.mgr,
                         port=args.mgr_port,
                         ssid=args.ssid,
                         passwd=args.passwd,
                         input=input_data,
                         security=args.security,
                         debug_=args.debug,
                         radio=args.radio)

    multi_obj.build()
    multi_obj.start()
    time.sleep(60)  #TODO:  Shouldn't need this much sleep, maybe some wait_for_foo method instead?
    multi_obj.monitor_vlan_ip()
    if args.n_vlan == "1":
        multi_obj.get_sta_ip()
    else:
        multi_obj.get_sta_ip_for_more_vlan()

    logger.info("checking for vlan ips")
    result = multi_obj.compare_ip()

    logger.info("now checking ip for non vlan port")
    multi_obj.monitor_non_vlan_ip()
    multi_obj.get_non_vlan_sta_ip()
    if args.mode == "BRIDGE":
        result1 = multi_obj.compare_nonvlan_ip_bridge()
    else:
        result1 = multi_obj.compare_nonvlan_ip_nat()

    # TODO:  Verify connections were able to start and pass traffic.

    logger.info("all result gathered")
    logger.info("clean up")
    multi_obj.postcleanup()

    if multi_obj.passes():
        multi_obj.exit_success()
    else:
        multi_obj.exit_fail()

if __name__ == '__main__':
    main()

