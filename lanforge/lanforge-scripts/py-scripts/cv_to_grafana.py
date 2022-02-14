#!/usr/bin/env python3
"""
This script loads and builds a Chamber View Scenario, runs WiFi Capacity Test, runs Dataplane Test,
and posts the results to Influx.
There are optional arguments which will create a Grafana dashboard which will import the data posted to
Influx from this script.
./cv_to_grafana.py
--mgr 192.168.1.4
--influx_host 192.168.100.201
--influx_token TOKEN
--influx_tag testbed Stidmatt-01
--influx_bucket stidmatt
--influx_org Candela
--pull_report
--ssid_dut "ssid_idx=0 ssid=lanforge security=WPA2 password=password bssid=04:f0:21:2c:41:84"
--line "Resource=1.1 Profile=default Amount=4 Uses-1=wiphy1 DUT=DUT_TO_GRAFANA_DUT Traffic=wiphy1 Freq=-1"
--line "Resource=1.1 Profile=upstream Amount=1 Uses-1=eth1 DUT=DUT_TO_GRAFANA_DUT Traffic=eth1 Freq=-1"
--dut DUT_TO_GRAFANA
--create_scenario DUT_TO_GRAFANA_SCENARIO
--station 1.1.sta00002
--duration 15s
--upstream 1.1.eth1
--radio2 1.1.wiphy1
--radio5 1.1.wiphy2
--dut5_0 linksys-8450
--set 'Basic Client Connectivity' 1
--set 'Multi-Station Throughput vs Pkt Size' 0
--set 'Multi Band Performance' 1
--set Stability 1
--set 'Throughput vs Pkt Size' 0
--set Capacity 0
--set Band-Steering 0

OPTIONAL GRAFANA ARGUMENTS
--grafana_token TOKEN
--grafana_host 192.168.100.201
--title "Grafana Dashboard"

The Grafana arguments are only required once. After the Grafana dashboard is built it will automatically update
as more data is added to the Influx database. Running the Grafana arguments to create a dashboard will do nothing.

The pull_report flag is to be used when running this on a computer which is different from the LANforge Manager.
It downloads the reports to the device which is running the script.

Each line argument adds a line to the Chamber View Scenario which you create in the script.

DUT flag gives the name of the DUT which is created by this script. It can be found in the DUT tab in LANforge Manager.

The station flag tells Dataplane test which station to test with.

The AP Auto test is triggered by the radio2 or radio5 flag. Select which tests in the AP Auto Test with the set argument.

AP Auto test has the following argument:
* max_stations_2: Specify maximum 2.4Ghz stations
* max_stations_5: Specify maximum 5Ghz stations
* max_stations_dual: Specify maximum stations for dual-band tests
* dut5_0: Specify 5Ghz DUT entry
* dut2_0: Specify 2Ghz DUT entry
DUT syntax is somewhat tricky:  DUT-name SSID BSID (bssid-idx), example: linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)
* radio2: Specify 2.4Ghz radio.  May be specified multiple times.
* radio5: Specify 5Ghz radio.  May be specified multiple times.
"""
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_wifi_capacity_test = importlib.import_module("py-scripts.lf_wifi_capacity_test")
WiFiCapacityTest = lf_wifi_capacity_test.WiFiCapacityTest
cv_test_manager = importlib.import_module("py-json.cv_test_manager")
create_chamberview = importlib.import_module("py-scripts.create_chamberview")
CreateChamberview = create_chamberview.CreateChamberview
create_chamberview_dut = importlib.import_module("py-scripts.create_chamberview_dut")
DUT = create_chamberview_dut.DUT
lf_dataplane_test = importlib.import_module("py-scripts.lf_dataplane_test")
DataplaneTest = lf_dataplane_test.DataplaneTest
grafana_profile = importlib.import_module("py-scripts.grafana_profile")
UseGrafana = grafana_profile.UseGrafana
lf_ap_auto_test = importlib.import_module("py-scripts.lf_ap_auto_test")
ApAutoTest = lf_ap_auto_test.ApAutoTest

cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser


def main():
    parser = argparse.ArgumentParser(
        prog='cv_to_grafana.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Run Wifi Capacity and Dataplane Test and record results to Grafana''',
        description='''\
        cv_to_grafana.py
        ------------------
        ./cv_to_grafana.py
            --mgr 
            --influx_host
            --influx_token
            --influx_tag testbed
            --influx_bucket 
            --influx_org 
            --pull_report
            --ssid_dut 
            --line 
            --line
            --dut 
            --create_scenario
            --station 
            --influx_tag 
            --duration 
            --upstream 
            '''
    )

    cv_add_base_parser(parser)  # see cv_test_manager.py

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
    parser.add_argument('--number_template',
                        help='Start the station numbering with a particular number. Default is 0000',
                        default=0000)
    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--ap', help='Used to force a connection to a particular AP')
    parser.add_argument("--num_stations", default=2)
    parser.add_argument("--mgr_port", default=8080)
    parser.add_argument("--upstream_port", default="1.1.eth1")
    parser.add_argument("--scenario", help="", default=None)
    parser.add_argument("--line", action='append', nargs='+',
                        help="line number", default=[])
    parser.add_argument("-ds", "--delete_scenario", default=False, action='store_true',
                        help="delete scenario (by default: False)")

    parser.add_argument("--create_scenario", "--create_lf_scenario", type=str,
                        help="name of scenario to be created")
    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth2")
    parser.add_argument("--station", type=str, default="",
                        help="Station to be used in this test, example: 1.1.sta01500")

    parser.add_argument("--dut", default="",
                        help="Specify DUT used by this test, example: linksys-8450")
    parser.add_argument("--download_speed", default="",
                        help="Specify requested download speed.  Percentage of theoretical is also supported.")
    parser.add_argument("--upload_speed", default="",
                        help="Specify requested upload speed.  Percentage of theoretical is also supported.  Default: 0")
    parser.add_argument("--graph_groups", help="File to save graph_groups to", default=None)
    parser.add_argument("--ssid_dut", action='append', nargs=1, help="SSID", default=[])

    parser.add_argument("--sw_version", default="NA", help="DUT Software version.")
    parser.add_argument("--hw_version", default="NA", help="DUT Hardware version.")
    parser.add_argument("--serial_num", default="NA", help="DUT Serial number.")
    parser.add_argument("--model_num", default="NA", help="DUT Model Number.")
    parser.add_argument("--report_dir", default="")
    parser.add_argument('--grafana_token', help='token to access your Grafana database')
    parser.add_argument('--grafana_port', help='Grafana port if different from 3000', default=3000)
    parser.add_argument('--grafana_host', help='Grafana host', default='localhost')

    # Flags for AP-Auto Test config

    parser.add_argument("--max_stations_2", type=int, default=-1,
                        help="Specify maximum 2.4Ghz stations")
    parser.add_argument("--max_stations_5", type=int, default=-1,
                        help="Specify maximum 5Ghz stations")
    parser.add_argument("--max_stations_dual", type=int, default=-1,
                        help="Specify maximum stations for dual-band tests")
    parser.add_argument("--dut5_0", type=str, default="",
                        help="Specify 5Ghz DUT entry.  Syntax is somewhat tricky:  DUT-name SSID BSID (bssid-idx), example: linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)")
    parser.add_argument("--dut2_0", type=str, default="",
                        help="Specify 2Ghz DUT entry.  Syntax is somewhat tricky:  DUT-name SSID BSID (bssid-idx), example: linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)")

    parser.add_argument("--radio2", action='append', nargs=1, default=[],
                        help="Specify 2.4Ghz radio.  May be specified multiple times.")
    parser.add_argument("--radio5", action='append', nargs=1, default=[],
                        help="Specify 5Ghz radio.  May be specified multiple times.")

    # Flags for Grafana

    parser.add_argument('--dashboard_title', help='Titles of dashboards', default=None, action='append')
    parser.add_argument('--scripts', help='Scripts to graph in Grafana', default=None, action='append')
    parser.add_argument('--title', help='title of your Grafana Dashboard', default=None)
    parser.add_argument('--testbed', help='Which testbed you want to query', default=None)
    parser.add_argument('--graph_groups_file',
                        help='File which determines how you want to filter your graphs on your dashboard',
                        default=None)
    parser.add_argument('--kpi', help='KPI file(s) which you want to graph form', action='append', default=None)
    parser.add_argument('--datasource', help='Name of Influx database if different from InfluxDB', default='InfluxDB')
    parser.add_argument('--from_date', help='Date you want to start your Grafana dashboard from', default='now-1y')
    parser.add_argument('--graph_height', help='Custom height for the graph on grafana dashboard', default=8)
    parser.add_argument('--graph_width', help='Custom width for the graph on grafana dashboard', default=12)

    args = parser.parse_args()

    cv_base_adjust_parser(args)

    # Create/update new DUT
    print("Make new DUT")
    new_dut = DUT(lfmgr=args.mgr,
                  port=args.port,
                  dut_name=args.dut,
                  ssid=args.ssid_dut,
                  sw_version=args.sw_version,
                  hw_version=args.hw_version,
                  serial_num=args.serial_num,
                  model_num=args.model_num,
                  )
    new_dut.setup()
    new_dut.add_ssids()
    new_dut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
    new_dut.cv_test.sync_cv()
    time.sleep(2)
    new_dut.cv_test.sync_cv()

    print("Build Chamber View Scenario")
    Create_Chamberview = CreateChamberview(lfmgr=args.mgr,
                                           port=args.port,
                                           )
    if args.delete_scenario:
        Create_Chamberview.clean_cv_scenario(type="Network-Connectivity", scenario_name=args.create_scenario)

    Create_Chamberview.setup(create_scenario=args.create_scenario,
                             line=args.line,
                             raw_line=args.raw_line)
    Create_Chamberview.build(args.create_scenario)

    print("Run WiFi Capacity Test")
    wifi_capacity = WiFiCapacityTest(lfclient_host=args.mgr,
                                     lf_port=args.mgr_port,
                                     lf_user=args.lf_user,
                                     lf_password=args.lf_password,
                                     instance_name='testing',
                                     config_name=args.config_name,
                                     upstream=args.upstream_port,
                                     batch_size=args.batch_size,
                                     loop_iter=args.loop_iter,
                                     protocol=args.protocol,
                                     duration=args.duration,
                                     pull_report=args.pull_report,
                                     load_old_cfg=args.load_old_cfg,
                                     download_rate=args.download_rate,
                                     upload_rate=args.upload_rate,
                                     sort=args.sort,
                                     enables=args.enable,
                                     disables=args.disable,
                                     raw_lines=args.raw_line,
                                     raw_lines_file=args.raw_lines_file,
                                     sets=args.set,
                                     graph_groups=args.graph_groups_file)
    wifi_capacity.apply_cv_scenario(args.scenario)
    wifi_capacity.build_cv_scenario()
    wifi_capacity.setup()
    wifi_capacity.run()
    wifi_capacity.check_influx_kpi(args)

    print("Run Dataplane test")

    CV_Test = DataplaneTest(lf_host=args.mgr,
                            lf_port=args.port,
                            lf_user=args.lf_user,
                            lf_password=args.lf_password,
                            instance_name='dataplane-instance',
                            config_name=args.config_name,
                            upstream=args.upstream,
                            pull_report=args.pull_report,
                            load_old_cfg=args.load_old_cfg,
                            download_speed=args.download_speed,
                            upload_speed=args.upload_speed,
                            duration=args.duration,
                            dut=args.dut,
                            station=args.station,
                            enables=args.enable,
                            disables=args.disable,
                            raw_lines=args.raw_line,
                            raw_lines_file=args.raw_lines_file,
                            sets=args.set,
                            graph_groups=args.graph_groups_file
                            )
    CV_Test.setup()
    CV_Test.run()

    CV_Test.check_influx_kpi(args)

    if len(args.radio2) + len(args.radio5) > 0:
        ApAuto = ApAutoTest(lf_host=args.mgr,
                            lf_port=args.port,
                            lf_user=args.lf_user,
                            lf_password=args.lf_password,
                            instance_name=args.instance_name,
                            config_name=args.config_name,
                            upstream=args.upstream,
                            pull_report=args.pull_report,
                            dut5_0=args.dut5_0,
                            dut2_0=args.dut2_0,
                            load_old_cfg=args.load_old_cfg,
                            max_stations_2=args.max_stations_2,
                            max_stations_5=args.max_stations_5,
                            max_stations_dual=args.max_stations_dual,
                            radio2=args.radio2,
                            radio5=args.radio5,
                            enables=args.enable,
                            disables=args.disable,
                            raw_lines=args.raw_line,
                            raw_lines_file=args.raw_lines_file,
                            sets=args.set,
                            graph_groups=args.graph_groups_file
                            )
        ApAuto.setup()
        ApAuto.run()

        ApAuto.check_influx_kpi(args)

    if args.grafana_token:
        print("Create Grafana dashboard")
        Grafana = UseGrafana(args.grafana_token,
                             args.grafana_port,
                             args.grafana_host
                             )
        Grafana.create_custom_dashboard(scripts=args.scripts,
                                        title=args.title,
                                        bucket=args.influx_bucket,
                                        graph_groups=args.graph_groups,
                                        graph_groups_file=args.graph_groups_file,
                                        testbed=args.testbed,
                                        datasource=args.datasource,
                                        from_date=args.from_date,
                                        graph_height=args.graph_height,
                                        graph__width=args.graph_width)


if __name__ == "__main__":
    main()
