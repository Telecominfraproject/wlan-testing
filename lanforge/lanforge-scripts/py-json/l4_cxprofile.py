#!/usr/bin/env python3
import sys
import os
import importlib
import requests
import pandas as pd
import time
import datetime
import ast
from pprint import pformat
import logging

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase

logger = logging.getLogger(__name__)


class L4CXProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_url = "http://%s:%s" % (lfclient_host, lfclient_port)
        self.debug = debug_
        self.url = "http://localhost/"
        self.requests_per_ten = 600
        self.local_realm = local_realm
        self.created_cx = {}
        self.created_endp = []
        self.test_type = "urls"
        self.lfclient_port = lfclient_port
        self.lfclient_host = lfclient_host

    def check_errors(self, debug=False):
        fields_list = ["!conn", "acc.+denied", "bad-proto", "bad-url", "other-err", "total-err", "rslv-p", "rslv-h",
                       "timeout", "nf+(4xx)", "http-r", "http-p", "http-t", "login-denied"]
        endp_list = self.json_get("layer4/list?fields=%s" % ','.join(fields_list))
        debug_info = {}
        if endp_list is not None and endp_list['endpoint'] is not None:
            endp_list = endp_list['endpoint']
            expected_passes = len(endp_list)
            passes = len(endp_list)
            for item in range(len(endp_list)):
                for name, info in endp_list[item].items():
                    for field in fields_list:
                        if info[field.replace("+", " ")] > 0:
                            passes -= 1
                            debug_info[name] = {field: info[field.replace("+", " ")]}
            if debug:
                logger.debug(debug_info)
            if passes == expected_passes:
                return True
            else:
                logger.info(list(debug_info), " Endps in this list showed errors getting to %s " % self.url)
                return False

    def start_cx(self):
        logger.info("Starting CXs...")
        for cx_name in self.created_cx.keys():
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": self.created_cx[cx_name],
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')
        print("")

    def stop_cx(self):
        logger.info("Stopping CXs...")
        for cx_name in self.created_cx.keys():
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": self.created_cx[cx_name],
                "cx_state": "STOPPED"
            }, debug_=self.debug)
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')
        print("")

    @staticmethod
    def compare_vals(old_list, new_list):
        passes = 0
        expected_passes = 0
        if len(old_list) == len(new_list):
            for item, value in old_list.items():
                expected_passes += 1
                if new_list[item] > old_list[item]:
                    passes += 1
            if passes == expected_passes:
                return True
            else:
                return False
        else:
            return False

    def get_bytes(self):
        time.sleep(1)
        cx_list = self.json_get("layer4/list?fields=name,%s" % self.test_type, debug_=self.debug)
        # logger.info("==============\n", cx_list, "\n==============")
        cx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if item in self.created_cx.keys() and value_name == self.test_type:
                            cx_map[item] = value_rx
        return cx_map

    def check_request_rate(self):
        endp_list = self.json_get("layer4/list?fields=urls/s")
        expected_passes = 0
        passes = 0
        # TODO: this might raise a nameerror lower down
        #  if self.target_requests_per_ten is None:
        #    raise NameError("check request rate: missing self.target_requests_per_ten")
        if endp_list is not None and endp_list['endpoint'] is not None:
            endp_list = endp_list['endpoint']
            for item in endp_list:
                for name, info in item.items():
                    if name in self.created_cx.keys():
                        expected_passes += 1
                        if info['urls/s'] * self.requests_per_ten >= self.target_requests_per_ten * .9:
                            # logger.info(name, info['urls/s'], info['urls/s'] * self.requests_per_ten, self.target_requests_per_ten * .9)
                            passes += 1

        return passes == expected_passes

    def cleanup(self):
        logger.info("Cleaning up cxs and endpoints")
        if len(self.created_cx) != 0:
            for cx_name in self.created_cx.keys():
                req_url = "cli-json/rm_cx"
                data = {
                    "test_mgr": "default_tm",
                    "cx_name": self.created_cx[cx_name]
                }
                self.json_post(req_url, data)
                # logger.debug(pformat(data))
                req_url = "cli-json/rm_endp"
                data = {
                    "endp_name": cx_name
                }
                self.json_post(req_url, data)
                # logger.debug(pformat(data))

    def create(self, ports=None, sleep_time=.5, debug_=False, suppress_related_commands_=None):
        if ports is None:
            ports = []
        cx_post_data = []
        for port_name in ports:
            logger.info("port_name: {} len: {} self.local_realm.name_to_eid(port_name): {}".format(port_name,
                                                                                             len(self.local_realm.name_to_eid(
                                                                                                 port_name)),
                                                                                             self.local_realm.name_to_eid(
                                                                                                 port_name)))
            shelf = self.local_realm.name_to_eid(port_name)[0]
            resource = self.local_realm.name_to_eid(port_name)[1]
            name = self.local_realm.name_to_eid(port_name)[2]
            endp_data = {
                "alias": name + "_l4",
                "shelf": shelf,
                "resource": resource,
                "port": name,
                "type": "l4_generic",
                "timeout": 10,
                "url_rate": self.requests_per_ten,
                "url": self.url,
                "proxy_auth_type": 0x200
            }
            url = "cli-json/add_l4_endp"
            self.local_realm.json_post(url, endp_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands_)
            time.sleep(sleep_time)

            endp_data = {
                "alias": "CX_" + name + "_l4",
                "test_mgr": "default_tm",
                "tx_endp": name + "_l4",
                "rx_endp": "NA"
            }
            cx_post_data.append(endp_data)
            self.created_cx[name + "_l4"] = "CX_" + name + "_l4"

        for cx_data in cx_post_data:
            url = "/cli-json/add_cx"
            self.local_realm.json_post(url, cx_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands_)
            time.sleep(sleep_time)

        # TODO:  Verify they were created here, or at least add a method to verify they were
        # created and add that to create_l4.py
        return True

    def monitor(self,
                duration_sec=60,
                monitor_interval=1,
                col_names=None,
                created_cx=None,
                monitor=True,
                report_file=None,
                output_format=None,
                script_name=None,
                arguments=None,
                iterations=0,
                debug=False):
        if duration_sec:
            duration_sec = LFCliBase.parse_time(duration_sec).seconds
        else:
            if (duration_sec is None) or (duration_sec <= 1):
                logger.critical("L4CXProfile::monitor wants duration_sec > 1 second")
                raise ValueError("L4CXProfile::monitor wants duration_sec > 1 second")
        if duration_sec <= monitor_interval:
            logger.critical("L4CXProfile::monitor wants duration_sec > monitor_interval")
            raise ValueError("L4CXProfile::monitor wants duration_sec > monitor_interval")
        if report_file is None:
            logger.critical("Monitor requires an output file to be defined")
            raise ValueError("Monitor requires an output file to be defined")
        if created_cx is None:
            logger.critical("Monitor needs a list of Layer 4 connections")
            raise ValueError("Monitor needs a list of Layer 4 connections")
        if (monitor_interval is None) or (monitor_interval < 1):
            logger.critical("L4CXProfile::monitor wants monitor_interval >= 1 second")
            raise ValueError("L4CXProfile::monitor wants monitor_interval >= 1 second")
        if output_format is not None:
            if output_format.lower() != report_file.split('.')[-1]:
                logger.critical('Filename %s does not match output format %s' % (report_file, output_format))
                raise ValueError('Filename %s does not match output format %s' % (report_file, output_format))
        else:
            output_format = report_file.split('.')[-1]

        # Step 1 - Assign column names 

        if col_names is not None and len(col_names) > 0:
            header_row = col_names
        else:
            header_row = list((list(self.json_get("/layer4/all")['endpoint'][0].values())[0].keys()))
        if debug:
            logger.debug(header_row)

        # Step 2 - Monitor columns
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=duration_sec)
        sleep_interval = round(duration_sec // 5)
        if debug:
            logger.debug("Sleep_interval is %s ", sleep_interval)
            logger.debug("Start time is %s ", start_time)
            logger.debug("End time is %s ", end_time)
        value_map = dict()
        passes = 0
        expected_passes = 0
        timestamps = []
        if self.test_type != 'urls':
            old_rx_values = self.get_bytes()

        for test in range(1 + iterations):
            while datetime.datetime.now() < end_time:
                if col_names is None:
                    response = self.json_get("/layer4/all")
                else:
                    fields = ",".join(col_names)
                    response = self.json_get("/layer4/%s?fields=%s" % (created_cx, fields))
                if debug:
                    logger.debug(response)
                if response is None:
                    logger.debug(response)
                    raise ValueError("Cannot find any endpoints")
                if monitor:
                    if debug:
                        logger.debug(response)

                time.sleep(sleep_interval)
                t = datetime.datetime.now()
                timestamps.append(t)
                value_map[t] = response
                expected_passes += 1
                if self.test_type == 'urls':
                    if self.check_errors(self.debug):
                        if self.check_request_rate():
                            passes += 1
                        else:
                            self._fail("FAIL: Request rate did not exceed target rate")
                            break
                    else:
                        self._fail("FAIL: Errors found getting to %s " % self.url)
                        break

                else:
                    new_rx_values = self.get_bytes()
                    if self.compare_vals(old_rx_values, new_rx_values):
                        passes += 1
                    else:
                        self._fail("FAIL: Not all stations increased traffic")

                    # self.exit_fail()
                time.sleep(monitor_interval)

        logger.info(value_map)

        # [further] post-processing data, after test completion
        full_test_data_list = []
        for test_timestamp, data in value_map.items():
            # reduce the endpoint data to single dictionary of dictionaries
            for datum in data["endpoint"]:
                for endpoint_data in datum.values():
                    if debug:
                        logger.debug(endpoint_data)
                    endpoint_data["Timestamp"] = test_timestamp
                    full_test_data_list.append(endpoint_data)

        header_row.append("Timestamp")
        header_row.append('Timestamp milliseconds')
        df = pd.DataFrame(full_test_data_list)

        df["Timestamp milliseconds"] = [self.get_milliseconds(x) for x in df["Timestamp"]]
        # round entire column
        df["Timestamp milliseconds"] = df["Timestamp milliseconds"].astype(int)
        df["Timestamp"] = df["Timestamp"].apply(lambda x: x.strftime("%m/%d/%Y %I:%M:%S"))
        df = df[["Timestamp", "Timestamp milliseconds", *header_row[:-2]]]
        # compare previous data to current data

        systeminfo = ast.literal_eval(
            requests.get('http://' + str(self.lfclient_host) + ':' + str(self.lfclient_port)).text)

        if output_format == 'hdf':
            df.to_hdf(report_file, 'table', append=True)
        if output_format == 'parquet':
            df.to_parquet(report_file, engine='pyarrow')
        if output_format == 'png':
            fig = df.plot().get_figure()
            fig.savefig(report_file)
        if output_format.lower() in ['excel', 'xlsx'] or report_file.split('.')[-1] == 'xlsx':
            df.to_excel(report_file, index=False)
        if output_format == 'df':
            return df
        supported_formats = ['csv', 'json', 'stata', 'pickle', 'html']
        for x in supported_formats:
            if output_format.lower() == x or report_file.split('.')[-1] == x:
                exec('df.to_' + x + '("' + report_file + '")')
