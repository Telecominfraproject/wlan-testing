#!/usr/bin/python3

'''
NAME:
lf_read_json.py

PURPOSE:
Test out reading configuration data from a .json style config file

EXAMPLE:
./lf_read_json.py --file <name>.json

NOTES:


TO DO NOTES:


'''
import sys
if sys.version_info[0]  != 3:
    print("This script requires Python3")
    exit()


from time import sleep
import argparse
import json

class lf_read_json():
     def __init__(self):

          self.timeout = 10

     
     def preprocess_data(self):
          pass

     

def main():
     # arguments
     parser = argparse.ArgumentParser(
          prog='lf_read_json.py',
          formatter_class=argparse.RawTextHelpFormatter,
          epilog='''\
            lf_read_json.py : read json
            ''',
          description='''\
lf_read_json.py
-----------

Summary :
---------

./lf_dataplane_json.py --mgr 192.168.0.101 --port 8080 --lf_user lanforge --lf_password lanforge --instance_name dataplane-instance --config_name test_con --upstream 1.1.eth1 --dut asus_5g --duration 15s --station 1.1.13.sta0002 --download_speed 85% --upload_speed 0 --raw_line 'pkts: Custom;60;MTU' --raw_line 'cust_pkt_sz: 88 1200' --raw_line 'directions: DUT Transmit' --raw_line 'traffic_types: UDP' --raw_line 'bandw_options: 20' --raw_line 'spatial_streams: 1

            ''')

     parser.add_argument('--json', help="--json <config.json> json input file", default="config.json")

     args = parser.parse_args()    

     config_json = args.json
     print("config_json {}".format(config_json))

     with open(config_json, 'r') as config_file:
         config_data = json.load(config_file)

     print(config_data)
     print("mgr: {}".format(config_data["mgr"]))
     #print("raw_line: {}".format(config_data["raw_line"]))
     raw = []
     raw = config_data["raw_line"]
     print(raw)
     # raw is a list
     raw2 = [[x] for x in raw]
     print(raw2)

     '''
     for r in raw_lines:
            cfg_options.append(r[0])
     '''

     '''./lf_dataplane_json.py --mgr 192.168.0.101 --port 8080 --lf_user lanforge --lf_password lanforge --instance_name dataplane-instance --config_name test_con --upstream 1.1.eth1 --dut asus_5g --duration 15s --station 1.1.13.sta0002 --download_speed 85% --upload_speed 0 --raw_line 'pkts: Custom;60;MTU' --raw_line 'cust_pkt_sz: 88 1200' --raw_line 'directions: DUT Transmit' --raw_line 'traffic_types: UDP' --raw_line 'bandw_options: 20' --raw_line 'spatial_streams: 1'
Namespace(config_name='test_con', disable=[], download_speed='85%', duration='15s', dut='asus_5g', enable=[], graph_groups=None, influx_bucket=None, influx_host=None, influx_org=None, influx_port=8086, influx_tag=[], influx_token=None, instance_name='dataplane-instance', json='', lf_password='lanforge', lf_user='lanforge', load_old_cfg=False, mgr='192.168.0.101', port=8080, pull_report=False, 
     correct version:
     raw_line=[['pkts: Custom;60;MTU'], ['cust_pkt_sz: 88 1200'], ['directions: DUT Transmit'], ['traffic_types: UDP'], ['bandw_options: 20'], ['spatial_streams: 1']], raw_lines_file='', report_dir='', set=[], station='1.1.13.sta0002', test_rig='', upload_speed='0', upstream='1.1.eth1')
     '''

     ''' Incorrect version 
     raw_line={'pkts': ['Custom', '60', 'MTU'], 'cust_pkt_sz': ['88', '1200'], 'directions': 'DUT Transmit', 'traffic_types': 'UDP', 'bandw_options': '20', 'stpatial_streams': '1'}
     '''
     '''cfg_options = []
     for r in raw:
          print(r)
          test = '{}:{}'.format(r,raw[r])
          cfg_options.append(test)
     print(cfg_options)          
     '''     





     #dave = []
     #for key,val in raw.items(): dave.append(raw.items())

     #print(dave)

     if "mgr" in config_data:
          print("mgr present")

     print("END  lf_read_json.py")


if __name__ == "__main__":
     main()