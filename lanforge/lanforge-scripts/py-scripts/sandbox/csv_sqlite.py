#!/usr/bin/env python3
'''
File: will search sub diretories for kpi.csv and place the data into an sqlite database
Usage: csv_sqlite.py --path <path to directories to traverse> --database <name of database>
'''

import sys
if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit
import pandas as pd
import sqlite3
import argparse
from  pathlib import Path

class csv_to_sqlite():
    def __init__(self,
                _path = '.',
                _file = 'kpi.csv',
                _database = 'qa_db',
                _table = 'qa_table'):
        self.path = _path
        self.file = _file
        self.database = _database
        self.table = _table

    # information on sqlite database
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    def store(self):
        path = Path(self.path)
        kpi_list = list(path.glob('**/{}'.format(self.file)))

        df = pd.DataFrame()
        for kpi in kpi_list:
            append_df = pd.read_csv(kpi, sep='\t')
            df = df.append(append_df, ignore_index=True)

        print(self.database)
        conn = sqlite3.connect(self.database) 
        #data may be appended setting if_exists='append'
        df.to_sql(self.table,conn,if_exists='replace')
        conn.close()

def main():

    parser = argparse.ArgumentParser(
        prog='csv_sqlite.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        read kpi.csv into sqlit database

            ''',
        description='''\
File: will search path recursivly for kpi.csv and place into sqlite database
Usage: csv_sqlite.py --path <path to directories to traverse> --database <name of database>

        ''')
    parser.add_argument('--path', help='--path ./top directory path to kpi',required=True)
    parser.add_argument('--file', help='--file kpi.csv',default='kpi.csv')
    parser.add_argument('--database', help='--database qa_db',default='qa_db')
    parser.add_argument('--table', help='--table qa_table',default='qa_table')
    
    args = parser.parse_args()

    __path = args.path
    __file = args.file
    __database = args.database
    __table = args.table

    csv_sqlite = csv_to_sqlite(
                _path = __path,
                _file = __file,
                _database = __database,
                _table= __table)

    csv_sqlite.store()

if __name__ == '__main__':
    main()    