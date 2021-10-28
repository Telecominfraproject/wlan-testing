# !/usr/bin/env python3
import sys
import os
import importlib
from pprint import pprint
import csv
import pandas as pd
import time
import datetime

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
pandas_extensions = importlib.import_module("py-json.LANforge.pandas_extensions")


class L3CXProfile(LFCliBase):
    def __init__(self,
                 lfclient_host,
                 lfclient_port,
                 local_realm,
                 side_a_min_bps=None,
                 side_b_min_bps=None,
                 side_a_max_bps=0,
                 side_b_max_bps=0,
                 side_a_min_pdu=-1,
                 side_b_min_pdu=-1,
                 side_a_max_pdu=0,
                 side_b_max_pdu=0,
                 report_timer_=3000,
                 name_prefix_="Unset",
                 number_template_="00000",
                 mconn=0,
                 debug_=False):
        """
        :param lfclient_host:
        :param lfclient_port:
        :param local_realm:
        :param side_a_min_bps:
        :param side_b_min_bps:
        :param side_a_max_bps:
        :param side_b_max_bps:
        :param side_a_min_pdu:
        :param side_b_min_pdu:
        :param side_a_max_pdu:
        :param side_b_max_pdu:
        :param name_prefix_: prefix string for connection
        :param number_template_: how many zeros wide we padd, possibly a starting integer with left padding
        :param mconn:  Multi-conn setting for this connection.
        :param debug_:
        """
        super().__init__(lfclient_host, lfclient_port, _debug=debug_)
        self.debug = debug_
        self.local_realm = local_realm
        self.side_a_min_pdu = side_a_min_pdu
        self.side_b_min_pdu = side_b_min_pdu
        self.side_a_max_pdu = side_a_max_pdu
        self.side_b_max_pdu = side_b_max_pdu
        self.side_a_min_bps = side_a_min_bps
        self.side_b_min_bps = side_b_min_bps
        self.side_a_max_bps = side_a_max_bps
        self.side_b_max_bps = side_b_max_bps
        self.report_timer = report_timer_
        self.created_cx = {}
        self.created_endp = {}
        self.name_prefix = name_prefix_
        self.number_template = number_template_
        self.mconn = mconn

    def get_cx_count(self):
        return len(self.created_cx.keys())

    def get_cx_names(self):
        return self.created_cx.keys()

    def get_cx_report(self):
        self.data = {}
        for cx_name in self.get_cx_names():
            self.data[cx_name] = self.json_get("/cx/" + cx_name).get(cx_name)
        return self.data

    def __get_rx_values(self):
        cx_list = self.json_get("endp?fields=name,rx+bytes")
        if self.debug:
            print(self.created_cx.values())
            print("==============\n", cx_list, "\n==============")
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes' and item in self.created_cx.values():
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    def __compare_vals(self, old_list, new_list):
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

    def instantiate_file(self, file_name, file_format):
        pass

    def monitor(self,
                duration_sec=60,
                monitor_interval_ms=1,
                sta_list=None,
                layer3_cols=None,
                port_mgr_cols=None,
                created_cx=None,
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
        except:
            if (duration_sec is None) or (duration_sec <= 1):
                raise ValueError("L3CXProfile::monitor wants duration_sec > 1 second")
            if (duration_sec <= monitor_interval_ms):
                raise ValueError("L3CXProfile::monitor wants duration_sec > monitor_interval")
        if report_file == None:
            raise ValueError("Monitor requires an output file to be defined")
        if systeminfopath == None:
            raise ValueError("Monitor requires a system info path to be defined")
        if created_cx == None:
            raise ValueError("Monitor needs a list of Layer 3 connections")
        if (monitor_interval_ms is None) or (monitor_interval_ms < 1):
            raise ValueError("L3CXProfile::monitor wants monitor_interval >= 1 second")
        if layer3_cols is None:
            raise ValueError("L3CXProfile::monitor wants a list of column names to monitor")
        if output_format is not None:
            if output_format.lower() != report_file.split('.')[-1]:
                raise ValueError('Filename %s has an extension that does not match output format %s .' % (
                    report_file, output_format))
        else:
            output_format = report_file.split('.')[-1]

        # default save to csv first
        if report_file.split('.')[-1] != 'csv':
            report_file = report_file.replace(str(output_format), 'csv', 1)
            print("Saving rolling data into..." + str(report_file))

        # ================== Step 1, set column names and header row
        layer3_cols = [self.replace_special_char(x) for x in layer3_cols]
        layer3_fields = ",".join(layer3_cols)
        default_cols = ['Timestamp', 'Timestamp milliseconds epoch', 'Timestamp seconds epoch', 'Duration elapsed']
        default_cols.extend(layer3_cols)
        if port_mgr_cols is not None:
            default_cols.extend(port_mgr_cols)
        header_row = default_cols

        # csvwriter.writerow([systeminfo['VersionInfo']['BuildVersion'], script_name, str(arguments)])

        if port_mgr_cols is not None:
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

        passes = 0
        expected_passes = 0
        old_cx_rx_values = self.__get_rx_values()

        # instantiate csv file here, add specified column headers
        csvfile = open(str(report_file), 'w')
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(header_row)

        # wait 10 seconds to get proper port data
        time.sleep(10)

        # for x in range(0,int(round(iterations,0))):
        initial_starttime = datetime.datetime.now()
        while datetime.datetime.now() < end_time:
            t = datetime.datetime.now()
            timestamp = t.strftime("%m/%d/%Y %I:%M:%S")
            t_to_millisec_epoch = int(self.get_milliseconds(t))
            t_to_sec_epoch = int(self.get_seconds(t))
            time_elapsed = int(self.get_seconds(t)) - int(self.get_seconds(initial_starttime))
            basecolumns = [timestamp, t_to_millisec_epoch, t_to_sec_epoch, time_elapsed]
            layer_3_response = self.json_get("/endp/%s?fields=%s" % (created_cx, layer3_fields))
            if port_mgr_cols is not None:
                port_mgr_response = self.json_get("/port/1/1/%s?fields=%s" % (sta_list, port_mgr_fields))
            # get info from port manager with list of values from cx_a_side_list
            if "endpoint" not in layer_3_response or layer_3_response is None:
                print(layer_3_response)
                raise ValueError("Cannot find columns requested to be searched. Exiting script, please retry.")
                if debug:
                    print("Json layer_3_response from LANforge... " + str(layer_3_response))
            if port_mgr_cols is not None:
                if "interfaces" not in port_mgr_response or port_mgr_response is None:
                    print(port_mgr_response)
                    raise ValueError("Cannot find columns requested to be searched. Exiting script, please retry.")
                if debug:
                    print("Json port_mgr_response from LANforge... " + str(port_mgr_response))

            for endpoint in layer_3_response["endpoint"]:  # each endpoint is a dictionary
                endp_values = list(endpoint.values())[0]
                temp_list = basecolumns
                for columnname in header_row[len(basecolumns):]:
                    temp_list.append(endp_values[columnname])
                    if port_mgr_cols is not None:
                        for sta_name in sta_list_edit:
                            if sta_name in current_sta:
                                for interface in port_mgr_response["interfaces"]:
                                    if sta_name in list(interface.keys())[0]:
                                        merge = temp_endp_values.copy()
                                        # rename keys (separate port mgr 'rx bytes' from layer3 'rx bytes')
                                        port_mgr_values_dict = list(interface.values())[0]
                                        renamed_port_cols = {}
                                        for key in port_mgr_values_dict.keys():
                                            renamed_port_cols['port mgr - ' + key] = port_mgr_values_dict[key]
                                        merge.update(renamed_port_cols)
                                        for name in port_mgr_cols:
                                            temp_list.append(merge[name])
                csvwriter.writerow(temp_list)

            new_cx_rx_values = self.__get_rx_values()
            if debug:
                print(old_cx_rx_values, new_cx_rx_values)
                print("\n-----------------------------------")
                print(t)
                print("-----------------------------------\n")
            expected_passes += 1
            if self.__compare_vals(old_cx_rx_values, new_cx_rx_values):
                passes += 1
            else:
                self.fail("FAIL: Not all stations increased traffic")
                self.exit_fail()
            try:
                cx_data = self.json_get("/cx/all")
                cx_data.pop("handler")
                cx_data.pop("uri")

                for i in self.created_cx.keys():
                    endp_a_data = self.json_get("/endp/"+ cx_data[i]['endpoints'][0])
                    endp_b_data = self.json_get("/endp/" + cx_data[i]['endpoints'][1])
                    print("cx name:", i, "\n",
                          " bps tx a :", endp_a_data['endpoint']['tx rate'], " --> ",
                          "  bps rx b : ", endp_b_data['endpoint']['rx rate'],
                          "  rx drop % b : ", cx_data[i]['rx drop % b'], "\n"
                          "  tx bytes a : ", endp_a_data['endpoint']['tx bytes'], " --> " 
                          "  rx bytes b", endp_b_data['endpoint']['rx bytes'],  "\n"
                          "  tx bytes b : ", endp_b_data['endpoint']['tx bytes'], " --> " 
                          "  rx bytes a", endp_a_data['endpoint']['rx bytes'], "\n"
                          "  bps tx b :", endp_b_data['endpoint']['tx rate'], " --> "
                          "  bps rx a : ", endp_a_data['endpoint']['rx rate'],
                          "  rx drop % a :", cx_data[i]['rx drop % a'], "\n"
                          "  pkt rx a :", cx_data[i]['pkt rx a'], "  pkt rx b : ", cx_data[i]['pkt rx b'],
                          )
                print("\n\n\n")
            except Exception as e:
                print(e)
            time.sleep(monitor_interval_ms)
        csvfile.close()

        # comparison to last report / report inputted
        if compared_report is not None:
            compared_df = pandas_extensions.compare_two_df(dataframe_one=pandas_extensions.file_to_df(report_file),
                                                           dataframe_two=pandas_extensions.file_to_df(compared_report))
            exit(1)
            # append compared df to created one
            if output_format.lower() != 'csv':
                pandas_extensions.df_to_file(dataframe=pd.read_csv(report_file), output_f=output_format, save_path=report_file)
        else:
            if output_format.lower() != 'csv':
                pandas_extensions.df_to_file(dataframe=pd.read_csv(report_file), output_f=output_format, save_path=report_file)

    def refresh_cx(self):
        for cx_name in self.created_cx.keys():
            self.json_post("/cli-json/show_cxe", {
                "test_mgr": "ALL",
                "cross_connect": cx_name
            }, debug_=self.debug)
            print(".", end='')

    def start_cx(self):
        print("Starting CXs...")
        for cx_name in self.created_cx.keys():
            if self.debug:
                print("cx-name: %s" % (cx_name))
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx_name,
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            if self.debug:
                print(".", end='')
        if self.debug:
            print("")

    def stop_cx(self):
        print("Stopping CXs...")
        for cx_name in self.created_cx.keys():
            self.local_realm.stop_cx(cx_name)
            print(".", end='')
        print("")

    def cleanup_prefix(self):
        self.local_realm.cleanup_cxe_prefix(self.name_prefix)

    def cleanup(self):
        print("Cleaning up cxs and endpoints")
        if len(self.created_cx) != 0:
            for cx_name in self.created_cx.keys():
                if self.debug:
                    print("Cleaning cx: %s" % (cx_name))
                self.local_realm.rm_cx(cx_name)

                for side in range(len(self.created_cx[cx_name])):
                    ename = self.created_cx[cx_name][side]
                    if self.debug:
                        print("Cleaning endpoint: %s" % (ename))
                    self.local_realm.rm_endp(self.created_cx[cx_name][side])

        self.clean_cx_lists()

    def clean_cx_lists(self):
        # Clean out our local lists, this by itself does NOT remove anything from LANforge manager.
        # but, if you are trying to modify existing connections, then clearing these arrays and
        # re-calling 'create' will do the trick.
        self.created_cx.clear()
        self.created_endp.clear()

    def create(self, endp_type, side_a, side_b, sleep_time=0.03, suppress_related_commands=None, debug_=False,
               tos=None):
        if self.debug:
            debug_ = True

        cx_post_data = []
        timer_post_data = []
        these_endp = []
        these_cx = []

        # print(self.side_a_min_rate, self.side_a_max_rate)
        # print(self.side_b_min_rate, self.side_b_max_rate)
        if (self.side_a_min_bps is None) \
                or (self.side_a_max_bps is None) \
                or (self.side_b_min_bps is None) \
                or (self.side_b_max_bps is None):
            raise ValueError(
                "side_a_min_bps, side_a_max_bps, side_b_min_bps, and side_b_max_bps must all be set to a value")

        if type(side_a) == list and type(side_b) != list:
            side_b_info = self.local_realm.name_to_eid(side_b)
            side_b_shelf = side_b_info[0]
            side_b_resource = side_b_info[1]

            for port_name in side_a:
                side_a_info = self.local_realm.name_to_eid(port_name, debug=debug_)
                side_a_shelf = side_a_info[0]
                side_a_resource = side_a_info[1]
                if port_name.find('.') < 0:
                    port_name = "%d.%s" % (side_a_info[1], port_name)

                cx_name = "%s%s-%i" % (self.name_prefix, side_a_info[2], len(self.created_cx))

                endp_a_name = cx_name + "-A"
                endp_b_name = cx_name + "-B"
                self.created_cx[cx_name] = [endp_a_name, endp_b_name]
                self.created_endp[endp_a_name] = endp_a_name
                self.created_endp[endp_b_name] = endp_b_name
                these_cx.append(cx_name)
                these_endp.append(endp_a_name)
                these_endp.append(endp_b_name)
                mconn_b = self.mconn
                if mconn_b > 1:
                    mconn_b = 1
                endp_side_a = {
                    "alias": endp_a_name,
                    "shelf": side_a_shelf,
                    "resource": side_a_resource,
                    "port": side_a_info[2],
                    "type": endp_type,
                    "min_rate": self.side_a_min_bps,
                    "max_rate": self.side_a_max_bps,
                    "min_pkt": self.side_a_min_pdu,
                    "max_pkt": self.side_a_max_pdu,
                    "ip_port": -1,
                    "multi_conn": self.mconn,
                }
                endp_side_b = {
                    "alias": endp_b_name,
                    "shelf": side_b_shelf,
                    "resource": side_b_resource,
                    "port": side_b_info[2],
                    "type": endp_type,
                    "min_rate": self.side_b_min_bps,
                    "max_rate": self.side_b_max_bps,
                    "min_pkt": self.side_b_min_pdu,
                    "max_pkt": self.side_b_max_pdu,
                    "ip_port": -1,
                    "multi_conn": mconn_b,
                }

                # print("1: endp-side-b: ", endp_side_b)

                url = "/cli-json/add_endp"
                self.local_realm.json_post(url, endp_side_a, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                self.local_realm.json_post(url, endp_side_b, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                # print("napping %f sec"%sleep_time)
                time.sleep(sleep_time)

                url = "cli-json/set_endp_flag"
                data = {
                    "name": endp_a_name,
                    "flag": "AutoHelper",
                    "val": 1
                }
                self.local_realm.json_post(url, data, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                data["name"] = endp_b_name
                self.local_realm.json_post(url, data, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)

                if (endp_type == "lf_udp") or (endp_type == "udp") or (endp_type == "lf_udp6") or (endp_type == "udp6"):
                    data["name"] = endp_a_name
                    data["flag"] = "UseAutoNAT"
                    self.local_realm.json_post(url, data, debug_=debug_,
                                               suppress_related_commands_=suppress_related_commands)
                    data["name"] = endp_b_name
                    self.local_realm.json_post(url, data, debug_=debug_,
                                               suppress_related_commands_=suppress_related_commands)

                if tos != None:
                    self.local_realm.set_endp_tos(endp_a_name, tos)
                    self.local_realm.set_endp_tos(endp_b_name, tos)

                data = {
                    "alias": cx_name,
                    "test_mgr": "default_tm",
                    "tx_endp": endp_a_name,
                    "rx_endp": endp_b_name,
                }
                # pprint(data)
                cx_post_data.append(data)
                timer_post_data.append({
                    "test_mgr": "default_tm",
                    "cx_name": cx_name,
                    "milliseconds": self.report_timer
                })

        elif type(side_b) == list and type(side_a) != list:
            side_a_info = self.local_realm.name_to_eid(side_a, debug=debug_)
            side_a_shelf = side_a_info[0]
            side_a_resource = side_a_info[1]
            # side_a_name = side_a_info[2]

            for port_name in side_b:
                print(side_b)
                side_b_info = self.local_realm.name_to_eid(port_name, debug=debug_)
                side_b_shelf = side_b_info[0]
                side_b_resource = side_b_info[1]
                side_b_name = side_b_info[2]

                cx_name = "%s%s-%i" % (self.name_prefix, port_name, len(self.created_cx))
                endp_a_name = cx_name + "-A"
                endp_b_name = cx_name + "-B"
                self.created_cx[cx_name] = [endp_a_name, endp_b_name]
                self.created_endp[endp_a_name] = endp_a_name
                self.created_endp[endp_b_name] = endp_b_name
                these_cx.append(cx_name)
                these_endp.append(endp_a_name)
                these_endp.append(endp_b_name)
                mconn_b = self.mconn
                if mconn_b > 1:
                    mconn_b = 1
                endp_side_a = {
                    "alias": endp_a_name,
                    "shelf": side_a_shelf,
                    "resource": side_a_resource,
                    "port": side_a_info[2],
                    "type": endp_type,
                    "min_rate": self.side_a_min_bps,
                    "max_rate": self.side_a_max_bps,
                    "min_pkt": self.side_a_min_pdu,
                    "max_pkt": self.side_a_max_pdu,
                    "ip_port": -1,
                    "multi_conn": self.mconn,
                }
                endp_side_b = {
                    "alias": endp_b_name,
                    "shelf": side_b_shelf,
                    "resource": side_b_resource,
                    "port": side_b_info[2],
                    "type": endp_type,
                    "min_rate": self.side_b_min_bps,
                    "max_rate": self.side_b_max_bps,
                    "min_pkt": self.side_b_min_pdu,
                    "max_pkt": self.side_b_max_pdu,
                    "ip_port": -1,
                    "multi_conn": mconn_b,
                }

                # print("2: endp-side-b: ", endp_side_b)

                url = "/cli-json/add_endp"
                self.local_realm.json_post(url, endp_side_a, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                self.local_realm.json_post(url, endp_side_b, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                # print("napping %f sec" %sleep_time )
                time.sleep(sleep_time)

                url = "cli-json/set_endp_flag"
                data = {
                    "name": endp_a_name,
                    "flag": "autohelper",
                    "val": 1
                }
                self.local_realm.json_post(url, data, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)

                url = "cli-json/set_endp_flag"
                data = {
                    "name": endp_b_name,
                    "flag": "autohelper",
                    "val": 1
                }
                self.local_realm.json_post(url, data, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                # print("CXNAME451: %s" % cx_name)
                data = {
                    "alias": cx_name,
                    "test_mgr": "default_tm",
                    "tx_endp": endp_a_name,
                    "rx_endp": endp_b_name,
                }
                cx_post_data.append(data)
                timer_post_data.append({
                    "test_mgr": "default_tm",
                    "cx_name": cx_name,
                    "milliseconds": self.report_timer
                })
        else:
            raise ValueError(
                "side_a or side_b must be of type list but not both: side_a is type %s side_b is type %s" % (
                    type(side_a), type(side_b)))
        print("wait_until_endps_appear these_endp: {} debug_ {}".format(these_endp, debug_))
        self.local_realm.wait_until_endps_appear(these_endp, debug=debug_)

        for data in cx_post_data:
            url = "/cli-json/add_cx"
            self.local_realm.json_post(url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands)
            time.sleep(0.01)

        self.local_realm.wait_until_cxs_appear(these_cx, debug=debug_)

        return these_cx, these_endp

    def to_string(self):
        pprint.pprint(self)
