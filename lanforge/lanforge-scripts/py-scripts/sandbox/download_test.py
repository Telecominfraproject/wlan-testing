#!/usr/bin/env python3
"""download_test.py will do lf_report::add_kpi(tags, 'throughput-download-bps', $my_value);"""
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
influx = importlib.import_module("py-scripts.influx")
RecordInflux = influx.RecordInflux
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class DownloadTest(Realm):
    def __init__(self,
                 _sta_list=None,
                 _ssid=None,
                 _password=None,
                 _security=None,
                 ):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.ssid=_ssid
        self.security = _security
        self.password = _password
        
        self.sta_list= _sta_list

def main():
    parser = LFCliBase.create_bare_argparse(
        prog='download_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''
        Download throughput test''',

    )
    parser.add_argument('--influx_user', help='Username for your Influx database', required=True)
    parser.add_argument('--influx_passwd', help='Password for your Influx database', required=True)
    parser.add_argument('--influx_db', help='Name of your Influx database', required=True)
    parser.add_argument('--longevity', help='How long you want to gather data', default='4h')
    parser.add_argument('--device', help='Device to monitor', action='append', required=True)
    parser.add_argument('--monitor_interval', help='How frequently you want to append to your database', default='5s')
    parser.add_argument('--target_kpi', help='Monitor only selected columns', action='append', default=target_kpi)

    args = parser.parse_args()


    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list = LFUtils.port_name_series(prefix="sta",
                                            start_id=0,
                                            end_id=num_sta-1,
                                            padding_number=10000,
                                            radio=args.radio)

    monitor_interval = LFCliBase.parse_time(args.monitor_interval).total_seconds()
    longevity = LFCliBase.parse_time(args.longevity).total_seconds()
    grapher = DownloadTest(_host=args.mgr,
                           _port=args.mgr_port,
                           _influx_db=args.influx_db,
                           _influx_user=args.influx_user,
                           _influx_passwd=args.influx_passwd,
                           _longevity=longevity,
                           _devices=args.device,
                           _monitor_interval=monitor_interval,
                           _target_kpi=args.target_kpi,
                           _ssid=args.ssid,
                           _password=args.passwd,
                           )

if __name__ == "__main__":
    main()
