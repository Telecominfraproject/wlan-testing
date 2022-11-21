#!/usr/bin/env python3
'''
NAME: lf_create_db.py

PURPOSE:
    This script will create the BLANK & FACTORY_DFLT database's on a newly built LANforge system.
     The script will preform the following tasks:
     - set existing ports up, down, and then up again.
     - enable and disable dhcp on existing ethernet ports.
     - create BLANK db and arrange port coordinates.
     - create FACTORY_DFLT db and arrange port coordinates.


EXAMPLE ct521a:
    ./lf_create_db.py --mgr <localhost> --db_name defaults

COPYRIGHT:
    Copyright 2022 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
'''

import sys
import os
import importlib
import argparse
import time
import logging
import json
import requests
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
set_port = importlib.import_module("py-json.LANforge.set_port")
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")

logger = logging.getLogger(__name__)

class create_database(Realm):
    def __init__(self,
                 mgr='localhost',
                 mgr_port=8080,
                 resource=1,
                 load_db=None,
                 db_name=None,
                 timeout=120,
                 debug=False):
        super().__init__(lfclient_host=mgr,
                         lfclient_port=mgr_port,
                         debug_=debug)
        self.mgr = mgr
        self.mgr_port = mgr_port
        self.resource = resource
        self.load_db = load_db
        self.db_name = db_name
        self.timeout = timeout
        self.lf_mgr_user = "lanforge"
        self.lf_mgr_pass = "lanforge"
        self.lf_ports_df = ""
        self.debug = debug

    
    # returns all port data as a pandas.df:
    def get_ports_data(self):
        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/ports/ | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{port}/ports/'.format(lfmgr=self.mgr, port=self.mgr_port)
        request = requests.get(request_command, auth=(self.lf_mgr_user, self.lf_mgr_pass))

        logger.info("port request command: {request_command}".format(request_command=request_command))
        logger.info("port request status_code {status}".format(status=request.status_code))
        lanforge_ports_json = request.json()

        lanforge_ports_formatted_str = json.dumps(lanforge_ports_json, indent=2)
        logger.info("lanforge_radio_json: {lanforge_radio_json}".format(lanforge_radio_json=lanforge_ports_formatted_str))
        
        self.lf_ports_df = pd.DataFrame(
            columns=[
                'EID',
                '_links',
                'Alias',
                'Down',
                'Phantom',
                'Port'])
        for key in lanforge_ports_json:
            if 'interfaces' in key:
                for entity_id in lanforge_ports_json['interfaces']:
                    
                    # get initial key name which is the eid:
                    port_name = list(entity_id.keys())[0]
                    
                    # create pandas df from localhost:8080/ports/
                    self.lf_ports_df = self.lf_ports_df.append(
                        {'EID': port_name,
                         '_links': entity_id[port_name].get('_links'),
                         'Alias': entity_id[port_name].get('alias'),
                         'Down': entity_id[port_name].get('down'),
                         'Phantom': entity_id[port_name].get('phantom'),
                         'Port': entity_id[port_name].get('port')}, ignore_index=True)

        return self.lf_ports_df

    def pre_config_ports(self):
        # initial port config steps:
        # if wlans are down, bring them up and down. if they're already up just set them down (this sets a database flag)
        # while eth1 and eth2 are unplugged.. modify eth1 and eth2 and set dhcp ipv4
        # modify eth1 and eth2 and uncheck dhcp ipv4 (this sets more database flags)
        # modify eth1 and eth2 to verify dhcp ipv4 unchecked
        
        port_status = self.lf_ports_df.get(["EID", "Down"])

        for row in port_status.index:
            if not "eth0" in port_status.loc[row, "EID"]:
                # enable dhcp and then disable dhcp for eth ports > eth0
                if self.resource + ".eth" in port_status.loc[row, "EID"]:
                    eth_eid = port_status.loc[row, "EID"]
                    logger.info(eth_eid)
                    eid = LFUtils.name_to_eid(eth_eid)
                    # set_port enable dhcp:
                    set_dhcp_up = {
                        "shelf": 1,
                        "resource": eid[1],
                        "port": eid[2],
                        "current_flags": 2147483648,  # use_dhcp = 0x800000000
                        "interest": 16386,  # use_current_flags + dhcp = 0x4002
                        "report_timer": 1500
                    }
                    set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port")
                    set_port_r.addPostData(set_dhcp_up)
                    set_port_r.jsonPost()
                    
                    # TODO: check/verify that DHCP is enabled on the eth port prior to continuing - error msg if dhcp is not set

                    # set_port disable dhcp:
                    set_dhcp_down = {
                        "shelf": 1,
                        "resource": eid[1],
                        "port": eid[2],
                        "current_flags": 0,  # set dhcp bit to 0 
                        "interest": 16386,  # use_current_flags + dhcp = 0x4002
                        "report_timer": 1500
                    }
                    set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port")
                    set_port_r.addPostData(set_dhcp_down)
                    set_port_r.jsonPost()


                if self.resource + "wlan" in port_status.loc[row, "EID"]:
                    wlan_eid = port_status.loc[row, "EID"]
                    wlan_list = [wlan_eid]
                    eid = LFUtils.name_to_eid(wlan_eid)
                    # if wlan ports are down, set them admin up and then back to admin down:
                    if port_status.loc[row, "Down"] == True:
                        # set wlan port admin up:
                        up_request = LFUtils.port_up_request(resource_id=eid[1], port_name=eid[2])
                        self.json_post("cli-json/set_port", up_request)
                        
                        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=wlan_list,
                                              debug_=self.debug)
                        
                        # TODO: check/verify that wlans are now set to admin up prior to continuing
                        # get updated port data from http://localhost:8080/ports/:
                        # self.lf_ports_df = self.get_ports_data()
                        # logger.info(self.lf_ports_df)
                        # wlan_status = self.lf_ports_df.get(["EID", "Down"])                       


                        # set wlan port admin down:
                        down_request = LFUtils.port_down_request(resource_id=eid[1], port_name=eid[2])
                        self.json_post("cli-json/set_port", down_request)

                        LFUtils.wait_until_ports_admin_down(base_url=self.lfclient_url, port_list=wlan_list,
                                              debug_=self.debug)
                    
                    # if wlan port is already admin up, then set the port to admin down:
                    elif port_status.loc[row, "Down"] == False:
                        # set wlan port admin down:
                        down_request = LFUtils.port_down_request(resource_id=eid[1], port_name=eid[2])
                        self.json_post("cli-json/set_port", down_request)

                        LFUtils.wait_until_ports_admin_down(base_url=self.lfclient_url, port_list=wlan_list,
                                              debug_=self.debug)

        
        if self.db_name == "defaults":
            logger.info("creating FACTORY_DFLT and BLANK Netsmith Databases...")

    def config_netsmith(self):
        # Netsmith FACTORY_DFLT config steps:
        # open netsmith, drag all ports to the top and right of legend (so legend isn't covering them)
        # enable IPv4 checkbox
        # click apply in netsmith
        # save database as FACTORY_DFLT
        #
        # Netsmith BLANK config steps:
        # delete wlan ports
        # open netsmith and delete wlan ports
        # apply in netsmith
        # save database as BLANK

        if self.db_name == "defaults":
            logger.info("creating FACTORY_DFLT and BLANK Netsmith Databases...")
    
# ~class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def main():
    parser = argparse.ArgumentParser(
        prog='lf_create_db.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
---------------------------
LANforge Unit Test:  Create Netsmith Database's - lf_create_db.py
---------------------------
Summary:
This script will create the FACTORY_DFLT and BLANK Netsmith database's.
---------------------------
CLI Example:

Create default database BLANK and FACTORY_DFLT
./lf_create_db.py --mgr localhost --db_name defaults

---------------------------
''')
    parser.add_argument("-m", "--mgr", type=str, help="address of the LANforge GUI machine (localhost is default)",
                        default='localhost')
    parser.add_argument('--load', help='name of database to load', default=None)
    parser.add_argument('--db_name', help='name of database to create.', default=None)
    parser.add_argument("--debug", help="enable debugging", action="store_true")
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default="1")

    # logging configuration:
    parser.add_argument("--lf_logger_config_json",
                        help="--lf_logger_config_json <json file> , json configuration of logger")
    parser.add_argument('--log_level',
                        default=None,
                        help='Set logging level: debug | info | warning | error | critical')

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if (args.log_level):
        logger_config.set_level(level=args.log_level)

    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    if args.debug:
        logger_config.set_level("debug")

    create_db = create_database(mgr=args.mgr,
                                mgr_port=8080,
                                resource=args.resource,
                                load_db=args.load,
                                db_name=args.db_name,
                                debug=args.debug)

    # get all system port information as pandas df:
    all_ports_df = create_db.get_ports_data()
    logger.info(all_ports_df)

    # apply initial port configuration steps for default DB's:
    create_db.pre_config_ports()

    # configure Netsmith for FACTORY_DFLT & BLANK DB's:
    create_db.config_netsmith()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    main()