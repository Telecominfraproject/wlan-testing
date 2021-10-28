#!/usr/bin/env python3

"""
The best way to use create_custom_dashboard by creating a graph_groups_file
The Graph_groups_file command is a txt file which lists the files which are going to be added to the Grafana Dashboard
It gets the columns of the files and from that it automatically determines the necessary titles on your dashboard.
"""
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

# from GrafanaRequest import GrafanaRequest
GrafanaRequest = importlib.import_module("py-dashboard.GrafanaRequest")
GrafanaRequest = GrafanaRequest.GrafanaRequest
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


class UseGrafana(GrafanaRequest):

    def read_csv(self, file):
        csv = open(file).read().split('\n')
        rows = list()
        for x in csv:
            if len(x) > 0:
                rows.append(x.split('\t'))
        return rows

    def get_values(self, csv, target):
        value = csv[0].index(target)
        results = []
        for row in csv[1:]:
            results.append(row[value])
        return results

    def get_units(self, target_csv):
        csv = self.read_csv(target_csv)
        graph_group = self.get_values(csv, 'Graph-Group')
        units = self.get_values(csv, 'Units')
        return dict(zip(graph_group, units))


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='grafana_profile.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Manage Grafana database''',
        description='''\
        grafana_profile.py
        ------------------
        Command example:
        ./grafana_profile.py
            --grafana_token 
            --dashbaord_name
            --scripts "Wifi Capacity"

        Create a custom dashboard with the following command:
        ./grafana_profile.py --create_custom yes 
                            --title Dataplane 
                            --influx_bucket lanforge 
                            --grafana_token TOKEN 
                            --graph_groups 'Per Stations Rate DL'
                            --graph_groups 'Per Stations Rate UL'
                            --graph_groups 'Per Stations Rate UL+DL'

        Create a snapshot of a dashboard:
        ./grafana_profile.py --grafana_token TOKEN
                             --grafana_host HOST
                             --create_snapshot
                             --title TITLE_OF_DASHBOARD
            ''')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--grafana_token', help='token to access your Grafana database', required=True)

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--dashboard_name', help='name of dashboard to create', default=None)
    optional.add_argument('--dashboard_uid', help='UID of dashboard to modify', default=None)
    optional.add_argument('--delete_dashboard',
                          help='Call this flag to delete the dashboard defined by UID',
                          default=None)
    optional.add_argument('--grafana_port', help='Grafana port if different from 3000', default=3000)
    optional.add_argument('--grafana_host', help='Grafana host', default='localhost')
    optional.add_argument('--list_dashboards', help='List dashboards on Grafana server', default=None)
    optional.add_argument('--dashboard_json', help='JSON of existing Grafana dashboard to import', default=None)
    optional.add_argument('--create_custom', help='Guided Dashboard creation', action='store_true')
    optional.add_argument('--dashboard_title', help='Titles of dashboards', default=None, action='append')
    optional.add_argument('--scripts', help='Scripts to graph in Grafana', default=None, action='append')
    optional.add_argument('--title', help='title of your Grafana Dashboard', default=None)
    optional.add_argument('--influx_bucket', help='Name of your Influx Bucket', default=None)
    optional.add_argument('--graph_groups', help='How you want to filter your graphs on your dashboard',
                          action='append', default=[None])
    optional.add_argument('--graph_groups_file',
                          help='File which determines how you want to filter your graphs on your dashboard',
                          default=None)
    optional.add_argument('--testbed', help='Which testbed you want to query', default=None)
    optional.add_argument('--kpi', help='KPI file(s) which you want to graph form', action='append', default=None)
    optional.add_argument('--datasource', help='Name of Influx database if different from InfluxDB', default='InfluxDB')
    optional.add_argument('--from_date', help='Date you want to start your Grafana dashboard from', default='now-1y')
    optional.add_argument('--graph_height', help='Custom height for the graph on grafana dashboard', default=8)
    optional.add_argument('--graph_width', help='Custom width for the graph on grafana dashboard', default=12)
    optional.add_argument('--create_snapshot', action='store_true')
    optional.add_argument('--list_snapshots', action='store_true')
    args = parser.parse_args()

    Grafana = UseGrafana(args.grafana_token,
                         args.grafana_host,
                         grafanajson_port=args.grafana_port
                         )
    if args.dashboard_name is not None:
        Grafana.create_dashboard(args.dashboard_name)

    if args.delete_dashboard is not None:
        Grafana.delete_dashboard(args.dashboard_uid)

    if args.list_dashboards is not None:
        Grafana.list_dashboards()

    if args.dashboard_json is not None:
        Grafana.create_dashboard_from_data(args.dashboard_json)

    if args.kpi is not None:
        args.graph_groups = args.graph_groups + Grafana.get_graph_groups(args.graph_groups)

    if args.create_custom:
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

    if args.create_snapshot:
        Grafana.create_snapshot(args.title)

    if args.list_snapshots:
        Grafana.list_snapshots()


if __name__ == "__main__":
    main()
