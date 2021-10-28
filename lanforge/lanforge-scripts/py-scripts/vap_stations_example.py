#!/usr/bin/env python3
"""
This is an outdated example. Please see modern py-scripts/test_X example scripts.
"""
import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))


lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
# from generic_cx import GenericCx

mgrURL = "http://localhost:8080/"
staName = "sta0"
staNameUri = "port/1/1/" + staName


class VapStations(LFCliBase):
    def __init__(self, lfhost, lfport):
        super().__init__(lfhost, lfport, _debug=False)
        super().check_connect()

    def run(self):
        list_resp = self.json_get("/stations/list")
        list_map = self.response_list_to_map(list_resp, 'stations')
        # pprint.pprint(list_map)

        attribs = ["ap", "capabilities", "tx rate", "rx rate", "signal"]
        for eid,record in list_map.items():
            # print("mac: %s" % mac)
            mac = record["station bssid"]
            station_resp = self.json_get("/stations/%s?fields=capabilities,tx+rate,rx+rate,signal,ap" % mac)
            print("Station %s:" %mac)
            #pprint.pprint(station_resp)
            for attrib in attribs:
                print("     %s:    %s" % (attrib, station_resp["station"][attrib]))


def main():
    vapsta_test = VapStations("localhost", 8080)
    vapsta_test.run()

if __name__ == '__main__':
    main()
