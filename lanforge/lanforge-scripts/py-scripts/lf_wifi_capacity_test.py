#!/usr/bin/env python3
"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

Note: This is a test file which will run a wifi capacity test.
    ex. on how to run this script (if stations are available in lanforge):
    The influx part can be skipped if you are not using influx/graphana.

    ./lf_wifi_capacity_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
             --instance_name this_inst --config_name test_con --upstream 1.1.eth2 --batch_size 1,5,25,50,100 --loop_iter 1 \
             --protocol UDP-IPv4 --duration 6000 --pull_report \
             --test_rig Testbed-01 \
             --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
             --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
             --influx_bucket ben \
             --influx_tag testbed Ferndale-01

    ex. on how to run this script (to create new stations):
    ./lf_wifi_capacity_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
             --instance_name wct_instance --config_name wifi_config --upstream 1.1.eth1 --batch_size 1,5,25 --loop_iter 1 \
             --protocol UDP-IPv4 --duration 6000 --pull_report --stations 1.1.sta0000,1.1.sta0001 \
             --create_stations --radio wiphy0 --ssid test-ssid --security open --paswd [BLANK] \
             --test_rig Testbed-01 --set DUT_NAME linksys-8450


Note:
    --pull_report == If specified, this will pull reports from lanforge to your code directory,
                    from where you are running this code

    --stations == Enter stations to use for wifi capacity

    --set DUT_NAME XXXX == Determines which DUT the wifi capacity test should use to get details on

Example of raw text config for Capacity, to show other possible options:

sel_port-0: 1.1.eth1
sel_port-1: 1.1.sta00000
sel_port-2: 1.1.sta00001
sel_port-3: 1.1.sta00002
sel_port-4: 1.1.sta00003
sel_port-5: 1.1.sta00004
sel_port-6: 1.1.sta00005
sel_port-7: 1.1.sta00006
sel_port-8: 1.1.sta00007
sel_port-9: 1.1.sta00008
sel_port-10: 1.1.sta00009
sel_port-11: 1.1.sta00010
sel_port-12: 1.1.sta00011
sel_port-13: 1.1.sta00012
sel_port-14: 1.1.sta00013
sel_port-15: 1.1.sta00014
sel_port-16: 1.1.sta00015
sel_port-17: 1.1.sta00016
sel_port-18: 1.1.sta00017
sel_port-19: 1.1.sta00018
sel_port-20: 1.1.sta00019
sel_port-21: 1.1.sta00020
sel_port-22: 1.1.sta00021
sel_port-23: 1.1.sta00022
sel_port-24: 1.1.sta00023
sel_port-25: 1.1.sta00024
sel_port-26: 1.1.sta00025
sel_port-27: 1.1.sta00026
sel_port-28: 1.1.sta00027
sel_port-29: 1.1.sta00028
sel_port-30: 1.1.sta00029
sel_port-31: 1.1.sta00030
sel_port-32: 1.1.sta00031
sel_port-33: 1.1.sta00032
sel_port-34: 1.1.sta00033
sel_port-35: 1.1.sta00034
sel_port-36: 1.1.sta00035
sel_port-37: 1.1.sta00036
sel_port-38: 1.1.sta00037
sel_port-39: 1.1.sta00038
sel_port-40: 1.1.sta00039
sel_port-41: 1.1.sta00040
sel_port-42: 1.1.sta00041
sel_port-43: 1.1.sta00042
sel_port-44: 1.1.sta00043
sel_port-45: 1.1.sta00044
sel_port-46: 1.1.sta00045
sel_port-47: 1.1.sta00046
sel_port-48: 1.1.sta00047
sel_port-49: 1.1.sta00048
sel_port-50: 1.1.sta00049
sel_port-51: 1.1.sta00500
sel_port-52: 1.1.sta00501
sel_port-53: 1.1.sta00502
sel_port-54: 1.1.sta00503
sel_port-55: 1.1.sta00504
sel_port-56: 1.1.sta00505
sel_port-57: 1.1.sta00506
sel_port-58: 1.1.sta00507
sel_port-59: 1.1.sta00508
sel_port-60: 1.1.sta00509
sel_port-61: 1.1.sta00510
sel_port-62: 1.1.sta00511
sel_port-63: 1.1.sta00512
sel_port-64: 1.1.sta00513
sel_port-65: 1.1.sta00514
sel_port-66: 1.1.sta00515
sel_port-67: 1.1.sta00516
sel_port-68: 1.1.sta00517
sel_port-69: 1.1.sta00518
sel_port-70: 1.1.sta00519
sel_port-71: 1.1.sta00520
sel_port-72: 1.1.sta00521
sel_port-73: 1.1.sta00522
sel_port-74: 1.1.sta00523
sel_port-75: 1.1.sta00524
sel_port-76: 1.1.sta00525
sel_port-77: 1.1.sta00526
sel_port-78: 1.1.sta00527
sel_port-79: 1.1.sta00528
sel_port-80: 1.1.sta00529
sel_port-81: 1.1.sta00530
sel_port-82: 1.1.sta00531
sel_port-83: 1.1.sta00532
sel_port-84: 1.1.sta00533
sel_port-85: 1.1.sta00534
sel_port-86: 1.1.sta00535
sel_port-87: 1.1.sta00536
sel_port-88: 1.1.sta00537
sel_port-89: 1.1.sta00538
sel_port-90: 1.1.sta00539
sel_port-91: 1.1.sta00540
sel_port-92: 1.1.sta00541
sel_port-93: 1.1.sta00542
sel_port-94: 1.1.sta00543
sel_port-95: 1.1.sta00544
sel_port-96: 1.1.sta00545
sel_port-97: 1.1.sta00546
sel_port-98: 1.1.sta00547
sel_port-99: 1.1.sta00548
sel_port-100: 1.1.sta00549
sel_port-101: 1.1.sta01000
sel_port-102: 1.1.sta01001
sel_port-103: 1.1.sta01002
sel_port-104: 1.1.sta01003
sel_port-105: 1.1.sta01004
sel_port-106: 1.1.sta01005
sel_port-107: 1.1.sta01006
sel_port-108: 1.1.sta01007
sel_port-109: 1.1.sta01008
sel_port-110: 1.1.sta01009
sel_port-111: 1.1.sta01010
sel_port-112: 1.1.sta01011
sel_port-113: 1.1.sta01012
sel_port-114: 1.1.sta01013
sel_port-115: 1.1.sta01014
sel_port-116: 1.1.sta01015
sel_port-117: 1.1.sta01016
sel_port-118: 1.1.sta01017
sel_port-119: 1.1.sta01018
sel_port-120: 1.1.sta01019
sel_port-121: 1.1.sta01020
sel_port-122: 1.1.sta01021
sel_port-123: 1.1.sta01022
sel_port-124: 1.1.sta01023
sel_port-125: 1.1.sta01024
sel_port-126: 1.1.sta01025
sel_port-127: 1.1.sta01026
sel_port-128: 1.1.sta01027
sel_port-129: 1.1.sta01028
sel_port-130: 1.1.sta01029
sel_port-131: 1.1.sta01030
sel_port-132: 1.1.sta01031
sel_port-133: 1.1.sta01032
sel_port-134: 1.1.sta01033
sel_port-135: 1.1.sta01034
sel_port-136: 1.1.sta01035
sel_port-137: 1.1.sta01036
sel_port-138: 1.1.sta01037
sel_port-139: 1.1.sta01038
sel_port-140: 1.1.sta01039
sel_port-141: 1.1.sta01040
sel_port-142: 1.1.sta01041
sel_port-143: 1.1.sta01042
sel_port-144: 1.1.sta01043
sel_port-145: 1.1.sta01044
sel_port-146: 1.1.sta01045
sel_port-147: 1.1.sta01046
sel_port-148: 1.1.sta01047
sel_port-149: 1.1.sta01048
sel_port-150: 1.1.sta01049
sel_port-151: 1.1.sta01500
sel_port-152: 1.1.sta01501
sel_port-153: 1.1.sta01502
sel_port-154: 1.1.sta01503
sel_port-155: 1.1.sta01504
sel_port-156: 1.1.sta01505
sel_port-157: 1.1.sta01506
sel_port-158: 1.1.sta01507
sel_port-159: 1.1.sta01508
sel_port-160: 1.1.sta01509
sel_port-161: 1.1.sta01510
sel_port-162: 1.1.sta01511
sel_port-163: 1.1.sta01512
sel_port-164: 1.1.sta01513
sel_port-165: 1.1.sta01514
sel_port-166: 1.1.sta01515
sel_port-167: 1.1.sta01516
sel_port-168: 1.1.sta01517
sel_port-169: 1.1.sta01518
sel_port-170: 1.1.sta01519
sel_port-171: 1.1.sta01520
sel_port-172: 1.1.sta01521
sel_port-173: 1.1.sta01522
sel_port-174: 1.1.sta01523
sel_port-175: 1.1.sta01524
sel_port-176: 1.1.sta01525
sel_port-177: 1.1.sta01526
sel_port-178: 1.1.sta01527
sel_port-179: 1.1.sta01528
sel_port-180: 1.1.sta01529
sel_port-181: 1.1.sta01530
sel_port-182: 1.1.sta01531
sel_port-183: 1.1.sta01532
sel_port-184: 1.1.sta01533
sel_port-185: 1.1.sta01534
sel_port-186: 1.1.sta01535
sel_port-187: 1.1.sta01536
sel_port-188: 1.1.sta01537
sel_port-189: 1.1.sta01538
sel_port-190: 1.1.sta01539
sel_port-191: 1.1.sta01540
sel_port-192: 1.1.sta01541
sel_port-193: 1.1.sta01542
sel_port-194: 1.1.sta01543
sel_port-195: 1.1.sta01544
sel_port-196: 1.1.sta01545
sel_port-197: 1.1.wlan4
sel_port-198: 1.1.wlan5
sel_port-199: 1.1.wlan6
sel_port-200: 1.1.wlan7
show_events: 1
show_log: 0
port_sorting: 0
kpi_id: WiFi Capacity
bg: 0xE0ECF8
test_rig:
show_scan: 1
auto_helper: 1
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
batch_size: 1
loop_iter: 1
duration: 6000
test_groups: 0
test_groups_subset: 0
protocol: UDP-IPv4
dl_rate_sel: Total Download Rate:
dl_rate: 1000000000
ul_rate_sel: Total Upload Rate:
ul_rate: 10000000
prcnt_tcp: 100000
l4_endp:
pdu_sz: -1
mss_sel: 1
sock_buffer: 0
ip_tos: 0
multi_conn: -1
min_speed: -1
ps_interval: 60-second Running Average
fairness: 0
naptime: 0
before_clear: 5000
rpt_timer: 1000
try_lower: 0
rnd_rate: 1
leave_ports_up: 0
down_quiesce: 0
udp_nat: 1
record_other_ssids: 0
clear_reset_counters: 0
do_pf: 0
pf_min_period_dl: 0
pf_min_period_ul: 0
pf_max_reconnects: 0
use_mix_pdu: 0
pdu_prcnt_pps: 1
pdu_prcnt_bps: 0
pdu_mix_ln-0: 
show_scan: 1
show_golden_3p: 0
save_csv: 0
show_realtime: 1
show_pie: 1
show_per_loop_totals: 1
show_cx_time: 1
show_dhcp: 1
show_anqp: 1
show_4way: 1
show_latency: 1

"""
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
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

logger = logging.getLogger(__name__)


class WiFiCapacityTest(cv_test):
    def __init__(self,
                 lfclient_host="localhost",
                 lf_port=8080,
                 ssh_port=22,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 instance_name="wct_instance",
                 config_name="wifi_config",
                 upstream="eth1",
                 batch_size="1",
                 loop_iter="1",
                 protocol="UDP-IPv4",
                 duration="5000",
                 pull_report=False,
                 load_old_cfg=False,
                 upload_rate="10Mbps",
                 download_rate="1Gbps",
                 sort="interleave",
                 stations="",
                 create_stations=False,
                 radio="wiphy0",
                 security="open",
                 paswd="[BLANK]",
                 ssid="",
                 enables=None,
                 disables=None,
                 raw_lines=None,
                 raw_lines_file="",
                 sets=None,
                 influx_host="localhost",
                 influx_port=8086,
                 report_dir="",
                 graph_groups=None,
                 test_rig="",
                 test_tag="",
                 local_lf_report_dir=""
                 ):
        super().__init__(lfclient_host=lfclient_host, lfclient_port=lf_port)

        if enables is None:
            enables = []
        if disables is None:
            disables = []
        if raw_lines is None:
            raw_lines = []
        if sets is None:
            sets = []
        self.lfclient_host = lfclient_host
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_password = lf_password
        self.station_profile = self.new_station_profile()
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.instance_name = instance_name
        self.config_name = config_name
        self.test_name = "WiFi Capacity"
        self.batch_size = batch_size
        self.loop_iter = loop_iter
        self.protocol = protocol
        self.duration = duration
        self.upload_rate = upload_rate
        self.download_rate = download_rate
        self.upstream = upstream
        self.sort = sort
        self.stations = stations
        self.create_stations = create_stations
        self.security = security
        self.ssid = ssid
        self.paswd = paswd
        self.ssh_port = ssh_port
        self.radio = radio
        self.enables = enables
        self.disables = disables
        self.raw_lines = raw_lines
        self.raw_lines_file = raw_lines_file
        self.sets = sets
        self.influx_host = influx_host,
        self.influx_port = influx_port
        self.report_dir = report_dir
        self.graph_groups = graph_groups
        self.test_rig = test_rig
        self.test_tag = test_tag
        self.local_lf_report_dir = local_lf_report_dir

    def setup(self):
        if self.create_stations and self.stations != "":
            sta = self.stations.split(",")
            self.station_profile.cleanup(sta)
            self.station_profile.use_security(self.security, self.ssid, self.paswd)
            self.station_profile.create(radio=self.radio, sta_names_=sta, debug=self.debug)
            self.station_profile.admin_up()
            self.wait_for_ip(station_list=sta)
            logger.info("stations created")

    def run(self):
        self.sync_cv()
        time.sleep(2)
        self.sync_cv()

        self.rm_text_blob(self.config_name, "Wifi-Capacity-")  # To delete old config with same name
        self.show_text_blob(None, None, False)

        # Test related settings
        cfg_options = []

        eid = LFUtils.name_to_eid(self.upstream)
        port = "%i.%i.%s" % (eid[0], eid[1], eid[2])

        port_list = [port]
        if self.stations == "":
            stas = self.station_map()  # See realm
            for eid in stas.keys():
                port_list.append(eid)
        else:
            stas = self.stations.split(",")
            for s in stas:
                port_list.append(s)

        idx = 0
        for eid in port_list:
            add_port = "sel_port-" + str(idx) + ": " + eid
            self.create_test_config(self.config_name, "Wifi-Capacity-", add_port)
            idx += 1

        self.apply_cfg_options(cfg_options, self.enables, self.disables, self.raw_lines, self.raw_lines_file)

        if self.batch_size != "":
            cfg_options.append("batch_size: " + self.batch_size)
        if self.loop_iter != "":
            cfg_options.append("loop_iter: " + self.loop_iter)
        if self.protocol != "":
            cfg_options.append("protocol: " + str(self.protocol))
        if self.duration != "":
            cfg_options.append("duration: " + self.duration)
        if self.upload_rate != "":
            cfg_options.append("ul_rate: " + self.upload_rate)
        if self.download_rate != "":
            cfg_options.append("dl_rate: " + self.download_rate)
        if self.test_rig != "":
            cfg_options.append("test_rig: " + self.test_rig)
        if self.test_tag != "":
            cfg_options.append("test_tag: " + self.test_tag)

        cfg_options.append("save_csv: 1")

        blob_test = "Wifi-Capacity-"

        # We deleted the scenario earlier, now re-build new one line at a time.
        self.build_cfg(self.config_name, blob_test, cfg_options)

        cv_cmds = []

        if self.sort == 'linear':
            cmd = "cv click '%s' 'Linear Sort'" % self.instance_name
            cv_cmds.append(cmd)
        if self.sort == 'interleave':
            cmd = "cv click '%s' 'Interleave Sort'" % self.instance_name
            cv_cmds.append(cmd)

        self.create_and_run_test(self.load_old_cfg, self.test_name, self.instance_name,
                                 self.config_name, self.sets,
                                 self.pull_report, self.lfclient_host, self.lf_user, self.lf_password,
                                 cv_cmds, ssh_port=self.ssh_port, graph_groups_file=self.graph_groups, local_lf_report_dir=self.local_lf_report_dir)

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name

        self.rm_text_blob(self.config_name, "Wifi-Capacity-")  # To delete old config with same name


def main():
    parser = argparse.ArgumentParser(
        prog="lf_wifi_capacity_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        ./lf_wifi_capacity_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
             --instance_name wct_instance --config_name wifi_config --upstream 1.1.eth1 --batch_size 1 --loop_iter 1 \
             --protocol UDP-IPv4 --duration 6000 --pull_report --stations 1.1.sta0000,1.1.sta0001 \
             --create_stations --radio wiphy0 --ssid test-ssid --security open --paswd [BLANK] \
             --test_rig Testbed-01 -test_tag TAG\
             --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
             --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
             --influx_bucket ben \
             --influx_tag testbed Ferndale-01
               """)

    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth1")
    parser.add_argument("-b", "--batch_size", type=str, default="",
                        help="station increment ex. 1,2,3")
    parser.add_argument("-l", "--loop_iter", type=str, default="",
                        help="Loop iteration ex. 1")
    parser.add_argument("-p", "--protocol", type=str, default="",
                        help="Protocol ex.TCP-IPv4")
    parser.add_argument("-d", "--duration", type=str, default="",
                        help="duration in ms. ex. 5000")
    parser.add_argument("--download_rate", type=str, default="1Gbps",
                        help="Select requested download rate.  Kbps, Mbps, Gbps units supported.  Default is 1Gbps")
    parser.add_argument("--upload_rate", type=str, default="10Mbps",
                        help="Select requested upload rate.  Kbps, Mbps, Gbps units supported.  Default is 10Mbps")
    parser.add_argument("--sort", type=str, default="interleave",
                        help="Select station sorting behaviour:  none | interleave | linear  Default is interleave.")
    parser.add_argument("-s", "--stations", type=str, default="",
                        help="If specified, these stations will be used.  If not specified, all available stations will be selected.  Example: 1.1.sta001,1.1.wlan0,...")
    parser.add_argument("-cs", "--create_stations", default=False, action='store_true',
                        help="create stations in lanforge (by default: False)")
    parser.add_argument("-radio", "--radio", default="wiphy0",
                        help="create stations in lanforge at this radio (by default: wiphy0)")
    parser.add_argument("-ssid", "--ssid", default="",
                        help="ssid name")
    parser.add_argument("-security", "--security", default="open",
                        help="ssid Security type")
    parser.add_argument("-paswd", "--paswd", default="[BLANK]",
                        help="ssid Password")
    parser.add_argument("--report_dir", default="")
    parser.add_argument("--scenario", default="")
    parser.add_argument("--graph_groups", help="File to save graph groups to", default=None)
    parser.add_argument("--local_lf_report_dir", help="--local_lf_report_dir <where to pull reports to>  default '' put where dataplane script run from", default="")
    parser.add_argument("--lf_logger_config_json", help="--lf_logger_config_json <json file> , json configuration of logger")


    args = parser.parse_args()

    cv_base_adjust_parser(args)

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    WFC_Test = WiFiCapacityTest(lfclient_host=args.mgr,
                                lf_port=args.port,
                                lf_user=args.lf_user,
                                lf_password=args.lf_password,
                                instance_name=args.instance_name,
                                config_name=args.config_name,
                                upstream=args.upstream,
                                batch_size=args.batch_size,
                                loop_iter=args.loop_iter,
                                protocol=args.protocol,
                                duration=args.duration,
                                pull_report=args.pull_report,
                                load_old_cfg=args.load_old_cfg,
                                download_rate=args.download_rate,
                                upload_rate=args.upload_rate,
                                sort=args.sort,
                                stations=args.stations,
                                create_stations=args.create_stations,
                                radio=args.radio,
                                ssid=args.ssid,
                                security=args.security,
                                paswd=args.paswd,
                                enables=args.enable,
                                disables=args.disable,
                                raw_lines=args.raw_line,
                                raw_lines_file=args.raw_lines_file,
                                sets=args.set,
                                graph_groups=args.graph_groups,
                                test_rig=args.test_rig,
                                test_tag=args.test_tag,
                                local_lf_report_dir=args.local_lf_report_dir
                                )
    WFC_Test.setup()
    WFC_Test.run()

    WFC_Test.check_influx_kpi(args)


if __name__ == "__main__":
    main()
