#!/usr/bin/python3

'''
NAME:
lf_json_test.py

PURPOSE:


EXAMPLE:
./lf_json_test.py -

NOTES:


TO DO NOTES:


'''
import os
import sys
if sys.version_info[0]  != 3:
    print("This script requires Python3")
    exit()


from time import sleep
import argparse
import json
#if 'py-json' not in sys.path:
#    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))
#    print("path: {}".format(os.path.join(os.path.abspath('..'))))

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

from LANforge import lf_json_autogen

class lf_read_json():
    def __init__(self):

        self.timeout = 10

     
    def preprocess_data(self):
          pass

     

def main():
     # arguments
    parser = argparse.ArgumentParser(
          prog='lf_json_test.py',
          formatter_class=argparse.RawTextHelpFormatter,
          epilog='''\
            lf_json_test.py : lf json test
            ''',
          description='''\
lf_json_test.py
-----------

Summary :
---------


./lf_dataplane_json.py --mgr 192.168.0.101 --port 8080 --lf_user lanforge --lf_password lanforge --instance_name dataplane-instance --config_name test_con --upstream 1.1.eth1 --dut asus_5g --duration 15s --station 1.1.13.sta0002 --download_speed 85% --upload_speed 0 --raw_line 'pkts: Custom;60;MTU' --raw_line 'cust_pkt_sz: 88 1200' --raw_line 'directions: DUT Transmit' --raw_line 'traffic_types: UDP' --raw_line 'bandw_options: 20' --raw_line 'spatial_streams: 1

            ''')

    #parser.add_argument('--json', help="--json <config.json> json input file", default="config.json")
    parser.add_argument('--cmd', help="--cmd <json_cmd> json command", default="")
    args = parser.parse_args()   
    json_cmd = args.cmd
    print("json cmd {}".format(json_cmd))
    #with open(config_json, 'r') as config_file:
    #    config_data = json.load(config_file)
    #print(config_data)

    lf_get = lf_json_autogen.LFJsonGet(lfclient_host='192.168.0.101',
                                        lfclient_port=8080,
                                        debug_=True,
                                        )

    duts = lf_get.get_chamber(fields = [lf_get.duts])
    print("duts {}".format(duts))

    


    print("END  lf_read_json.py")


if __name__ == "__main__":
     main()