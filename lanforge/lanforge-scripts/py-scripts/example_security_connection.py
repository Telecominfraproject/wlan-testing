#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import logging
from time import sleep

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class IPv4Test(Realm):
    def __init__(self, ssid, security, password, sta_list=None, ap=None, mode=0, number_template="00000",
                 host="localhost", port=8080, radio="wiphy0", _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.mode = mode
        self.ap = ap
        self.radio = radio
        self.security = security
        self.password = password
        self.sta_list = sta_list
        self.timeout = 120
        self.number_template = number_template
        self.debug = _debug_on
        self.station_profile = self.new_station_profile()

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.mode = self.mode
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = mode
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)

    def build(self):
        # Build stations
        # print("We've gotten into the build stations function")
        self.station_profile.use_security(
            self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        logger.info("Creating stations")
        self.station_profile.set_command_flag(
            "add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param(
            "set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)

        if self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug):
            self._pass("Station build successful")
        else:
            self._fail("Station build was not successful")

        self.station_profile.admin_up()
        if self.wait_for_ip(station_list=self.sta_list, debug=self.debug, timeout_sec=30):
            self._pass("Stations went admin up and acquired IP address")
        else:
            self._fail("Stations not able to acquire IP. Please check network input.")

    def cleanup(self, sta_list):
        self.station_profile.cleanup(sta_list)
        if LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                              debug=self.debug):
            self._pass("Successfully deleted stations.")
        else:
            self._fail("Could not successfully delete stations")


def main():

    parser = Realm.create_basic_argparse(
        prog='example_security_connection.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
             This python script creates a specified number of stations using with specified configuration.
             This verifies that the most basic form of security works with the LANforge device.
                ''',
        description='''\
        example_security_connection.py
        ---------------------------------------------------------------------------

    Example of command line to run:
   ./example_security_connection.py  
        --mgr localhost 
        --mgr_port 8080  
        --num_stations 6 
        --mode   1      
        --radio wiphy2
        --security {open|wep|wpa|wpa2|wpa3} 
        --ssid netgear-wpa3 
        --ap "00:0e:8e:78:e1:76"
        --passwd admin123-wpa3
        --radio 1.1.wiphy0
        --debug 
        --log_level info
            ''')
    # if required is not None:
    optional = None
    for agroup in parser._action_groups:
        if agroup.title == "optional arguments":
            optional = agroup
    if optional is not None:
        optional.add_argument('--mode', help=Realm.Help_Mode)
        optional.add_argument(
            '--ap', help='Add BSSID of access point to connect to')

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list = LFUtils.portNameSeries(prefix_="sta",
                                          start_id_=0,
                                          end_id_=num_sta-1,
                                          padding_number_=10000,
                                          radio=args.radio)
    ip_test = IPv4Test(host=args.mgr, port=args.mgr_port,
                       ssid=args.ssid, password=args.passwd,
                       radio=args.radio, mode=args.mode,
                       security=args.security, sta_list=station_list,
                       ap=args.ap, _debug_on=args.debug)
    ip_test.cleanup(station_list)
    ip_test.timeout = 60
    ip_test.build()

    if not args.no_cleanup:
        sleep(5)
        ip_test.cleanup(station_list)

    if ip_test.passes():
        ip_test.exit_success()
    else:
        ip_test.exit_fail()

if __name__ == "__main__":
    main()
