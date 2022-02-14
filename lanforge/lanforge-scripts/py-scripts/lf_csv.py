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

def main():
    test = lf_csv()
    test.generate_csv()

if __name__ == "__main__":
    main()    
