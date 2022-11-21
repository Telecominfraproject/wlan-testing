#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import json
import random
import string

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
csv_to_influx = importlib.import_module("py-scripts.csv_to_influx")
CSVtoInflux = csv_to_influx.CSVtoInflux
influx_add_parser_args = csv_to_influx.influx_add_parser_args
grafana_profile = importlib.import_module("py-scripts.grafana_profile")
UseGrafana = grafana_profile.UseGrafana
influx = importlib.import_module("py-scripts.influx_utils")
RecordInflux = influx.RecordInflux
InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")
influx_add_parser_args = InfluxRequest.influx_add_parser_args


class data_to_grafana(LFCliBase):
    def __init__(self,
                 _bucket=None,
                 _script=None,
                 _panel_name=None):
        self.bucket = _bucket
        self.script = _script
        self.panel_name = _panel_name
        pass

    @property
    def json_parser(self):
        options = string.ascii_lowercase + string.ascii_uppercase + string.digits
        uid = ''.join(random.choice(options) for _ in range(9))
        print(uid)
        json_dict = {
            "annotations": {
                "list": [
                    {
                        "builtIn": 1,
                        "datasource": "-- Grafana --",
                        "enable": True,
                        "hide": True,
                        "iconColor": "rgba(0, 211, 255, 1)",
                        "name": "Annotations & Alerts",
                        "type": "dashboard"
                    }
                ]
            },
            "editable": True,
            "gnetId": None,
            "graphTooltip": 0,
            "id": 10,
            "links": [],
            "panels": [
                {
                    "aliasColors": {},
                    "bars": False,
                    "dashLength": 10,
                    "dashes": False,
                    "datasource": "InfluxDB",
                    "fieldConfig": {
                        "defaults": {},
                        "overrides": []
                    },
                    "fill": 1,
                    "fillGradient": 0,
                    "gridPos": {
                        "h": 8,
                        "w": 12,
                        "x": 0,
                        "y": 0
                    },
                    "hiddenSeries": False,
                    "id": 2,
                    "legend": {
                        "avg": False,
                        "current": False,
                        "max": False,
                        "min": False,
                        "show": True,
                        "total": False,
                        "values": False
                    },
                    "lines": True,
                    "linewidth": 1,
                    "NonePointMode": "None",
                    "options": {
                        "alertThreshold": True
                    },
                    "percentage": False,
                    "pluginVersion": "7.5.4",
                    "pointradius": 2,
                    "points": False,
                    "renderer": "flot",
                    "seriesOverrides": [],
                    "spaceLength": 10,
                    "stack": False,
                    "steppedLine": False,
                    "targets": [
                        {
                            "delimiter": ",",
                            "groupBy": [
                                {
                                    "params": [
                                        "$__interval"
                                    ],
                                    "type": "time"
                                },
                                {
                                    "params": [
                                        "None"
                                    ],
                                    "type": "fill"
                                }
                            ],
                            "header": True,
                            "ignoreUnknown": False,
                            "orderByTime": "ASC",
                            "policy": "default",
                            "query": (
                                "from(bucket: \" %s \")\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  |> filter(fn: (r) => r[\"script\"] == \" %s\")\n  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: False)\n  |> yield(name: \"mean\")\n  " % self.bucket,
                                self.script),
                            "refId": "A",
                            "resultFormat": "time_series",
                            "schema": [],
                            "select": [
                                [
                                    {
                                        "params": [
                                            "value"
                                        ],
                                        "type": "field"
                                    },
                                    {
                                        "params": [],
                                        "type": "mean"
                                    }
                                ]
                            ],
                            "skipRows": 0,
                            "tags": []
                        }
                    ],
                    "thresholds": [],
                    "timeRegions": [],
                    "title": "json test",
                    "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                    },
                    "type": "graph",
                    "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                    },
                    "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                    ],
                    "yaxis": {
                        "align": False,
                        "alignLevel": None
                    }
                }
            ],
            "refresh": False,
            "schemaVersion": 27,
            "style": "dark",
            "tags": [],
            "templating": {
                "list": []
            },
            "time": {
                "from": "now-6h",
                "to": "now"
            },
            "timepicker": {},
            "timezone": "",
            "title": str(self.script),
            "uid": uid,
            "version": 2
        }
        return json.dumps(json_dict)


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='csv_to_grafana.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Auto-create Grafana dashboard from a CSV''',
        description='''\
        csv_to_grafana.py
        --------------------
        Command example:
        ./csv_to_grafana.py
            --grafana_token
            --influx_host
            --influx_org
            --influx_token
            --influx_bucket
            --target_csv
            --panel_name'''
    )
    required = parser.add_argument_group('required arguments')
    required.add_argument('--grafana_token', help='token to access your Grafana database', required=True)

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--grafana_port', help='Grafana port if different from 3000', default=3000)
    optional.add_argument('--grafana_host', help='Grafana host', default='localhost')
    optional.add_argument('--panel_name', help='Custom name of the panel', default=None)

    influx_add_parser_args(parser)

    # This argument is specific to this script, so not part of the generic influxdb parser args
    # method above.
    parser.add_argument('--target_csv', help='CSV file to record to influx database', default="")

    args = parser.parse_args()

    influxdb = RecordInflux(_influx_host=args.influx_host,
                            _influx_port=args.influx_port,
                            _influx_org=args.influx_org,
                            _influx_token=args.influx_token,
                            _influx_bucket=args.influx_bucket)

    csvtoinflux = CSVtoInflux(influxdb=influxdb,
                              target_csv=args.target_csv,
                              _influx_tag=args.influx_tag)

    GrafanaDB = UseGrafana(args.grafana_token,
                           args.grafana_port,
                           args.grafana_host)

    scriptname = csvtoinflux.script_name()

    csvtoinflux.post_to_influx()

    GrafanaDB.create_custom_dashboard(scripts=[scriptname],
                                      title=args.panel_name,
                                      bucket=args.influx_bucket)


if __name__ == "__main__":
    main()
