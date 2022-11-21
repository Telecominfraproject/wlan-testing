#!/usr/bin/env python3
import sys
import os
import argparse
import pandas as pd

#https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
#https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

class L3CSVParcer():
    def __init__(self,csv_file):


        # left this in for testing
        '''csv_obj = open(csv_file, 'r')
        csv_reader = csv.reader(csv_obj)
        print(csv_reader)

        for row in csv_reader:
            if row[1] == 'rx':
                print(row)'''

        include_summary = ['Time epoch','Time','Monitor','least','most','average']
        self.csv_file = csv_file
        df_s = pd.read_csv(self.csv_file,header = 0, usecols = lambda column : any(substr in column for substr in include_summary))

        print('{}'.format(csv_file))
        csv_file_summary = self.csv_file.replace('results_','results_summary_')

        df_s.to_csv(csv_file_summary, index = False, header=True)

        include_raw = ['Time epoch','Time','Monitor','LT','MT']
        self.csv_file = csv_file
        df_r = pd.read_csv(self.csv_file,header = 0, usecols = lambda column : any(substr in column for substr in include_raw))

        csv_file_raw = self.csv_file.replace('results_','results_raw_')
        df_r.to_csv(csv_file_raw, index = False, header=True)

        '''df_rx_delta = df_r.loc[df['Monitor'] == 'rx_delta']

        df_rx_delta.plot(x='Time epoch', y='average_rx_data')
        plt.show()

        total_cols = len(df.axes[0])


        print(df.columns)

        print(df.loc[df['Monitor'] == 'rx_delta'])
        print(df.loc[df['Monitor'] == 'rx'])

        print(df.loc[df['Monitor'] == 'rx_delta', df.columns != 'Time'])


        df_rx_delta = df.loc[df['Monitor'] == 'rx_delta']

        print(df_rx_delta.describe())

        df_rx_delta.plot(x='Time epoch', y='average_rx_data')
        plt.show()

        df_rx_delta.plot(x='Time', y='average_rx_data')
        plt.show()

        df_rx_drop_pct = df.loc[df['Monitor'] == 'rx_drop_percent']
        print(df_rx_drop_pct)
        df_rx_delta.plot(x='Time epoch', y='rx_drop_percent')
        plt.show()


        df2 = df.filter(regex='LT-s')
        print(df2)
        #plt.plot(df2[0], df2[1]
        #plt.show()

        df2_mean = df2.mean().sort_values(ascending=False)

        print(df2_mean)

        df2_mean_no_outliers = df2_mean[df2_mean(df2_mean.quantile(.10), df2_mean.quantile(.90))]

        print("no outliers")
        print(df2_mean_no_outliers)

        print("Top 10")
        print(df2_mean.head(10))
        print("Bottom 10")
        print(df2_mean.tail(10))

        print("mean others")



        # set display format otherwise get scientific notation
        pd.set_option('display.float_format', lambda x: '%.3f' % x)

        df_mean = df_rx_delta.mean().sort_values()

        #print(df_mean)

        print(df_mean[0])




        #df_uni_cast = [col for col in df_rx_delta if 'LT' in col]
        #df_LT_rx_delta_mean = df_uni_cast.mean().sort_values()

        #print(df_LT_rx_delta_mean)
        x = np.linspace(0, 20, 100)
        plt.plot(x, np.sin(x))
        plt.show()'''


def main():

    #debug_on = False
    parser = argparse.ArgumentParser(
        prog='csv_processor.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
 Useful Information:
            ''',
        
        description='''quick_test.py:

        ''')


    parser.add_argument('-i','--infile', help="file of csv data", default='longevity_results_08_14_2020_14_37.csv')
    parser.add_argument('--debug', help='--debug:  Enable debugging',default=True)


    args = parser.parse_args()

    #debug_on = args.debug

    if args.infile:
        csv_file_name = args.infile

    L3CSVParcer(csv_file_name)



if __name__ == "__main__":
    main()
