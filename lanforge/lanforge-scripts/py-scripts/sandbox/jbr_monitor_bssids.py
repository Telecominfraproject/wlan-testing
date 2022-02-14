#!/usr/bin/env python3
"""
NAME: jbr_monitor_bssids.py

PURPOSE: Creates a series of stations and L3 connections
Uses lanforge_api.

EXAMPLE:
$ ./jbr_monitor_bssids.py --host ct521a-manx \
    --radio 1.1.wiphy0 \
    --traffic_dur_sec 60 \
    --test_duration_min 120 \
    --security wpa2 \
    --ssid cyrus \
    --passwd HelloRudy \
    --bssid cc:32:e5:4b:ef:b3 \
    --bssid cc:32:e5:4b:ef:b4 \
    --bssid 70:4f:57:1e:15:af \
    --bssid 70:4f:57:1e:15:ae \
    --bssid d8:0d:17:be:ab:36 \
    --bssid d8:0d:17:be:ab:37 \
    --bssid 54:83:3a:9c:38:7f \

Notes:
  # cyrus1 161-    3x3 MCS 0-9 AC WPA2     cc:32:e5:4b:ef:b3 -31.0  5805      100    5.76 m
  cyrus1 11      3x3 MIMO       WPA2     cc:32:e5:4b:ef:b4 -32.0  2462      100    5.76 m
  cyrus  1       3x3 MIMO       WPA2     70:4f:57:1e:15:af -48.0  2412      100    5.76 m
  cyrus  149+    4x4 MCS 0-9 AC WPA2     70:4f:57:1e:15:ae -53.0  5745      100    5.76 m
  cyrus  157+    3x3 MCS 0-9 AC WPA2     d8:0d:17:be:ab:36 -64.0  5785      100    5.76 m
  cyrus  11      3x3 MIMO       WPA2     d8:0d:17:be:ab:37 -65.0  2462      100    5.76 m
  cyrus  11      3x3 MIMO       WPA WPA2 54:83:3a:9c:38:7f -72.0  2462      100    5.76 m



TO DO NOTES:

"""
import logging
import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import os
import importlib
import argparse
import time
from http.client import HTTPResponse
from typing import Optional
from pprint import pprint

path_hunks = os.path.abspath(__file__).split('/')
while (path_hunks[-1] != 'lanforge-scripts'):
    path_hunks.pop()
sys.path.append(os.path.join("/".join(path_hunks)))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
Logg = lanforge_api.Logg
LFSession = lanforge_api.LFSession
LFJsonCommand = lanforge_api.LFJsonCommand
LFJsonQuery = lanforge_api.LFJsonQuery


# from scenario import LoadScenario


# print(pprint.pformat(("ospath", sys.path)))

class BssidMonitor(Realm):
    def __init__(self,
                 host: str = "localhost",
                 port: int = 8080,
                 debug: bool = False,
                 args: argparse = None,
                 radio: str = None,
                 ssid: str = None,
                 security: str = None,
                 password: str = None,
                 upstream: str = None,
                 mode: int = 0,
                 side_a_min_rate: int = 256000,
                 side_b_min_rate: int = 256000,
                 test_duration_min: str = "5m",
                 report_file: str = None,
                 output_format: str = None,
                 layer3_cols: list = None,  # p3.9 list[str]
                 port_mgr_cols=None,
                 monitor_interval_sec: int = 10,
                 bssid_list: list = None):  # p3.9 list[str]
        """
                         lfclient_host="localhost",
                 lfclient_port=8080,
                 debug_=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=[]
        :param host:
        :param port:
        :param radio:
        :param ssid:
        :param security:
        :param password:
        :param upstream:
        :param mode:
        :param side_a_min_rate:
        :param side_b_min_rate:
        :param test_duration_min:
        :param report_file:
        :param output_format:
        :param layer3_cols:
        :param port_mgr_cols:
        :param monitor_interval_sec:
        :param bssid_list:
        """
        super().__init__(lfclient_host=host,
                         lfclient_port=port,
                         debug_=debug,
                         _exit_on_error=True,
                         _exit_on_fail=False)
        self.radio: str = radio
        self.ssid: str = ssid
        self.security: str = security
        self.password: str = password
        self.upstream: str = upstream
        self.mode: int = mode
        self.side_a_min_rate: int = side_a_min_rate
        self.side_b_min_rate: int = side_b_min_rate
        self.test_duration = test_duration_min
        self.report_file: str = report_file
        self.output_format: str = output_format
        self.port_mgr_cols: list = port_mgr_cols  # p3.9 list[str]
        self.layer3_cols = layer3_cols  # py 3.9.x tuple[Optional[list[str]]]
        # self.layer3_cols: tuple = layer3_cols # py 3.7.7
        self.monitor_interval_sec: int = monitor_interval_sec

        if not bssid_list:
            raise ValueError("bssid list necessary to continue")
        self.bssid_list: list = bssid_list  # p 3.9: list[str]
        self.bssid_sta_profiles: dict = {}  #p3.9: dict[str,str]

        '''
        session = LFSession(lfclient_url="http://localhost:8080",
                        connect_timeout_sec=20,
                        proxy_map={
                                'http':'http://192.168.1.250:3128'
                            },
                        debug=True,
                        die_on_error=False);'''

        self.lf_session: LFSession = \
            lanforge_api.LFSession(lfclient_url="http://{host}:{port}/".format(host=host, port=port),
                                   debug=debug,
                                   connection_timeout_sec=2,
                                   stream_errors=True,
                                   stream_warnings=True,
                                   require_session=True,
                                   exit_on_error=True)
        if args and args.debugging:
            pprint(args.debugging)
            # we could have a nested list here?
            for item in args.debugging:
                if (type(item) is list):
                    item = item[0]
                if item.startswith("tag:"):
                    Logg.register_tag(item[item.rindex(":"):])
                if item.startswith("method:"):
                    Logg.register_method_name(item[item.rindex(":"):])

        self.lf_command: LFJsonCommand = self.lf_session.get_command()
        self.lf_query: LFJsonQuery = self.lf_session.get_query()

    def build(self):
        # get last event id
        last_event_id = self.before_load_action()

        # load a database
        response: HTTPResponse = self.lf_command.post_load(name="BLANK",
                                                           action="overwrite",
                                                           clean_dut="NA",
                                                           clean_chambers="NA",
                                                           debug=self.debug)

        if not self.wait_for_load_to_finish(since_id=last_event_id):
            exit(1)

        if not response:
            raise ConnectionError("lf_command::post_load returned no response")

        # create a series of stations
        for bssid in self.bssid_list:
            print("build: bssid: %s" % bssid)

    def before_load_action(self):
        """
        Use this
        :return: last event ID in event list
        """
        err_warn_list = []
        self.lf_command.post_show_events(p_type='all',
                                         shelf=1,
                                         card='all',
                                         port='all',
                                         endp='all')
        time.sleep(0.2)

        event_response = self.lf_query.events_last_events(event_count=1,
                                                          debug=self.debug,
                                                          wait_sec=1,
                                                          max_timeout_sec=120,
                                                          errors_warnings=err_warn_list)
        if not event_response:
            Logg.logg(level=logging.ERROR, msg="No event_response, we should have retried that")
            return
        # pprint(("event_response:", event_response))
        if "id" not in event_response:
            pprint(("event_response:", event_response))
            return
        return event_response["id"]

    def wait_for_load_to_finish(self, since_id: int = None):
        """
        TODO: make this a standard method outside this module
        :param since_id:
        :return:
        """
        completed = False
        timer = 0
        timeout = 60
        while not completed:
            new_events = self.lf_query.events_since(event_id=since_id)
            if new_events:
                for event_tup in new_events:
                    for event_id in event_tup.keys():
                        event_record = event_tup[event_id]
                        if self.debug:
                            pprint("\n        wait_for_load_to_finish: {since} -> {id}: {descr}\n".format(
                                since=since_id,
                                id=event_id,
                                descr=event_record['event description']
                            ))
                        if event_record['event description'].startswith('LOAD COMPLETED'):
                            completed = True
                            self.lf_query.logger.warning('Scenario loaded after %s seconds' % timer)
                            break
            if completed:
                break
            else:
                if (timer % 5) == 0:
                    self.lf_command.post_show_events(p_type='all',
                                                     shelf=1,
                                                     card='all',
                                                     port='all',
                                                     endp='all')
                timer += 1
                time.sleep(1)
                if timer > timeout:
                    completed = True
                    print('Scenario failed to load after %s seconds' % timeout)
                    break
                else:
                    print('Waiting %s out of %s seconds to load scenario' % (timer, timeout))
        return completed

    def start(self):
        pass

    def stop(self):
        pass

    def cleanup(self):
        pass


def main():
    parser = Realm.create_basic_argparse(
        formatter_class=argparse.RawTextHelpFormatter,
        prog=__file__,
        epilog="",
        description="Monitor traffic to different APs and report connection stability")

    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--bssid',
                        action='append', # action='extend' appears in py 3.9
                        type=str,
                        nargs="+",
                        help='Add an AP to the list of APs to test connections to')
    #parser.add_argument('--debugging',
    #                    action='extend',
    #                    type=str,
    #                    nargs="+",
    #                    help='Debugging for specific areas: "tag:keyword" or "method:methodname" ')
    parser.add_argument('--output_format',
                        type=str,
                        help='choose either csv or xlsx')
    parser.add_argument('--report_file',
                        default=None,
                        type=str,
                        help='where you want to store results')
    parser.add_argument('--a_min',
                        default=256000,
                        type=int,
                        help='bps rate minimum for side_a')
    parser.add_argument('--b_min',
                        default=256000,
                        type=int,
                        help='bps rate minimum for side_b')
    parser.add_argument('--test_duration_min',
                        default="2",
                        type=int,
                        help='duration of the test in minutes')
    parser.add_argument('--layer3_cols',
                        type=list,  # py3.9 list[str]
                        help='titles of columns to report')
    parser.add_argument('--port_mgr_cols',
                        type=list,  # py3.9 list[str]
                        help='titles of columns to report')

    args = parser.parse_args()

    # pprint.pprint(("args.members:", dir(args)))

    bssid_monitor = BssidMonitor(host=args.mgr,
                                 port=args.mgr_port,
                                 debug=args.debug,
                                 args=args,
                                 radio=args.radio,
                                 ssid=args.ssid,
                                 security=args.security,
                                 password=args.passwd,
                                 upstream=args.upstream_port,
                                 mode=args.mode,
                                 side_a_min_rate=args.a_min,
                                 side_b_min_rate=args.b_min,
                                 test_duration_min=args.test_duration_min,
                                 report_file=args.report_file,
                                 output_format=args.output_format,
                                 layer3_cols=args.layer3_cols,
                                 port_mgr_cols=args.port_mgr_cols,
                                 monitor_interval_sec=10,
                                 bssid_list=args.bssid)

    bssid_monitor.build()
    bssid_monitor.start()
    bssid_monitor.stop()
    bssid_monitor.cleanup()


if __name__ == "__main__":
    main()
#
