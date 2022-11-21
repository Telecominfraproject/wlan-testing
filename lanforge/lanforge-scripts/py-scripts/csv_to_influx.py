#!/usr/bin/env python3
import sys
import os
import importlib
from pathlib import Path
import argparse

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser
InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")
RecordInflux = InfluxRequest.RecordInflux
influx_add_parser_args = InfluxRequest.influx_add_parser_args


class CSVtoInflux:
    def __init__(self,
                 influx_host,
                 influx_port,
                 influx_org,
                 influx_token,
                 influx_bucket,
                 path):
        self.path = path
        self.influxdb = RecordInflux(_influx_host=influx_host,
                                     _influx_port=influx_port,
                                     _influx_org=influx_org,
                                     _influx_token=influx_token,
                                     _influx_bucket=influx_bucket)

    def glob(self):
        path = Path(self.path)
        self.kpi_list = list(path.glob('**/kpi.csv'))
        for kpi in self.kpi_list:
            self.influxdb.csv_to_influx(kpi)


def main():
    parser = argparse.ArgumentParser(
        prog='csv_to_influx.py'
    )
    cv_add_base_parser(parser)

    parser.add_argument('--path', action='append')

    args = parser.parse_args()

    cv_base_adjust_parser(args)

    csvtoinflux = CSVtoInflux(args.influx_host,
                              args.influx_port,
                              args.influx_org,
                              args.influx_token,
                              args.influx_bucket,
                              args.path)

    csvtoinflux.glob()


if __name__ == "__main__":
    main()
