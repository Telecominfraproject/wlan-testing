#!/usr/bin/env python3
"""
    Script for creating a variable number of stations.
"""
import sys
import os
import importlib
import argparse
import pandas as pd
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class CreateStation(Realm):
    def __init__(self,
                 _ssid=None,
                 _security=None,
                 _password=None,
                 _host=None,
                 _port=None,
                 _sta_list=None,
                 _number_template="00000",
                 _radio="wiphy0",
                 _proxy_str=None,
                 _debug_on=False,
                 _up=True,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.sta_list = _sta_list
        self.radio = _radio
        self.timeout = 120
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
        if self.debug:
            print("----- Station List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.sta_list)
            print("---- ~Station List ----- ----- ----- ----- ----- ----- \n")

    def build(self):
        # Build stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)

        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        if self.up:
            self.station_profile.admin_up()

        self._pass("PASS: Station build finished")


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='create_station_from_df.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Create stations
            ''',
        description='''\
        create_station.py
        --------------------
        Command example:
        ./create_station_from_df.py
            --upstream_port eth1
            --df df.csv
            --security open
            --ssid netgear
            --passwd BLANK
            --debug
            ''')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--df', help='Which file do you want to build stations off of?', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.df)
    unique = df[['radio', 'ssid', 'passwd', 'security']].drop_duplicates().reset_index(drop=True)
    for item in unique.index:
        uniquedf = unique.iloc[item]
        df1 = df.merge(pd.DataFrame(uniquedf).transpose(), on=['radio', 'ssid', 'passwd', 'security'])
        if uniquedf['radio']:
            radio = uniquedf['radio']
        else:
            radio = args.radio
        station_list = df1['station']
        if uniquedf['ssid']:
            ssid = uniquedf['ssid']
            passwd = uniquedf['passwd']
            security = uniquedf['security']
        else:
            ssid = args.ssid
            passwd = args.passwd
            security = args.security
        create_station = CreateStation(_host=args.mgr,
                                       _port=args.mgr_port,
                                       _ssid=ssid,
                                       _password=passwd,
                                       _security=security,
                                       _sta_list=station_list,
                                       _radio=radio,
                                       _proxy_str=args.proxy,
                                       _debug_on=args.debug)

        create_station.build()
    print('Created %s stations' % len(unique.index))


if __name__ == "__main__":
    main()
