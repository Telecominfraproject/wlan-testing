#!/usr/bin/env python3
'''
NAME: lf_radio_info.py

PURPOSE:

 This script will gather all wiphy radio information, and then parse and
  return specific wiphy radio data that is requested per script function.

EXAMPLE:

 This will run through the module test:
 ./lf_radio_info.py --mgr 192.168.30.22

'''

import argparse
import sys
import os
import logging
import importlib
import json
import requests
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
removeCX = LFUtils.removeCX
removeEndps = LFUtils.removeEndps
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_report = importlib.import_module("py-scripts.lf_report")
lf_graph = importlib.import_module("py-scripts.lf_graph")
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

OPEN = "open"
WEP = "wep"
WPA = "wpa"
WPA2 = "wpa2"
WPA3 = "wpa3"
MODE_AUTO = 0


class radio_information(Realm):
    def __init__(self, host,
                 _resource="1",
                 debug_=False, _exit_on_fail=False):
        super().__init__(host, debug_=debug_, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.resource = _resource
        self.lf_mgr_ip = host
        self.lf_mgr_port = "8080"
        self.lf_mgr_user = "lanforge"
        self.lf_mgr_pass = "lanforge"
        self.lf_radio_df = ""
        self.debug = debug_

    # returns all wihpy radio data as a pandas.df:
    def get_lanforge_radio_information(self):
        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/radiostatus/all | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{port}/radiostatus/all'.format(lfmgr=self.lf_mgr_ip, port=self.lf_mgr_port)
        request = requests.get(request_command, auth=(self.lf_mgr_user, self.lf_mgr_pass))

        logger.info("radio request command: {request_command}".format(request_command=request_command))
        logger.info("radio request status_code {status}".format(status=request.status_code))
        lanforge_radio_json = request.json()

        lanforge_radio_formatted_str = json.dumps(lanforge_radio_json, indent=2)
        logger.info("lanforge_radio_json: {lanforge_radio_json}".format(lanforge_radio_json=lanforge_radio_formatted_str))
        # note put into the meta data
        # self.radio_dataframe
        self.lf_radio_df = pd.DataFrame(
            columns=[
                'Radio',
                'WIFI-Radio Driver',
                'Radio Capabilities',
                'Firmware Version',
                'max_sta',
                'max_vap',
                'max_vifs'])
        for key in lanforge_radio_json:
            if 'wiphy' in key:
                driver = lanforge_radio_json[key]['driver'].split(
                    'Driver:', maxsplit=1)[-1].split(maxsplit=1)[0]
                try:
                    firmware_version = lanforge_radio_json[key]['firmware version']
                except BaseException:
                    logger.info("5.4.5 radio fw version not in /radiostatus/all ")
                    firmware_version = "5.4.5 N/A"
                self.lf_radio_df = self.lf_radio_df.append(
                    {'Radio': lanforge_radio_json[key]['entity id'],
                     'WIFI-Radio Driver': driver,
                     'Radio Capabilities': lanforge_radio_json[key]['capabilities'],
                     'Firmware Version': firmware_version,
                     'max_sta': lanforge_radio_json[key]['max_sta'],
                     'max_vap': lanforge_radio_json[key]['max_vap'],
                     'max_vifs': lanforge_radio_json[key]['max_vifs']}, ignore_index=True)

        return self.lf_radio_df

    # returns all radios and maximum stations:
    def get_max_stations_all(self):
        max_station = self.lf_radio_df.get(["Radio", "max_sta"])
        # logger.info(max_station)

        return max_station

    # returns specific radio maximum stations:
    def get_radio_max_station(self, wiphy_radio):
        max_station = self.lf_radio_df.get(["Radio", "max_sta"])
        # logger.info(max_station)

        for row in max_station.index:
            if max_station.loc[row, "Radio"] == wiphy_radio:
                    max_sta = max_station.loc[row, "max_sta"]
                    # logger.info(max_sta)

        return max_sta

    # returns specific radio maximum virtual access points:
    def get_max_vap(self, wiphy_radio):
        max_vaps = self.lf_radio_df.get(["Radio", "max_vap"])
        # logger.info(max_vaps)

        for row in max_vaps.index:
            if max_vaps.loc[row, "Radio"] == wiphy_radio:
                    wiphy_max_vaps = max_vaps.loc[row, "max_vap"]
                    # logger.info(wiphy_max_vaps)

        return wiphy_max_vaps

    # returns specific radio maximum supported virtual clients:
    def get_max_vifs(self, wiphy_radio):
        max_vif = self.lf_radio_df.get(["Radio", "max_vifs"])
        # logger.info(max_vif)

        for row in max_vif.index:
            if max_vif.loc[row, "Radio"] == wiphy_radio:
                wiphy_max_vif = max_vif.loc[row, "max_vifs"]
                # logger.info(wiphy_max_vif)
                if int(wiphy_max_vif) > 200:
                    wiphy_max_vif = "200"

        return wiphy_max_vif

    # returns specific radio driver information:
    def get_radio_driver(self, wiphy_radio):
        radio_driver = self.lf_radio_df.get(["Radio", "WIFI-Radio Driver"])
        # logger.info(radio_driver)

        for row in radio_driver.index:
            if radio_driver.loc[row, "Radio"] == wiphy_radio:
                wiphy_driver = radio_driver.loc[row, "WIFI-Radio Driver"]
                # logger.info(wiphy_driver)

        return wiphy_driver

    # returns specific radio 802.11 wifi capabilities:
    def get_radio_capabilities(self, wiphy_radio):
        radio_caps = self.lf_radio_df.get(["Radio", "Radio Capabilities"])
        # logger.info(radio_caps)

        for row in radio_caps.index:
            if radio_caps.loc[row, "Radio"] == wiphy_radio:
                    wiphy_capability = radio_caps.loc[row, "Radio Capabilities"]
                    # logger.info(wiphy_capability)

        return wiphy_capability

    # returns radios installed on system:
    def get_radios(self):
        radios = self.lf_radio_df.get(["Radio"])
        # logger.info(radios)

        radio_list = []
        for row in radios.index:
            radio_list.append(radios.loc[row, "Radio"])
            # logger.info(radio_list)
        
        return radio_list

    # returns radio types installed on system:
    def get_radio_type(self, wiphy_radio):
        radio_types = self.lf_radio_df.get(["Radio", "WIFI-Radio Driver"])
        # logger.info(radio_types)

        for row in radio_types.index:
            if radio_types.loc[row, "Radio"] == wiphy_radio:
                    type_radio = radio_types.loc[row, "WIFI-Radio Driver"]
                    # logger.info(type_radio)

        return type_radio

# ~class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def main():
    parser = argparse.ArgumentParser(
        prog="lf_radio_info.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
---------------------------
LANforge Unit Test:  Retreive Wiphy Radio Information - lf_radio_info.py
---------------------------
Summary:
This script will gather all wiphy radio information to be used by other test scripts.
---------------------------
CLI Example:

./lf_radio_info.py --mgr 192.168.30.12

---------------------------
""")
    parser.add_argument("-m", "--mgr", type=str, help="address of the LANforge GUI machine (localhost is default)",
                        default='localhost')
    parser.add_argument("--debug", help="enable debugging", action="store_true")
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default="1")
    # logging configuration:
    parser.add_argument("--lf_logger_config_json",
                        help="--lf_logger_config_json <json file> , json configuration of logger")
    parser.add_argument('--log_level', default=None,
                        help='Set logging level: debug | info | warning | error | critical')

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if args.log_level:
        logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    if args.debug:
        logger_config.set_level("debug")

    wiphy_radio_info = radio_information(args.mgr,
                          _resource=args.resource,
                          debug_=args.debug,
                          _exit_on_fail=True)
    #lf_radio_info.RadioInfo

    # basic unit module test:

    radio = "1.1.wiphy7"

    # get all system radio information:
    all_radio_info = wiphy_radio_info.get_lanforge_radio_information()
    logger.info(all_radio_info)

    # get max stations per each install wiphy radio:
    all_max_sta = wiphy_radio_info.get_max_stations_all()
    print()
    logger.info(all_max_sta)

    # get max stations for specified wiphy radio:
    radio_max_sta = wiphy_radio_info.get_radio_max_station(radio)
    logger.info(radio_max_sta)

    # get max vap that can be created per spicified wiphy radio:
    max_vap = wiphy_radio_info.get_max_vap(radio)
    logger.info(max_vap)

    # get max vif that can be created per specified wiphy radio:
    max_vifs = wiphy_radio_info.get_max_vifs(radio)
    logger.info(max_vifs)

    # get radio driver for specified wiphy radio:
    radio_driver = wiphy_radio_info.get_radio_driver(radio)
    logger.info(radio_driver)

    # get 802.11 capabilities for specified radio:
    radio_capabilities = wiphy_radio_info.get_radio_capabilities(radio)
    logger.info(radio_capabilities)

    # get wiphy radio list:
    system_radios = wiphy_radio_info.get_radios()
    logger.info(system_radios)

    # get radio type:
    system_radios_type = wiphy_radio_info.get_radio_type(radio)
    logger.info(system_radios_type)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    main()
