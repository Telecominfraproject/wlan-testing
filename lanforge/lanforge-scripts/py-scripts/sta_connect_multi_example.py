#!/usr/bin/env python3
# Example of how to instantiate StaConnect and run the test
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

# if you lack __init__.py in this directory you will not find sta_connect module
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
sta_connect = importlib.import_module("py-scripts.sta_connect")
StaConnect = sta_connect.StaConnect


def main():
    parser = argparse.ArgumentParser(
        prog='sta_connected_multip_example.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        sta_connected_multip_example.py

            ''',
        description='''\
Example of how to instantiate StaConnect and run the test
        ''')
    # args = parser.parse_args() - add this line if adding arguments
    parser.parse_args()

    # create multiple OPEN stations
    station_names = LFUtils.port_name_series(start_id=0, end_id=1)

    test = StaConnect("localhost", 8080, _debugOn=False, _exit_on_error=True,
                      _cleanup_on_exit=False, _runtime_sec=360, _exit_on_fail=True)
    test.sta_mode = sta_connect.MODE_AUTO
    test.upstream_resource = 1
    test.upstream_port = "eth1"
    test.radio = "wiphy0"
    test.resource = 1
    test.dut_security = sta_connect.OPEN
    test.dut_ssid = "jedway-open"
    test.dut_passwd = "[BLANK]"
    test.station_names = station_names
    test.runtime_secs = 5
    test.cleanup_on_exit = True
    test.run()
    is_passing = test.passes()

    # recorded stations and endpoints can be retrieved this way:
    '''
    for sta_name in test.resulting_stations:
        print("** recorded: "+sta_name)
        pprint.pprint(test.resulting_stations[sta_name])

    for endp_name in test.resulting_endpoints:
        print("** endp: "+endp_name)
        pprint.pprint(test.resulting_endpoints[endp_name])
    '''
    if not is_passing:
        # run_results = staConnect.get_failed_result_list()
        fail_message = test.get_fail_message()
        print("Some tests failed:\n" + fail_message)
        return
    else:
        print("Tests pass")

    # Stations use WPA2
    test.dut_security = sta_connect.WPA2
    test.dut_ssid = "jedway-wpa2-x2048-5-1"
    test.dut_passwd = "jedway-wpa2-x2048-5-1"
    test.run()
    is_passing = test.passes()
    if not is_passing:
        # run_results = staConnect.get_failed_result_list()
        fail_message = test.get_fail_message()
        print("Some tests failed:\n" + fail_message)
        return
    else:
        print("Tests pass")

    if test.cleanup_on_exit:
        test.remove_stations()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':
    main()

#
