#!/usr/bin/env python3
'''
NAME: lf_csv.py

PURPOSE:
Common Library for generating csv for LANforge output
KPI - Key Performance Indicators

SETUP:
/lanforge/html-reports directory needs to be present or output generated in local file

EXAMPLE:
see: /py-scripts/lf_report_test.py for example

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
'''

import pandas as pd

class lf_csv:
    def __init__(self,
                 _columns=['Stations', 'bk', 'be', 'vi', 'vo'],
                 _rows=[['sta0001', 'sta0002', 'sta0003', 'sta0004', 'sta0005'],
                        [1, 2, 3, 4, 5],
                        [11, 22, 33, 44, 55],
                        [6, 7, 8, 9, 10],
                        [66, 77, 88, 99, 100]],
                 _filename='test.csv'):
        self.rows = _rows
        self.columns = _columns
        self.filename = _filename

    def generate_csv(self):
        df = {}
        for i in range(len(self.columns)):
            df[self.columns[i]] = self.rows[i]
        csv_df = pd.DataFrame(df)
        print(csv_df)
        csv_df.to_csv(self.filename, index=False, encoding='utf-8', na_rep='NA', float_format='%.2f')

# this layout may need to change
'''
kpi.csv : specific file that is used for the database, dashboard and blog post
A blank entry is a valid entry in some cases. 

    Date: date of run 
    test-rig : testbed that the tests are run on for example ct_us_001
    test-tag : test specific information to differenciate the test,  LANforge radios used, security modes (wpa2 , open)
    dut-hw-version : hardware version of the device under test
    dut-sw-version : software version of the device under test
    dut-model-num : model number / name of the device under test
    test-priority : test-priority is arbitrary number, choosing under 95 means it goes down at bottom of blog report, and higher priority goes at top.
    test-id : script or test name ,  AP Auto, wifi capacity, data plane, dfs
    short-description : short description of the test
    pass/fail : set blank for performance tests
    numeric-score : this is the value for the y-axis (x-axis is a timestamp),  numeric value of what was measured
    test-details : what was measured in the numeric-score,  e.g. bits per second, bytes per second, upload speed, minimum cx time (ms)
    Units : units used for the numeric-scort
    Graph-Group - For the dashboard the graph / panel to put the resutls in . Currently the dashboard is Grafana

'''
class lf_kpi_csv:
    def __init__(self,
                _kpi_headers = ['Date','test-rig','test-tag','dut-hw-version','dut-sw-version','dut-model-num',
                                'test-priority','test-id','short-description','pass/fail','numberic-score'
                                'test details','Units','Graph-Group','Subtest-Pass','Subtest-Fail'],
                _kpi_file='kpi.csv' #Currently this is the only file name accepted
                ):
        self.kpi_headers = _kpi_headers
        self.kpi_rows = ""
        self.kpi_filename = _kpi_file
                

if __name__ == "__main__":
    test = lf_csv()
    test.generate_csv()
