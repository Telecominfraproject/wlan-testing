#!/usr/bin/env python3
import sys
import os
import importlib
from pprint import pformat
from pprint import pprint
import csv
import pandas as pd
import time
import datetime
import json
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
pandas_extensions = importlib.import_module("py-json.LANforge.pandas_extensions")

logger = logging.getLogger(__name__)


class GenCXProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_host = lfclient_host
        self.lfclient_port = lfclient_port
        self.lfclient_url = "http://%s:%s" % (lfclient_host, lfclient_port)
        self.debug = debug_
        self.type = "lfping"
        self.dest = "127.0.0.1"
        self.interval = 1
        self.cmd = ""
        self.local_realm = local_realm
        self.name_prefix = "generic"
        self.created_cx = []
        self.created_endp = []
        self.file_output = "/dev/null"
        self.loop_count = 1
        self.speedtest_min_dl = 0
        self.speedtest_min_up = 0
        self.speedtest_max_ping = 0

    def parse_command(self, sta_name, gen_name):
        if self.type == "lfping":
            if self.dest and self.interval:
                self.cmd = "%s  -i %s -I %s %s" % (self.type, self.interval, sta_name, self.dest)
            else:
                logger.critical("Please ensure dest and interval have been set correctly")
                raise ValueError("Please ensure dest and interval have been set correctly")
        elif self.type == "generic":
            if self.cmd == "":
                logger.critical("Please ensure cmd has been set correctly")
                raise ValueError("Please ensure cmd has been set correctly")
        elif self.type == "speedtest":
            self.cmd = "vrf_exec.bash %s speedtest-cli --json --share" % sta_name
        elif self.type == "iperf3" and self.dest:
            self.cmd = "iperf3 --forceflush --format k --precision 4 -c %s -t 60 --tos 0 -b 1K --bind_dev %s -i 1 " \
                       "--pidfile /tmp/lf_helper_iperf3_%s.pid" % (self.dest, sta_name, gen_name)
        elif self.type == "iperf3_serv" and self.dest:
            self.cmd = "iperf3 --forceflush --format k --precision 4 -s --bind_dev %s -i 1 " \
                       "--pidfile /tmp/lf_helper_iperf3_%s.pid" % (sta_name, gen_name)
        elif self.type == "lfcurl":
            if self.file_output:
                self.cmd = "./scripts/lf_curl.sh  -p %s -i AUTO -o %s -n %s -d %s" % \
                           (sta_name, self.file_output, self.loop_count, self.dest)
            else:
                logger.critical("Please ensure file_output has been set correctly")
                raise ValueError("Please ensure file_output has been set correctly")
        else:
            logger.critical("Unknown command type")
            raise ValueError("Unknown command type")

    def start_cx(self):
        logger.info("Starting CXs: %s" %self.created_cx)
        logger.info("Created-Endp: %s" % self.created_endp)
        for cx_name in self.created_cx:
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx_name,
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')
        print("")

    def stop_cx(self):
        logger.info("Stopping CXs...")
        for cx_name in self.created_cx:
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx_name,
                "cx_state": "STOPPED"
            }, debug_=self.debug)
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')
        print("")

    def cleanup(self):
        logger.info("Cleaning up cxs and endpoints")
        for cx_name in self.created_cx:
            req_url = "cli-json/rm_cx"
            data = {
                "test_mgr": "default_tm",
                "cx_name": cx_name
            }
            self.json_post(req_url, data)

        for endp_name in self.created_endp:
            req_url = "cli-json/rm_endp"
            data = {
                "endp_name": endp_name
            }
            self.json_post(req_url, data)

    def set_flags(self, endp_name, flag_name, val):
        data = {
            "name": endp_name,
            "flag": flag_name,
            "val": val
        }
        self.json_post("cli-json/set_endp_flag", data, debug_=self.debug)

    def set_cmd(self, endp_name, cmd):
        data = {
            "name": endp_name,
            "command": cmd
        }
        self.json_post("cli-json/set_gen_cmd", data, debug_=self.debug)

    def parse_command_gen(self, sta_name, dest):
        if self.type == "lfping":
            if self.dest and self.interval:
                self.cmd = "%s  -i %s -I %s %s" % (self.type, self.interval, sta_name, dest)
                logger.debug(self.cmd)
            else:
                logger.critical("Please ensure dest and interval have been set correctly")
                raise ValueError("Please ensure dest and interval have been set correctly")
        elif self.type == "generic":
            if self.cmd == "":
                logger.critical("Please ensure cmd has been set correctly")
                raise ValueError("Please ensure cmd has been set correctly")
        elif self.type == "speedtest":
            self.cmd = "vrf_exec.bash %s speedtest-cli --json --share" % sta_name
        elif self.type == "iperf3" and self.dest:
            self.cmd = "iperf3 --forceflush --format k --precision 4 -c %s -t 60 --tos 0 -b 1K --bind_dev %s -i 1 " \
                       "--pidfile /tmp/lf_helper_iperf3_test.pid" % (self.dest, sta_name)
        elif self.type == "lfcurl":
            if self.file_output:
                self.cmd = "./scripts/lf_curl.sh  -p %s -i AUTO -o %s -n %s -d %s" % \
                           (sta_name, self.file_output, self.loop_count, self.dest)
            else:
                logger.critical("Please ensure file_output has been set correctly")
                raise ValueError("Please ensure file_output has been set correctly")
        else:
            logger.critical("Unknown command type")
            raise ValueError("Unknown command type")

    def create_gen(self, sta_port, dest, add, sleep_time=.5, debug_=False, suppress_related_commands_=None):
        if self.debug:
            debug_ = True
        post_data = []
        endp_tpls = []

        if type(sta_port) == str:
            if sta_port != "1.1.eth1":
                count = 5
            else:
                count = 40
            for i in range(0, count):
                port_info = self.local_realm.name_to_eid(sta_port)
                resource = port_info[1]
                shelf = port_info[0]
                name = port_info[2]

                gen_name_a = "%s-%s" % (self.name_prefix, name) + "_" + str(i) + add
                gen_name_b = "D_%s-%s" % (self.name_prefix, name) + "_" + str(i) + add
                endp_tpls.append((shelf, resource, name, gen_name_a, gen_name_b))

            print(endp_tpls)
        elif type(sta_port) == list:
            for port_name in sta_port:
                logger.info("hello............{sta_port}".format(sta_port=sta_port))
                for i in range(0, 5):
                    port_info = self.local_realm.name_to_eid(port_name)
                    try:
                        resource = port_info[1]
                        shelf = port_info[0]
                        name = port_info[2]
                    except ValueError:
                        logger.critical("Unexpected name for port_name {port_name}".format(port_name=port_name))
                        raise ValueError("Unexpected name for port_name {port_name}".format(port_name=port_name))

                    # this naming convention follows what you see when you use
                    # lf_firemod.pl --action list_endp after creating a generic endpoint
                    gen_name_a = "%s-%s" % (self.name_prefix, name) + "_" + str(i) + add
                    gen_name_b = "D_%s-%s" % (self.name_prefix, name) + "_" + str(i) + add
                    endp_tpls.append((shelf, resource, name, gen_name_a, gen_name_b))

        logger.info(endp_tpls)

        for endp_tpl in endp_tpls:
            shelf = endp_tpl[0]
            resource = endp_tpl[1]
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]

            data = {
                "alias": gen_name_a,
                "shelf": shelf,
                "resource": resource,
                "port": name,
                "type": "gen_generic"
            }
            logger.info(pformat(data))

            self.json_post("cli-json/add_gen_endp", data, debug_=self.debug)

        self.local_realm.json_post("/cli-json/nc_show_endpoints", {"endpoint": "all"})
        time.sleep(sleep_time)

        for endp_tpl in endp_tpls:
            gen_name_a = endp_tpl[3]
            gen_name_b = endp_tpl[4]
            self.set_flags(gen_name_a, "ClearPortOnStart", 1)
        time.sleep(sleep_time)

        if type(dest) == str:
            for endp_tpl in endp_tpls:
                name = endp_tpl[2]
                gen_name_a = endp_tpl[3]
                # gen_name_b  = endp_tpl[4]
                self.parse_command_gen(name, dest)
                self.set_cmd(gen_name_a, self.cmd)
            time.sleep(sleep_time)

        elif type(dest) == list:
            mm = 0
            for endp_tpl in endp_tpls:
                name = endp_tpl[2]
                gen_name_a = endp_tpl[3]
                # gen_name_b  = endp_tpl[4]
                self.parse_command_gen(name, dest[mm])
                self.set_cmd(gen_name_a, self.cmd)
                mm = mm + 1
                if mm == 8:
                    mm = 0
            time.sleep(sleep_time)

        j = 0
        for endp_tpl in endp_tpls:
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]
            gen_name_b = endp_tpl[4]
            cx_name = "CX_%s-%s" % (self.name_prefix, name) + "_" + str(j) + add
            j = j + 1
            data = {
                "alias": cx_name,
                "test_mgr": "default_tm",
                "tx_endp": gen_name_a,
                "rx_endp": gen_name_b
            }
            post_data.append(data)
            # self.created_cx = []
            self.created_cx.append(cx_name)
            # self.created_endp = []
            self.created_endp.append(gen_name_a)
            self.created_endp.append(gen_name_b)
        time.sleep(sleep_time)

        logger.info(self.created_cx)

        for data in post_data:
            url = "/cli-json/add_cx"
            logger.info(pformat(data))
            self.local_realm.json_post(url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands_)
            time.sleep(2)
        time.sleep(sleep_time)
        for data in post_data:
            self.local_realm.json_post("/cli-json/show_cx", {
                "test_mgr": "default_tm",
                "cross_connect": data["alias"]
            })
        time.sleep(sleep_time)

    def create(self, ports=None, sleep_time=.5, debug_=False, suppress_related_commands_=None):
        if not ports:
            ports = []
        if self.debug:
            debug_ = True
        post_data = []
        endp_tpls = []
        for port_name in ports:
            port_info = self.local_realm.name_to_eid(port_name)
            resource = port_info[1]
            shelf = port_info[0]
            name = port_info[2]

            # this naming convention follows what you see when you use
            # lf_firemod.pl --action list_endp after creating a generic endpoint
            gen_name_a = "%s-%s" % (self.name_prefix, name)
            endp_tpls.append((shelf, resource, name, gen_name_a))

        for endp_tpl in endp_tpls:
            shelf = endp_tpl[0]
            resource = endp_tpl[1]
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]

            data = {
                "alias": gen_name_a,
                "shelf": shelf,
                "resource": resource,
                "port": name,
                "type": "gen_generic"
            }
            logger.debug(pformat(data))

            self.json_post("cli-json/add_gen_endp", data, debug_=self.debug)

        self.local_realm.json_post("/cli-json/nc_show_endpoints", {"endpoint": "all"})
        if sleep_time:
            time.sleep(sleep_time)

        for endp_tpl in endp_tpls:
            gen_name_a = endp_tpl[3]
            self.set_flags(gen_name_a, "ClearPortOnStart", 1)
        if sleep_time:
            time.sleep(sleep_time)

        for endp_tpl in endp_tpls:
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]
            # gen_name_b  = endp_tpl[4]
            self.parse_command(name, gen_name_a)
            self.set_cmd(gen_name_a, self.cmd)
        if sleep_time:
            time.sleep(sleep_time)

        for endp_tpl in endp_tpls:
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]
            cx_name = "CX_%s-%s" % (self.name_prefix, name)
            data = {
                "alias": cx_name,
                "test_mgr": "default_tm",
                "tx_endp": gen_name_a
            }
            post_data.append(data)
            self.created_cx.append(cx_name)
            self.created_endp.append(gen_name_a)

        if sleep_time:
            time.sleep(sleep_time)

        for data in post_data:
            url = "/cli-json/add_cx"
            logger.info(pformat(data))
            self.local_realm.json_post(url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands_)
            #time.sleep(2)
        if sleep_time:
            time.sleep(sleep_time)

        for data in post_data:
            self.local_realm.json_post("/cli-json/show_cx", {
                "test_mgr": "default_tm",
                "cross_connect": data["alias"]
            })
        return True

    # Looks incorrect to me. --Ben
    def choose_ping_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        logger.debug(pformat(gen_results))
        if gen_results['endpoints']:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    logger.info("k: %s  v: %s" % (k, v))
                    if v['name'] in self.created_endp and not v['name'].endswith('1'):
                        if v['last results'] != "" and "Unreachable" not in v['last results']:
                            return True, v['name']
                        else:
                            return False, v['name']

    def choose_lfcurl_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        logger.debug(pformat(gen_results))
        if gen_results['endpoints']:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['name'] != '':
                        results = v['last results'].split()
                        if 'Finished' in v['last results']:
                            # TODO: What is this actually doing?
                            if results[1][:-1] == results[2]:
                                return True, v['name']
                            else:
                                return False, v['name']

    def choose_iperf3_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if gen_results['endpoints']:
            logger.info(gen_results['endpoints'])
            # for name in gen_results['endpoints']:
            # pprint(name.items)
            # for k,v in name.items():
        exit(1)

    def choose_speedtest_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if gen_results['endpoints']:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['last results'] and v['name'] in self.created_endp and v['last results'] != '':
                        last_results = json.loads(v['last results'])
                        if not last_results['download'] and not last_results['upload'] and not last_results['ping']:
                            return False, v['name']
                        elif last_results['download'] >= self.speedtest_min_dl and \
                                last_results['upload'] >= self.speedtest_min_up and \
                                last_results['ping'] <= self.speedtest_max_ping:
                            return True, v['name']

    def choose_generic_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if gen_results['endpoints']:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['name'] in self.created_endp and not v['name'].endswith('1'):
                        if v['last results'] != "" and "not known" not in v['last results']:
                            return True, v['name']
                        else:
                            return False, v['name']

    # TODO monitor is broken
    # TODO:  Can only monitor ports on a single resource.
    def monitor(self,
                duration_sec=60,
                monitor_interval=2, # seconds
                sta_list=None,
                resource_id=1,
                generic_cols=None,
                port_mgr_cols=None,
                must_increase_cols=None,
                monitor_endps=None, # list of endpoints to monitor
                monitor=True,
                report_file=None,
                systeminfopath=None,
                output_format=None,
                script_name=None,
                arguments=None,
                compared_report=None,
                debug=False):
        try:
            duration_sec = self.parse_time(duration_sec).seconds
        except ValueError:
            if not duration_sec or (duration_sec <= 1):
                logger.critical("GenCXProfile::monitor wants duration_sec > 1 second")
                raise ValueError("GenCXProfile::monitor wants duration_sec > 1 second")
            if duration_sec <= monitor_interval:
                logger.critical("GenCXProfile::monitor wants duration_sec > monitor_interval")
                raise ValueError("GenCXProfile::monitor wants duration_sec > monitor_interval")
        if not report_file:
            logger.critical("Monitor requires an output file to be defined")
            raise ValueError("Monitor requires an output file to be defined")
        if not systeminfopath:
            logger.critical("Monitor requires a system info path to be defined")
            raise ValueError("Monitor requires a system info path to be defined")
        if not monitor_endps:
            logger.critical("Monitor needs a list of Endpoints to monitor")
            raise ValueError("Monitor needs a list of Endpoints to monitor")
        if not monitor_interval or (monitor_interval < 1):
            logger.critical("GenCXProfile::monitor wants monitor_interval >= 1 second")
            raise ValueError("GenCXProfile::monitor wants monitor_interval >= 1 second")
        if not generic_cols:
            logger.critical("GenCXProfile::monitor wants a list of column names to monitor")
            raise ValueError("GenCXProfile::monitor wants a list of column names to monitor")
        if output_format:
            if output_format.lower() != report_file.split('.')[-1]:
                logger.critical(
                    'Filename {report_file} has an extension that does not match output format {output_format}'.format(
                        report_file=report_file, output_format=output_format))
                raise ValueError(
                    'Filename {report_file} has an extension that does not match output format {output_format}'.format(
                        report_file=report_file, output_format=output_format))
        else:
            output_format = report_file.split('.')[-1]

        # default save to csv first
        if report_file.split('.')[-1] != 'csv':
            report_file = report_file.replace(str(output_format), 'csv', 1)
            logger.info("Saving rolling data into: " + str(report_file))

        # ================== Step 1, set column names and header row
        generic_cols = [self.replace_special_char(x) for x in generic_cols]
        generic_fields = ",".join(generic_cols)
        default_cols = ['Timestamp', 'Timestamp milliseconds epoch', 'Timestamp seconds epoch', 'Duration elapsed']
        default_cols.extend(generic_cols)
        if port_mgr_cols:
            default_cols.extend(port_mgr_cols)
        header_row = default_cols

        # csvwriter.writerow([systeminfo['VersionInfo']['BuildVersion'], script_name, str(arguments)])

        if port_mgr_cols:
            port_mgr_cols = [self.replace_special_char(x) for x in port_mgr_cols]
            port_mgr_cols_labelled = []
            for col_name in port_mgr_cols:
                port_mgr_cols_labelled.append("port mgr - " + col_name)

            port_mgr_fields = ",".join(port_mgr_cols)
            header_row.extend(port_mgr_cols_labelled)

        # create sys info file
        systeminfo = self.json_get('/')
        sysinfo = [str("LANforge GUI Build: " + systeminfo['VersionInfo']['BuildVersion']),
                   str("Script Name: " + script_name), str("Argument input: " + str(arguments))]
        with open(systeminfopath, 'w') as filehandle:
            for listitem in sysinfo:
                filehandle.write('%s\n' % listitem)

        # ================== Step 2, monitor columns
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=duration_sec)

        fail_incr_count = 0
        pass_incr_count = 0
        prev_results = {} # dict of dicts
        if must_increase_cols:
            for en in monitor_endps:
                print("Monitoring Endpoint: %s" %(en))
                prev_results[en] = {} # dict of col names to values
                for cn in must_increase_cols:
                    prev_results[en][cn] = 0

        # instantiate csv file here, add specified column headers
        csvfile = open(str(report_file), 'w')
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(header_row)

        # for x in range(0,int(round(iterations,0))):
        initial_starttime = datetime.datetime.now()
        logger.info("Starting Test Monitoring for %s seconds..." % duration_sec)
        while datetime.datetime.now() < end_time:
            t = datetime.datetime.now()
            timestamp = t.strftime("%m/%d/%Y %I:%M:%S")
            t_to_millisec_epoch = int(self.get_milliseconds(t))
            t_to_sec_epoch = int(self.get_seconds(t))
            time_elapsed = int(self.get_seconds(t)) - int(self.get_seconds(initial_starttime))
            basecolumns = [timestamp, t_to_millisec_epoch, t_to_sec_epoch, time_elapsed]

            # get endp values
            gen_url = "/generic/%s?fields=%s" % (",".join(monitor_endps), generic_fields);
            #print("gen-url: %s" % (gen_url))
            generic_response = self.json_get(gen_url)

            if port_mgr_cols:
                # get info from port manager with list of values from cx_a_side_list
                port_mgr_response = self.json_get("/port/1/%s/%s?fields=%s" % (resource_id, sta_list, port_mgr_fields))

            if "endpoints" not in generic_response or not generic_response:
                logger.critical(generic_response)
                logger.critical("Json generic_response from LANforge... {generic_response}".format(generic_response=generic_response))
                logger.critical("Cannot find columns requested to be searched. Exiting script, please retry.")
                raise ValueError("Cannot find columns requested to be searched. Exiting script, please retry.")
            if port_mgr_cols:
                if "interfaces" not in port_mgr_response or not port_mgr_response:
                    logger.critical(port_mgr_response)
                    logger.critical("Cannot find columns requested to be searched. Exiting script, please retry.")
                    raise ValueError("Cannot find columns requested to be searched. Exiting script, please retry.")
                logger.debug("Json port_mgr_response from LANforge... {port_mgr_response}".format(port_mgr_response=port_mgr_response))

            #print("generic response: ")
            #pprint(generic_response)
            endp_array = generic_response["endpoints"]
            #print("endp-array: ")
            #pprint(endp_array)
            for endpoint in endp_array:  # each endpoint is a dictionary
                #print("endpoint: ")
                #pprint(endpoint)
                #print("endpoint values: ")
                #pprint(endpoint.values())

                endp_values_list = list(endpoint.values())
                #for x in endp_values_list:
                #    pprint(x)

                # There is only one value in the endp_values_list, the key is the name,
                # but the name is also in the value dict, so we ignore the key.
                endp_values = endp_values_list[0]

                endp_name = endp_values["name"]
                temp_list = basecolumns.copy() # Must make a deep copy or we just keep appending to basecolumns object.
                for columnname in generic_cols:
                    val = endp_values[columnname]
                    #print("column-name: %s val: %s must-increase-cols: %s" % (columnname, val, must_increase_cols))
                    temp_list.append(val)
                    if must_increase_cols:
                        if columnname in must_increase_cols:
                            # Ensure this has increased since last sample.
                            #print("endp_name: %s columname: %s value: %s  endpoint: %s" % (endp_name, columnname, val, endpoint))
                            if prev_results[endp_name][columnname] >= LFUtils.speed_to_int(val):
                                self._fail("Endpoint %s column: %s did not increase, old: %s  new: %s" %
                                           (endp_name, columnname, prev_results[endp_name][columnname], val))
                                fail_incr_count += 1
                            else:
                                logger.debug("Endpoint %s column: %s did increase, old: %s  new: %s" %
                                             (endp_name, columnname, prev_results[endp_name][columnname], val))
                                pass_incr_count += 1

                    if port_mgr_cols:
                        for sta_name in sta_list_edit:
                            if sta_name in current_sta:
                                for interface in port_mgr_response["interfaces"]:
                                    if sta_name in list(interface.keys())[0]:
                                        merge = temp_endp_values.copy()
                                        # rename keys (separate port mgr 'rx bytes' from generic 'rx bytes')
                                        port_mgr_values_dict = list(interface.values())[0]
                                        renamed_port_cols = {}
                                        for key in port_mgr_values_dict.keys():
                                            renamed_port_cols['port mgr - ' + key] = port_mgr_values_dict[key]
                                        merge.update(renamed_port_cols)
                                        for name in port_mgr_cols:
                                            temp_list.append(merge[name])
                csvwriter.writerow(temp_list)

            time.sleep(monitor_interval)
            # End of while loop for duration of monitor period.

        csvfile.close()

        if fail_incr_count == 0:
            if pass_incr_count > 0:
                self._pass("Verified requested counters: %s increased each of %s monitor attempts" %
                           (must_increase_cols, pass_incr_count));
        else:
            if pass_incr_count > 0:
                self._fail("Partial success: Verified requested counters: %s increased % of % attempts" %
                           (must_increase_cols, pass_incr_count, (pass_incr_count + fail_incr_count)));

        # TODO:  This looks broken, figure out intent and fix, or remove.
        # comparison to last report / report inputted
        if compared_report:
            compared_df = pandas_extensions.compare_two_df(dataframe_one=pandas_extensions.file_to_df(report_file),
                                                           dataframe_two=pandas_extensions.file_to_df(compared_report))
            exit(1)
            # append compared df to created one
            if output_format.lower() != 'csv':
                pandas_extensions.df_to_file(dataframe=pd.read_csv(report_file), output_f=output_format,
                                             save_path=report_file)
        else:
            if output_format.lower() != 'csv':
                pandas_extensions.df_to_file(dataframe=pd.read_csv(report_file), output_f=output_format,
                                             save_path=report_file)
