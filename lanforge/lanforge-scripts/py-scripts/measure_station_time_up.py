#!/usr/bin/env python3

"""
    Script for creating a variable number of stations.
"""
import sys
import os
import importlib
import argparse
import datetime
import pandas as pd
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class MeasureTimeUp(Realm):
    def __init__(self,
                 _ssid=None,
                 _security=None,
                 _password=None,
                 _host=None,
                 _port=None,
                 _num_sta=None,
                 _number_template="00000",
                 _radio=["wiphy0", "wiphy1"],
                 _proxy_str=None,
                 _debug_on=False,
                 _up=True,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _load=None,
                 _action="overwrite",
                 _clean_chambers="store_true",
                 _start=None,
                 _quiesce=None,
                 _stop=None,
                 _clean_dut="no"):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.num_sta = _num_sta
        self.radio = _radio
        # self.timeout = 120
        self.number_template = _number_template
        self.debug = _debug_on
        self.up = _up
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password,
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = 0
        self.load = _load
        self.action = _action
        self.clean_chambers = _clean_chambers
        self.start = _start
        self.quiesce = _quiesce
        self.stop = _stop
        self.clean_dut = _clean_dut

    def build(self):
        # Build stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)

        print("Creating stations")
        start_num = 0
        sta_names = []
        for item in self.radio:
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            sta_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=start_num,
                                                end_id=self.num_sta + start_num,
                                                padding_number=10000,
                                                radio=item)
            start_num = self.num_sta + start_num + 1
            sta_names.extend(sta_list)
            self.station_profile.create(radio=item, sta_names_=sta_list, debug=self.debug)

    def station_up(self):
        if self.up:
            self.station_profile.admin_up()
        self.wait_for_ip(station_list=self.station_profile.station_names)
        self._pass("PASS: Station build finished")

    def scenario(self):
        if self.load is not None:
            data = {
                "name": self.load,
                "action": self.action,
                "clean_dut": "no",
                "clean_chambers": "no"
            }
            if self.clean_dut:
                data['clean_dut'] = "yes"
            if self.clean_chambers:
                data['clean_chambers'] = "yes"
            print("Loading database %s" % self.load)
            self.json_post("/cli-json/load", data)

        elif self.start is not None:
            print("Starting test group %s..." % self.start)
            self.json_post("/cli-json/start_group", {"name": self.start})
        elif self.stop is not None:
            print("Stopping test group %s..." % self.stop)
            self.json_post("/cli-json/stop_group", {"name": self.stop})
        elif self.quiesce is not None:
            print("Quiescing test group %s..." % self.quiesce)
            self.json_post("/cli-json/quiesce_group", {"name": self.quiesce})


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='measure_station_time_up.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Measure how long it takes to up stations
            ''',

        description='''\
        measure_station_time_up.py
--------------------
Command example:
./measure_station_time_up.py
    --radio wiphy0
    --num_stations 3
    --security open
    --ssid netgear
    --passwd BLANK
    --debug
    --outfile
            ''')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--report_file', help='where you want to store results', required=True)

    args = parser.parse_args()

    dictionary = dict()
    for num_sta in list(filter(lambda x: (x % 2 == 0), [*range(0, 200)])):
        print(num_sta)
        try:
            create_station = MeasureTimeUp(_host=args.mgr,
                                           _port=args.mgr_port,
                                           _ssid=args.ssid,
                                           _password=args.passwd,
                                           _security=args.security,
                                           _num_sta=num_sta,
                                           _radio=["wiphy0", "wiphy1"],
                                           _proxy_str=args.proxy,
                                           _debug_on=args.debug,
                                           _load='FACTORY_DFLT')
            create_station.scenario()
            time.sleep(5.0 + num_sta / 10)
            start = datetime.datetime.now()
            create_station.build()
            built = datetime.datetime.now()
            create_station.station_up()
            stationsup = datetime.datetime.now()
            dictionary[num_sta] = [start, built, stationsup]
            create_station.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=station_list)
            time.sleep(5.0 + num_sta / 20)
        except:
            pass
    df = pd.DataFrame.from_dict(dictionary).transpose()
    df.columns = ['Start', 'Built', 'Stations Up']
    df['built duration'] = df['Built'] - df['Start']
    df['Up Stations'] = df['Stations Up'] - df['Built']
    df['duration'] = df['Stations Up'] - df['Start']
    for variable in ['built duration', 'duration']:
        df[variable] = [x.total_seconds() for x in df[variable]]
    df.to_pickle(args.report_file)


if __name__ == "__main__":
    main()
