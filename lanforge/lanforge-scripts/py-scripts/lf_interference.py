#!/usr/bin/env python3
"""
example: ./lf_interference.py --mgr 192.168.200.38 --port 8080 --lf_user lanforge --lf_password lanforge --dut_upstream 1.1.eth1
        --batch_size 1 --loop_iter 1 --pull_report_flag --protocol UDP-IPv4 --duration 240000 --download_rate 1Gbps
        --upload_rate 10Mbps --sort interleave --stations 1.1.sta0000 --create_stations --radio "wiphy3" --ssid "ASUS_2G"
        --security "wpa2" --paswd "Password@123" --delete_old_scenario --scenario_name "Automation" --vap_radio "wiphy0"
        --vap_freq "2437" --vap_ssid "routed-AP" --vap_passwd "something" --vap_security "wpa2" --vap_sta_number 1
        --vap_sta_radio "wiphy2" --vap_sta_name sta0000 --vap_sta_traffic_type lf_udp --vap_sta_upstream_port 1.1.vap0000
        --vap_sta_ssid "routed-AP" --vap_sta_passwd "something" --vap_sta_security "wpa2" --vap_sta_test_duration "60s"
        --vap_sta_a_min 600000000 --vap_sta_b_min 600000000 --vap_sta_mode 5 --vap_sta_cleanup --vap_sta_monitor_interval 10s

Note: Use this script to create co-channel and adjacent channel interference, by changing frequency argument.

Note: Provide same channel for co-channel interference, and adjacent channel for adjacent channel interference.

How does it work?
1. It creates a vap and station on user defined frequency
2. Start Wifi-capacity between station and DUT
3. start layer3 between VAP and Station on given frequency
4. we can notice drop in wifi capacity throughput once layer3 between vap-sta starts



"""
import subprocess
import sys
import os
import importlib
import argparse
import time
import logging

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_test = cv_test_manager.cv_test

create_chamberview = importlib.import_module("py-scripts.create_chamberview")
create_chamber = create_chamberview.CreateChamberview

add_profile = importlib.import_module("py-scripts.lf_add_profile")
lf_add_profile = add_profile.lf_add_profile

cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
set_port = importlib.import_module("py-json.LANforge.set_port")

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")

ipvt = importlib.import_module("py-scripts.test_ip_variable_time")
IPVariableTime = ipvt.IPVariableTime

logger = logging.getLogger(__name__)


class interference(cv_test):
    def __init__(self,
                 lfclient_host="192.168.200.36",
                 lf_port=8080,
                 ):
        super().__init__(lfclient_host=lfclient_host, lfclient_port=lf_port)

        self.lfclient_host = lfclient_host
        self.lf_port = lf_port
        self.lf_user= "lanforge"
        self.lf_passwd = "lanforge"
        self.COMMANDS = ["set_port"]
        self.desired_set_port_cmd_flags = []
        self.desired_set_port_current_flags = ["use_dhcp","dhcp"]  # do not default down, "if_down"
        self.desired_set_port_interest_flags = ["current_flags"]  # do not default down, "ifdown"
        # set_port 1 1 NA NA NA NA NA 2147483648 NA NA NA vap0000
        self.profile_name = None
        self.vap_radio = None
        self.freq = None
        self.set_upstream = True



    def setup_vap(self, scenario_name="Automation", radio="wiphy0", frequency="-1",name=None, vap_ssid=None, vap_pawd="[BLANK]", vap_security=None):

        profile = lf_add_profile(lf_mgr=self.lfclient_host,
                                 lf_port=self.lf_port,
                                 lf_user=self.lf_user,
                                 lf_passwd=self.lf_passwd,
                                 )

        profile.add_profile(
            _antenna=None,  # Antenna count for this profile.
            _bandwidth=None,  # 0 (auto), 20, 40, 80 or 160
            _eap_id=None,  # EAP Identifier
            _flags_mask=None,  # Specify what flags to set.
            _freq=frequency,  # WiFi frequency to be used, 0 means default.
            _instance_count=1,  # Number of devices (stations, vdevs, etc)
            _mac_pattern=None,  # Optional MAC-Address pattern, for instance: xx:xx:xx:*:*:xx
            _name=scenario_name,  # Profile Name. [R]
            _passwd=vap_pawd,  # WiFi Password to be used (AP Mode), [BLANK] means no password.
            _profile_flags="0x1009",  # Flags for this profile, see above.
            _profile_type="routed_ap",  # Profile type: See above. [W]
            _ssid=vap_ssid,  # WiFi SSID to be used, [BLANK] means any.
            _vid=None,  # Vlan-ID (only valid for vlan profiles).
            _wifi_mode=None  # WiFi Mode for this profile.
        )

    def setup_chamberview(self, delete_scenario=True,
                          scenario_name="Automation",
                          vap_radio="wiphy1",
                          profile_name=None,
                          freq=-1,
                          line=None):

        self.profile_name = profile_name
        self.vap_radio = vap_radio
        self.freq = freq

        chamber = create_chamber(lfmgr=self.lfclient_host,
                 port=self.lf_port)

        if delete_scenario:
            chamber.clean_cv_scenario(
                cv_type="Network-Connectivity",
                scenario_name=scenario_name)

        if self.set_upstream:
            self.raw_line_l1 = [[f'profile_link 1.1 {self.profile_name} 1 NA NA {self.vap_radio},AUTO {self.freq} NA'],
                                ["resource 1.1.0 0"],
                                ["profile_link 1.1 upstream-dhcp 1 NA NA eth1,AUTO -1 NA"]]
        else:
            self.raw_line_l1 = [[f'profile_link 1.1 {self.profile_name} 1 NA NA {self.vap_radio},AUTO {self.freq} NA'],
                                ["resource 1.1.0 0"]]

        print(self.raw_line_l1)

        chamber.setup(create_scenario=scenario_name,
                                 line=line,
                                 raw_line=self.raw_line_l1)


        return chamber

    def build_chamberview(self, chamber, scenario_name):
        chamber.build(scenario_name)        # self.apply_and_build_scenario("Sushant1")


    def build_and_setup_vap(self, delete_old_scenario=True, scenario_name="Automation", radio="wiphy0", frequency=-1,
                            vap_ssid=None, vap_pawd="[BLANK]", vap_security=None):
        self.setup_vap(scenario_name=scenario_name,
                       radio=radio,
                       frequency=frequency,
                       name=scenario_name,
                       vap_ssid=vap_ssid,
                       vap_pawd=vap_pawd,
                       vap_security=vap_security)


        chamber = self.setup_chamberview(delete_scenario=delete_old_scenario,
                               scenario_name=scenario_name,
                               vap_radio=radio,
                               profile_name=scenario_name,
                               freq=frequency,
                               line=None)


        self.build_chamberview(chamber=chamber,scenario_name=scenario_name)


    def build_vap_stations(self, create_vap_stations, vap_stations, vap_security, vap_ssid, vap_paswd, vap_sta_radio ):
        if create_vap_stations and vap_stations != "":
            vap_sta = vap_stations.split(",")
            self.station_profile.cleanup(vap_sta)
            self.station_profile.use_security(vap_security, vap_ssid, vap_paswd)
            self.station_profile.create(radio=vap_sta_radio, sta_names_=vap_sta, debug=self.debug)
            self.station_profile.admin_up()
            self.wait_for_ip(station_list=vap_sta)
            logger.info("VAP stations created")

    def build_dut_stations(self, create_dut_stations, dut_stations, dut_security, dut_ssid, dut_paswd, dut_sta_radio ):
        if create_dut_stations and dut_stations != "":
            dut_sta = dut_stations.split(",")
            self.station_profile.cleanup(dut_sta)
            self.station_profile.use_security(dut_security, dut_ssid, dut_paswd)
            self.station_profile.create(radio=dut_sta_radio, sta_names_=dut_sta, debug=self.debug)
            self.station_profile.admin_up()
            self.wait_for_ip(station_list=dut_sta)
            logger.info("DUT stations created")

    def create_layer3(self,num_stations=None,use_existing_sta=None,radio="wiphy0",sta_names=None,traffic_type=None,ipv6=None
                      ,upstream_port=None,ssid=None,passwd=None, security=None,test_duration=None,a_min=None,b_min=None
                      ,mode=None,ap=None,no_cleanup=None,layer3_cols=None,port_mgr_cols=None,monitor_interval=None,
                      debug=False):
        num_sta = 1

        print(f"radio {radio}")

        if num_stations:
            # logger.info("one")
            num_sta = int(num_stations)

        if not use_existing_sta:
            # logger.info("two")
            station_list = []

            for i in radio:
                station_list.append(LFUtils.portNameSeries(prefix_="R" + str(str(i)[-1]) + "-sta", start_id_=0,
                                                           end_id_=num_sta - 1,
                                                           padding_number_=10000, radio=i))
                print(station_list)

        else:
            logger.info("three")
            station_list = sta_names.split(",")

        CX_TYPES = ("tcp", "udp", "lf_tcp", "lf_udp")

        if not traffic_type or (traffic_type not in CX_TYPES):
            logger.error("cx_type needs to be lf_tcp, lf_udp, tcp, or udp, bye")
            exit(1)

        if ipv6:
            if traffic_type == "tcp" or traffic_type == "lf_tcp":
                traffic_type = "lf_tcp6"
            if traffic_type == "udp" or traffic_type == "lf_udp":
                traffic_type = "lf_udp6"
        else:
            if traffic_type == "tcp":
                traffic_type = "lf_tcp"
            if traffic_type == "udp":
                traffic_type = "lf_udp"

        ip_var_test = IPVariableTime(host=self.lfclient_host,
                                     port=self.lf_port,
                                     number_template="0000",
                                     sta_list=station_list,
                                     use_existing_sta=use_existing_sta,
                                     name_prefix="VT",
                                     upstream=upstream_port,
                                     ssid=ssid,
                                     password=passwd,
                                     radio=radio,
                                     security=security,
                                     test_duration=test_duration,
                                     use_ht160=False,
                                     side_a_min_rate=a_min,
                                     side_b_min_rate=b_min,
                                     mode=mode,
                                     ap=ap,
                                     no_cleanup=no_cleanup,
                                     layer3_cols=layer3_cols,
                                     port_mgr_cols=port_mgr_cols,
                                     monitor_interval=monitor_interval,
                                     ipv6=ipv6,
                                     traffic_type=traffic_type,
                                     _debug_on=debug)

        ip_var_test.build()


        return ip_var_test

    def run_layer3(self, ip_var_test):
        ip_var_test.run_only()

def main():
    parser = argparse.ArgumentParser(
        prog="lf_wifi_capacity_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        ./lf_interference.py --mgr 192.168.200.38 --port 8080 --lf_user lanforge --lf_password lanforge 
        --dut_upstream 1.1.eth1 --batch_size 1 --loop_iter 1 --protocol UDP-IPv4 --duration 240000 --download_rate 1Gbps
         --upload_rate 10Mbps --sort interleave --stations 1.1.sta0000 --create_stations --pull_report --radio "wiphy3" 
         --ssid "NETGEAR-2G" --security "wpa2" --paswd "[BLANK]" --delete_old_scenario --scenario_name "Automation" 
         --vap_radio "wiphy0" --vap_freq "2437" --vap_ssid "routed-AP" --vap_passwd "something" --vap_security "wpa2" 
         --vap_sta_number 1 --vap_sta_radio "wiphy2" --vap_sta_name sta0000 --vap_sta_traffic_type lf_udp 
         --vap_sta_upstream_port 1.1.vap0000 --vap_sta_ssid "routed-AP" --vap_sta_passwd "something" 
         --vap_sta_security "wpa2" --vap_sta_test_duration "60s" --vap_sta_a_min 600000000 --vap_sta_b_min 600000000 
         --vap_sta_mode 5 --vap_sta_cleanup --vap_sta_monitor_interval 10s    
               """)

    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--dut_upstream", type=str, default="1.1.eth1",
                        help="Upstream port for wifi capacity test ex. 1.1.eth1")
    parser.add_argument("-b", "--batch_size", type=str, default=1,
                        help="station increment ex. 1,2,3")
    parser.add_argument("-l", "--loop_iter", type=str, default=1,
                        help="Loop iteration ex. 1")
    parser.add_argument("-p", "--protocol", type=str, default="UDP-IPv4",
                        help="Protocol ex.TCP-IPv4")
    parser.add_argument("-d", "--duration", type=str, default="240000",
                        help="duration in ms. ex. 5000")
    parser.add_argument("--download_rate", type=str, default="1Gbps",
                        help="Select requested download rate.  Kbps, Mbps, Gbps units supported.  Default is 1Gbps")
    parser.add_argument("--upload_rate", type=str, default="10Mbps",
                        help="Select requested upload rate.  Kbps, Mbps, Gbps units supported.  Default is 10Mbps")
    parser.add_argument("--sort", type=str, default="interleave",
                        help="Select station sorting behaviour:  none | interleave | linear  Default is interleave.")
    parser.add_argument("-s", "--stations", type=str, default="1.1.sta0000",
                        help="If specified, these stations will be used.  If not specified, all available stations will be selected.  Example: 1.1.sta001,1.1.wlan0,...")
    parser.add_argument("-cs", "--create_stations", default=False, action='store_true',
                        help="create stations in lanforge (by default: False)")
    parser.add_argument("-prf", "--pull_report_flag", default=False, action='store_true',
                        help="pull report from lanforge (by default: False)")
    parser.add_argument("-radio", "--radio", default="wiphy3",
                        help="create stations in lanforge at this radio (by default: wiphy0)")
    parser.add_argument("-ssid", "--ssid", default="NETGEAR-2G",
                        help="ssid name")
    parser.add_argument("-security", "--security", default="wpa2",
                        help="ssid Security type")
    parser.add_argument("-paswd", "--paswd", default="Password@123",
                        help="ssid Password")
    parser.add_argument("--report_dir", default="")
    parser.add_argument("--scenario", default="")
    parser.add_argument("--graph_groups", help="File to save graph groups to", default=None)
    parser.add_argument("--local_lf_report_dir",
                        help="--local_lf_report_dir <where to pull reports to>  default '' put where dataplane script run from",
                        default="")
    parser.add_argument("--lf_logger_config_json",
                        help="--lf_logger_config_json <json file> , json configuration of logger")



    parser.add_argument("-dos", "--delete_old_scenario", default=True,
                        action='store_true',
                        help="To delete old scenarios (by default: True)")
    parser.add_argument("-sn", "--scenario_name", default="Automation",
                        help="Chamberview scenario name (by default: Automation")
    parser.add_argument("-vr", "--vap_radio", default="wiphy0",
                        help="vap radio name (by default: wiphy0")
    parser.add_argument("-vf", "--vap_freq", default="2437",
                        help="vap frequency (by default: 2437")
    parser.add_argument("-vs", "--vap_ssid", default="routed-AP",
                        help="vap ssid (by default: routed-AP")
    parser.add_argument("-vp", "--vap_passwd", default="something",
                        help="vap password (by default: something")
    parser.add_argument("-vse", "--vap_security", default="wpa2",
                        help="vap security (by default: wpa2")



    parser.add_argument("-vsnc", "--vap_sta_number", default=1,
                        help="To set vap station radio (by default: wiphy2)")
    parser.add_argument("-vsue", "--vap_sta_use_existing_sta",  default=False,
                        action='store_true',
                        help="To delete old scenarios (by default: True)")
    parser.add_argument("-vsr", "--vap_sta_radio", default="wiphy2",
                        help="To set vap station radio (by default: wiphy2)")
    parser.add_argument("-vsname", "--vap_sta_name", default="sta0000",
                        help="To set vap station name (by default: sta0000")
    parser.add_argument("-vstp", "--vap_sta_traffic_type", default="lf_udp",
                        help="To set vap station traffic (by default: lf_udp")
    parser.add_argument("-vsipv6", "--vap_sta_ipv6", default=None,
                        action='store_true',
                        help="")
    parser.add_argument("-vsupstream", "--vap_sta_upstream_port", default="1.1.vap0000",
                        help="")
    parser.add_argument("-vss", "--vap_sta_ssid", default="routed-AP",
                        help="vap ssid (by default: routed-AP")
    parser.add_argument("-vsp", "--vap_sta_passwd", default="something",
                        help="vap password (by default: something")
    parser.add_argument("-vssec", "--vap_sta_security", default="wpa2",
                        help="vap security (by default: wpa2")

    parser.add_argument("-vstd", "--vap_sta_test_duration", default="60s",
                        help="vap security (by default: wpa2")
    parser.add_argument("-vsam", "--vap_sta_a_min", default="600000000",
                        help="vap security (by default: wpa2")
    parser.add_argument("-vsbm", "--vap_sta_b_min", default="600000000",
                        help="vap security (by default: wpa2")
    parser.add_argument("-vsmode", "--vap_sta_mode", default="5",
                        help="vap security (by default: wpa2")
    parser.add_argument("-vsap", "--vap_sta_ap", default=None,
                        help="")
    parser.add_argument("-vsapc", "--vap_sta_cleanup", default=True,
                        action='store_true',
                        help="")
    parser.add_argument("-vsmi", "--vap_sta_monitor_interval", default="10s",
                        help="")
    parser.add_argument("-vsl3c", "--vap_sta_layer3_cols", default=['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate'],
                        help="")
    parser.add_argument("-vsmc", "--port_mgr_cols", default=['alias', 'ap', 'ip', 'parent dev', 'rx-rate'],
                        help="")
    parser.add_argument("-vsd", "--vap_sta_debug", default=False,
                        action='store_true',
                        help="")

    args = parser.parse_args()
    cv_base_adjust_parser(args)

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    lf_interference = interference(lfclient_host=args.mgr, lf_port=args.port)

    lf_mgr = args.mgr
    lf_port = args.port
    lf_user = args.lf_user
    lf_passwd = args.lf_password
    dut_upstreaam = args.dut_upstream
    batch_size = args.batch_size
    loop_iter = args.loop_iter
    dut_protocol = args.protocol
    dut_duration = args.duration
    dut_stations = args.stations
    dut_radio = args.radio
    dut_ssid = args.ssid
    dut_security = args.security
    dut_password = args.paswd
    dut_create_stations = args.create_stations

    if dut_create_stations:
        dut_create_stations = "--create_stations"
    else:
        dut_create_stations = ""

    pull_report = args.pull_report
    if pull_report:
        pull_report = "--pull_report"
    else:
        pull_report = ""

    # all needs user configurable upto config name , set default to something
    cmd_wifi_capacity = f"./lf_wifi_capacity_test.py --mgr {lf_mgr} --port {lf_port} --lf_user {lf_user} " \
                        f"--lf_password {lf_passwd} --instance_name wct_instance --config_name wifi_config " \
                        f"--upstream {dut_upstreaam} --batch_size {batch_size} --loop_iter {loop_iter} " \
                        f"--protocol {dut_protocol} --duration {dut_duration} {str(pull_report)} --stations {dut_stations} " \
                        f"{dut_create_stations} --radio {dut_radio} --ssid {dut_ssid} --security {dut_security} " \
                        f"--paswd {dut_password}"

    delete_old_scenario = args.delete_old_scenario
    vap_scenario_name = args.scenario_name
    vap_radio = args.vap_radio
    vap_freq = args.vap_freq
    vap_ssid = args.vap_ssid
    vap_passwd = args.vap_passwd
    vap_security = args.vap_security

    lf_interference.build_and_setup_vap(delete_old_scenario=delete_old_scenario, scenario_name=vap_scenario_name, radio=vap_radio,
                                        frequency=vap_freq, vap_ssid=vap_ssid, vap_pawd=vap_passwd, vap_security=vap_security)


    vap_sta_num = args.vap_sta_number
    vap_sta_use_existing_sta = args.vap_sta_use_existing_sta
    vap_sta_radio = args.vap_sta_radio
    vap_sta_name = args.vap_sta_name
    vap_sta_traffic_type = args.vap_sta_traffic_type
    vap_sta_ipv6 = args.vap_sta_ipv6
    vap_sta_upstream_port = args.vap_sta_upstream_port
    vap_sta_ssid = args.vap_sta_ssid
    vap_sta_passwd = args.vap_sta_passwd
    vap_sta_security = args.vap_sta_security
    vap_sta_test_duration = args.vap_sta_test_duration
    vap_sta_a_min = args.vap_sta_a_min
    vap_sta_b_min = args.vap_sta_b_min
    vap_sta_mode = args.vap_sta_mode
    vap_sta_ap = args.vap_sta_ap
    vap_sta_cleanup = args.vap_sta_cleanup
    vap_sta_monitor_interval = args.vap_sta_monitor_interval
    vap_sta_layer3_cols = args.vap_sta_layer3_cols
    vap_sta_port_mgr_cols = args.port_mgr_cols
    vap_sta_debug = args.vap_sta_debug

    obj = lf_interference.create_layer3(num_stations=vap_sta_num,use_existing_sta=vap_sta_use_existing_sta,radio=[vap_sta_radio],sta_names=vap_sta_name,
                                        traffic_type=vap_sta_traffic_type,ipv6=vap_sta_ipv6 ,upstream_port=[vap_sta_upstream_port],ssid=[vap_sta_ssid],
                                        passwd=[vap_sta_passwd], security=[vap_sta_security],test_duration=vap_sta_test_duration,a_min=vap_sta_a_min,
                                        b_min=vap_sta_b_min,mode=vap_sta_mode,ap=vap_sta_ap,no_cleanup=vap_sta_cleanup,monitor_interval=vap_sta_monitor_interval,
                                        layer3_cols=vap_sta_layer3_cols,debug=vap_sta_debug,
                                        port_mgr_cols=vap_sta_port_mgr_cols)

    proc = subprocess.Popen([cmd_wifi_capacity], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    time.sleep(120)
    lf_interference.run_layer3(obj)

if __name__ == "__main__":
    main()
