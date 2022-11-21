#!/usr/bin/env python3
'''
NAME: lf_json_api.py

PURPOSE:

 This script will is an example of using LANforge JSON API to use GET Requests to LANforge.

ADDITION INFORMATION:

https://www.w3schools.com/python/module_requests.asp

https://www.w3schools.com/PYTHON/ref_requests_post.asp


EXAMPLE:

    ./lf_json_api.py --lf_mgr 192.168.100.116 --lf_port 8080 --log_level debug --port wlan3 --lf_user lanforge --lf_passwd lanforge
        --port 1.1.vap0000 --get_request 'stations,04:f0:21:c5:33:97 stations,d8:f8:83:36:6c:44'

    ./lf_json_api.py --lf_mgr 192.168.100.116 --lf_port 8080 --log_level debug --port wlan3 --lf_user lanforge --lf_passwd lanforge
        --port 1.1.vap0000 --get_request 'wifi-stats'


NOTE:
    LANforge GUI , click on info -> API Help  look under GET Requests  use similiar format to what is being done below.
'''

import argparse
import sys
import os
import logging
import importlib
import pandas
import requests
from pandas import json_normalize
import json
import traceback
import csv
import time


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
# used for conversion from eid to shelf, resource , port
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class lf_json_api():
    def __init__(self,
                 lf_mgr='localhost',
                 lf_port=8080,
                 lf_user='lanforge',
                 lf_passwd='lanforge',
                 port=None,
                 csv_mode='write'):

        self.lf_mgr = lf_mgr
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_passwd = lf_passwd
        # this port is the Port like 1.1.sta000 , or 1.2.wiphy2
        self.port = port
        self.shelf = ''
        self.resource = ''
        self.port_name = ''
        # TODO support qvlan
        self.qval = ''
        self.request = ''
        # since the port may change we will initially us update_port_info to set initial values
        self.update_port_info()
        self.extra = '' # to be used for clearing ports

    def update_csv_mode(self):
        if self.csv_mode == 'append':
            self.csv_mode = 'a'
            self.csv_header = False
        else:
            self.csv_mode = 'w'
            self.csv_header = True


    def update_port_info(self):
        # TODO add support for non-port
        # TODO add support for qvan or attenuator
        # rv short for return value
        if not self.port:
            return

        #logger.error("update-port-info, port: %s  non-port: %s"%(self.port, self.non_port));
        self.shelf, self.resource, self.port_name, *nil = LFUtils.name_to_eid(self.port)
        logger.debug("shelf : {shelf} , resource : {resource}, port_name : {port_name}".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name))
        # the request can change

    def reformat_json(self, json_data ):
        lines = []
        key = list(dict(json_data).keys())[-1]

        if not json_data[key] is list:
            return pandas.json_normalize(json_data[key])
        else:
            lines = []
            for i in json_data[key]:
                inner_data = i[list(i.keys())[0]]  # getting the data under each device/port/object name in list
                lines.append(pandas.json_normalize(inner_data))
            return pandas.concat(lines, ignore_index=True)



    def get_request_port_information(self, port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # station command
        # curl -H 'Accept: application/json' 'http://localhost:8080/port/1/1/wlan3' | json_pp
        # a radio command
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/port/1/1/wlan3 | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{lfport}/port/1/{resource}/{port_name}'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, resource=self.resource, port_name=self.port_name)
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))
        logger.info(
            "port request command: {request_command}".format(
                request_command=request_command))
        logger.info(
            "port request status_code {status}".format(
                status=request.status_code))
        lanforge_json = request.json()
        logger.debug("port request.json: {json}".format(json=lanforge_json))
        lanforge_text = request.text
        logger.debug("port request.text: {text}".format(text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.debug("port request lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))
        
        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name
        ))

        csv_file_port = "{shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request)
        try:
            # TODO re-evalute this if port
            if self.request == "port":
                key = "interface"
            else:
                key = "{shelf}.{resource}.{port_name}".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name)
            df = json_normalize(lanforge_json[key])
            # TODO defaulting to the normal behavior
            df.to_csv(csv_file_port.format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request), 
                    mode = self.csv_mode, header = self.csv_header, index=False)
        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.info("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        logger.info("csv output:   {shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request))


        return lanforge_json, csv_file_port, lanforge_text, lanforge_json_formatted

    def get_request_wifi_stats_information(self,port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # station command
        # curl -H 'Accept: application/json' 'http://localhost:8080/wifi-stats/1/1/wlan4' | json_pp
        # a radio command
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/wifi-stats/1/1/wlan4 | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{lfport}/wifi-stats/1/{resource}/{port_name}'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, resource=self.resource, port_name=self.port_name)
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))

        logger.info(
            "wifi-stats request command: {request_command}".format(
                request_command=request_command))
        logger.info(
            "wifi-stats request status_code {status}".format(
                status=request.status_code))

        lanforge_json = request.json()
        logger.debug("wifi-stats request.json: {json}".format(json=lanforge_json))
        lanforge_text = request.text
        logger.debug("wifi-stats request.text: {text}".format(text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.info("wifi-stats lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))

        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name
        ))

        try:
            key = "{shelf}.{resource}.{port_name}".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name)
            df = json_normalize(lanforge_json[key])
            csv_file_wifi_stats = "{shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request)
            df.to_csv(csv_file_wifi_stats, mode = self.csv_mode, header = self.csv_header, index=False)
        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        # TODO just return lanforge_json and lanforge_txt, lanfore_json_formated to is may be the same for all commands
        return lanforge_json, csv_file_wifi_stats, lanforge_text, lanforge_json_formatted

    # give information on a single station if the mac is entered.
    def get_request_single_station_information(self,port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        #
        # curl -H 'Accept: application/json' http://localhost:8080/{request}/{shelf}/{resourse}/{port_name} | json_pp
        # request  command,  to see commands <lanforge ip>:8080
        # curl --user "lanforge:lanforge" -H 'Accept: application/json' http://192.168.100.116:8080/{request}/1/1/wlan4 | json_pp
        # where --user "USERNAME:PASSWORD"
        # request_command = 'http://{lfmgr}:{lfport}/{request}/1/{resource}/{port_name}/{mac}'.format(
        request_command = 'http://{lfmgr}:{lfport}/{request}/{mac}'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, request=self.request, mac=self.mac)
        #    lfmgr=self.lf_mgr, lfport=self.lf_port,request=self.request, resource=self.resource, port_name=self.port_name, mac=self.mac)
        logger.debug("request_command: {request_command}".format(request_command=request_command))
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))

        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name}/{mac} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name, mac=self.mac
        ))

        logger.info(
            "{request} request command: {request_command}".format(request=self.request,
                                                                  request_command=request_command))
        logger.info(
            "{request} request status_code {status}".format(request=self.request,
                                                            status=request.status_code))

        lanforge_json = request.json()
        logger.debug("{request} request.json: {json}".format(request=self.request, json=lanforge_json))
        lanforge_text = request.text
        logger.debug("{request} request.text: {text}".format(request=self.request, text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.info("lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))

        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name}/{mac} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name, mac=self.mac
        ))

        # TODO just return lanforge_json and lanforge_txt, lanfore_json_formated to is may be the same for all commands
        # TODO check for "status": "NOT_FOUND"
        try:
            key = "station"
            df = json_normalize(lanforge_json[key])
            df.to_csv("{shelf}.{resource}.{port_name}.{mac}_{request}.csv".
                format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request, mac=self.mac), 
                    mode = self.csv_mode, header = self.csv_header, index=False)
        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        logger.info("csv output:   {shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request))

        return lanforge_json, lanforge_text, lanforge_json_formatted


    def get_request_stations_information(self):

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        #
        # curl -H 'Accept: application/json' http://localhost:8080/stations/all | json_pp
        # request  command,  to see commands <lanforge ip>:8080
        # curl --user "lanforge:lanforge" -H 'Accept: application/json' http://192.168.100.116:8080/stations/all | json_pp
        # where --user "USERNAME:PASSWORD"
        logger.info("get_request_stations_information")
        request_command = 'http://{lfmgr}:{lfport}/{request}/all'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, request=self.request)
        #    lfmgr=self.lf_mgr, lfport=self.lf_port,request=self.request, resource=self.resource, port_name=self.port_name, mac=self.mac)
        logger.debug("request_command: {request_command}".format(request_command=request_command))
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))

        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/all | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request ))

        logger.info(
            "{request} request command: {request_command}".format(request=self.request,
                                                                  request_command=request_command))
        logger.info("{request} request status_code {status}".format(request=self.request, status=request.status_code))

        lanforge_json = request.json()
        logger.debug("{request} request.json: {json}".format(request=self.request, json=lanforge_json))
        lanforge_text = request.text
        logger.debug("{request} request.text: {text}".format(request=self.request, text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.info("lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))

        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/all | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request ))

        # TODO just return lanforge_json and lanforge_txt, lanfore_json_formated to is may be the same for all commands
        # TODO check for "status": "NOT_FOUND"

        try:
            key = "stations"
            lines = []
            for i in lanforge_json[key]:
                inner_data = i[list(i.keys())[0]]  # getting the data under each device/port/object name in list
                lines.append(pandas.json_normalize(inner_data))
            df3 = pandas.concat(lines, ignore_index=True)
            df3.to_csv("{request}.csv".format(request=self.request), index=False)


        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        logger.info("csv output: {request}.csv".format(request=self.request))

        return lanforge_json, lanforge_text, lanforge_json_formatted

    def get_request_adb_information(self,port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        #
        # curl -H 'Accept: application/json' http://localhost:8080/adb/1/1/0123456789ABCDEF | json_pp
        # request  command,  to see commands <lanforge ip>:8080
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/{request}/1/1/wlan4 | json_pp
        # where --user "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{lfport}/adb/1/{resource}/{port_name}'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, request=self.request, resource=self.resource, port_name=self.port_name)
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))
        logger.info(
            "{request} request command: {request_command}".format(request=self.request,
                                                                  request_command=request_command))
        logger.info(
            "{request} request status_code {status}".format(request=self.request,
                                                            status=request.status_code))
        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name
        ))
        lanforge_json = request.json()
        logger.debug("{request} request.json: {json}".format(request=self.request, json=lanforge_json))
        lanforge_text = request.text
        logger.debug("{request} request.text: {text}".format(request=self.request, text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.debug("lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))

        try:
            df = self.reformat_json(lanforge_json)
            df.to_csv("{shelf}.{resource}.{port_name}_{request}.csv".
                format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request), 
                    mode = self.csv_mode, header = self.csv_header, index=False)
        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        logger.info("csv output:   {shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request))

        return lanforge_json, lanforge_text, lanforge_json_formatted

    # TODO this is a generic one.

    def get_request_information(self, port=None
    ):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        #
        # curl -H 'Accept: application/json' http://localhost:8080/{request}/{shelf}/{resourse}/{port_name} | json_pp
        # request  command,  to see commands <lanforge ip>:8080
        # curl --user "lanforge:lanforge" -H 'Accept: application/json' http://192.168.100.116:8080/{request}/1/1/wlan4 | json_pp
        # where --user "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{lfport}/{request}/1/{resource}/{port_name}'.format(
            lfmgr=self.lf_mgr, lfport=self.lf_port, request=self.request, resource=self.resource, port_name=self.port_name)
        request = requests.get(
            request_command, auth=(
                self.lf_user, self.lf_passwd))
        logger.info(
            "{request} request command: {request_command}".format(request=self.request,
                                                                  request_command=request_command))
        logger.info(
            "{request} request status_code {status}".format(request=self.request,
                                                            status=request.status_code))
        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name} | json_pp  ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name
        ))
        lanforge_json = request.json()
        logger.debug("{request} request.json: {json}".format(request=self.request, json=lanforge_json))
        lanforge_text = request.text
        logger.debug("{request} request.text: {text}".format(request=self.request, text=lanforge_text))
        lanforge_json_formatted = json.dumps(lanforge_json, indent=4)
        logger.debug("lanforge_json_formatted: {json}".format(json=lanforge_json_formatted))
        # TODO just return lanforge_json and lanforge_txt, lanfore_json_formated to is may be the same for all commands
        # TODO check for "status": "NOT_FOUND"

        try:
            if self.request == "port":
                key = "interface"
            else:
                key = "{shelf}.{resource}.{port_name}".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name)
            df = json_normalize(lanforge_json[key])
            df.to_csv("{shelf}.{resource}.{port_name}_{request}.csv".
                format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request), 
                    mode = self.csv_mode, header = self.csv_header, index=False)
        except Exception as x:
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            logger.error("json returned : {lanforge_json_formatted}".format(lanforge_json_formatted=lanforge_json_formatted))

        logger.info("csv output:   {shelf}.{resource}.{port_name}_{request}.csv".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name, request=self.request))

        return lanforge_json, lanforge_text, lanforge_json_formatted

    # TODO This method is left in for an example it was taken from

    def get_request_radio_information(self,port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/radiostatus/all | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{port}/radiostatus/all'.format(lfmgr=self.lf_mgr, port=self.lf_port)
        request = requests.get(
            request_command, auth=(self.lf_user, self.lf_passwd))
        logger.info("radio request command: {request_command}".format(request_command=request_command))
        logger.info("radio request status_code {status}".format(status=request.status_code))
        logger.info("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' http://{lf_mgr}:{lf_port}/radiostatus/all | json_pp \n\n ".format(
            lf_mgr=self.lf_mgr, lf_port=self.lf_port))

        lanforge_radio_json = request.json()
        logger.info("radio request.json: {json}".format(json=lanforge_radio_json))
        lanforge_radio_text = request.text
        logger.info("radio request.text: {text}".format(text=lanforge_radio_text))
        lanforge_radio_json_formatted = json.dumps(lanforge_radio_json, indent=4)
        logger.info("lanforge_json_formatted: {json}".format(json=lanforge_radio_json_formatted))

        return lanforge_radio_json, lanforge_radio_text

    def post_clear_port_counters(self,port=None):
        # port passed in with command
        # this is needed for backward compatibility
        if port is not None:
            self.port = port
            logger.info("self.port updated to : {port}".format(port=self.port))
            self.update_port_info()

        # Syntax
        '''
        echo "{'shelf':1,'resource':1,'port':'vap3','extra':'dhcp_leases'}' > /tmp/curl_data
        curl --user "lanforge:lanforge"  -H 'Accept: application/json' -H "Content-type: application/json"
           -X POST -d 'http://<lanforge ip>:8080/{request}/
        where --user "USERNAME:PASSWORD"
        '''
        request_url = 'http://{lfmgr}:{port}/cli-json/clear_port_counters'.format(lfmgr=self.lf_mgr, port=self.lf_port)
        json_data = "{{'shelf':{shelf},'resource':{resource},'port':{port_name}}}".format(shelf=self.shelf, resource=self.resource, port_name=self.port_name)
        
        request = requests.post(request_url, json = json_data, auth=(self.lf_user, self.lf_passwd))

        logger.info("request url: {request_url}".format(request_url=request_url))
        logger.info("request status_code {status}".format(status=request.status_code))

        logger_msg =("equivalent curl command: curl --user \"lanforge:lanforge\" -H 'Accept: application/json' -H 'Content-type: application/json' -X POST -d \"{json_data} http://{lf_mgr}:{lf_port}/{request}/{shelf}/{resource}/{port_name} | json_pp  ".format(
            json_data=json_data,lf_mgr=self.lf_mgr, lf_port=self.lf_port, request=self.request, shelf=self.shelf, resource=self.resource, port_name=self.port_name
        ))
        logger.info(logger_msg)

    # TODO this method currently under development and not working.
    def post_wifi_cli_cmd(self, wifi_cli_cmd):

        # request_command = 'http://{lfmgr}:{port}/{wifi_cli_cmd}'.format(lfmgr=self.lf_mgr, port=self.lf_port, wifi_cli_cmd=json.dumps(wifi_cli_cmd).encode("utf-8"))
        request_command = 'http://{lfmgr}:{port}/{wifi_cli_cmd}'.format(lfmgr=self.lf_mgr, port=self.lf_port, wifi_cli_cmd=wifi_cli_cmd)
        # request_command = 'http://{lfmgr}:{port}/set_wifi_radio 1 1 wiphy1 NA NA NA NA NA NA NA NA NA 4'.format(lfmgr=self.lf_mgr, port=self.lf_port)
        request = requests.post(request_command, auth=(self.lf_user, self.lf_passwd))
        logger.info(
            "wifi_cli_cmd request command: {request_command}".format(
                request_command=request_command))
        logger.info(
            "wifi_cli_cmd request status_code {status}".format(
                status=request.status_code))
        lanforge_wifi_cli_cmd_json = request.json()
        logger.info("radio request.json: {json}".format(json=lanforge_wifi_cli_cmd_json))


# unit test
def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    parser = argparse.ArgumentParser(
        prog="lf_json_api.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        The script will read column data from lanforge GUI using request

    EXAMPLE:

    ./lf_json_api.py --lf_mgr 192.168.100.116 --lf_port 8080 --log_level debug --port wlan3 --lf_user lanforge --lf_passwd lanforge
        --port 1.1.vap0000 --get_request 'stations,04:f0:21:c5:33:97 stations,d8:f8:83:36:6c:44'

    ./lf_json_api.py --lf_mgr 192.168.100.116 --lf_port 8080 --log_level debug --port wlan3 --lf_user lanforge --lf_passwd lanforge
        --port 1.1.vap0000 --get_request 'wifi-stats'

        """)

    parser.add_argument("--lf_mgr", type=str, help="address of the LANforge GUI machine (localhost is default)",
                        default='localhost')
    parser.add_argument("--lf_port", help="IP Port the LANforge GUI is listening on (8080 is default)",
                        default=8080)
    parser.add_argument("--lf_user", type=str, help="user: lanforge")
    parser.add_argument("--lf_passwd", type=str, help="passwd: lanforge")
    parser.add_argument("--port", type=str, help=" port : 1.2.wlan3  provide full eid  (endpoint id")
    parser.add_argument("--radio", type=str, help=" --radio wiphy0")
    # TODO should be parsed from EID
    parser.add_argument('--log_level', default=None, help='Set logging level: debug | info | warning | error | critical')
    # logging configuration
    parser.add_argument("--lf_logger_config_json", help="--lf_logger_config_json <json file> , json configuration of logger")
    # TODO check command
    # TODO make generic so any request may be passed in
    parser.add_argument("--get_requests", type=str, help="perform get request may be a list:  port | radio | port_rssi | wifi-stats | stations | adb")
    # parser.add_argument("--mac", type=str, help="--mac <station bssid> for vap stations")
    parser.add_argument("--post_requests", type=str, help="perform set request may be a list:  nss , in development")
    parser.add_argument("--nss", type=str, help="--nss 4  set the number of spatial streams for a speific antenna ")
    parser.add_argument("--csv_mode", type=str, help="--csv_mode 'write' or 'append' ",choices = ['append' , 'write'])

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

    lf_json = lf_json_api(args.lf_mgr,
                          args.lf_port,
                          args.lf_user,
                          args.lf_passwd,
                          args.port,
                          args.csv_mode)

    if args.get_requests:
        get_requests = args.get_requests.split()
        radios = {}
        for get_request in get_requests:
            if get_request == "radio":
                lf_json.request = get_request
                lanforge_radio_json, lanforge_radio_text = lf_json.get_request_radio_information()
                for radio in list(lanforge_radio_json):
                    if radio != 'handler' and radio != 'uri' and radio != 'empty' and radio != 'warnings':
                        logger.debug("{radio}: {type}".format(radio=radio,type=lanforge_radio_json[radio]['driver']))
                        radio_result = "{radio}: {type}".format(radio=radio,type=lanforge_radio_json[radio]['driver'])
                        radio_result = radio_result.split('Bus', 1)[0]
                        radio_result = str(radio_result).replace('Port Type: WIFI-Radio   Driver:','')
                        radio_update = {radio: radio_result}
                        radios.update(radio_update)

                logger.debug("radios: {radios}".format(radios=radios))
                # used to list radios on a lanforge
                for radio in list(radios.keys()):
                    print("{radio}".format(radio=radios[radio]))
                        


            elif get_request == "port":
                lf_json.request = get_request
                lanforge_port_json, csv_file_port, lanforge_port_text, lanforge_port_json_formatted = lf_json.get_request_port_information()

                logger.debug("lanforge_port_json = {lanforge_port_json}".format(lanforge_port_json=lanforge_port_json))
                logger.debug("lanforge_port_text = {lanforge_port_text}".format(lanforge_port_text=lanforge_port_text))
                logger.debug("lanforge_port_json_formatted = {lanforge_port_json_formatted}".format(lanforge_port_json_formatted=lanforge_port_json_formatted))

            elif get_request == "port_rssi":
                lf_json.request = get_request
                lanforge_port_json, csv_file_port, lanforge_port_text, lanforge_port_json_formatted = lf_json.get_request_port_information()
                logger.debug("lanforge_port_json = {lanforge_port_json}".format(lanforge_port_json=lanforge_port_json))
                logger.debug("lanforge_port_json_formatted = {lanforge_port_json_formatted}".format(lanforge_port_json_formatted=lanforge_port_json_formatted))

                for key in lanforge_port_json:
                    if 'interface' in key:
                        avg_chain_rssi = lanforge_port_json[key]['avg chain rssi']
                        logger.info("avg chain rssi = {avg_chain_rssi}".format(avg_chain_rssi=avg_chain_rssi))
                        chain_rssi = lanforge_port_json[key]['chain rssi']
                        logger.info("chain rssi = {chain_rssi}".format(chain_rssi=chain_rssi))
                        signal = lanforge_port_json[key]['signal']
                        logger.info("signal = {signal}".format(signal=signal))

            elif get_request == "alerts":
                lf_json.request = get_request
                lanforge_alerts_json = lf_json.get_alerts_information()

            elif get_request == "wifi-stats":
                lf_json.request = get_request
                lanforge_wifi_stats_json, lanforge_wifi_stats_text, lanforge_wifi_stats_json_formatted = lf_json.get_request_wifi_stats_information()

                logger.debug("lanforge_wifi_stats_json = {lanforge_wifi_stats_json}".format(lanforge_wifi_stats_json=lanforge_wifi_stats_json))
                logger.debug("lanforge_wifi_stats_text = {lanforge_wifi_stats_text}".format(lanforge_wifi_stats_text=lanforge_wifi_stats_text))
                logger.debug("lanforge_wifi_stats_json_formatted = {lanforge_wifi_stats_json_formatted}".format(lanforge_wifi_stats_json_formatted=lanforge_wifi_stats_json_formatted))

            elif get_request == "adb":
                lf_json.request = get_request
                lanforge_adb_json, lanforge_adb_text, lanforge_adb_json_formatted = lf_json.get_request_adb_information()

                logger.debug("lanforge_adb_json = {lanforge_adb_json}".format(lanforge_adb_json=lanforge_adb_json))
                logger.debug("lanforge_adb_text = {lanforge_adb_text}".format(lanforge_adb_text=lanforge_adb_text))
                logger.debug("lanforge_adb_json_formatted = {lanforge_adb_json_formatted}".format(lanforge_adb_json_formatted=lanforge_adb_json_formatted))

            elif "single_station" in get_request:
                lf_json.request, mac = get_request.split(',')
                lf_json.mac = mac
                lanforge_wifi_stats_json, lanforge_wifi_stats_text, lanforge_wifi_stats_json_formatted = lf_json.get_request_single_station_information()

                logger.debug("lanforge_wifi_stats_json = {lanforge_wifi_stats_json}".format(lanforge_wifi_stats_json=lanforge_wifi_stats_json))
                logger.debug("lanforge_wifi_stats_text = {lanforge_wifi_stats_text}".format(lanforge_wifi_stats_text=lanforge_wifi_stats_text))
                logger.debug("lanforge_wifi_stats_json_formatted = {lanforge_wifi_stats_json_formatted}".format(lanforge_wifi_stats_json_formatted=lanforge_wifi_stats_json_formatted))


            elif get_request == "stations":
                lf_json.request = get_request

                lanforge_wifi_stats_json, lanforge_wifi_stats_text, lanforge_wifi_stats_json_formatted = lf_json.get_request_stations_information()

                logger.debug("lanforge_wifi_stats_json = {lanforge_wifi_stats_json}".format(lanforge_wifi_stats_json=lanforge_wifi_stats_json))
                logger.debug("lanforge_wifi_stats_text = {lanforge_wifi_stats_text}".format(lanforge_wifi_stats_text=lanforge_wifi_stats_text))
                logger.debug("lanforge_wifi_stats_json_formatted = {lanforge_wifi_stats_json_formatted}".format(lanforge_wifi_stats_json_formatted=lanforge_wifi_stats_json_formatted))

            # Generic so can do any query
            else:
                # set the generic request
                # set the generic request
                lf_json.request = get_request
                lanforge_json, lanforge_text, lanforge_json_formatted = lf_json.get_request_information()
                logger.debug("{request} : lanforge_json = {lanforge_json}".format(request=get_request, lanforge_json=lanforge_json))
                logger.debug("{request} : lanforge__text = {lanforge_text}".format(request=get_request, lanforge_text=lanforge_text))
                logger.debug("{request} : lanforge_json_formatted = {lanforge_json_formatted}".format(request=get_request, lanforge_json_formatted=lanforge_json_formatted))

    if args.post_requests:
        post_requests = args.post_requests.split()

        for post_request in post_requests:
            if post_request == "nss":
                nss = int(args.nss)
                if (nss == 1):
                    antennas_set = 1
                if (nss == 2):
                    antennas_set = 4
                if (nss == 3):
                    antennas_set = 7
                if (nss == 4):
                    antennas_set = 8

                wifi_cli_cmd = 'set_wifi_radio 1 {resource} {radio} NA NA NA NA NA NA NA NA NA {antennas}'.format(
                    resource=args.resource, radio=args.radio, antennas=antennas_set)
                lf_json.post_wifi_cli_cmd(wifi_cli_cmd=wifi_cli_cmd)

            if post_request == "clear_port_counters":
                lf_json.post_clear_port_counters()               

    # sample of creating layer 3


if __name__ == '__main__':
    main()
