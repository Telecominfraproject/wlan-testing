#!/usr/bin/python3

"""
NAME:
asus_ap.py

PURPOSE:
Generic AP library that will work for the ASUS ap's

EXAMPLE:

./asus_ap.py --ap_port '/dev/ttyUSB0' --ap_baud '115200' --ap_cmd "wl -i wl1 bs_data"

./asus_ap.py --ap_port '/dev/ttyUSB0' --ap_baud '115200' --ap_cmd "wl -i wl1 bs_data" --ap_file 'ap_file.txt'



NOTES:



"""

import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import argparse
import pexpect
import serial
from pexpect_serial import SerialSpawn


# see https://stackoverflow.com/a/13306095/11014343
class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip()  # ignore leading/trailing whitespace
        if data:  # non-blank
            self.logger.info(data)

    def flush(self):
        pass  # leave it to logging to flush properly


class lf_ap:
    def __init__(self,
                 _ap_test_mode=False,
                 _ap_2G_interface="wl0",
                 _ap_5G_interface="wl1",
                 _ap_6G_interface="wl2",
                 _ap_scheme='serial',
                 _ap_serial_port='/dev/ttyUSB0',
                 _ap_ssh_port="22",
                 _ap_telnet_port="23",
                 _ap_serial_baud='115200',
                 _ap_report_dir="",
                 _ap_log_file=""):
        self.ap_test_mode = _ap_test_mode
        self.ap_2G_interface = _ap_2G_interface
        self.ap_5G_interface = _ap_5G_interface
        self.ap_6G_interface = _ap_6G_interface
        self.ap_scheme = _ap_scheme
        self.ap_serial_port = _ap_serial_port
        self.ap_telnet_port = _ap_ssh_port
        self.ap_telnet = _ap_telnet_port
        self.ap_serial_baud = _ap_serial_baud
        self.ap_report_dir = _ap_report_dir
        self.ap_log_file = _ap_log_file

    def ap_action(self):

        print("ap_cmd: {}".format(self.ap_cmd))
        try:
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd))
            ss.expect([pexpect.TIMEOUT], timeout=2)  # do not detete line, waits for output
            ap_results = ss.before.decode('utf-8', 'ignore')
            print("ap_results {}".format(ap_results))
        except:
            ap_results = "exception on accessing {} Command: {}\r\n".format(self.ap_port, self.ap_cmd)
            print("{}".format(ap_results))

        if self.ap_file is not None:
            ap_file = open(str(self.ap_file), "a")
            ap_file.write(ap_results)
            ap_file.close()
            print("ap file written {}".format(str(self.ap_file)))

    # ASUS 
    def ap_clear_stats(self, band):
        pass

    # ASUS bs_data
    def ap_ul_data(self, band):
        pass

    # ASUS rx_report
    def ap_dl_data(self, band):
        pass

    # ASUS chanel info (channel utilization)
    def ap_chanim(self, band):
        pass

    def ap_ul_stats(self, band):
        pass

    def ap_dl_stats(self, band):
        pass

    @staticmethod
    def ap_store_dl_scheduler_stats(band):
        if band is "6G":
            pass

    def ap_store_ul_scheduler_stats(self, band):
        pass

    def ap_ofdma_stats(self, band):
        pass


def main():
    parser = argparse.ArgumentParser(
        prog='lf_ap.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Useful Information:
            1. Useful Information goes here
            ''',

        description='''\
lf_ap.py:
--------------------
Summary : 
----------
This file is used for verification

Commands: (wl2 == 6GHz wl1 == 5GHz , wl0 == 24ghz)

read ap data:: 'wl -i wl1 bs_data'
reset scheduler's counters:: 'wl -i wl1 dump_clear'
UL scheduler statistics:: 'wl -i wl1 dump umsched'
DL scheduler statistics:: 'wl -i wl1 dump msched'

Generic command layout:
-----------------------

        ''')
    parser.add_argument('--ap_test_mode', help='--ap_mode ', default=True)
    parser.add_argument('--ap_port', help='--ap_port \'/dev/ttyUSB0\'', default='/dev/ttyUSB0')
    parser.add_argument('--ap_baud', help='--ap_baud  \'115200\'', default='115200')
    parser.add_argument('--ap_cmd', help='--ap_cmd \'wl -i wl1 bs_data\'', default='wl -i wl1 bs_data')
    parser.add_argument('--ap_file', help='--ap_file \'ap_file.txt\'')

    args = parser.parse_args()

    __ap_port = args.ap_port
    __ap_baud = args.ap_baud
    __ap_cmd = args.ap_cmd
    __ap_file = args.ap_file

    ap_dut = lf_ap(
        _ap_port=__ap_port,
        _ap_baud=__ap_baud,
        _ap_cmd=__ap_cmd,
        _ap_file=__ap_file)

    ap_dut.ap_action()


if __name__ == '__main__':
    main()
