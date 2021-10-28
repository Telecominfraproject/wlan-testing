#!/usr/bin/python3

'''
NAME:
lf_check.py

PURPOSE:
Script to verify connectivity to an AP

EXAMPLE:

./lf_check_ap.py --ap_port '/dev/ttyUSB0' --ap_baud '115200' --ap_cmd "wl -i wl1 bs_data"

./lf_check_ap.py --ap_port '/dev/ttyUSB0' --ap_baud '115200' --ap_cmd "wl -i wl1 bs_data" --ap_file 'ap_file.txt'



NOTES:

Script is in the sandbox
run /py-scripts/update_dependencies.py 

'''

import sys
if sys.version_info[0]  != 3:
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
        data = data.strip() # ignore leading/trailing whitespace
        if data: # non-blank
           self.logger.info(data)
    def flush(self):
        pass  # leave it to logging to flush properly


class lf_check():
    def __init__(self, 
                 _ap_port, 
                 _ap_baud, 
                 _ap_cmd,
                 _ap_file):
        self.ap_port = _ap_port
        self.ap_baud = _ap_baud
        self.ap_cmd = _ap_cmd
        self.ap_file = _ap_file
    
    def ap_action(self):

        print("ap_cmd: {}".format(self.ap_cmd))
        try:
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd))
            ss.expect([pexpect.TIMEOUT], timeout=2) # do not detete line, waits for output
            ap_results = ss.before.decode('utf-8','ignore')
            print("ap_results {}".format(ap_results))
        except:
            ap_results = "exception on accessing {} Command: {}\r\n".format(self.ap_port,self.ap_cmd)
            print("{}".format(ap_results))

        if(self.ap_file != None):
            ap_file = open(str(self.ap_file),"a")
            ap_file.write(ap_results)
            ap_file.close()
            print("ap file written {}".format(str(self.ap_file)))

def main():

    parser = argparse.ArgumentParser(
        prog='lf_check.py',
        #formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Useful Information:
            1. Useful Information goes here
            ''',
        
        description='''\
lf_check.py:
--------------------
#ssid TCH-XB7
#ssidpw comcats123
Summary : 
----------
This file is used for verification

Commands: (wl1 == 5ghz , wl0 == 24ghz)

read ap data:: 'wl -i wl1 bs_data'
reset scheduler's counters:: 'wl -i wl1 dump_clear'
UL scheduler statistics:: 'wl -i wl1 dump umsched'
DL scheduler statistics:: 'wl -i wl1 dump msched'

Generic command layout:
-----------------------

        ''')
    parser.add_argument('--ap_port', help='--ap_port \'/dev/ttyUSB0\'',default='/dev/ttyUSB0')
    parser.add_argument('--ap_baud', help='--ap_baud  \'115200\'',default='115200')
    parser.add_argument('--ap_cmd', help='--ap_cmd \'wl -i wl1 bs_data\'',default='wl -i wl1 bs_data')
    parser.add_argument('--ap_file', help='--ap_file \'ap_file.txt\'')
    
    args = parser.parse_args()

    __ap_port = args.ap_port
    __ap_baud = args.ap_baud
    __ap_cmd  = args.ap_cmd
    __ap_file = args.ap_file

    check = lf_check(
                _ap_port = __ap_port,
                _ap_baud = __ap_baud,
                _ap_cmd = __ap_cmd ,
                _ap_file = __ap_file)

    check.ap_action()

if __name__ == '__main__':
    main()


