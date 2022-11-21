#!/usr/bin/env python3

"""
NAME: lf_kpi_csv.py

PURPOSE:
Common Library for generating kpi csv for LANforge output
KPI - Key Performance Indicators

SETUP:
None

EXAMPLE:


COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
"""
# may need pandas if a data frame is passed in
# import pandas as pd
import csv
import time
import argparse
import traceback

'''
Note teh delimiter for the kpi.csv is a tab

kpi.csv : specific file that is used for the database, dashboard and blog post
A blank entry is a valid entry in some cases.

    Date: date of run
    test-rig : testbed that the tests are run on for example ct_us_001
    test-tag : test specific information to differenciate the test,  LANforge radios used, security modes (wpa2 , open)
    dut-hw-version : hardware version of the device under test
    dut-sw-version : software version of the device under test
    dut-model-num : model number / name of the device under test
    dut-serial-num : serial number / serial number of the device under test
    test-priority : test-priority is arbitrary number, choosing under 95 means it goes down at bottom of blog report, and higher priority goes at top.
    test-id : script or test name ,  AP Auto, wifi capacity, data plane, dfs
    short-description : short description of the test
    pass/fail : set blank for performance tests
    numeric-score : this is the value for the y-axis (x-axis is a timestamp),  numeric value of what was measured
    test-details : what was measured in the numeric-score,  e.g. bits per second, bytes per second, upload speed, minimum cx time (ms)
    Units : units used for the numeric-scort
    Graph-Group - Items graphed together used by dashboard, For the lf_qa.py dashboard

'''


# NOTE, Passing in _kpi_headers only used for testing.
# Do Not pass in headers , Please use the defaults
class lf_kpi_csv:
    def __init__(self,
                # NOTE, Passing in _kpi_headers only used for testing.
                # Do Not pass in headers , Please use the defaults
                 _kpi_headers=None,
                 _kpi_filename='kpi.csv',  # Currently this is the only file name accepted
                 _kpi_path="",
                 _kpi_test_rig="TEST_RIG",
                 _kpi_test_tag="TEST_TAG",
                 _kpi_dut_hw_version="HW_VERSION",
                 _kpi_dut_sw_version="SW_VERSION",
                 _kpi_dut_model_num="MODEL_NUM",
                 _kpi_dut_serial_num="SERIAL_NUM",
                 _kpi_test_id="TEST_ID"
                 ):
        if _kpi_headers is None:
            _kpi_headers = ['Date', 'test-rig', 'test-tag', 'dut-hw-version', 'dut-sw-version', 'dut-model-num',
                            'dut-serial-num',
                            'test-priority', 'test-id', 'short-description', 'pass/fail', 'numeric-score',
                            'test details', 'Units', 'Graph-Group', 'Subtest-Pass', 'Subtest-Fail']
        self.kpi_headers = _kpi_headers
        self.kpi_filename = _kpi_filename
        self.kpi_full_path = ''
        self.kpi_file = ""
        self.kpi_path = _kpi_path
        self.kpi_test_rig = _kpi_test_rig
        self.kpi_test_tag = _kpi_test_tag
        self.kpi_dut_hw_version = _kpi_dut_hw_version
        self.kpi_dut_sw_version = _kpi_dut_sw_version
        self.kpi_dut_model_num = _kpi_dut_model_num
        self.kpi_dut_serial_num = _kpi_dut_serial_num
        self.kpi_test_id = _kpi_test_id
        self.kpi_rows = ""
        try:
            print("self.kpi_path {kpi_path}".format(kpi_path=self.kpi_path))
            print("self.kpi_filename {kpi_filename}".format(kpi_filename=self.kpi_filename))
            if self.kpi_path == "":
                kpifile = self.kpi_filename
            else:
                kpifile = self.kpi_path + '/' + self.kpi_filename
            print("kpifile {kpifile}".format(kpifile=kpifile))
            self.kpi_file = open(kpifile, 'w')
            self.kpi_writer = csv.DictWriter(self.kpi_file, delimiter="\t", fieldnames=self.kpi_headers)
            self.kpi_writer.writeheader()
        except Exception as x:
            print("lf_kpi_csv.py: {} WARNING unable to open".format(self.kpi_file))
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)

        self.kpi_dict = dict()
        self.kpi_dict['Date'] = '{date}'.format(date=int(time.time()))
        self.kpi_dict['test-rig'] = '{test_rig}'.format(test_rig=self.kpi_test_rig)
        self.kpi_dict['test-tag'] = '{test_tag}'.format(test_tag=self.kpi_test_tag)
        self.kpi_dict['dut-hw-version'] = '{dut_hw_version}'.format(dut_hw_version=self.kpi_dut_hw_version)
        self.kpi_dict['dut-sw-version'] = '{dut_sw_version}'.format(dut_sw_version=self.kpi_dut_sw_version)
        self.kpi_dict['dut-model-num'] = '{dut_model_num}'.format(dut_model_num=self.kpi_dut_model_num)
        self.kpi_dict['dut-serial-num'] = '{dut_serial_num}'.format(dut_serial_num=self.kpi_dut_serial_num)
        self.kpi_dict['test-priority'] = ''
        self.kpi_dict['test-id'] = '{test_id}'.format(test_id=self.kpi_test_id)
        self.kpi_dict['short-description'] = ''
        self.kpi_dict['pass/fail'] = ''
        self.kpi_dict['numeric-score'] = ''
        self.kpi_dict['test details'] = ''
        self.kpi_dict['Units'] = ''
        self.kpi_dict['Graph-Group'] = ''
        self.kpi_dict['Subtest-Pass'] = ''
        self.kpi_dict['Subtest-Fail'] = ''

    def kpi_csv_get_dict_update_time(self):
        self.kpi_dict['Date'] = '{date}'.format(date=round(time.time() * 1000))
        return self.kpi_dict

    def kpi_csv_write_dict(self, kpi_dict):
        self.kpi_writer.writerow(kpi_dict)
        self.kpi_file.flush()


def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='lf_kpi_csv.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_kpi_csv.py : unit test in lf_kpi_csv.py for exersiging lf_kpi_csv.py library
            ''',
        description='''\
lf_kpi_csv.py
-----------

Summary :
---------
lf_kpi_csv.py library :

    Date: date of run
    test-rig : testbed that the tests are run on for example ct_us_001
    test-tag : test specific information to differenciate the test,  LANforge radios used, security modes (wpa2 , open)
    dut-hw-version : hardware version of the device under test
    dut-sw-version : software version of the device under test
    dut-model-num : model number / name of the device under test
    dut-serial-num : serial number / serial number of the device under test
    test-priority : test-priority is arbitrary number, choosing under 95 means it goes down at bottom of blog report, and higher priority goes at top.
    test-id : script or test name ,  AP Auto, wifi capacity, data plane, dfs
    short-description : short description of the test
    pass/fail : set blank for performance tests
    numeric-score : this is the value for the y-axis (x-axis is a timestamp),  numeric value of what was measured
    test-details : what was measured in the numeric-score,  e.g. bits per second, bytes per second, upload speed, minimum cx time (ms)
    Units : units used for the numeric-scort
    Graph-Group - Items graphed together used by dashboard, For the lf_qa.py dashboard

Example :

    This module is included to assist in filling out the kpi.csv correctly
    The Unit test is used for helping to become familiar with the library

---------
            ''')

    parser.add_argument(
        '--local_lf_report_dir',
        help='--local_lf_report_dir override the report path, primary use when running test in test suite',
        default="")
    parser.add_argument("--test_rig", default="lanforge",
                        help="test rig for kpi.csv, testbed that the tests are run on")
    parser.add_argument("--test_tag", default="kpi_generation",
                        help="test tag for kpi.csv,  test specific information to differenciate the test")
    parser.add_argument("--dut_hw_version", default="hw_01",
                        help="dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument("--dut_sw_version", default="sw_01",
                        help="dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument("--dut_model_num", default="can_ap",
                        help="dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument("--test_priority", default="95",
                        help="dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument("--test_id", default="kpi_unit_test", help="test-id for kpi.csv,  script or test name")
    '''
    Other values that are included in the kpi.csv row.
    short-description : short description of the test
    pass/fail : set blank for performance tests
    numeric-score : this is the value for the y-axis (x-axis is a timestamp),  numeric value of what was measured
    test details : what was measured in the numeric-score,  e.g. bits per second, bytes per second, upload speed, minimum cx time (ms)
    Units : units used for the numeric-scort
    Graph-Group - For the lf_qa.py dashboard
    '''

    args = parser.parse_args()

    # Get the report path to create the kpi.csv path
    # kpi_path = report.get_report_path() in normal use case would get from lf_report.py library
    kpi_csv = lf_kpi_csv(
        _kpi_path=args.local_lf_report_dir,
        _kpi_test_rig=args.test_rig,
        _kpi_test_tag=args.test_tag,
        _kpi_dut_hw_version=args.dut_hw_version,
        _kpi_dut_sw_version=args.dut_sw_version,
        _kpi_dut_model_num=args.dut_model_num,
        _kpi_test_id=args.test_id)

    results_dict = kpi_csv.kpi_dict

    results_dict['Graph-Group'] = "graph_group"
    results_dict['short-description'] = "short_description"
    results_dict['numeric-score'] = "100"
    results_dict['Units'] = "Mbps"

    print("results_dict {results_dict}".format(results_dict=results_dict))
    print("date {date}".format(date=results_dict['Date']))

    kpi_csv.kpi_csv_write_dict(results_dict)

    # reuse the dictionary
    results_dict['Graph-Group'] = "graph_group_1_5"
    results_dict['short-description'] = "short_description_1_5"
    results_dict['numeric-score'] = "99"
    results_dict['Units'] = "Mbps"

    kpi_csv.kpi_csv_write_dict(results_dict)

    # append to a row to the existing dictionary
    results_dict_2 = kpi_csv.kpi_dict
    # modify an entry
    results_dict_2['test-tag'] = 'kpi_generation_2'
    results_dict_2['Graph-Group'] = "graph_group"
    results_dict_2['short-description'] = "short_description"
    results_dict_2['numeric-score'] = "100"
    results_dict_2['Units'] = "Mbps"
    print("results_dict_2 {results_dict_2}".format(results_dict_2=results_dict_2))
    print("date 2 {date}".format(date=results_dict_2['Date']))
    kpi_csv.kpi_csv_write_dict(results_dict_2)


if __name__ == "__main__":
    main()
