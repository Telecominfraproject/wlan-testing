#!/usr/bin/env python3
# Contains examples of using realm to query stations and get specific information from them
import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class StationsConnected(LFCliBase):
    def __init__(self, lfjson_host, lfjson_port):
        super().__init__(_lfjson_host=lfjson_host, _lfjson_port=lfjson_port, _debug=False)
        self.localrealm = Realm(lfclient_host=lfjson_host, lfclient_port=lfjson_port, debug=False)
        self.check_connect()

    def run(self):
        self.clear_test_results()
        fields = "_links,port,alias,ip,ap,port+type"
        self.station_results = self.localrealm.find_ports_like("sta*", fields, debug_=False)
        #pprint(self.station_results)
        if (self.station_results is None) or (len(self.station_results) < 1):
            self.get_failed_result_list()
            return False
        return True

    def num_associated(self, bssid):
        counter = 0
        # print("there are %d results" % len(self.station_results))
        for eid,record in self.station_results.items():
            #print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
            #pprint(eid)
            #pprint(record)
            if record["ap"] == bssid:
                counter += 1
            #print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
        return counter

def main():
    qstationsx = StationsConnected("localhost", 8080)
    bssid = "00:0E:8E:7B:DF:9B"
    if qstationsx.run():
        associated_stations = qstationsx.num_associated(bssid)
        print("Number of stations associated to %s: %s" % (bssid, associated_stations))
    else:
        print("problem querying for stations for %s" % bssid)

if __name__ == "__main__":
    main()
