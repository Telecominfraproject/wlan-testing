#!/usr/bin/python3
# Create and modify WAN Links Using LANforge JSON AP : http://www.candelatech.com/cookbook.php?vol=cli&book=JSON:+Managing+WANlinks+using+JSON+and+Python
# Written by Candela Technologies Inc.
# Updated by: Erin Grimes

"""
sample command:
./test_wanlink.py --name my_wanlink4 --latency_A 20 --latency_B 69 --rate 1000 --jitter_A 53 --jitter_B 73 --jitter_freq 6 --drop_A 12 --drop_B 11
"""

import sys
import urllib
import importlib
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

import os
from time import sleep
from urllib import error
import pprint
import argparse
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

logger = logging.getLogger(__name__)

j_printer = pprint.PrettyPrinter(indent=2)
# todo: this needs to change
resource_id = 1


def main(args):
    base_url = 'http://'+args['host']+':8080'
    print(base_url)
    json_post = ""
    json_response = ""
    num_wanlinks = -1

    # see if there are old wanlinks to remove
    lf_r = LFRequest.LFRequest(base_url+"/wl/list")
    logger.info(lf_r.get_as_json())

    # remove old wanlinks
    if num_wanlinks > 0:
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_cx")
        lf_r.addPostData({
         'test_mgr': 'all',
         'cx_name': args['name']
        })
        lf_r.jsonPost()
        sleep(0.05)

    try:
        json_response = lf_r.getAsJson()
        LFUtils.debug_printer.pprint(json_response)
        for key, value in json_response.items():
            if isinstance(value, dict) and "_links" in value:
                num_wanlinks = 1
    except urllib.error.HTTPError as error:
        logger.error("Error code %s" % error.code)

        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_endp")
        lf_r.addPostData({
           'endp_name': args['name']+"-A"
        })
        lf_r.jsonPost()
        sleep(0.05)

        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_endp")
        lf_r.addPostData({
           'endp_name': args['name']+"-B"
        })
        lf_r.jsonPost()
        sleep(0.05)

    # create wanlink endpoint A
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_wl_endp")
    lf_r.addPostData({
        'alias': args['name']+"-A",
        'shelf': 1,
        'resource': '1',
        'port': args['port_A'],
        'latency': args['latency_A'],
        'max_rate': args['rate_A'],
    })
    lf_r.jsonPost()
    sleep(0.05)

    # create wanlink endpoint B
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_wl_endp")
    lf_r.addPostData({
        'alias': args['name']+"-B",
        'shelf': 1,
        'resource': '1',
        'port': args['port_B'],
        'latency': args['latency_B'],
        'max_rate': args['rate_B'],
    })
    lf_r.jsonPost()
    sleep(0.05)

    # create cx
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_cx")
    lf_r.addPostData({
       'alias': args['name'],
       'test_mgr': 'default_tm',
       'tx_endp': args['name']+"-A",
       'rx_endp': args['name']+"-B",
    })
    lf_r.jsonPost()
    sleep(0.05)

    # modify wanlink endpoint A
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_wanlink_info")
    lf_r.addPostData({
        'name': args['name']+"-A",
        'max_jitter': args['jitter_A'],
        'jitter_freq': args['jitter_freq_A'],
        'drop_freq': args['drop_A']
    })
    lf_r.jsonPost()
    sleep(0.05)

    # modify wanlink endpoint B
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_wanlink_info")
    lf_r.addPostData({
        'name': args['name']+"-B",
        'max_jitter': args['jitter_B'],
        'jitter_freq': args['jitter_freq_B'],
        'drop_freq': args['drop_B']
    })
    lf_r.jsonPost()
    sleep(0.05)

    # start wanlink once we see it
    seen = 0
    while seen < 1:
        sleep(1)
        lf_r = LFRequest.LFRequest(base_url+"/wl/"+args['name']+"?fields=name,state,_links")
        try:
            json_response = lf_r.getAsJson()
            if not json_response:
                continue
            LFUtils.debug_printer.pprint(json_response)
            for key, value in json_response.items():
                if isinstance(value, dict):
                    if "_links" in value:
                        if value["name"] == args['name']:
                            seen = 1
                        else:
                            pass
            #         else:
            #             print(" name was not wl_eg1")
            #     else:
            #         print("value lacks _links")
            # else:
            #     print("value not a dict")

        except urllib.error.HTTPError as error:
            logger.error("Error code %s " % error.code)
            continue

    # print("starting wanlink:")
    # # print("the latency is {laten}".format(laten=latency))
    # lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_cx_state")
    # lf_r.addPostData({
    #    'test_mgr': 'all',
    #    'cx_name': args['name'],
    #    'cx_state': 'RUNNING'
    # })
    # lf_r.jsonPost()

    running = 0
    while running < 1:
        sleep(1)
        lf_r = LFRequest.LFRequest(base_url+"/wl/"+args['name']+"?fields=name,state,_links")
        try:
            json_response = lf_r.getAsJson()
            if not json_response:
                continue
            for key, value in json_response.items():
                if isinstance(value, dict):
                    if "_links" in value:
                        if value["name"] == args['name']:
                            if value["state"].startswith("Run"):
                                LFUtils.debug_printer.pprint(json_response)
                                running = 1

        except urllib.error.HTTPError as error:
            logger.error("Error code %s" % error.code)
            continue

    logger.info("Wanlink is running")


if __name__ == '__main__':
    parser = LFCliBase.create_basic_argparse(
        prog='create_wanlink.py',
        formatter_class=argparse.RawTextHelpFormatter)
    for group in parser._action_groups:
        if group.title == "required arguments":
            required_args = group
            break

    optional_args = None
    for group in parser._action_groups:
        if group.title == "optional arguments":
            optional_args = group
            break
    if optional_args:
        optional_args.add_argument('--host', help='The resource IP address', default="localhost")
        optional_args.add_argument('--port_A', help='Endpoint A', default="eth1")
        optional_args.add_argument('--port_B', help='Endpoint B', default="eth2")
        optional_args.add_argument('--name', help='The name of the wanlink', default="wl_eg1")
        optional_args.add_argument('--rate', help='The maximum rate of transfer at both endpoints (bits/s)', default=1000000)
        optional_args.add_argument('--rate_A', help='The max rate of transfer at endpoint A (bits/s)', default=None)
        optional_args.add_argument('--rate_B', help='The maximum rate of transfer (bits/s)', default=None)
        optional_args.add_argument('--latency', help='The delay of both ports', default=20)
        optional_args.add_argument('--latency_A', help='The delay of port A', default=None)
        optional_args.add_argument('--latency_B', help='The delay of port B', default=None)
        optional_args.add_argument('--jitter', help='The max jitter of both ports (ms)', default=None)
        optional_args.add_argument('--jitter_A', help='The max jitter of port A (ms)', default=None)
        optional_args.add_argument('--jitter_B', help='The max jitter of port B (ms)', default=None)
        optional_args.add_argument('--jitter_freq', help='The jitter frequency of both ports (%%)', default=None)
        optional_args.add_argument('--jitter_freq_A', help='The jitter frequency of port A (%%)', default=None)
        optional_args.add_argument('--jitter_freq_B', help='The jitter frequency of port B (%%)', default=None)
        optional_args.add_argument('--drop', help='The drop frequency of both ports (%%)', default=None)
        optional_args.add_argument('--drop_A', help='The drop frequency of port A (%%)', default=None)
        optional_args.add_argument('--drop_B', help='The drop frequency of port B (%%)', default=None)
        # todo: packet loss A and B
        # todo: jitter A and B
        for group in parser._action_groups:
            if group.title == "optional arguments":
                optional_args = group
                break
    parseargs = parser.parse_args()
    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    args = {
        "host": parseargs.mgr,
        "port": parseargs.mgr_port,
        "name": parseargs.name,
        "port_A": parseargs.port_A,
        "port_B": parseargs.port_B,
        "latency": parseargs.latency,
        "latency_A": (parseargs.latency_A if parseargs.latency_A else parseargs.latency),
        "latency_B": (parseargs.latency_B if parseargs.latency_B else parseargs.latency),
        "rate": parseargs.rate,
        "rate_A": (parseargs.rate_A if parseargs.rate_A else parseargs.rate),
        "rate_B": (parseargs.rate_B if parseargs.rate_B else parseargs.rate),
        "jitter": parseargs.jitter,
        "jitter_A": (parseargs.jitter_A if parseargs.jitter_A else parseargs.jitter),
        "jitter_B": (parseargs.jitter_B if parseargs.jitter_B else parseargs.jitter),
        "jitter_freq": parseargs.jitter,
        "jitter_freq_A": (parseargs.jitter_freq_A if parseargs.jitter_freq_A else parseargs.jitter_freq),
        "jitter_freq_B": (parseargs.jitter_freq_B if parseargs.jitter_freq_B else parseargs.jitter_freq),
        "drop": parseargs.drop,
        "drop_A": (parseargs.drop_A if parseargs.drop_A else parseargs.drop),
        "drop_B": (parseargs.drop_B if parseargs.drop_B else parseargs.drop),
    }

    main(args)
