#!/usr/bin/env python3

"""
NAME: sta_scan_test.py

PURPOSE:
Creates a station with specified ssid info (can be real or fake ssid, if fake use open for security), then
starts a scan and waits 15 seconds, finally scan results are printed to console

Use './sta_scan_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os
import importlib
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

import argparse
import time

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


class StaScan(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 sta_list=None,
                 upstream=None,
                 radio=None,
                 host="localhost",
                 port=8080,
                 mode=0,
                 number_template="00000",
                 csv_output=False,
                 use_ht160=False,
                 use_existing_station=False,
                 scan_time=15,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        if sta_list is None:
            sta_list = []
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.mode = mode
        self.number_template = number_template
        self.csv_output = csv_output
        self.debug = _debug_on
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug

        self.station_profile.use_ht160 = use_ht160
        self.scan_time = scan_time
        self.use_existing_station = use_existing_station
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode

    def start(self):
        if self.use_existing_station:
            # bring up existing sta list
            #print(self.sta_list)
            for s in self.sta_list:
                eid = LFUtils.name_to_eid(s)
                up_request = LFUtils.port_up_request(resource_id=eid[1], port_name=eid[2])
                self.json_post("/cli-json/set_port", up_request)
        else:
            self.station_profile.admin_up()
            self.sta_list = self.station_profile.station_names

        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=self.sta_list,
                                          debug_=self.debug)

        if self.debug:
            print("ports are admin-up, initiating scan requests.")

        # Request port-table info for stations on each resource.
        #stations = [LFUtils.name_to_eid(x) for x in self.sta_list]
        #stations = pd.DataFrame(stations)
        #resources = stations[1].unique()
        #interfaces = list()
        #for resource in resources:
        #    if self.debug:
        #        print("Requesting port listing on resource: %s"%(resource))
        #    shelf = stations[0][0]
        #    resource_station = list(stations[stations[1] == resource][2])
        #    url = '/port/%s/%s/%s' % (shelf, resource, ','.join(resource_station))
        #    if self.debug:
        #        print("Requesting station scan on resource with url: %s"%(url))
        #    response = self.json_get(url)
        #    if 'interface' in response.keys():
        #        interface = response['interface']
        #        interfaces.append(interface)
        #    elif 'interfaces' in response.keys():
        #        response_interfaces = response['interfaces']
        #        for interface in response_interfaces:
        #            for item in interface.values():
        #                interfaces.append(item)

        #df = pd.DataFrame(interfaces)
        #stations = df[df['port type'] == 'WIFI-STA']
        #stations = list(stations.drop_duplicates('parent dev')['alias'])
        #stations = [station for station in stations if station in self.sta_list]

        #if self.debug:
        #    print("interfaces: %s\nstations: %s"%(interfaces, stations))

        # Start scan on all stations.
        for port in self.sta_list:
            port = LFUtils.name_to_eid(port)
            data = {
                "shelf": port[0],
                "resource": port[1],
                "port": port[2]
            }
            self.json_post("/cli-json/scan_wifi", data)

        # TODO:  Make configurable
        # Wait for scans to complete.
        if self.debug:
            print("Waiting for %s seconds for scan to complete" %(self.scan_time))
        time.sleep(self.scan_time)

        # Get results for all stations.
        fmt = "%08s\t%015s\t%023s\t%07s\t%020s\t%07s\t%09s\t%07s"
        if not self.csv_output:
            print(fmt % ("Resource", "Station", "BSS", "Signal", "SSID", "Channel", "Frequency", "Age"))

        for p in self.sta_list:
            port = LFUtils.name_to_eid(p)
            data = {
                "shelf": port[0],
                "resource": port[1],
                "port": port[2]
            }
            scan_results = self.json_get("scanresults/%s/%s/%s" % (port[0], port[1], port[2]))
            if self.debug:
                print("Scan results for port: %s\n%s"%(port, scan_results))
            if self.csv_output:
                # TODO:  This clobbers output of previous station, need a way to
                # append (and add resource and wlan to the csv output so that
                # multiple stations can be reported.
                results = scan_results['scan-results']
                df = pd.DataFrame([list(result.values())[0] for result in results])
                df.to_csv(self.csv_output)
                print('CSV output saved at %s' % self.csv_output)
            else:
                for result in scan_results['scan-results']:
                    for name, info in result.items():
                        print(fmt % (port[1], port[2], info['bss'], info['signal'], info['ssid'],
                                     info['channel'], info['frequency'], info['age']))

    def pre_cleanup(self):
        self.station_profile.cleanup(self.sta_list)

    def cleanup(self):
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, num_stations=1, debug=self.debug)
        self._pass("PASS: Station build finished")
        LFUtils.wait_until_ports_appear(base_url=self.lfclient_url, port_list=self.sta_list, debug=self.debug)


def main():
    parser = Realm.create_basic_argparse(
        prog='sta_scan_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Used to scan for ssids after creating a station
            ''',
        description='''\
        Optionally creates a station with specified ssid info (can be real or fake ssid, if fake use open for security).
        If not creating a station, it can use existing station.
        Then starts a scan and waits 15 seconds, finally scan results are printed to console.
        
        Example:
        ./sta_scan_test.py --ssid test_name --security open --radio wiphy0
        ./sta_scan_test.py --sta_name 1.14.wlan0 1.1.wlan0 --use_existing_station --scan_time 5
        ''')

    parser.add_argument('--use_existing_station', action='store_true', help='Use existing station instead of trying to create stations.')
    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--sta_name', help='Optional: User defined station names: 1.2.wlan0 1.3.wlan0', nargs='+',
                        default=["sta0000"])
    parser.add_argument('--csv_output', help='Specify file to which csv output will be saved, otherwise print it in the terminal',
                        default=None)
    parser.add_argument('--scan_time', help='Specify time in seconds to wait for scan to complete.  Default is 15',
                        default=15, type=int)

    args = parser.parse_args()

    station_list = args.sta_name
    sta_scan_test = StaScan(host=args.mgr,
                            port=args.mgr_port,
                            number_template="0000",
                            sta_list=station_list,
                            upstream=args.upstream_port,
                            ssid=args.ssid,
                            password=args.passwd,
                            radio=args.radio,
                            security=args.security,
                            use_ht160=False,
                            use_existing_station=args.use_existing_station,
                            scan_time=args.scan_time,
                            csv_output=args.csv_output,
                            mode=args.mode,
                            _debug_on=args.debug)

    if (not args.use_existing_station):
        sta_scan_test.pre_cleanup()

        sta_scan_test.build()
        # exit()
        if not sta_scan_test.passes():
            print(sta_scan_test.get_fail_message())
            sta_scan_test.exit_fail()

    sta_scan_test.start()

    if (not args.use_existing_station):
        sta_scan_test.cleanup()


if __name__ == "__main__":
    main()
