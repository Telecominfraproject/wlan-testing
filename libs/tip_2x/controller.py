"""

    Base Library for Ucentral

"""
import datetime
import json
import logging
import os
import sys
import time
from operator import itemgetter
from urllib.parse import urlparse
from urllib.parse import urlencode
import allure
import pytest
import requests


# logging.basicConfig(level=logging.DEBUG)
# from http.client import HTTPConnection
#
# HTTPConnection.debuglevel = 1
# requests.logging.getLogger()


class ConfigureController:

    def __init__(self, controller_data):
        self.username = controller_data["username"]
        self.password = controller_data["password"]
        self.host = urlparse(controller_data["url"])
        self.access_token = ""
        # self.session = requests.Session()
        self.login_resp = self.login()
        self.gw_host, self.fms_host, \
            self.prov_host, self.owrrm_host, \
            self.owanalytics_host, self.owsub_host = self.get_gw_endpoint()
        if self.gw_host == "" or self.fms_host == "" or self.prov_host == "":
            time.sleep(60)
            self.gw_host, self.fms_host, \
                self.prov_host, self.owrrm_host, \
                self.owanalytics_host, self.owsub_host = self.get_gw_endpoint()
            if self.gw_host == "" or self.fms_host == "" or self.prov_host == "":
                self.logout()
                logging.info(self.gw_host, self.fms_host + self.prov_host)
                pytest.exit("All Endpoints not available in Controller Service")
                sys.exit()

    def build_uri_sec(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        return new_uri

    def build_url_fms(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.fms_host.hostname, self.fms_host.port, path)
        return new_uri

    def build_uri(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.gw_host.hostname, self.gw_host.port, path)
        return new_uri

    def build_url_prov(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.prov_host.hostname, self.prov_host.port, path)
        return new_uri

    def build_url_owrrm(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.owrrm_host.hostname, self.owrrm_host.port, path)
        return new_uri

    def build_url_owanalytics(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.owanalytics_host.hostname, self.owanalytics_host.port, path)
        return new_uri

    def build_url_owsub(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.owsub_host.hostname, self.owsub_host.port, path)
        return new_uri

    def request(self, service, command, method, params, payload):
        if service == "sec":
            uri = self.build_uri_sec(command)
        elif service == "gw":
            uri = self.build_uri(command)
        elif service == "fms":
            uri = self.build_url_fms(command)
        elif service == "prov":
            uri = self.build_url_prov(command)
        elif service == "rrm":
            uri = self.build_url_owrrm(command)
        elif service == "analytics":
            uri = self.build_url_owanalytics(command)
        elif service == "sub":
            uri = self.build_url_owsub(command)
        else:
            raise NameError("Invalid service code for request.")
        params = params
        if method == "GET":
            resp = requests.get(uri, headers=self.make_headers(), params=params, verify=False, timeout=120)
        elif method == "POST":
            resp = requests.post(uri, params=params, data=payload, headers=self.make_headers(), verify=False,
                                 timeout=120)
        elif method == "PUT":
            resp = requests.put(uri, params=params, data=payload, headers=self.make_headers(), verify=False,
                                timeout=120)
        elif method == "DELETE":
            resp = requests.delete(uri, headers=self.make_headers(), params=params, verify=False, timeout=120)

        self.check_response(method, resp, self.make_headers(), payload, uri)

        return resp

    def login(self):
        uri = self.build_uri_sec("oauth2")
        # self.session.mount(uri, HTTPAdapter(max_retries=15))
        payload = json.dumps({"userId": self.username, "password": self.password})
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, "", payload, uri)
        token = resp
        self.access_token = token.json()['access_token']
        resp.close()
        if resp.status_code != 200:
            pytest.exit(str(resp.json()))
        # self.session.headers.update({'Authorization': self.access_token})
        return token

    def get_gw_endpoint(self):
        uri = self.build_uri_sec("systemEndpoints")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        services = resp.json()
        gw_host = None
        fms_host = None
        prov_host = None
        owrrm_host = None
        owanalytics_host = None
        owsub_host = None
        for service in services['endpoints']:
            if service['type'] == "owgw":
                gw_host = urlparse(service["uri"])
            if service['type'] == "owfms":
                fms_host = urlparse(service["uri"])
            if service['type'] == "owprov":
                prov_host = urlparse(service["uri"])
            if service['type'] == "owrrm":
                owrrm_host = urlparse(service["uri"])
            if service['type'] == "owanalytics":
                owanalytics_host = urlparse(service["uri"])
            if service['type'] == "owsub":
                owsub_host = urlparse(service["uri"])
        if (gw_host is None) or (fms_host is None) or (prov_host is None) or (owrrm_host is None) or (
                owanalytics_host is None) or (
                owsub_host is None):
            logging.error("Not All Microservices available:" + str(
                json.dumps(services['endpoints'], indent=2)))
        return gw_host, fms_host, prov_host, owrrm_host, owanalytics_host, owsub_host

    def logout(self):
        uri = self.build_uri_sec('oauth2/%s' % self.access_token)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        r = resp
        resp.close()
        return r

    def make_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.access_token,
                   "Connection": "keep-alive",
                   "Content-Type": "application/json",
                   "Keep-Alive": "timeout=10, max=1000"
                                 "conte"
                   }
        return headers

    def check_response(self, cmd, response, headers, data_str, url=""):
        try:
            logging.info("Command Response: " + "\n" +
                         "Command Type: " + str(cmd) + "\n" +
                         "Response URI: " + str(url) + "\n" +
                         "Response Headers: " + str(headers) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Response Code: " + str(response.status_code) + "\n" +
                         "Response Body: " + str(response.json()))
            allure.attach(name="Command Response: ", body="Command Response: " + "\n" +
                                                          "Command Type: " + str(cmd) + "\n" +
                                                          "Response URI: " + str(url) + "\n" +
                                                          "Response Headers: " + str(headers) + "\n" +
                                                          "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                          "Response Code: " + str(response.status_code) + "\n" +
                                                          "Response Body: " + str(response.json()))
        except:
            pass
        return True


class Controller(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def get_devices(self):
        uri = self.build_uri("devices")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_by_serial_number(self, serial_number):
        uri = self.build_uri("device/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_sdk_version_gw(self):
        uri = self.build_uri("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def perform_system_wide_commands(self, payload):
        uri = self.build_uri("system")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def get_sdk_version_fms(self):
        uri = self.build_url_fms("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_sdk_version_prov(self):
        uri = self.build_url_prov("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_sdk_version_owrrm(self):
        uri = self.build_url_owrrm("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_sdk_version_ow_analytics(self):
        uri = self.build_url_owanalytics("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_sdk_version_owsub(self):
        uri = self.build_url_owsub("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_sdk_version_sec(self):
        uri = self.build_uri_sec("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        return version['version']

    def get_system_gw(self):
        uri = self.build_uri("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_fms(self):
        uri = self.build_url_fms("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    # FMS
    def get_different_values_from_the_running_service(self):
        uri = self.build_url_fms("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def perform_system_wide_commands(self, payload):
        uri = self.build_url_fms("system")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def get_list_of_firmwares(self):
        uri = self.build_url_fms("firmwares")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_list_all_the_defined_device_revision_history(self, serial_number):
        uri = self.build_url_fms("revisionHistory/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_list_of_connected_devices_and_some_values(self):
        uri = self.build_url_fms("connectedDevices")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_status_of_connected_device(self, serial_number):
        uri = self.build_url_fms("connectedDevice/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_analysis_of_the_existing_devices_we_know_about(self):
        uri = self.build_url_fms("deviceReport")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_receive_a_report_on_single_decide(self, serial_number):
        uri = self.build_url_fms("deviceInformation/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_configuration_items(self, entries):
        uri = self.build_url_fms("systemConfiguration?entries=" + entries)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_prov(self):
        uri = self.build_url_prov("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_ow_rrm(self):
        uri = self.build_url_owrrm("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_ow_analytics(self):
        uri = self.build_url_owanalytics("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_ow_sub(self):
        uri = self.build_url_owsub("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_uuid(self, serial_number):
        device_info = self.get_device_by_serial_number(serial_number=serial_number)
        device_info = device_info.json()
        return device_info["UUID"]

    def add_device_to_gw(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_device_from_gw(self, device_name):
        uri = self.build_uri("device/" + device_name)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def get_commands(self, serial_number):
        uri = self.build_uri("commands?serialNumber=" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_logs(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/logs")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_health_checks(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/healthchecks")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_capabilities(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/capabilities")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_statistics(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/statistics")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_status(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/status")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def ap_reboot(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/reboot")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def ap_factory_reset(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/factory")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def ping_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/ping")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def led_blink_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/leds")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def trace_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/trace")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def wifi_scan_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/wifiscan")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def request_specific_msg_from_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/request")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def event_queue(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/eventqueue")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def telemetry(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/telemetry")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def get_rtty_params(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/rtty")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def edit_device_on_gw(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def check_restrictions(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/capabilities")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        resp = resp.json()
        if 'restrictions' in resp['capabilities'].keys():
            return True
        else:
            return False

    def asb_script(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/script")
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        resp = resp.json()
        resp = resp['UUID']
        return resp

    def get_file(self, serial_number, uuid):
        uri = self.build_uri("file/" + uuid + "?serialNumber=" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        time.sleep(10)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        if resp.headers.get("Transfer-Encoding") == "chunked":
            file = resp.content
            with open("gopi.tar.gz", "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            file = resp.content
            logging.info(file)
            with open("gopi.tar.gz", "wb") as f:
                f.write(file)
        allure.attach.file(name="file", source="gopi.tar.gz", extension=".tar")
        return resp

    def get_lists_of_all_default_configurations(self):
        uri = self.build_uri("default_configurations")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_list_of_OUIs(self, maclist):
        uri = self.build_uri("ouis" + "?macList=" + maclist)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_list_of_scripts(self):
        uri = self.build_uri("scripts")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_list_of_blacklisted_devices(self):
        uri = self.build_uri("blacklist")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_radius_proxy_configuration(self):
        uri = self.build_uri("radiusProxyConfig")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_country_code_for_ip_address(self, iplist):
        uri = self.build_uri("iptocountry" + "?iplist=" + iplist)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def create_default_configuration(self, name, payload):
        uri = self.build_uri("default_configuration/" + name)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def get_default_configuration(self, name):
        uri = self.build_uri("default_configuration/" + name)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def edit_default_configuration(self, name, payload):
        uri = self.build_uri("default_configuration/" + name)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def delete_default_configuration(self, name):
        uri = self.build_uri("default_configuration/" + name)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def create_to_the_blacklist(self, serial_number, payload):
        uri = self.build_uri("blacklist/" + serial_number)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def get_blacklist_entry(self, serial_number):
        uri = self.build_uri("blacklist/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def modify_to_the_blacklist(self, serial_number, payload):
        uri = self.build_uri("blacklist/" + serial_number)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)

        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def delete_from_blacklist(self, serial_number):
        uri = self.build_uri("blacklist/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def debug_device(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number + "/script")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        time.sleep(10)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_file(self, serial_number, uuid):
        uri = self.build_uri("file/" + uuid + "?serialNumber=" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        time.sleep(10)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_some_commands(self, serial_number):
        uri = self.build_uri("commands" + "?serialNumber=" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_some_device_logs(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/logs")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_some_device_health_checks(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/healthchecks")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_capabilities_device(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/capabilities")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_statistics_device(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/statistics")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def delete_radius_proxy_configuration(self):
        uri = self.build_uri("radiusProxyConfig")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def modify_radius_proxy_configuration(self, payload):
        uri = self.build_uri("radiusProxyConfig")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=120)
        time.sleep(2)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def get_radius_proxy_configuration(self):
        uri = self.build_uri("radiusProxyConfig")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_radius_sessions(self, serial_number):
        uri = self.build_uri("radiusSessions/" + serial_number)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.make_headers()))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=120)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp


class FMSUtils:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client

    def upgrade_firmware(self, serial="", url=""):
        payload = "{ \"serialNumber\" : " + "\"" + \
                  serial + "\"" + " , \"uri\" : " \
                  + "\"" + url \
                  + "\"" + ", \"when\" : 0" \
                  + " }"
        command = "device/" + serial + "/upgrade"
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(command) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(command) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        response = self.sdk_client.request(service="gw", command="device/" + serial + "/upgrade",
                                           method="POST", params="serialNumber=" + serial,
                                           payload="{ \"serialNumber\" : " + "\"" + serial + "\"" +
                                                   " , \"uri\" : " + "\"" + url + "\"" +
                                                   ", \"when\" : 0" + " }")

    def ap_model_lookup(self, model=""):
        devices = self.get_device_set()
        model_name = ""
        for device in devices['deviceTypes']:
            if str(device).__eq__(model):
                model_name = device
        return model_name

    def get_revisions(self):
        response = self.sdk_client.request(service="fms", command="firmwares", method="GET", params="revisionSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_latest_fw(self, model=""):

        device_type = self.ap_model_lookup(model=model)

        response = self.sdk_client.request(service="fms", command="firmwares", method="GET",
                                           params="latestOnly=true&deviceType=" + device_type,
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_device_set(self):
        response = self.sdk_client.request(service="fms", command="firmwares", method="GET", params="deviceSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_firmwares(self, limit="10000", model="", latestonly="", branch="", commit_id="", offset="3000"):

        deviceType = self.ap_model_lookup(model=model)
        params = "limit=" + limit + \
                 "&deviceType=" + deviceType + \
                 "&latestonly=" + latestonly + \
                 "offset=" + offset
        command = "firmwares"
        response = self.sdk_client.request(service="fms", command=command, method="GET", params=params, payload="")
        allure.attach(name=command + params,
                      body=str(response.status_code) + "\n" + str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        if response.status_code == 200:
            data = response.json()
            newlist = sorted(data['firmwares'], key=itemgetter('created'))

            return newlist

        return "error"

    def get_least_three_release_images_from_current_image(self, firmware_list=[], current_image=""):
        """This method will return latest three release images"""
        image_date = []
        all_images_from_current_image = []
        current_image_index = None
        for i in firmware_list:
            image_date.append(i["imageDate"])
        image_date.sort(reverse=True)
        ordered_list_firmware = []
        for i in image_date:
            for j in firmware_list:
                if i == j["imageDate"]:
                    ordered_list_firmware.append(j)
                    break
        for i in range(len(ordered_list_firmware)):
            if current_image in ordered_list_firmware[i]["revision"]:
                current_image_index = i
                break
        logging.info("current_image_index: " + str(current_image_index))
        all_images_from_current_image = ordered_list_firmware[current_image_index:]
        logging.info("all_images_from_current_image" + str(all_images_from_current_image))
        release_images_all = []
        least_3_release_images = []
        for firmware in all_images_from_current_image:
            if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1][0] == "v":
                if "rc" not in firmware['image']:
                    release_images_all.append(firmware)
        logging.info("release_images_all" + str(release_images_all))
        latest_release_image_number = int(release_images_all[0]['image'].split(".")[1])
        logging.info("latest_release_image_number: " + str(latest_release_image_number))
        all_releases_num_list = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 11, 10]
        index_latest_release = all_releases_num_list.index(latest_release_image_number)
        latest_3_releases_list_num = [all_releases_num_list[index_latest_release], all_releases_num_list[index_latest_release+1],
                                      all_releases_num_list[index_latest_release+2]]
        logging.info("latest_3_releases_list_num: " + str(latest_3_releases_list_num))
        count = 0
        # Find out List of least 3 release Image
        # Logic for least 3 release Images
        for i in release_images_all:
            if "." + str(latest_3_releases_list_num[count]) + "." in str(i['image']):
                least_3_release_images.append(i)
                count = count + 1
            if len(least_3_release_images) == 3:
                break
        logging.info("least three release images from current image: " + str(least_3_release_images))
        return least_3_release_images


class ProvUtils:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client

    def get_inventory(self):
        uri = self.sdk_client.build_url_prov("inventory")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_inventory_by_device(self, device_name):
        uri = self.sdk_client.build_url_prov("inventory/" + device_name)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_system_prov(self):
        uri = self.sdk_client.build_url_prov("system?command=info")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_device_to_inventory(self, device_name, payload):
        uri = self.sdk_client.build_url_prov("inventory/" + device_name)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))

        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_device_from_inventory(self, device_name):
        uri = self.sdk_client.build_url_prov("inventory/" + device_name)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_entity(self):
        uri = self.sdk_client.build_url_prov("entity")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_entity_by_id(self, entity_id):
        uri = self.sdk_client.build_url_prov("entity/" + entity_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_entity(self, payload):
        uri = self.sdk_client.build_url_prov("entity/1")

        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_entity(self, entity_id):
        uri = self.sdk_client.build_url_prov("entity/" + entity_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_device_from_inventory(self, device_name, payload):
        uri = self.sdk_client.build_url_prov("inventory/" + device_name)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def edit_entity(self, payload, entity_id):
        uri = self.sdk_client.build_url_prov("entity/" + entity_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_contact(self):
        uri = self.sdk_client.build_url_prov("contact")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_contact_by_id(self, contact_id):
        uri = self.sdk_client.build_url_prov("contact/" + contact_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_contact(self, payload):
        uri = self.sdk_client.build_url_prov("contact/1")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_contact(self, contact_id):
        uri = self.sdk_client.build_url_prov("contact/" + contact_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_contact(self, payload, contact_id):
        uri = self.sdk_client.build_url_prov("contact/" + contact_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_location(self):
        uri = self.sdk_client.build_url_prov("location")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_location_by_id(self, location_id):
        uri = self.sdk_client.build_url_prov("location/" + location_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_location(self, payload):
        uri = self.sdk_client.build_url_prov("location/1")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_location(self, location_id):
        uri = self.sdk_client.build_url_prov("location/" + location_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_location(self, payload, location_id):
        uri = self.sdk_client.build_url_prov("location/" + location_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)

        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_venue(self):
        uri = self.sdk_client.build_url_prov("venue")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_venue_by_id(self, venue_id):
        uri = self.sdk_client.build_url_prov("venue/" + venue_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_venue(self, payload):
        uri = self.sdk_client.build_url_prov("venue/0")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_venue(self, venue_id):
        uri = self.sdk_client.build_url_prov("venue/" + venue_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_venue(self, payload, venue_id):
        uri = self.sdk_client.build_url_prov("venue/" + venue_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_map(self):
        uri = self.sdk_client.build_url_prov("map")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_map_by_id(self, map_id):
        uri = self.sdk_client.build_url_prov("map/" + map_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_map(self, payload):
        uri = self.sdk_client.build_url_prov("map/0")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_map(self, map_id):
        uri = self.sdk_client.build_url_prov("map/" + map_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_map(self, payload, map_id):
        uri = self.sdk_client.build_url_prov("map/" + map_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_operator(self):
        uri = self.sdk_client.build_url_prov("operator")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_operator_by_id(self, operator_id):
        uri = self.sdk_client.build_url_prov("operator/" + operator_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_operator(self, payload):
        uri = self.sdk_client.build_url_prov("operator/1")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_operator(self, operator_id):
        uri = self.sdk_client.build_url_prov("operator/" + operator_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_operator(self, payload, operator_id):
        uri = self.sdk_client.build_url_prov("operator/" + operator_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_service_class_by_operator_id(self, operator_id):
        uri = self.sdk_client.build_url_prov("serviceClass?operatorId=" + operator_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_service_class_by_id(self, service_class_id):
        uri = self.sdk_client.build_url_prov("serviceClass/" + service_class_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_service_class(self, payload):
        uri = self.sdk_client.build_url_prov("serviceClass/1")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_service_class(self, service_class_id):
        uri = self.sdk_client.build_url_prov("serviceClass/" + service_class_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_service_class(self, payload, service_class_id):
        uri = self.sdk_client.build_url_prov("serviceClass/" + service_class_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def get_configuration(self):
        uri = self.sdk_client.build_url_prov("configuration")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def get_configuration_by_id(self, configuration_id):
        uri = self.sdk_client.build_url_prov("configuration/" + configuration_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def add_configuration(self, payload):
        uri = self.sdk_client.build_url_prov("configuration/1")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), payload, uri)
        return resp

    def delete_configuration(self, configuration_id):
        uri = self.sdk_client.build_url_prov("configuration/" + configuration_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("DELETE", resp, self.sdk_client.make_headers(), "", uri)
        return resp

    def edit_configuration(self, payload, configuration_id):
        uri = self.sdk_client.build_url_prov("configuration/" + configuration_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("PUT", resp, self.sdk_client.make_headers(), payload, uri)
        return resp


class AnalyticsUtility:
    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client

    def create_board(self, payload):
        uri = self.sdk_client.build_url_owanalytics("board/0")
        data = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Create a Board", body="Sending Command: POST" + str(uri) + "\n" +
                                                  "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                  "Data: " + str(payload) + "\n" +
                                                  "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=data, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_board(self, board_id="7475645a-9df9-4f45-834f-d73d2e801927"):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def edit_board(self, payload, board_id):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id)
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.put(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def delete_board(self, board_id):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_boards(self):
        uri = self.sdk_client.build_url_owanalytics("boards")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Get List of Boards", body="Sending Command: GET " + str(uri) + "\n" +
                                                      "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                      "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_board_devices(self, board_id):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id + "/devices")
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_board_data(self, board_id):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id + "/timepoints")
        current_time = int(time.time())
        params = {
            'fromDate': current_time,
            'endDate': current_time
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def delete_board_data(self, board_id):
        uri = self.sdk_client.build_url_owanalytics("board/" + board_id + "/timepoints")
        current_time = int(time.time())
        params = {
            'fromDate': current_time,
            'endDate': current_time
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_wifi_clients_history(self, venue):
        uri = self.sdk_client.build_url_owanalytics("wifiClientHistory")
        params = {
            'venue': venue,
            'macsOnly': json.dumps(True),
            'limit': 500,
            'offset': 0
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_wifi_client_history(self, client, venue):
        uri = self.sdk_client.build_url_owanalytics("wifiClientHistory/" + client)
        params = {
            'venue': venue,
            'macsOnly': json.dumps(True)
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def delete_wifi_client_history(self, client, venue):
        uri = self.sdk_client.build_url_owanalytics("wifiClientHistory/" + client)
        params = {
            'venue': venue,
            'macsOnly': json.dumps(True)
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.delete(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def post_system_commands(self, payload):
        uri = self.sdk_client.build_url_owanalytics("system")
        payload = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(payload) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.post(uri, data=payload, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        return resp

    def get_system_commands(self, command):
        uri = self.sdk_client.build_url_owanalytics("system")
        params = {
            'command': command
        }
        params = urlencode(params)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))
        resp = requests.get(uri, params=params, headers=self.sdk_client.make_headers(), verify=False, timeout=120)
        self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        return resp


class UProfileUtility:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client
        self.base_profile_config = {
            "uuid": 1,
            "radios": [],
            "interfaces": [{
                "name": "WAN",
                "role": "upstream",
                "services": ["ssh", "lldp", "dhcp-snooping"],
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            },
                {
                    "name": "LAN",
                    "role": "downstream",
                    "services": ["ssh", "lldp", "dhcp-snooping"],
                    "ethernet": [
                        {
                            "select-ports": [
                                "LAN*"
                            ]
                        }
                    ],
                    "ipv4": {
                        "addressing": "static",
                        "subnet": "192.168.1.1/16",
                        "dhcp": {
                            "lease-first": 10,
                            "lease-count": 10000,
                            "lease-time": "6h"
                        }
                    },
                }],
            "metrics": {
                "statistics": {
                    "interval": 60,
                    "types": ["ssids", "lldp", "clients"]
                },
                "health": {
                    "interval": 120
                },
                "wifi-frames": {
                    "filters": ["probe",
                                "auth",
                                "assoc",
                                "disassoc",
                                "deauth",
                                "local-deauth",
                                "inactive-deauth",
                                "key-mismatch",
                                "beacon-report",
                                "radar-detected"]
                },
                "dhcp-snooping": {
                    "filters": ["ack", "discover", "offer", "request", "solicit", "reply", "renew"]
                }
            },
            "services": {
                "lldp": {
                    "describe": "TIP OpenWiFi",
                    "location": "QA"
                },
                "ssh": {
                    "port": 22
                }
            }
        }
        self.vlan_section = {
            "name": "WAN100",
            "role": "upstream",
            "vlan": {
                "id": 100
            },
            "ethernet": [
                {
                    "select-ports": [
                        "WAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "dynamic"
            }
        }
        self.mode = None

    def set_mesh_services(self):
        self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.97.1/24"
        self.base_profile_config["interfaces"][1]["ipv4"]["dhcp"]["lease-count"] = 100
        del self.base_profile_config['metrics']['wifi-frames']
        del self.base_profile_config['metrics']['dhcp-snooping']
        var = {
            "filters": ["probe",
                        "auth"]
        }
        self.base_profile_config["metrics"]['wifi-frames'] = var
        del self.base_profile_config['services']
        var2 = {
            "lldp": {
                "describe": "uCentral",
                "location": "universe"
            },
            "ssh": {
                "port": 22
            }
        }
        self.base_profile_config['services'] = var2

    def set_express_wifi(self, open_flow=None):
        if self.mode == "NAT":
            self.base_profile_config["interfaces"][1]["services"] = ["ssh", "lldp", "open-flow"]
            self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.97.1/24"
            self.base_profile_config["interfaces"][1]["ipv4"]["dhcp"]["lease-count"] = 100
            self.base_profile_config['services']["open-flow"] = open_flow
            self.base_profile_config['services']['lldp']['describe'] = "OpenWiFi - expressWiFi"
            self.base_profile_config['services']['lldp']['location'] = "Hotspot"

    def set_captive_portal(self):

        if self.mode == "NAT":
            max_client = {
                "max-clients": 32
            }
            # sourceFile = open('captive_config.py', 'w')

            self.base_profile_config["interfaces"][1]["name"] = "captive"
            self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.2.1/24"
            self.base_profile_config["interfaces"][1]["captive"] = max_client
            del self.base_profile_config["interfaces"][1]["ethernet"]
            del self.base_profile_config["interfaces"][1]["services"]
            del self.base_profile_config["metrics"]["wifi-frames"]
            del self.base_profile_config["metrics"]["dhcp-snooping"]

    def encryption_lookup(self, encryption="psk"):
        encryption_mapping = {
            "none": "open",
            "psk": "wpa",
            "psk2": "wpa2",
            "sae": "wpa3",
            "psk-mixed": "wpa|wpa2",
            "sae-mixed": "wpa3",
            "wpa": 'wap',
            "wpa2": "eap",
            "wpa3": "eap",
            "wpa-mixed": "eap",
            "wpa3-mixed": "sae"
        }
        if encryption in encryption_mapping.keys():
            return encryption_mapping[encryption]
        else:
            return False

    def get_ssid_info(self):
        ssid_info = []
        for interfaces in self.base_profile_config["interfaces"]:
            if "ssids" in interfaces.keys():
                for ssid_data in interfaces["ssids"]:
                    for band in ssid_data["wifi-bands"]:
                        temp = [ssid_data["name"]]
                        if ssid_data["encryption"]["proto"] == "none" or "radius" in ssid_data.keys():
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append('[BLANK]')
                        else:
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append(ssid_data["encryption"]["key"])
                        temp.append(band)
                        ssid_info.append(temp)
        return ssid_info

    def set_radio_config(self, radio_config={}, open_roaming=False):
        if open_roaming:
            base_radio_config_2g = {
                "band": "2G",
                "country": "CA",
                "channel-mode": "HT",
                "channel-width": 20,
                "channel": "auto"
            }
            base_radio_config_5g = {
                "band": "5G",
                "country": "CA",
                "channel-mode": "VHT",
                "channel-width": 80,
                "channel": "auto"
            }

            for band in radio_config:
                if band == "2G" and radio_config[band] is not None:
                    for keys in radio_config[band]:
                        base_radio_config_2g[keys] = radio_config[band][keys]
                if band == "5G" and radio_config[band] is not None:
                    for keys in radio_config[band]:
                        base_radio_config_5g[keys] = radio_config[band][keys]
            self.base_profile_config["radios"].append(base_radio_config_2g)
            self.base_profile_config["radios"].append(base_radio_config_5g)
        else:
            base_radio_config_2g = {
                "band": "2G",
                "country": "US",
                "channel-mode": "HE",
                "channel": "auto"
            }
            base_radio_config_5g = {
                "band": "5G",
                "country": "US",
                "allow-dfs": True,
                "channel-mode": "HE",
                "channel": "auto"
            }
            base_radio_config_6g = {
                "band": "6G",
                "country": "US",
                "channel-mode": "HE",
                "channel": "auto"
            }
            for band in radio_config:
                if band == "2G" and radio_config[band] is not None:
                    for keys in radio_config[band]:
                        base_radio_config_2g[keys] = radio_config[band][keys]
                if band == "5G" and radio_config[band] is not None:
                    for keys in radio_config[band]:
                        base_radio_config_5g[keys] = radio_config[band][keys]
                if band == "6G" and radio_config[band] is not None:
                    for keys in radio_config[band]:
                        base_radio_config_6g[keys] = radio_config[band][keys]

            self.base_profile_config["radios"].append(base_radio_config_2g)
            self.base_profile_config["radios"].append(base_radio_config_5g)
            self.base_profile_config["radios"].append(base_radio_config_6g)
        self.vlan_section["ssids"] = []
        self.vlan_ids = []

    def set_mode(self, mode, mesh=False, open_roaming=False):
        self.mode = mode
        if mode == "NAT":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            elif open_roaming:
                self.base_profile_config['metrics']['statistics']['interval'] = 120
                self.base_profile_config['interfaces'][1]['ipv4']['subnet'] = "192.168.1.1/24"
                self.base_profile_config['interfaces'][1]['ipv4']['dhcp']['lease-count'] = 100
                del self.base_profile_config['metrics']['dhcp-snooping']
            self.base_profile_config['interfaces'][1]['ssids'] = []
        elif mode == "BRIDGE":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            elif open_roaming:
                self.base_profile_config['metrics']['statistics']['interval'] = 120
                self.base_profile_config['interfaces'][1]['ipv4']['subnet'] = "192.168.1.1/24"
                self.base_profile_config['interfaces'][1]['ipv4']['dhcp']['lease-count'] = 100
                del self.base_profile_config['interfaces'][0]['services']
                del self.base_profile_config['metrics']['wifi-frames']
                del self.base_profile_config['metrics']['dhcp-snooping']
                del self.base_profile_config['services']['lldp']
            self.base_profile_config['interfaces'][0]['ssids'] = []
        elif mode == "VLAN":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            del self.base_profile_config['interfaces'][1]
            self.base_profile_config['interfaces'][0]['ssids'] = []
            self.base_profile_config['interfaces'] = []
            wan_section_vlan = {
                "name": "WAN",
                "role": "upstream",
                "services": ["lldp", "ssh", "dhcp-snooping"],
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            }
            self.base_profile_config['interfaces'].append(wan_section_vlan)
        else:
            logging.error("Invalid Mode")
            return 0

    def add_ssid(self, ssid_data, radius=False, radius_auth_data={}, radius_accounting_data={}, pass_point_data=None,
                 open_roaming=False):
        open_ssid = {
            "name": "To_Download_profile",
            "wifi-bands": [
                "5G"
            ],
            "bss-mode": "ap",
            "encryption": {
                "proto": "none",
                "ieee80211w": "optional"
            }
        }
        if open_roaming:
            ssid_info = {'name': ssid_data["ssid_name"], "bss-mode": "ap", "wifi-bands": []}
            for options in ssid_data:
                if options == "multi-psk":
                    ssid_info[options] = ssid_data[options]
                if options == "rate-limit":
                    ssid_info[options] = ssid_data[options]
                if options == "isolate-clients":
                    ssid_info[options] = ssid_data[options]
                if options == "strict-forwarding":
                    ssid_info[options] = ssid_data[options]
                if options == "captive":
                    ssid_info[options] = ssid_data[options]
            for i in ssid_data["appliedRadios"]:
                ssid_info["wifi-bands"].append(i)
            ssid_info['encryption'] = {}
            ssid_info['encryption']['proto'] = ssid_data["security"]
            try:
                ssid_info['encryption']['key'] = ssid_data["security_key"]
            except Exception as e:
                pass
            ssid_info['encryption']['ieee80211w'] = "optional"
            if radius:
                ssid_info["radius"] = {}
                ssid_info["radius"]["authentication"] = {
                    "nas-identifier": radius_auth_data["nas-identifier"],
                    "chargeable-user-id": radius_auth_data["chargeable-user-id"],
                    "host": radius_auth_data["ip"],
                    "port": radius_auth_data["port"],
                    "secret": radius_auth_data["secret"],
                    "request-attribute": radius_auth_data["request-attribute"],
                }
                ssid_info["radius"]["accounting"] = {
                    "host": radius_accounting_data["ip"],
                    "port": radius_accounting_data["port"],
                    "secret": radius_accounting_data["secret"],
                    "request-attribute": radius_accounting_data["request-attribute"],
                    "interval": radius_accounting_data["interval"]
                }
                ssid_info["pass-point"] = pass_point_data

        else:
            ssid_info = {'name': ssid_data["ssid_name"], "bss-mode": "ap", "wifi-bands": [],
                         "services": ["wifi-frames"]}
            for options in ssid_data:
                if options == "multi-psk":
                    ssid_info[options] = ssid_data[options]
                if options == "rate-limit":
                    ssid_info[options] = ssid_data[options]
                if options == "isolate-clients":
                    ssid_info[options] = ssid_data[options]
                if options == "strict-forwarding":
                    ssid_info[options] = ssid_data[options]
                if options == "captive":
                    ssid_info[options] = ssid_data[options]
                    ssid_info["services"] = ["captive"]
            for i in ssid_data["appliedRadios"]:
                ssid_info["wifi-bands"].append(i)
            ssid_info['encryption'] = {}
            ssid_info['encryption']['proto'] = ssid_data["security"]
            try:
                ssid_info['encryption']['key'] = ssid_data["security_key"]
            except Exception as e:
                pass
            ssid_info['encryption']['ieee80211w'] = "optional"
            if radius:
                ssid_info["radius"] = {}
                ssid_info["radius"]["authentication"] = {
                    "host": radius_auth_data["ip"],
                    "port": radius_auth_data["port"],
                    "secret": radius_auth_data["secret"]
                }
                ssid_info["radius"]["accounting"] = {
                    "host": radius_accounting_data["ip"],
                    "port": radius_accounting_data["port"],
                    "secret": radius_accounting_data["secret"]
                }
        if self.mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'].append(ssid_info)
            if open_roaming is True:
                self.base_profile_config['interfaces'][1]['ssids'].append(open_ssid)
        elif self.mode == "BRIDGE":
            self.base_profile_config['interfaces'][0]['ssids'].append(ssid_info)
            if open_roaming is True:
                self.base_profile_config['interfaces'][0]['ssids'].append(open_ssid)
        elif self.mode == "VLAN":
            vid = ssid_data["vlan"]
            self.vlan_section = {
                "name": "WAN100",
                "role": "upstream",
                "services": ["lldp", "dhcp-snooping"],
                "vlan": {
                    "id": 100
                },
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            }
            vlan_section = self.vlan_section
            if vid in self.vlan_ids:
                for i in self.base_profile_config['interfaces']:
                    if i["name"] == "WANv%s" % (vid):
                        i["ssids"].append(ssid_info)
            else:
                self.vlan_ids.append(vid)
                vlan_section['name'] = "WANv%s" % (vid)
                vlan_section['vlan']['id'] = int(vid)
                vlan_section["ssids"] = []
                vlan_section["ssids"].append(ssid_info)
                self.base_profile_config['interfaces'].append(vlan_section)

                vsection = 0
        else:
            logging.error("invalid Operating Mode")
            pytest.exit("invalid Operating Mode")

    def push_config(self, serial_number):
        payload = {"configuration": self.base_profile_config, "serialNumber": serial_number, "UUID": 1}
        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        logging.info("Sending Command: " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                     "Headers: " + str(self.sdk_client.make_headers()))
        allure.attach(name="Sending Command:", body="Sending Command: " + "\n" +
                                                    "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                    "URI: " + str(uri) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(self.sdk_client.make_headers()))

        resp = requests.post(uri, data=basic_cfg_str, headers=self.sdk_client.make_headers(),
                             verify=False, timeout=240)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), basic_cfg_str, uri)
        resp.close()
        return resp


if __name__ == '__main__':
    controller = {
        'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
        'username': "tip@ucentral.com",
        'password': 'OpenWifi%123',
    }
    obj = Controller(controller_data=controller)
    # po = ProvUtils(sdk_client=obj)
    # print(po.get_inventory())
    # up = UProfileUtility(sdk_client=obj, controller_data=controller)
    # up.set_mode(mode="BRIDGE")
    # up.set_radio_config()
    # up.add_ssid(ssid_data={"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"})
    # up.push_config(serial_number="3c2c99f44e77")
    # print(obj.get_device_by_serial_number(serial_number="3c2c99f44e77"))
    # print(datetime.datetime.utcnow())
    # fms = FMSUtils(sdk_client=obj)
    # new = fms.get_firmwares(model='ecw5410')
    # for i in new:
    #     print(i)
    # print(len(new))

    # print(profile.get_ssid_info())
    # # print(obj.get_devices())
    obj.logout()
