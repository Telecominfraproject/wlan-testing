#!/usr/bin/env python3
"""

 This program is used to read in a LANforge Dataplane CSV file and output
 a csv file that works with a customer's RvRvO visualization tool.

 Example use case:

 Read in ~/text-csv-0-candela.csv, output is stored at outfile.csv
 ./py-scripts/csv_convert.py -i ~/text-csv-0-candela.csv

 Output is csv file with mixxed columns, top part:
 Test Run,Position [Deg],Attenuation 1 [dB], Pal Stats Endpoint 1 Control Rssi [dBm],  Pal Stats Endpoint 1 Data Rssi [dBm]

 Second part:
 Step Index,Position [Deg],Attenuation [dB],Traffic Pair 1 Throughput [Mbps]
"""
import sys
import os
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))


class CSVParser:
    def __init__(self, csv_infile=None, csv_infile2=None, csv_outfile=None):

        i_atten = -1
        i_rotation = -1
        i_rxbps = -1
        i_beacon_rssi = -1
        i_data_rssi = -1
        i_rx_mcs = -1
        i_tx_mcs = -1
        rate_with_units = False

        fpo = open(csv_outfile, "w")
        fp = open(csv_infile)
        fp2 = None
        if csv_infile2:
            fp2 = open(csv_infile2)

        if True:
            line = fp.readline()
            if not line:
                exit(1)

            # Concat lines so we can read data from both csv files.
            if fp2:
                l2 = fp2.readline()
                if l2:
                    line = "%s,%s" %(line, l2)

            # Read in initial line, this is the CSV headers.  Parse it to find the column indices for
            # the columns we care about.
            x = line.split(",")
            cni = 0
            for cn in x:
                #print("cn: " + cn)
                # This works with the 'brief' csv output.
                if cn == "Attenuation [dB]":
                    i_atten = cni
                if cn == "Position [Deg]":
                    i_rotation = cni
                if cn == "Throughput [Mbps]":
                    i_rxbps = cni
                if cn == "Beacon RSSI [dBm]":
                    i_beacon_rssi = cni
                if cn == "Data RSSI [dBm]":
                    i_data_rssi = cni

                # This is for parsing the more complete csv output.
                if cn == "Atten":
                    i_atten = cni
                if cn == "Rotation":
                    i_rotation = cni
                if cn == "Rx-Bps":
                    rate_with_units = True
                    i_rxbps = cni
                # NOTE: Beacon RSSI does not exist in the 'full' csv
                if cn == "RSSI":
                    i_data_rssi = cni
                if cn == "Tx-Rate":
                    i_tx_mcs = cni
                if cn == "Rx-Rate":
                    i_rx_mcs = cni
                    
                cni += 1

            # Write out out header for the new file.
            fpo.write("Test Run,Position [Deg],Attenuation 1 [dB],Pal Stats Endpoint 1 Control Rssi [dBm],Pal Stats Endpoint 1 Data Rssi [dBm] Mean,Pal Stats Endpoint 1 RX rate [Mbps] Mode,Pal Stats Endpoint 1 TX rate [Mbps] Mode\n")

            # Read rest of the input lines, processing one at a time.  Covert the columns as
            # needed, and write out new data to the output file.
            line = fp.readline()

            # Concat lines so we can read data from both csv files.
            if fp2:
                l2 = fp2.readline()
                if l2:
                    line = "%s,%s" %(line, l2)

            bottom_half = "Step Index,Position [Deg],Attenuation [dB],Traffic Pair 1 Throughput [Mbps]\n"

            test_run = "1"

            step_i = 0
            while line:
                x = line.split(",")
                beacon_rssi = "0"
                if (i_beacon_rssi >= 0):
                    beacon_rssi = x[i_beacon_rssi]
                tx_rate = "0"
                rx_rate = "0"
                if (i_tx_mcs >= 0):
                    tx_rate = self.convert_to_mbps(x[i_tx_mcs])
                if (i_rx_mcs >= 0):
                    rx_rate = self.convert_to_mbps(x[i_rx_mcs])
                fpo.write("%s,%s,%s,%s,%s,%s,%s\n" % (test_run, x[i_rotation], x[i_atten], beacon_rssi, x[i_data_rssi], tx_rate, rx_rate))
                bottom_half += ("%s,%s,%s,%s\n" % (step_i, x[i_rotation], x[i_atten], self.convert_to_mbps(x[i_rxbps])))
                line = fp.readline()

                # Concat lines so we can read data from both csv files.
                if fp2:
                    l2 = fp2.readline()
                    if l2:
                        line = "%s,%s" %(line, l2)

                step_i += 1

            # First half is written out now, and second half is stored...
            fpo.write("\n\n# RvRvO Data\n\n")
            fpo.write(bottom_half)

    def convert_to_mbps(self, val):
        tokens = val.split(" ")
        rv = float(tokens[0])

        try:
            units = tokens[1]
            if units == "Gbps":
                rv = rv * 1000.0;
            if units == "Kbps":
                rv = rv / 1000.0
            return int(rv)
        except:
            # Assume no units and that it is already mbps
            return int(rv)

def main():
    parser = argparse.ArgumentParser(
        prog='csv_convert.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
 Useful Information:
            ''',

        description='''
csv_convert.py:  
    converts the candela brief csv and/or more complete csv into the data for specific customer.
    Both csv files need to be passed in order to have beacon rssi and phy rates since neither
    csv file contains all of that data.

Example:
    ./csv_convert.py -i ~/dataplane-2022-02-08-12-18-45/text-csv-2.csv -I ~/dataplane-2022-02-08-12-18-45/text-csv-0.csv
        ''')

    parser.add_argument('-i', '--infile', help="input file of csv data", required=True)
    parser.add_argument('-I', '--infile2', help="secondary input file of csv data", required=True)
    parser.add_argument('-o', '--outfile', help="output file in .csv format", default='outfile.csv')

    args = parser.parse_args()
    csv_outfile_name = None
    csv_infile_name = None
    csv_infile_name2 = None

    if args.infile:
        csv_infile_name = args.infile
    if args.infile2:
        csv_infile_name2 = args.infile2
    if args.outfile:
        csv_outfile_name = args.outfile

    print("infile: %s infile2: %s  outfile: %s" % (csv_infile_name, csv_infile_name2, csv_outfile_name))

    CSVParser(csv_infile_name, csv_infile_name2, csv_outfile_name)


if __name__ == "__main__":
    main()
