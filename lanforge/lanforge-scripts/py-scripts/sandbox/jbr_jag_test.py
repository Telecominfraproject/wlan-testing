#!/usr/bin/env python3
'''
NAME: jbr_jag_test.py

PURPOSE: exercises the LANforge/lf_json_autogen.py library

EXAMPLE:
$ ./jbr_jag_test.py --host ct521a-jana --test set_port

NOTES:
    this has not been worked on in a while, many parameters have changed

TO DO NOTES:

'''
import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()
import os

sys.path.append(os.path.join(os.path.abspath(__file__ + "/../../../")))
import importlib

import argparse
import pprint
import traceback

lanforge_client = importlib.import_module("lanforge_client")

import lanforge_client.lanforge_api
from lanforge_client.lanforge_api import LFSession
from lanforge_client.lanforge_api import LFJsonQuery as LFGet
from lanforge_client.lanforge_api import LFJsonCommand as LFPost

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
station_profile = importlib.import_module("py-json.station_profile")
StationProfile = station_profile.StationProfile

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
class TestStation(Realm):
    def __init__(self,
                 host="localhost",
                 port=8080,
                 debug_=True,
                 _exit_on_error=True,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=host,
                         lfclient_port=port,
                         debug_=debug_,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail)

    def run(self, get_request: LFGet = None, post_request: LFPost = None):
        station_profile = StationProfile(
            "http://%s:%s" % (self.lfclient_host, self.lfclient_port),
            self,
            ssid="jedway-r7800-5G",
            ssid_pass="jedway-r7800-5G",
            security="wpa2",
            number_template_="000",
            mode=0,
            up=True,
            resource=1,
            shelf=1,
            dhcp=True,
            debug_=self.debug,
            use_ht160=False)

        print("Checking for previous station:")
        try:
            response = get_request.get_port(eid_list=["1.1.sta000"], requested_col_names=['_links', 'alias'],
                                            debug=self.debug)
            if response:
                pprint.pprint(response)
                print("Deleting previous station:")
                post_request.post_rm_vlan(shelf=1,
                                          resource=1,
                                          port="sta000",
                                          debug=self.debug,
                                          suppress_related_commands=True)
            else:
                print("Previous station not seen")

            print("Creating station:")
            station_profile.create(radio="1.1.wiphy0",
                                   num_stations=1,
                                   sta_names_=['sta000'],
                                   debug=True)
            print("Created station:")
            response = get_request.get_port(eid_list=["1.1.sta000"])
            if response:
                pprint.pprint(response)
            else:
                print("Station did not get created.")

        except Exception as x:
            traceback.print_tb(x)
            print(x.__repr__())
            exit(1)


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='tests lf_json_autogen')
    parser.add_argument("--host", help='specify the GUI to connect to, assumes port 8080')
    parser.add_argument("--test", help='specify a test to run')

    args = parser.parse_args()
    if not args.test:
        print("No test requested")
        exit(1)

    session = LFSession(lfclient_url=args.host,
                        debug=True,
                        connection_timeout_sec=1.0,
                        require_session=True,
                        exit_on_error=True)

    post_request = LFPost(session_obj=session)
    get_request = LFGet(session_obj=session)

    if args.test.endswith("get_port"):
        test_get_port(args, get_request=get_request, post_request=post_request)
    if args.test.endswith("set_port"):
        test_set_port(args, get_request=get_request, post_request=post_request)


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def test_get_port(args=None,
                  get_request: LFGet = None,
                  post_request: LFPost = None):
    print("test_get_port")
    if not args:
        raise ValueError("test_get_port needs args")

    result = get_request.get_port(eid_list=["1.1.eth0", "1.1.eth1", "1.1.eth2"],
                                  requested_col_names=(),
                                  debug=True)
    pprint.pprint(result)


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def test_set_port(args=None,
                  get_request: LFGet = None,
                  post_request: LFPost = None):
    print("test_set_port")
    if not args:
        raise ValueError("test_set_port needs args")

    my_current_flags = 0
    my_interest_flags = 0
    try:
        my_current_flags = LFPost.set_flags(LFPost.SetPortCurrentFlags,
                                            0,
                                            ['if_down', 'use_dhcp'])

        my_current_flags = LFPost.set_flags(LFPost.SetPortCurrentFlags,
                                            my_current_flags,
                                            [
                                             LFPost.SetPortCurrentFlags.if_down,
                                             LFPost.SetPortCurrentFlags.use_dhcp
                                         ])

        my_interest_flags = LFPost.set_flags(LFPost.SetPortInterest,
                                             0,
                                             [
                                              'current_flags',
                                              'ifdown',
                                              'dhcp'
                                          ])
        post_request.post_set_port(current_flags=my_current_flags,  # See above, or NA.
                                   current_flags_msk=my_current_flags,
                                   mac='NA',
                                   # This sets 'interest' for flags 'Enable RADIUS service' and higher. See above, or NA.
                                   interest=my_interest_flags,
                                   port='eth2',  # Port number for the port to be modified.
                                   report_timer=2000,
                                   resource=1,  # Resource number for the port to be modified.
                                   shelf=1,  # Shelf number for the port to be modified.
                                   suppress_related_commands=True,
                                   debug=True)

        my_current_flags = LFPost.clear_flags(LFPost.SetPortCurrentFlags,
                                              my_current_flags,
                                              flag_names=LFPost.SetPortCurrentFlags.use_dhcp)
        my_current_flags = LFPost.clear_flags(LFPost.SetPortCurrentFlags,
                                              my_current_flags,
                                              flag_names=[LFPost.SetPortCurrentFlags.if_down])

        my_interest_flags = LFPost.set_flags(LFPost.SetPortInterest,
                                             0,
                                             [
                                              'current_flags',
                                              'ifdown',
                                              'dhcp',
                                              LFPost.SetPortInterest.ip_address,
                                              LFPost.SetPortInterest.ip_gateway,
                                              LFPost.SetPortInterest.ip_Mask,
                                          ])

        post_request.post_set_port(alias=None,  # A user-defined name for this interface.  Can be BLANK or NA.
                                   current_flags=my_current_flags,  # See above, or NA.
                                   current_flags_msk=my_current_flags,
                                   mac='NA',
                                   ip_addr='10.32.23.1',
                                   netmask='255.255.255.0',
                                   gateway='0.0.0.0',
                                   # This sets 'interest' for flags 'Enable RADIUS service' and higher. See above, or NA.
                                   interest=my_interest_flags,
                                   port='eth2',  # Port number for the port to be modified.
                                   report_timer=2000,
                                   resource=1,  # Resource number for the port to be modified.
                                   shelf=1,  # Shelf number for the port to be modified.
                                   suppress_related_commands=True,
                                   debug=True)

        result = get_request.get_port(eid_list="1.1.eth2",
                                      requested_col_names=["_links",
                                                           "alias",
                                                           "port",
                                                           "mac",
                                                           "down",
                                                           "ip",
                                                           "PORT_SUPPORTED_FLAGS_L",
                                                           "PORT_SUPPORTED_FLAGS_H",
                                                           "PORT_CUR_FLAGS_L",
                                                           "PORT_CUR_FLAGS_H"],
                                      debug=True)
        pprint.pprint(result)
    except Exception as x:
        traceback.print_tb(x)
        print(x.__repr__())
        exit(1)

    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
    #       Create a station using the station_profile object
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
    try:
        station_test = TestStation(host=args.host,
                                   port=8080)
        station_test.run(get_request=get_request, post_request=post_request)

    except Exception as x:
        traceback.print_tb(x)
        print(x.__repr__())
        exit(1)


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #


if __name__ == "__main__":
    main()
#
