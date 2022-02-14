# !/usr/bin/env python3
import sys
import os
import importlib
import pandas as pd
import time
import datetime
import logging

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
pandas_extensions = importlib.import_module("py-json.LANforge.pandas_extensions")
port_probe = importlib.import_module("py-json.port_probe")
ProbePort = port_probe.ProbePort

logger = logging.getLogger(__name__)


class L3CXProfile(LFCliBase):
    def __init__(self,
                 lfclient_host,
                 lfclient_port,
                 local_realm,
                 side_a_min_bps=256000,
                 side_b_min_bps=256000,
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
        data = dict()
        for cx_name in self.get_cx_names():
            data[cx_name] = self.json_get("/cx/" + cx_name).get(cx_name)
        return data

    def __get_rx_values(self):
        cx_list = self.json_get("endp?fields=name,rx+bytes")
        if self.debug:
            logger.debug(self.created_cx.values())
            logger.debug("==============\n {cx_list}\n==============".format(cx_list=cx_list))
        cx_rx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if value_name == 'rx bytes' and item in self.created_cx.values():
                            cx_rx_map[item] = value_rx
        return cx_rx_map

    @staticmethod
    def __compare_vals(old_list, new_list):
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
                report_file=None,
                systeminfopath=None,
                output_format=None,
                script_name=None,
                arguments=None,
                compared_report=None,
                debug=False):
        if duration_sec:
            duration_sec = self.parse_time(duration_sec).seconds
        else:
            logger.critical("L3CXProfile::monitor wants duration_sec > 1 second")
            raise ValueError("L3CXProfile::monitor wants duration_sec > 1 second")
        if duration_sec <= monitor_interval_ms:
            logger.critical("L3CXProfile::monitor wants duration_sec > monitor_interval")
            raise ValueError("L3CXProfile::monitor wants duration_sec > monitor_interval")
        if report_file is None:
            logger.critical("Monitor requires an output file to be defined")
            raise ValueError("Monitor requires an output file to be defined")
        if systeminfopath is None:
            raise ValueError("Monitor requires a system info path to be defined")
        if created_cx is None:
            logger.critical("Monitor needs a list of Layer 3 connections")
            raise ValueError("Monitor needs a list of Layer 3 connections")
        if (monitor_interval_ms is None) or (monitor_interval_ms < 1):
            logger.critical("L3CXProfile::monitor wants monitor_interval >= 1 second")
            raise ValueError("L3CXProfile::monitor wants monitor_interval >= 1 second")
        if layer3_cols is None:
            logger.critical("L3CXProfile::monitor wants a list of column names to monitor")
            raise ValueError("L3CXProfile::monitor wants a list of column names to monitor")
        if output_format:
            if output_format.lower() != report_file.split('.')[-1]:
                logger.critical('Filename {report_file} has an extension that does not match output format {output_format} '.format(
                    report_file=report_file, output_format=output_format))

                raise ValueError('Filename {report_file} has an extension that does not match output format {output_format} '.format(
                    report_file=report_file, output_format=output_format))
        else:
            output_format = report_file.split('.')[-1]

        # default save to csv first
        if report_file.split('.')[-1] != 'csv':
            report_file = report_file.replace(str(output_format), 'csv', 1)
            logger.info("Saving rolling data into...{report_file}".format(report_file=report_file))

        # ================== Step 1, set column names and header row
        layer3_cols = [self.replace_special_char(x) for x in layer3_cols]
        layer3_fields = ",".join(layer3_cols)
        default_cols = ['Timestamp', 'Timestamp milliseconds epoch', 'Timestamp seconds epoch', 'Duration elapsed']
        default_cols.extend(layer3_cols)
        # append alias to port_mgr_cols if not present needed later
        if port_mgr_cols:
            if 'alias' not in port_mgr_cols:
                port_mgr_cols.append('alias')

        if port_mgr_cols:
            default_cols.extend(port_mgr_cols)
        header_row = default_cols

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

        passes = 0
        expected_passes = 0
        old_cx_rx_values = self.__get_rx_values()

        # wait 10 seconds to get proper port data
        time.sleep(10)

        # for x in range(0,int(round(iterations,0))):
        initial_starttime = datetime.datetime.now()
        timestamp_data = list()
        while datetime.datetime.now() < end_time:
            t = datetime.datetime.now()
            timestamp = t.strftime("%m/%d/%Y %I:%M:%S")
            t_to_millisec_epoch = int(self.get_milliseconds(t))
            t_to_sec_epoch = int(self.get_seconds(t))
            time_elapsed = int(self.get_seconds(t)) - int(self.get_seconds(initial_starttime))
            stations = [station.split('.')[-1] for station in sta_list]
            stations = ','.join(stations)

            if port_mgr_cols:
                port_mgr_response = self.json_get("/port/1/1/%s?fields=%s" % (stations, port_mgr_fields))

            layer_3_response = self.json_get("/endp/%s?fields=%s" % (created_cx, layer3_fields))

            new_cx_rx_values = self.__get_rx_values()
            if debug:
                logger.debug(old_cx_rx_values, new_cx_rx_values)
                logger.debug("\n-----------------------------------")
                logger.debug(t)
                logger.debug("-----------------------------------\n")
            expected_passes += 1
            if self.__compare_vals(old_cx_rx_values, new_cx_rx_values):
                passes += 1
            else:
                # TODO track where this goes?
                self.fail("FAIL: Not all stations increased traffic")

            result = dict()  # create dataframe from layer 3 results
            if type(layer_3_response) is dict:
                for dictionary in layer_3_response['endpoint']:
                    logger.debug('layer_3_data: {dictionary}'.format(dictionary=dictionary))
                    result.update(dictionary)
            else:
                pass
            layer3 = pd.DataFrame(result.values())
            layer3.columns = ['l3-' + x for x in layer3.columns]

            if port_mgr_cols:  # create dataframe from port mgr results
                result = dict()
                if type(port_mgr_response) is dict:
                    logger.info("port_mgr_response {pmr}".format(pmr=port_mgr_response))
                    if 'interfaces' in port_mgr_response:
                        for dictionary in port_mgr_response['interfaces']:
                            if debug:
                                logger.debug('port mgr data: {dictionary}'.format(dictionary=dictionary))
                            result.update(dictionary)

                    elif 'interface' in port_mgr_response:
                        dict_update = {port_mgr_response['interface']['alias']: port_mgr_response['interface']}
                        if debug:
                            logger.debug(dict_update)
                        result.update(dict_update)
                        if debug:
                            logger.debug(result)
                    else:
                        logger.critical('interfaces and interface not in port_mgr_response')
                        raise ValueError('interfaces and interface not in port_mgr_response')
                    portdata_df = pd.DataFrame(result.values())
                    logger.info("portdata_df {pd}".format(pd=portdata_df))
                    portdata_df.columns = ['port-' + x for x in portdata_df.columns]
                    portdata_df['alias'] = portdata_df['port-alias']

                    layer3_alias = list()  # Add alias to layer 3 dataframe
                    for cross_connect in layer3['l3-name']:
                        for port in portdata_df['port-alias']:
                            if port in cross_connect:
                                layer3_alias.append(port)
                    if len(layer3_alias) == layer3.shape[0]:
                        layer3['alias'] = layer3_alias
                    else:
                        logger.critical(("The Stations or Connection on LANforge did not match expected,",
                                        " Check if LANForge initial state correct or delete/cleanup corrects"))
                        raise ValueError(("The Stations or Connection on LANforge did not match expected,",
                                        " Check if LANForge initial state correct or delete/cleanup corrects"))

                    timestamp_df = pd.merge(layer3, portdata_df, on='alias')
            else:
                timestamp_df = layer3
            probe_port_df_list = list()
            for station in sta_list:
                probe_port = ProbePort(lfhost=self.lfclient_host,
                                       lfport=self.lfclient_port,
                                       eid_str=station,
                                       debug=self.debug)
                probe_results = dict()
                probe_port.refreshProbe()
                probe_results['Signal Avg Combined'] = probe_port.getSignalAvgCombined()
                probe_results['Signal Avg per Chain'] = probe_port.getSignalAvgPerChain()
                probe_results['Signal Combined'] = probe_port.getSignalCombined()
                probe_results['Signal per Chain'] = probe_port.getSignalPerChain()
                if 'Beacon Av Signal' in probe_results.keys():
                    probe_results['Beacon Avg Signal'] = probe_port.getBeaconSignalAvg()
                else:
                    probe_results['Beacon Avg Signal'] = "0"
                # probe_results['HE status'] = probe_port.he
                probe_results['TX Bitrate'] = probe_port.tx_bitrate
                probe_results['TX Mbps'] = probe_port.tx_mbit
                probe_results['TX MCS ACTUAL'] = probe_port.tx_mcs
                if probe_port.tx_mcs:
                    probe_results['TX MCS'] = int(probe_port.tx_mcs) % 8
                else:
                    probe_results['TX MCS'] = probe_port.tx_mcs
                probe_results['TX NSS'] = probe_port.tx_nss
                probe_results['TX MHz'] = probe_port.tx_mhz
                if probe_port.tx_gi:
                    probe_results['TX GI ns'] = (probe_port.tx_gi * 10**9)
                else:
                    probe_results['TX GI ns'] = probe_port.tx_gi
                probe_results['TX Mbps Calc'] = probe_port.tx_mbit_calc
                probe_results['TX GI'] = probe_port.tx_gi
                probe_results['TX Mbps short GI'] = probe_port.tx_data_rate_gi_short_Mbps
                probe_results['TX Mbps long GI'] = probe_port.tx_data_rate_gi_long_Mbps
                probe_results['RX Bitrate'] = probe_port.rx_bitrate
                probe_results['RX Mbps'] = probe_port.rx_mbit
                probe_results['RX MCS ACTUAL'] = probe_port.rx_mcs
                if probe_port.rx_mcs:
                    probe_results['RX MCS'] = int(probe_port.rx_mcs) % 8
                else:
                    probe_results['RX MCS'] = probe_port.rx_mcs
                probe_results['RX NSS'] = probe_port.rx_nss
                probe_results['RX MHz'] = probe_port.rx_mhz
                if probe_port.rx_gi:
                    probe_results['RX GI ns'] = (probe_port.rx_gi * 10**9)
                else:
                    probe_results['RX GI ns'] = probe_port.rx_gi
                probe_results['RX Mbps Calc'] = probe_port.rx_mbit_calc
                probe_results['RX GI'] = probe_port.rx_gi
                probe_results['RX Mbps short GI'] = probe_port.rx_data_rate_gi_short_Mbps
                probe_results['RX Mbps long GI'] = probe_port.rx_data_rate_gi_long_Mbps

                probe_df_initial = pd.DataFrame(probe_results.values()).transpose()
                probe_df_initial.columns = probe_results.keys()
                probe_df_initial.columns = ['probe ' + x for x in probe_df_initial.columns]
                probe_df_initial['alias'] = station.split('.')[-1]
                probe_port_df_list.append(probe_df_initial)
            probe_port_df = pd.concat(probe_port_df_list)
            timestamp_df = pd.merge(timestamp_df, probe_port_df, on='alias')
            timestamp_df['Timestamp'] = timestamp
            timestamp_df['Timestamp milliseconds epoch'] = t_to_millisec_epoch
            timestamp_df['Timestamp seconds epoch'] = t_to_sec_epoch
            timestamp_df['Duration elapsed'] = time_elapsed
            timestamp_data.append(timestamp_df)
            time.sleep(monitor_interval_ms)
        df = pd.concat(timestamp_data)
        df = df.drop('alias', axis=1)
        df.to_csv(str(report_file), index=False)

        # comparison to last report / report inputted
        if compared_report:
            pandas_extensions.compare_two_df(dataframe_one=pandas_extensions.file_to_df(report_file),
                                             dataframe_two=pandas_extensions.file_to_df(compared_report))
            # TODO why is this exit here?
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
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')

    def start_cx(self):
        logger.info("Starting CXs...")
        for cx_name in self.created_cx.keys():
            if self.debug:
                logger.debug("cx-name: {cx_name}".format(cx_name=cx_name))
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx_name,
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            # this is for a visual affect someone watching the screen, leave as print
            if self.debug:
                print(".", end='')
        if self.debug:
            print("")

    def stop_cx(self):
        logger.info("Stopping CXs...")
        for cx_name in self.created_cx.keys():
            self.local_realm.stop_cx(cx_name)
            # this is for a visual affect someone watching the screen, leave as print
            print(".", end='')
        print("")

    def cleanup_prefix(self):
        self.local_realm.cleanup_cxe_prefix(self.name_prefix)

    def cleanup(self):
        logger.info("Cleaning up cxs and endpoints")
        if len(self.created_cx) != 0:
            for cx_name in self.created_cx.keys():
                if self.debug:
                    logger.debug("Cleaning cx: {cx_name}".format(cx_name=cx_name))
                self.local_realm.rm_cx(cx_name)

                for side in range(len(self.created_cx[cx_name])):
                    ename = self.created_cx[cx_name][side]
                    if self.debug:
                        logger.debug("Cleaning endpoint: {ename}".format(ename=ename))
                    self.local_realm.rm_endp(self.created_cx[cx_name][side])

        self.clean_cx_lists()

    def clean_cx_lists(self):
        # Clean out our local lists, this by itself does NOT remove anything from LANforge manager.
        # but, if you are trying to modify existing connections, then clearing these arrays and
        # re-calling 'create' will do the trick.
        self.created_cx.clear()
        self.created_endp.clear()

    def create(self, endp_type, side_a, side_b, sleep_time=0.03, suppress_related_commands=None, debug_=False,
               tos=None, timeout=300):
        # Returns a 2-member array, list of cx, list of endp on success.
        # If endpoints creation fails, returns False, False
        # if Endpoints creation is OK, but CX creation fails, returns False, list of endp
        if self.debug:
            debug_ = True
            logger.info('Start L3CXProfile.create')

        cx_post_data = []
        timer_post_data = []
        these_endp = []
        these_cx = []

        if (self.side_a_min_bps is None) \
                or (self.side_a_max_bps is None) \
                or (self.side_b_min_bps is None) \
                or (self.side_b_max_bps is None):
            logger.critical(
                "side_a_min_bps, side_a_max_bps, side_b_min_bps, and side_b_max_bps must all be set to a value")
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

                url = "/cli-json/add_endp"
                self.local_realm.json_post(url, endp_side_a, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                self.local_realm.json_post(url, endp_side_b, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
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

                if tos:
                    self.local_realm.set_endp_tos(endp_a_name, tos)
                    self.local_realm.set_endp_tos(endp_b_name, tos)

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

        elif type(side_b) == list and type(side_a) != list:
            side_a_info = self.local_realm.name_to_eid(side_a, debug=debug_)
            side_a_shelf = side_a_info[0]
            side_a_resource = side_a_info[1]

            for port_name in side_b:
                logger.info(side_b)
                side_b_info = self.local_realm.name_to_eid(port_name, debug=debug_)
                side_b_shelf = side_b_info[0]
                side_b_resource = side_b_info[1]

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

                url = "/cli-json/add_endp"
                self.local_realm.json_post(url, endp_side_a, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
                self.local_realm.json_post(url, endp_side_b, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands)
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
            logger.critical(
                "side_a or side_b must be of type list but not both: side_a is type {side_a} side_b is type {side_b}".format(
                    side_a=type(side_a), side_b=type(side_b)))

            raise ValueError(
                "side_a or side_b must be of type list but not both: side_a is type %s side_b is type %s" % (
                    type(side_a), type(side_b)))
        if debug_:
            logger.debug("wait_until_endps_appear these_endp: {these_endp} debug_ {debug_}".format(
                these_endp=these_endp, debug_=debug_))
        rv = self.local_realm.wait_until_endps_appear(these_endp, debug=debug_, timeout=timeout)
        if not rv:
            logger.error("L3CXProfile::create, Could not create/find endpoints")
            return False, False

        for data in cx_post_data:
            url = "/cli-json/add_cx"
            self.local_realm.json_post(url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands)
            time.sleep(0.01)

        rv = self.local_realm.wait_until_cxs_appear(these_cx, debug=debug_, timeout=timeout)
        if not rv:
            logger.error("L3CXProfile::create, Could not create/find connections.")
            return False, these_endp

        return these_cx, these_endp
