#!/usr/bin/env python3
"""recordinflux will record data from existing lanforge endpoints to record to an already existing influx database.

This data can then be streamed in Grafana or any other graphing program the user chooses while this script runs.

https://influxdb-python.readthedocs.io/en/latest/include-readme.html


Use './recordinflux.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
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


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='recordinflux.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''
        Record data to an Influx database in order to be able stream to Grafana or other graphing software''',
        description='''
        recordinflux.py:
        ----------------------------
        Generic command example:
        ./recordinflux.py --influx_user  lanforge \\
        --influx_passwd password \\
        --influx_db lanforge \\
        --stations \\
        --longevity 5h'''
    )
    target_kpi = ['bps rx', 'rx bytes', 'pps rx', 'rx pkts', 'rx drop']
    parser.add_argument('--influx_user', help='Username for your Influx database')
    parser.add_argument('--influx_passwd', help='Password for your Influx database')
    parser.add_argument('--influx_token', help='Token for your Influx database', default=None)
    parser.add_argument('--influx_db', help='Name of your Influx database')
    parser.add_argument('--influx_bucket', help='Name of your Influx bucket')
    parser.add_argument('--influx_org', help='Name of your Influx Organization')
    parser.add_argument('--influx_port', help='Name of your Influx Port', default=8086)
    parser.add_argument('--longevity', help='How long you want to gather data', default='4h')
    parser.add_argument('--device', help='Device to monitor', action='append', required=True)
    parser.add_argument('--monitor_interval', help='How frequently you want to append to your database', default='5s')
    parser.add_argument('--target_kpi', help='Monitor only selected columns', action='append', default=target_kpi)
    args = parser.parse_args()
    monitor_interval = LFCliBase.parse_time(args.monitor_interval).total_seconds()
    longevity = LFCliBase.parse_time(args.longevity).total_seconds()
    tags = dict()
    tags['script'] = 'recordinflux'
    if args.influx_user is None:
        from InfluxRequest import RecordInflux
        grapher = RecordInflux(_influx_host=args.mgr,
                               _influx_port=args.influx_port,
                               _influx_bucket=args.influx_db,
                               _influx_token=args.influx_token,
                               _influx_org=args.influx_org)
        grapher.monitor_port_data(longevity=longevity,
                                  devices=args.device,
                                  monitor_interval=monitor_interval,
                                  tags=tags)

    else:
        from influx_utils import RecordInflux
        grapher = RecordInflux(_influx_host=args.mgr,
                               _influx_port=args.mgr_port,
                               _influx_db=args.influx_db,
                               _influx_user=args.influx_user,
                               _influx_passwd=args.influx_passwd)
        grapher.monitor_port_data(longevity=longevity,
                                  devices=args.device,
                                  monitor_interval=monitor_interval)


if __name__ == "__main__":
    main()
