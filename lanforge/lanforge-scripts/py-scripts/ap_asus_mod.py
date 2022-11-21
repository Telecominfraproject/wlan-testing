#!/usr/bin/python3

"""
NAME:
asus_ap.py

PURPOSE:
ap_asus_module

EXAMPLE:

./ap_asus_mod.py 


NOTES:



"""

import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import os
import argparse
import pexpect
import serial
from pexpect_serial import SerialSpawn
import importlib
from pprint import pformat
import traceback
import paramiko
import logging
from pprint import pformat


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

logger = logging.getLogger(__name__)



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

# LAN-1423
class create_ap_obj:
    def __init__(self,
                 ap_test_mode=False,
                 ap_ip=None,
                 ap_user=None,
                 ap_passwd=None,
                 ap_scheme='ssh',
                 ap_serial_port='/dev/ttyUSB0',
                 ap_ssh_port="22",
                 ap_telnet_port="23",
                 ap_serial_baud='115200',
                 ap_if_2g="eth6",
                 ap_if_5g="eth7",
                 ap_if_6g="eth8",
                 ap_report_dir="",
                 ap_file="",
                 ap_band_list=['2g','5g','6g']):
        self.ap_test_mode = ap_test_mode
        self.ap_ip = ap_ip
        self.ap_user = ap_user
        self.ap_passwd = ap_passwd
        self.ap_scheme = ap_scheme
        self.ap_ssh_port = ap_ssh_port
        self.ap_serial_port = ap_serial_port
        self.ap_telnet_port = ap_ssh_port
        self.ap_telnet = ap_telnet_port
        self.ap_serial_baud = ap_serial_baud
        self.ap_if_2g = ap_if_2g
        self.ap_if_5g = ap_if_5g
        self.ap_if_6g = ap_if_6g
        self.ap_report_dir = ap_report_dir
        self.ap_file = ap_file
        self.ap_band_list = ap_band_list

        self.cmd_clear_stats = 'wl -i INF dump_clear'
        self.cmd_tx_stats = 'wl -i INF bs_data'
        self.cmd_rx_stats = 'wl -i INF rx_report'
        self.cmd_chanim = 'wl -i INF chanim_stats'
        self.cmd_umsched = 'wl -i INF dump umsched'
        self.cmd_msched = 'wl -i INF dump msched'
        self.cmd_muinfo = 'wl -i INF muifo -v'

        # need to have separate for 2g, 5g, and 6g
        self.tx_results = {}
        self.tx_results_rows = ''
        self.ap_tx_row = ''
        self.rx_results = {}
        self.rx_results_rows = ''
        self.ap_rx_row = ''
        self.chanim_results = {}
        self.chanim_results_rows = ''
        self.ap_chanim_row = ''


        # the --ap_read will use these headers
        self.dl_col_titles = [
            "Station Address",
            "Dl-PHY-Mbps",
            "Dl-Data-Mbps",
            "Dl-Air-Use",
            "Dl-Data-Use",
            "Dl-Retries",
            "Dl-BW",
            "Dl-MCS",
            "Dl-NSS",
            "Dl-OFDMA",
            "Dl-MU-MIMO",
            "Dl-Channel-Utilization"]

        self.ul_col_titles = [
            "UL Station Address",
            "Ul-rssi",
            "Ul-tid",
            "Ul-ampdu",
            "Ul-mpdu",
            "Ul-Data-Mbps",
            "Ul-PHY-Mbps",
            "UL-BW",
            "Ul-MCS",
            "Ul-NSS",
            "Ul-OOW",
            "Ul-HOLES",
            "Ul-DUP",
            "Ul-Retries",
            "Ul-OFDMA",
            "Ul-Tones",
            "Ul-AIR"]


    # For testing module
    def action(self, ap_cmd=None, ap_file=None):

        results = ''
        if ap_cmd != None:
            self.ap_cmd = ap_cmd
        logger.info("ap_cmd: {}".format(ap_cmd))
        try:
            # TODO - add paramiko.SSHClient
            if self.ap_scheme == 'serial':
                # configure the serial interface
                ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
                ss = SerialSpawn(ser)
                ss.sendline(str(self.ap_cmd))
                # do not detete line, waits for output
                ss.expect([pexpect.TIMEOUT], timeout=1)
                results = ss.before.decode('utf-8', 'ignore')
                logger.debug("ap_stats serial from AP: {}".format(results))
            elif self.ap_scheme == 'ssh':
                results = self.ap_ssh(str(self.ap_cmd))
                logger.debug("ap_stats ssh from AP : {}".format(results))

        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error(" unable to read AP")

        if self.ap_file is not None:
            ap_file = open(str(self.ap_file), "a")
            ap_file.write(results)
            ap_file.close()
            print("ap file written {}".format(str(self.ap_file)))

        return results

    def ap_ssh(self, command):
        # in python3 bytes and str are two different types.  str is used to reporesnt any
        # type of string (also unicoe), when you encode()
        # something, you confvert it from it's str represnetation to it's bytes reprrestnetation for a specific 
        # endoding
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ap_ip, port=self.ap_ssh_port, username=self.ap_user, password=self.ap_passwd, timeout=5)
        stdin, stdout, steerr = ssh.exec_command(command)
        output = stdout.read()
        logger.debug("command:  {command} output: {output}".format(command=command,output=output))
        output = output.decode('utf-8', 'ignore')
        logger.debug("after utf-8 ignoer output: {output}".format(command=command,output=output))

        ssh.close()
        return output

    def say_hi(self):
        logger.info("HI")

    # ASUS dl ap column heading
    def get_dl_col_titles(self):
        return self.dl_col_titles

    # ASUS ul ap column heading
    def get_ul_col_titles(self):
        return self.ul_col_titles

    # ASUS 
    def clear_stats(self, band):
        if band == '2g':
            cmd = self.cmd_clear_stats.replace('INF',self.ap_if_2g)
        elif band == '5g':
            cmd = self.cmd_clear_stats.replace('INF',self.ap_if_5g)
        elif band == '6g':
            cmd = self.cmd_clear_stats.replace('INF',self.ap_if_6g)

        self.action(ap_cmd=cmd)

    # ASUS bs_data,  tx_data , data transmitted from AP stats
    # This will gather the statistics to be read later
    # read_ap_stats
    def read_tx_dl_stats(self, band):
        if band == '2g':
            cmd = self.cmd_tx_stats.replace('INF',self.ap_if_2g)
        elif band == '5g':
            cmd = self.cmd_tx_stats.replace('INF',self.ap_if_5g)
        elif band == '6g':
            cmd = self.cmd_tx_stats.replace('INF',self.ap_if_6g)
        # may ned a copy 
        # self.tx_results[band] = self.action(ap_cmd=cmd).copy()
        self.tx_results[band] = self.action(ap_cmd=cmd) #.decode('utf-8', 'ignore')
        logger.debug(pformat(self.tx_results))

    # ASUS bs_data,  tx_data , data transmitted from AP stats
    def tx_dl_stats(self, mac):
        # need to do read_tx_dl_stats first
        mac_found = False 
        self.tx_ap_row = ''        

        # the mac should only match once
        for band in self.ap_band_list:
            self.tx_results_rows = self.tx_results[band].splitlines()
            logger.debug("From AP tx_dl_stats : self.tx_results_rows {tx_rows}".format(tx_rows=self.tx_results_rows))

            for row in self.tx_results_rows:
                split_row = row.split()
                # Test mode would go here
                try:
                    if split_row[0].lower() == mac.lower():
                        self.tx_ap_row = split_row
                        mac_found = True
                        logger.debug("AP read tx_dl_stats mac {ap_mac} Port mac {port_mac}".format(ap_mac=split_row[0].lower(), port_mac=mac.lower()))
                        # the mac should only show up once
                        break
                    else:
                        logger.debug("AP no match read tx_dl_stats mac {ap_mac} Port mac {port_mac}".format(ap_mac=split_row[0].lower(), port_mac=mac.lower()))
                except Exception as x:
                    traceback.print_exception(Exception, x, x.__traceback__, chain=True)
                    logger.info("'No stations are currently associated.'? from AP")
                    logger.info("since possibly no stations: exception on compare split_row[0].lower() ")


            if mac_found:
                # mac_found = False
                logger.info("selected tx_ap_row (from split_row): {row}".format(row=self.tx_ap_row))
                break


        return mac_found, self.tx_ap_row
    
    # report_rx
    def read_rx_ul_stats(self, band):
        if band == '2g':
            cmd = self.cmd_rx_stats.replace('INF',self.ap_if_2g)
        elif band == '5g':
            cmd = self.cmd_rx_stats.replace('INF',self.ap_if_5g)
        elif band == '6g':
            cmd = self.cmd_rx_stats.replace('INF',self.ap_if_6g)

        self.rx_results[band] = self.action(ap_cmd=cmd) #.decode('utf-8', 'ignore')
        logger.debug(pformat(self.rx_results))

    # ASUS rx_report,  rx_data  , receive statatistics at AP
    def rx_ul_stats(self, mac):
        mac_found = False
        self.rx_ap_row = ''
        # the mac should only match once
        for band in self.ap_band_list:

            # need to do read_rx_stats first
            self.rx_results_rows = self.rx_results[band].splitlines()

            for row in self.rx_results_rows:
                split_row = row.split()
                # Test mode would go here
                try:
                    if split_row[0].lower() == mac.lower():
                        self.rx_ap_row = split_row
                        mac_found = True
                        logger.debug("AP read mac {ap_mac} Port mac {port_mac}".format(ap_mac=split_row[0], port_mac=mac))
                        logger.debug("self.rx_ap_row {rx_ap_row}".format(rx_ap_row=self.rx_ap_row))
                        break
                    else:
                        logger.debug("AP no match read mac {ap_mac} Port mac {port_mac}".format(ap_mac=split_row[0], port_mac=mac))

                except Exception as x:
                    traceback.print_exception(Exception, x, x.__traceback__, chain=True)
                    logger.info("'No stations are currently associated.'? from AP")
                    logger.info("since possibly no stations: exception on compare split_row[0].lower() ")


            if mac_found:
                # mac_found = False
                logger.info("selected ap_row (from split_row): {row}".format(row=self.rx_ap_row))
                break

        return mac_found, self.rx_ap_row

    # ASUS chanel info (channel utilization)
    def read_chanim_stats(self, band):
        if band == '2g':
            cmd = self.cmd_chanim.replace('INF',self.ap_if_2g)
        elif band == '5g':
            cmd = self.cmd_chanim.replace('INF',self.ap_if_5g)
        elif band == '6g':
            cmd = self.cmd_chanim.replace('INF',self.ap_if_6g)

        self.chanim_results[band] = self.action(ap_cmd=cmd) # .decode('utf-8', 'ignore')
        logger.debug(pformat(self.chanim_results[band]))

    def chanim_stats(self, mac):
        xtop_reported = False
        channel_utilization = 0
        # the mac should only match once
        for band in self.ap_band_list:
            logger.debug("chanim_results [{band}] {chanim}".format(band=band,chanim=self.chanim_results[band]))
            self.chanim_results_rows = self.chanim_results[band].splitlines()
            for row in self.chanim_results_rows:
                split_row = row.split()
                if xtop_reported:
                    logger.info("xtop_reported {band} row: {row}".format(band=band,row=row))
                    logger.info("xtop_reported {band} split_row: {split_row}".format(band=band,split_row=split_row))
                    try:
                        xtop = split_row[7]
                        logger.info("{band} xtop {xtop}".format(band=band,xtop=xtop))
                    except Exception as x:
                        traceback.print_exception(Exception, x, x.__traceback__, chain=True)
                        logger.info("{band} detected chanspec with reading chanim_stats, exception reading xtop".format(band=band))
                    try:
                        channel_utilization = float(100) - float(xtop)
                        logger.info("{band} channel_utilization {utilization}".format(band=band,utilization=channel_utilization))
                    except Exception as x:
                        traceback.print_exception(Exception, x, x.__traceback__, chain=True)
                        logger.info("{band} detected chanspec with reading chanim_stats, failed calcluating channel_utilization from xtop".format(band=band))

                    # should be on ly one channel utilization
                    break
                else:
                    try:
                        if split_row[0].lower() == 'chanspec':
                            logger.info("{band} chanspec found xtop_reported = True".format(band=band))
                            xtop_reported = True
                    except Exception as x:
                        traceback.print_exception(Exception, x, x.__traceback__, chain=True)
                        logger.error("{band} Error reading xtop".format(band=band))

        return xtop_reported, str(channel_utilization)




                    








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

Notes:
------
    
        .git/bs_data Display per station band steering data
    usage: bs_data [options]
    options are:
        -comma    Use commas to separate values rather than blanks.
        -tab      Use <TAB> to separate values rather than blanks.
        -raw      Display raw values as received from driver.
        -noidle   Do not display idle stations
        -nooverall  Do not display total of all stations
        -noreset  Do not reset counters after reading

    rx_report
            Display per station live data about rx datapath
    usage: rx_report [options]
    options are:
        -sta xx:xx:xx:xx:xx:xx  only display specific mac addr.
        -comma      Use commas to separate values rather than blanks.
        -tab        Use <TAB> to separate values rather than blanks.
        -raw        Display raw values as received from driver.
        -noidle     Do not display idle stations
        -nooverall  Do not display total of all stations
        -noreset    Do not reset counters after reading
           


        ''')
    parser.add_argument('--ap_read', help='--ap_read  flag present enable reading ap', action='store_true')
    parser.add_argument('--ap_test_mode', help='--ap_mode ', default=True)

    parser.add_argument('--ap_scheme', help="--ap_scheme '/dev/ttyUSB0'", choices=['serial', 'telnet', 'ssh', 'mux_serial'], default='serial')
    parser.add_argument('--ap_serial_port', help="--ap_serial_port '/dev/ttyUSB0'", default='/dev/ttyUSB0')
    parser.add_argument('--ap_serial_baud', help="--ap_baud '115200'',  default='115200", default="115200")
    parser.add_argument('--ap_ip', help='--ap_ip', default='192.168.50.1')
    parser.add_argument('--ap_ssh_port', help='--ap_ssh_port', default='1025')
    parser.add_argument('--ap_telnet_port', help='--ap_telnet_port', default='23')
    parser.add_argument('--ap_user', help='--ap_user , the user name for the ap, default = lanforge', default='lanforge')
    parser.add_argument('--ap_passwd', help='--ap_passwd, the password for the ap default = lanforge', default='lanforge')
    # ASUS interfaces
    parser.add_argument('--ap_if_2g', help='--ap_if_2g eth6', default='wl0')
    parser.add_argument('--ap_if_5g', help='--ap_if_5g eth7', default='wl1')
    parser.add_argument('--ap_if_6g', help='--ap_if_6g eth8', default='wl2')
    parser.add_argument('--ap_file', help="--ap_file 'ap_file.txt'", default=None)

    parser.add_argument('--log_level', default=None, help='Set logging level: debug | info | warning | error | critical')
    # logging configuration
    parser.add_argument("--lf_logger_config_json", help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if (args.log_level):
        logger_config.set_level(level=args.log_level)

    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()


    ap = create_ap_obj(
                ap_test_mode=args.ap_test_mode,
                ap_ip=args.ap_ip,
                ap_user=args.ap_user,
                ap_passwd=args.ap_passwd,
                ap_scheme=args.ap_scheme,
                ap_serial_port=args.ap_serial_port,
                ap_ssh_port=args.ap_ssh_port,
                ap_telnet_port=args.ap_telnet_port,
                ap_serial_baud=args.ap_serial_baud,
                ap_if_2g=args.ap_if_2g,
                ap_if_5g=args.ap_if_5g,
                ap_if_6g=args.ap_if_6g,
                ap_report_dir="",
                ap_file=args.ap_file
                )


    ap.clear_stats(band='5g')
    ap.read_tx_dl_stats(band='5g')
    ap.read_rx_ul_stats(band='5g')


if __name__ == '__main__':
    main()
