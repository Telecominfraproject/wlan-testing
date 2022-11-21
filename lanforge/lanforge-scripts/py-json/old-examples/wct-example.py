#!/usr/bin/python3
'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                                                                             -
# Example of how to operate a WCT instance using cli-socket.                  -
# This script is out-dated. Please refer to py-scripts/run_cv_scenario.py     -
#                                                                             -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
make sure pexpect is installed:
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial
$ pip3 install XlsxWriter

'''

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()
import argparse
import logging
import time
from time import sleep
import pexpect
import xlsxwriter
import pprint
import LANforge
from LANforge import LFRequest
from LANforge import LFUtils
from LANforge.LFUtils import NA

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main():
    host = "ct524-debbie.jbr.candelatech.com"
    base_url = "http://%s:8080"%host
    resource_id = 1     # typically you're using resource 1 in stand alone realm
    radio = "wiphy0"
    start_id = 200
    end_id = 202
    padding_number = 10000 # the first digit of this will be deleted
    ssid = "jedway-wpa2-x64-3-1"
    passphrase = "jedway-wpa2-x64-3-1"
    clisock = 3990
    cliprompt = 'lfgui# '

    parser = argparse.ArgumentParser(description="test creating a station")
    parser.add_argument("-m", "--host", type=str, help="json host to connect to")
    parser.add_argument("-r", "--radio", type=str, help="radio to create a station on")
    parser.add_argument("-a", "--start_id", type=int, help="starting station id")
    parser.add_argument("-b", "--end_id", type=int, help="ending station id")
    parser.add_argument("-s", "--ssid", type=str, help="station ssid")
    parser.add_argument("-p", "--passwd", type=str, help="password for ssid")

    args = None
    try:
      args = parser.parse_args()
      if (args.host is not None):
         host = args.host,
         baseurl = base_url = "http://%s:8080"%host
      if (args.radio is not None):
         radio = args.radio
      if (args.start_id is not None):
         start_id = args.start_id
      if (args.end_id is not None):
         end_id = args.end_id
      if (args.ssid is not None):
         ssid = args.ssid
      if (args.passwd is not None):
         passphrase = args.passwd
    except Exception as e:
      logging.exception(e)
      usage()
      exit(2)

    # station numbers are heavily manipulated strings, often using manual padding
    # sta200 is not sta0200 nor sta00200, and we can format these numbers by adding
    # a 1000 or 10000 to the station id, and trimming the first digit off

    j_printer = pprint.PrettyPrinter(indent=2)
    json_post = ""
    json_response = ""
    found_stations = []
    lf_r = LFRequest.LFRequest(base_url+"/port/1/1/wiphy2")
    wiphy0_json = lf_r.getAsJson()
    if (wiphy0_json is None) or (wiphy0_json['interface'] is None):
        print("Unable to find radio. Are we connected?")
        exit(1)

    desired_stations = LFUtils.portNameSeries("sta", start_id, end_id, padding_number)
    #LFUtils.debug_printer.pprint(desired_stations)
    print("Example 1: will create stations %s"%(",".join(desired_stations)))
    for sta_name in desired_stations:
        url = base_url+"/port/1/%s/%s" % (resource_id, sta_name)
        print("Ex 1: Checking for station : "+url)
        lf_r = LFRequest.LFRequest(url)
        json_response = lf_r.getAsJson(show_error=False)
        if (json_response != None):
            found_stations.append(sta_name)

    for sta_name in found_stations:
        print("Ex 1: Deleting station %s ...."%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/rm_vlan")
        lf_r.addPostData( {
            "shelf":1,
            "resource": resource_id,
            "port": sta_name
        })
        json_response = lf_r.formPost()
        sleep(0.05) # best to give LANforge a few millis between rm_vlan commands

    LFUtils.waitUntilPortsDisappear(resource_id, base_url, found_stations)

    print("Ex 1: Next we create stations...")
    #68727874560 was previous flags
    for sta_name in desired_stations:
        print("Ex 1: Next we create station %s"%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/add_sta")
        lf_r.addPostData( LFUtils.staNewDownStaRequest(sta_name, resource_id=resource_id, radio=radio, ssid=ssid, passphrase=passphrase))
        lf_r.formPost()
        sleep(0.1)

    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)
    for sta_name in desired_stations:
        sleep(1)
        print("doing portSetDhcpDownRequest on "+sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/set_port")
        data = LFUtils.portDhcpUpRequest(resource_id, sta_name)
        lf_r.addPostData(data)
        lf_r.jsonPost()

    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)

    # Now lets do some cli-socket scripting
    gui_telnet = pexpect.spawn('telnet %s %s'%(host, clisock))
    if gui_telnet is None:
        print ("Unable to telnet to %s:%s"%(host,clisock));
        exit(1)

    gui_telnet.expect('lfgui# ')
    gui_telnet.sendline("cv create 'WiFi Capacity' 'wct'")
    gui_telnet.expect('OK')
    gui_telnet.sendline("cv load wct wct-wpa2-x64-two-loops")
    gui_telnet.expect('OK')
    gui_telnet.sendline("cv click wct 'Auto Save Report'")
    gui_telnet.expect('OK')
    gui_telnet.sendline("cv click wct Start")


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()


####
####
####
