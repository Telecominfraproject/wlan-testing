#!/usr/bin/env python3
"""
NAME: test_generic.py

PURPOSE:
test_generic.py will create stations and endpoints to generate traffic based on a command-line specified command type.

This script will create a variable number of stations to test generic endpoints. Multiple command types can be tested
including ping, speedtest, generic types. The test will check the last-result attribute for different things
depending on what test is being run. Ping will test for successful pings, speedtest will test for download
speed, upload speed, and ping time, generic will test for successful generic commands

SETUP:
Enable the generic tab in LANforge GUI

EXAMPLE:

    LFPING:
        ./test_generic.py --radio 1.1.wiphy0 --ssid j-wpa2-153 --passwd j-wpa2-153 --security wpa2 --num_stations 4 \
        --type lfping --dest 10.40.0.1 --debug --mgr localhost --log_level info --report_file /tmp/ben.csv --test_duration 20s
    LFCURL (under construction):
        ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy1  --num_stations 26 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type lfcurl --dest 10.40.0.1
    GENERIC:
        ./test_generic.py --mgr localhost--mgr_port 4122 --radio wiphy1  --num_stations 2 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type generic
    SPEEDTEST:
        ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy2 --num_stations 13 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --type speedtest --speedtest_min_up 20
        --speedtest_min_dl 20 --speedtest_max_ping 150 --security wpa2
    IPERF3 (under construction):
        ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy1 --num_stations 3 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type iperf3

Use './test_generic.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import pprint
import argparse
import time
import datetime
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class GenTest(Realm):
    def __init__(self, ssid, security, passwd, sta_list, client, name_prefix, upstream, host="localhost", port=8080,
                 number_template="000", test_duration="5m", test_type="lfping", dest=None, cmd=None,
                 interval=1, radio=None, speedtest_min_up=None, speedtest_min_dl=None, speedtest_max_ping=None,
                 file_output=None,
                 loop_count=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        self.ssid = ssid
        self.radio = radio
        self.upstream = upstream
        self.sta_list = sta_list
        self.security = security
        self.passwd = passwd
        self.number_template = number_template
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.debug = _debug_on
        if client:
            self.client_name = client
        self.station_profile = self.new_station_profile()
        self.generic_endps_profile = self.new_generic_endp_profile()

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.passwd,
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = 0

        self.generic_endps_profile.name = name_prefix
        self.generic_endps_profile.type = test_type
        self.generic_endps_profile.dest = dest
        self.generic_endps_profile.cmd = cmd
        self.generic_endps_profile.interval = interval
        self.generic_endps_profile.file_output = file_output
        self.generic_endps_profile.loop_count = loop_count
        if speedtest_min_up is not None:
            self.generic_endps_profile.speedtest_min_up = float(speedtest_min_up)
        if speedtest_min_dl is not None:
            self.generic_endps_profile.speedtest_min_dl = float(speedtest_min_dl)
        if speedtest_max_ping is not None:
            self.generic_endps_profile.speedtest_max_ping = float(speedtest_max_ping)

    def check_tab_exists(self):
        response = self.json_get("generic")
        if response is None:
            return False
        else:
            return True

    def start(self):
        self.station_profile.admin_up()
        temp_stas = []
        for station in self.sta_list.copy():
            temp_stas.append(self.name_to_eid(station)[2])
        if self.debug:
            pprint.pprint(self.station_profile.station_names)

        if LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url,
                                             port_list=self.station_profile.station_names,
                                             debug_=self.debug):
            self._pass("All stations went admin up.")
        else:
            self._fail("All stations did NOT go admin up.")

        if self.wait_for_ip(station_list=temp_stas, ipv4=True, debug=self.debug, timeout_sec=-1):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()

        self.generic_endps_profile.start_cx()

    def stop(self):
        logger.info("Stopping Test...")
        self.generic_endps_profile.stop_cx()
        self.station_profile.admin_down()

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.passwd)
        self.station_profile.set_number_template(self.number_template)
        logger.info("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)

        if self.station_profile.create(radio=self.radio, sleep_time=0, sta_names_=self.sta_list, debug=self.debug):
            self._pass("Station creation completed.")
        else:
            self._fail("Station creation failed.")

        if self.generic_endps_profile.create(ports=self.station_profile.station_names, sleep_time=.5):
            self._pass("Generic endpoints creation completed.")
        else:
            self._fail("Generic endpoints NOT completed.")

    def cleanup(self, sta_list):
        self.generic_endps_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        if LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list, debug=self.debug):
            self._pass("Ports successfully cleaned up.")
        else:
            self._fail("Ports NOT successfully cleaned up.")


def main():
    optional = []
    optional.append({'name': '--mode', 'help': 'Used to force mode of stations'})
    optional.append({'name': '--ap', 'help': 'Used to force a connection to a particular AP'})
    optional.append({'name': '--output_format', 'default': 'csv', 'help': 'choose either csv or xlsx'})
    optional.append({'name': '--report_file', 'help': 'where you want to store results', 'default': None})
    optional.append({'name': '--a_min', 'help': '--a_min bps rate minimum for side_a', 'default': 256000})
    optional.append({'name': '--b_min', 'help': '--b_min bps rate minimum for side_b', 'default': 256000})
    optional.append({'name': '--gen_cols', 'help': 'Columns wished to be monitored from layer 3 endpoint tab',
                     'default': ['name', 'tx bytes', 'rx bytes']})
    optional.append({'name': '--port_mgr_cols', 'help': 'Columns wished to be monitored from port manager tab',
                     'default': ['ap', 'ip', 'parent dev']})
    optional.append(
        {'name': '--compared_report', 'help': 'report path and file which is wished to be compared with new report',
         'default': None})
    optional.append({'name': '--monitor_interval',
                     'help': 'how frequently do you want your monitor function to take measurements; 250ms, 35s, 2h',
                     'default': '2s'})

    parser = Realm.create_basic_argparse(
        prog='test_generic.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Create generic endpoints and test for their ability to execute chosen commands\n''',
        description='''
test_generic.py
--------------------
Generic command example:
python3 ./test_generic.py 
    --mgr localhost (optional)
    --mgr_port 4122 (optional)
    --upstream_port eth1 (optional)
    --radio wiphy0 (required)
    --num_stations 3 (optional)
    --security {open|wep|wpa|wpa2|wpa3} (required)
    --ssid netgear (required)
    --passwd admin123 (required)
    --type lfping  {generic|lfping|iperf3-client | speedtest | lf_curl} (required)
    --dest 10.40.0.1 (required - also target for iperf3)
    --test_duration 2m 
    --interval 1s 
    --debug 


    Example commands: 
    LFPING:
        ./test_generic.py --radio 1.1.wiphy0 --ssid j-wpa2-153 --passwd j-wpa2-153 --security wpa2 --num_stations 4 \\
        --type lfping --dest 10.40.0.1 --debug --mgr localhost --log_level info --report_file /tmp/ben.csv --test_duration 20s
    LFCURL (under construction):
    ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy1  --num_stations 26 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type lfcurl --dest 10.40.0.1
    GENERIC: 
    ./test_generic.py --mgr localhost--mgr_port 4122 --radio wiphy1  --num_stations 2 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type generic
    SPEEDTEST:
  ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy2 --num_stations 13 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --type speedtest --speedtest_min_up 20 
    --speedtest_min_dl 20 --speedtest_max_ping 150 --security wpa2
    IPERF3 (under construction):
   ./test_generic.py --mgr localhost --mgr_port 4122 --radio wiphy1 --num_stations 3 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --type iperf3 
''',
        more_optional=optional)

    parser.add_argument('--type', help='type of command to run: generic, lfping, iperf3-client, iperf3-server, lfcurl',
                        default="lfping")
    parser.add_argument('--cmd', help='specifies command to be run by generic type endp', default='')
    parser.add_argument('--dest', help='destination IP for command', default="10.40.0.1")
    parser.add_argument('--test_duration', help='duration of the test eg: 30s, 2m, 4h', default="2m")
    parser.add_argument('--interval', help='interval to use when running lfping (1s, 1m)', default=1)
    parser.add_argument('--speedtest_min_up', help='sets the minimum upload threshold for the speedtest type',
                        default=None)
    parser.add_argument('--speedtest_min_dl', help='sets the minimum download threshold for the speedtest type',
                        default=None)
    parser.add_argument('--speedtest_max_ping', help='sets the minimum ping threshold for the speedtest type',
                        default=None)
    parser.add_argument('--client', help='client to the iperf3 server', default=None)
    parser.add_argument('--file_output', help='location to output results of lf_curl, absolute path preferred',
                        default=None)
    parser.add_argument('--loop_count', help='determines the number of loops to use in lf_curl', default=None)

    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

        # Create directory

        # if file path with output file extension is not given...
        # check if home/lanforge/report-data exists. if not, save
        # in new folder based in current file's directory
    systeminfopath = None
    if args.report_file is None:
        new_file_path = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':',
                                                                                                 '-') + '-test_generic'  # create path name
        if os.path.exists('/home/lanforge/report-data/'):
            path = os.path.join('/home/lanforge/report-data/', new_file_path)
            os.mkdir(path)
        else:
            curr_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(curr_dir_path, new_file_path)
            os.mkdir(path)
        systeminfopath = str(path) + '/systeminfo.txt'

        if args.output_format in ['csv', 'json', 'html', 'hdf', 'stata', 'pickle', 'pdf', 'png', 'parquet',
                                  'xlsx']:
            report_f = str(path) + '/data.' + args.output_format
            output = args.output_format
        else:
            logger.info('Not supporting report format: %s. Defaulting to csv data file output type, naming it data.csv.' % args.output_format)
            report_f = str(path) + '/data.csv'
            output = 'csv'

    else:
        systeminfopath = str(args.report_file).split('/')[-1]
        report_f = args.report_file
        if args.output_format is None:
            output = str(args.report_file).split('.')[-1]
        else:
            output = args.output_format

    logger.warning("Saving final report data in: " + report_f)

    # Retrieve last data file
    compared_rept = None
    if args.compared_report:
        compared_report_format = args.compared_report.split('.')[-1]
        # if compared_report_format not in ['csv', 'json', 'dta', 'pkl','html','xlsx','parquet','h5']:
        if compared_report_format != 'csv':
            raise ValueError("Cannot process this file type. Please select a different file and re-run script.")
        else:
            compared_rept = args.compared_report

    station_list = LFUtils.portNameSeries(radio=args.radio,
                                          prefix_="sta",
                                          start_id_=0,
                                          end_id_=num_sta - 1,
                                          padding_number_=100)

    generic_test = GenTest(host=args.mgr, port=args.mgr_port,
                           number_template="00",
                           radio=args.radio,
                           sta_list=station_list,
                           name_prefix="GT",
                           test_type=args.type,
                           dest=args.dest,
                           cmd=args.cmd,
                           interval=1,
                           ssid=args.ssid,
                           upstream=args.upstream_port,
                           passwd=args.passwd,
                           security=args.security,
                           test_duration=args.test_duration,
                           speedtest_min_up=args.speedtest_min_up,
                           speedtest_min_dl=args.speedtest_min_dl,
                           speedtest_max_ping=args.speedtest_max_ping,
                           file_output=args.file_output,
                           loop_count=args.loop_count,
                           client=args.client,
                           _debug_on=args.debug)

    if not generic_test.check_tab_exists():
        raise ValueError("Error received from GUI, please ensure generic tab is enabled")
    generic_test.cleanup(station_list)
    generic_test.build()
    if not generic_test.passes():
        logger.error(generic_test.get_fail_message())
        generic_test.exit_fail()
    generic_test.start()
    if not generic_test.passes():
        logger.error(generic_test.get_fail_message())
        generic_test.exit_fail()

    mon_endp = generic_test.generic_endps_profile.created_endp;

    if type(args.gen_cols) is not list:
        generic_cols = list(args.gen_cols.split(","))
        # send col names here to file to reformat
    else:
        generic_cols = args.gen_cols
        # send col names here to file to reformat
    if type(args.port_mgr_cols) is not list:
        port_mgr_cols = list(args.port_mgr_cols.split(","))
        # send col names here to file to reformat
    else:
        port_mgr_cols = args.port_mgr_cols
        # send col names here to file to reformat
    logger.info("Generic Endp column names are...")
    logger.info(generic_cols)
    logger.info("Port Manager column names are...")
    logger.info(port_mgr_cols)
    try:
        monitor_interval = Realm.parse_time(args.monitor_interval).total_seconds()
    except ValueError as error:
        raise ValueError("The time string provided for monitor_interval argument is invalid. Please see supported time stamp increments and inputs for monitor_interval in --help. %s" % error)

    logger.info("Starting connections with 5 second settle time.")
    generic_test.start()
    time.sleep(5) # give traffic a chance to get started.

    resource_id = LFUtils.name_to_eid(args.radio)[1]

    must_increase_cols = None
    if args.type == "lfping":
        must_increase_cols = ["rx bytes"]

    generic_test.generic_endps_profile.monitor(generic_cols=generic_cols,
                                               must_increase_cols=must_increase_cols,
                                               sta_list=station_list,
                                               resource_id=resource_id,
                                               # port_mgr_cols=port_mgr_cols,
                                               report_file=report_f,
                                               systeminfopath=systeminfopath,
                                               duration_sec=Realm.parse_time(args.test_duration).total_seconds(),
                                               monitor_interval=monitor_interval,
                                               monitor_endps=mon_endp,
                                               output_format=output,
                                               compared_report=compared_rept,
                                               script_name='test_generic',
                                               arguments=args,
                                               debug=args.debug)

    logger.info("Done with connection monitoring")
    generic_test.stop()

    generic_test.cleanup(station_list)


    if len(generic_test.get_passed_result_list()) > 0:
        logger.info("Test-Generic Passing results:\n%s" % "\n".join(generic_test.get_passed_result_list()))
    if len(generic_test.generic_endps_profile.get_passed_result_list()) > 0:
        logger.info("Test-Generic Monitor Passing results:\n%s" % "\n".join(generic_test.generic_endps_profile.get_passed_result_list()))
    if len(generic_test.get_failed_result_list()) > 0:
        logger.warning("Test-Generic Failing results:\n%s" % "\n".join(generic_test.get_failed_result_list()))
    if len(generic_test.generic_endps_profile.get_failed_result_list()) > 0:
        logger.warning("Test-Generic Monitor Failing results:\n%s" % "\n".join(generic_test.generic_endps_profile.get_failed_result_list()))

    generic_test.generic_endps_profile.print_pass_fail()
    if generic_test.passes() and generic_test.generic_endps_profile.passes():
        generic_test.exit_success()
    else:
        generic_test.exit_fail()

if __name__ == "__main__":
    main()
