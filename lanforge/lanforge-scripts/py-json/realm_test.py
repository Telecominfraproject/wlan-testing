#!/usr/bin/env python3
import sys
import os
import importlib
import time
from pprint import pprint

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


localrealm = Realm("localhost", 8080, True)

print("** Existing Stations **")
try:
    sta_list = localrealm.station_list()
    print("\n%s Station List:" % len(sta_list))
    print(sta_list)
    del sta_list
    sta_map = localrealm.station_map()
    print("\n%s Station Map:" % len(sta_map))
    print(sta_map)
    del sta_map
    print("\n  Stations like wlan+:")
    print(localrealm.find_ports_like("wlan+"))
    print("\n  Stations like wlan0:")
    print(localrealm.find_ports_like("wlan0*"))
    print("\n  Stations between wlan0..wlan2:")
    print(localrealm.find_ports_like("wlan[0..2]"))
except Exception as x:
    pprint(x)
    exit(1)

print("\n** Removing previous stations **")
station_map = localrealm.find_ports_like("sta+")
for eid,record in station_map.items():
    pprint(eid)
    # a list of these objects is not super useful unless
    localrealm.remove_vlan_by_eid(eid)
    time.sleep(0.03)

# convert station map to plain list
del_sta_names = []
try:
    for eid,value in station_map.items():
        #print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        #pprint(eid)
        #print("rfind: %d" % )
        #print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        tname = eid[eid.rfind('.'):]
        del_sta_names.append(tname)
except Exception as x:
    localrealm.error(x)

LFUtils.waitUntilPortsDisappear(resource_id=1, base_url=localrealm.lfclient_url, port_list=del_sta_names, debug=False)
print("** Creating Stations **")
profile = localrealm.new_station_profile()
profile.use_wpa2(True, "jedway-wpa2-x2048-5-1", "jedway-wpa2-x2048-5-1")
profile.set_command_flag("add_sta", "80211u_enable", 1)
profile.set_number_template("0100")
profile.create(1, "wiphy0", 5)

try:
    sta_list = localrealm.station_list()
    print("%s Stations:" % {len(sta_list)})
    pprint(sta_list)
    print("  Stations like wlan+:")
    print(localrealm.find_ports_like("wlan+"))
    print("  Stations like wlan0:")
    print(localrealm.find_ports_like("wlan0*"))
    print("  Stations between wlan0..wlan2:")
    print(localrealm.find_ports_like("wlan[0..2]"))
except Exception as x:
    pprint(x)
    exit(1)

print(" - - - - TESTING - - - - - -")
#exit(0)

print("** Existing vAPs **")
try:
    vap_list = localrealm.vap_list()
    print("%s VAPs:" % len(vap_list))
    pprint(vap_list)
except Exception as x:
    localrealm.error(x)
    exit(1)

print("** Existing CXs **")
try:
    cx_list = localrealm.cx_list()
    print("%s CXs:" % len(cx_list))
    pprint(cx_list)
except Exception as x:
    localrealm.error(x)
    exit(1)

print("** Removing previous CXs **")

print("** Creating Layer 3 CXs **")
try:
    cx_profile = localrealm.new_l3_cx_profile()
    # set attributes of cxProfile
    cx_profile.create("lf_udp", side_a="1.1.eth1", side_b=list(localrealm.find_ports_like("sta+")))
except Exception as x:
    pprint(x)
    exit(1)

try:
    cx_profile = localrealm.new_l3_cx_profile()
    # set attributes of cxProfile
    cx_profile.create("lf_udp", side_a=list(localrealm.find_ports_like("sta+")), side_b="1.1.eth1")
except Exception as x:
    pprint(x)
    exit(1)

print("** Creating Layer 4 CXs **")
try:
    cx_profile = localrealm.new_l4_cx_profile()
    # set attributes of cxProfile
    cx_profile.create(localrealm.find_ports_like("sta+"))
except Exception as x:
    pprint(x)
    exit(1)

print("** Creating Generic CXs **")
try:
    cx_profile = localrealm.new_generic_cx_profile()
    # set attributes of cxProfile
    cx_profile.create(localrealm.find_ports_like("sta+"))
except Exception as x:
    pprint(x)
    exit(1)
#
exit(0)
