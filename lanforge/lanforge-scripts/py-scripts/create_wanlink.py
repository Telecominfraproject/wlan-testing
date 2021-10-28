#!/usr/bin/python3
"""

 Create and modify WAN Links Using LANforge JSON AP : http://www.candelatech.com/cookbook.php?vol=cli&book=JSON:+Managing+WANlinks+using+JSON+and+Python
 Written by Candela Technologies Inc.
 Updated by: Erin Grimes

"""
import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)




from time import sleep
import urllib
import pprint

sys.path.append("../py-json")
from LANforge import LFRequest
from LANforge import LFUtils
from LANforge.lfcli_base import LFCliBase

j_printer = pprint.PrettyPrinter(indent=2)
# todo: this needs to change
resource_id = 1


def main():
    parser = LFCliBase.create_basic_argparse()
    args = parser.parse_args()
    base_url = 'http://%s:%s' % (args.mgr, args.mgr_port)
    print(base_url)
    json_post = ""
    json_response = ""
    num_wanlinks = -1

    # force a refresh on the ports and wanlinks
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/nc_show_ports", debug_=True)
    lf_r.addPostData({
        "shelf": 1,
        "resource": 1,
        "port": "all",
    })
    json_response = lf_r.jsonPost(debug=True)

    lf_r = LFRequest.LFRequest(base_url+"/cli-json/nc_show_endpoints", debug_=True)
    lf_r.addPostData({
        "endpoint": "all"
    })
    json_response = lf_r.jsonPost(debug=True)

    sleep(1)

    # see if there are old wanlinks to remove
    lf_r = LFRequest.LFRequest(base_url+"/wl_ep/list", debug_=True)
    json_reponse = lf_r.get_as_json()

    endpA = args['name']+"-A"
    endpB = args['name']+"-B"

    # count the number of wanlink endpoints
    if "endpoint" in json_response:
        endpoint_map = LFUtils.list_to_alias_map(json_list=json_reponse, from_element="endpoint")
        if endpA in endpoint_map:
            num_wanlinks += 1
        if endpB in endpoint_map:
            num_wanlinks += 1

    # remove old wanlinks
    if (num_wanlinks > 0):
        print("Removing old wanlinks...")
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_cx", debug_=True)
        lf_r.addPostData({
         'test_mgr': 'all',
         'cx_name': args['name']
        })
        lf_r.jsonPost()

        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_endp", debug_=True)
        lf_r.addPostData({
           'endp_name': endpA
        })
        lf_r.jsonPost()

        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_endp", debug_=True)
        lf_r.addPostData({
           'endp_name': endpB
        })
        lf_r.jsonPost()
        sleep(1)

    # check to see if we have ports
    lf_r = LFRequest.LFRequest(base_url+"/ports/1/1/list", debug_=True)
    port_response = lf_r.getAsJson()

    if "interfaces" not in port_response:
        print("No interfaces in port_response!")
        pprint.pprint(port_response)
        exit(1)

    if "interfaces" in port_response:
        port_map = LFUtils.list_to_alias_map(json_list=port_response, from_element="interfaces")
        ports_created = 0
        if args["port_A"] not in port_map:
            lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_rdd", debug_=True)
            lf_r.addPostData({
                "shelf": 1,
                "resource": 1,
                "port": args["port_A"],
                "peer_ifname": args["port_A"]+"b",
            })
            json_reponse = lf_r.jsonPost(debug=True)
            if not json_response:
                print("could not create port "+args["port_A"])
                exit(1)
            sleep(0.1)
            ports_created += 1
        if args["port_B"] not in port_map:
            lf_r.addPostData({
                "shelf": 1,
                "resource": 1,
                "port": args["port_B"],
                "peer_ifname": args["port_B"]+"b",
            })
            json_reponse = lf_r.jsonPost(debug=True)
            if not json_response:
                print("could not create port " + args["port_B"])
                exit(1)
            ports_created += 1
            sleep(0.1)
        if ports_created > 0:
            LFUtils.wait_until_ports_appear(base_url=base_url,
                                            port_list=(args["port_A"], args["port_B"]),
                                            debug=True)
            print("Created {} ports".format(ports_created))

    # create wanlink endpoint A
    print("Adding WL Endpoints...", end='')
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_wl_endp", debug_=True)
    lf_r.addPostData({
        'alias': endpA,
        'shelf': 1,
        'resource': '1',
        'port': args['port_A'],
        'latency': args['latency_A'],
        'max_rate': args['rate_A'],
    })
    json_response = lf_r.jsonPost(debug=True)
    if not json_response:
        print("Unable to create "+endpA)
    else:
        print("A, ", end='')
    # create wanlink endpoint B
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_wl_endp", debug_=True)
    lf_r.addPostData({
        'alias': endpB,
        'shelf': 1,
        'resource': '1',
        'port': args['port_B'],
        'latency': args['latency_B'],
        'max_rate': args['rate_B'],
    })
    json_response = lf_r.jsonPost()
    if not json_response:
        print("Unable to create "+endpB)
    else:
        print("B")
    sleep(1)

    # create cx
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_cx", debug_=True)
    lf_r.addPostData({
       'alias': args['name'],
       'test_mgr': 'default_tm',
       'tx_endp': endpA,
       'rx_endp': endpB
    })
    lf_r.jsonPost(debug=True)
    sleep(0.5)

    # modify wanlink endpoint A
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_wanlink_info", debug_=True)
    lf_r.addPostData({
        'name': endpA,
        'max_jitter': args['jitter_A'],
        'jitter_freq': args['jitter_freq_A'],
        'drop_freq': args['drop_A']
    })
    lf_r.jsonPost(debug=True)

    # modify wanlink endpoint B
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_wanlink_info", debug_=True)
    lf_r.addPostData({
        'name': endpB,
        'max_jitter': args['jitter_B'],
        'jitter_freq': args['jitter_freq_B'],
        'drop_freq': args['drop_B']
    })
    lf_r.jsonPost()

    # start wanlink once we see it
    seen = 0
    print("Looking for {} and {}: ".format(endpA, endpB), end='')
    while (seen < 2):
        sleep(1)
        lf_r = LFRequest.LFRequest(base_url+"/wl_ep/list?fields=name,eid")
        try:
            json_response = lf_r.getAsJson()
            if json_response is None:
                print(".", end="")
                continue
            LFUtils.debug_printer.pprint(json_response)
            if "endpoint" not in json_response:
                print("-", end="")
                continue

            endpoint_map = LFUtils.list_to_alias_map(json_list=json_response["endpoint"],
                                                     from_element="endpoint")
            if endpA in endpoint_map:
                seen += 1
                print("+", end="")
            if endpB in endpoint_map:
                seen += 1
                print("+", end="")

        except urllib.error.HTTPError as error:
            print("Error code {}".format(error.code))
            continue
    print("")
    print("Starting wanlink:")
    # print("the latency is {laten}".format(laten=latency))
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_cx_state")
    lf_r.addPostData({
       'test_mgr': 'all',
       'cx_name': args['name'],
       'cx_state': 'RUNNING'
    })
    lf_r.jsonPost()

    running = 0
    while (running < 1):
        sleep(1)
        lf_r = LFRequest.LFRequest(base_url+"/wl/"+args['name']+"?fields=name,state,_links")
        try:
            json_response = lf_r.getAsJson()
            if (json_response is None):
                continue
            for key, value in json_response.items():
                if (isinstance(value, dict)):
                    if ("_links" in value):
                        if (value["name"] == args['name']):
                            if (value["state"].startswith("Run")):
                                LFUtils.debug_printer.pprint(json_response)
                                running = 1

        except urllib.error.HTTPError as error:
            print("Error code {}".format(error.code))
            continue

    print("Wanlink is running")

    # stop wanlink
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_cx_state")
    lf_r.addPostData({
       'test_mgr': 'all',
       'cx_name': args['name'],
       'cx_state': 'STOPPED'
    })
    lf_r.jsonPost()
    running = 1
    while (running > 0):
        sleep(1)
        lf_r = LFRequest.LFRequest(base_url+"/wl/"+args['name']+"?fields=name,eid,state,_links")
        LFUtils.debug_printer.pprint(json_response)
        try:
            json_response = lf_r.getAsJson()
            if (json_response is None):
                continue
            for key, value in json_response.items():
                if (isinstance(value, dict)):
                    if ("_links" in value):
                        if (value["name"] == args['name']):
                            if (value["state"].startswith("Stop")):
                                LFUtils.debug_printer.pprint(json_response)
                                running = 0

        except urllib.error.HTTPError as error:
            print("Error code {}".format(error.code))
            continue

    print("Wanlink is stopped.")

    # print("Wanlink info:")
    # lf_r = LFRequest.LFRequest(base_url+"/wl/wl_eg1")
    # json_response = lf_r.getAsJson()
    # LFUtils.debug_printer.pprint(json_response)

    # lf_r = LFRequest.LFRequest(base_url+"/wl_ep/wl_eg1-A")
    # json_response = lf_r.getAsJson()
    # LFUtils.debug_printer.pprint(json_response)

    # lf_r = LFRequest.LFRequest(base_url+"/wl_ep/wl_eg1-B")
    # json_response = lf_r.getAsJson()
    # LFUtils.debug_printer.pprint(json_response)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':
    main()
