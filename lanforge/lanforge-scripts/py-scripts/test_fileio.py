#!/usr/bin/env python3
"""
NAME: test_fileio.py

PURPOSE:
test_fileio.py will create stations or macvlans with matching fileio endpoints to generate and verify  fileio related traffic.

This script will create a variable number of stations or macvlans to test fileio traffic. Pre-existing stations and
macvlans can be used as well. Command line options are available to update cross-connects as well as using a list of
existing cross-connects if desired. if none are given, cross-connects and endpoints will be created by the script.
Modes such as read-only, write-only, or both can be specified along with ip addresses and starting numbers for sequential
stations or macvlans that are created in case of limited or pre-existing configurations. The test that is run during
this script will depend on the mode used, a read-only test will check the read-bps attribute, write-only will check write-bps
and both will check both attributes. If the relevant attributes increase over the duration of the test it will pass,
otherwise it will fail.

EXAMPLE:
./test_fileio.py --macvlan_parent <port> --num_ports <num ports> --use_macvlans 
                 --first_mvlan_ip <first ip in series> --netmask <netmask to use> --gateway <gateway ip addr>

./test_fileio.py --macvlan_parent eth2 --num_ports 3 --use_macvlans --first_mvlan_ip 192.168.92.13 
                 --netmask 255.255.255.0 --gateway 192.168.92.1


Use './test_fileio.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse
import time
import datetime

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
add_file_endp = importlib.import_module("py-json.LANforge.add_file_endp")
fe_fstype = add_file_endp.fe_fstype
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
lf_report = importlib.import_module("py-scripts.lf_report")


class FileIOTest(Realm):
    def __init__(self, host, port, ssid, security, password,
                 number_template="00000",
                 radio="wiphy0",
                 fs_type=fe_fstype.EP_FE_NFS4.name,
                 min_rw_size=64 * 1024,
                 max_rw_size=64 * 1024,
                 min_file_size=25 * 1024 * 1024,
                 max_file_size=25 * 1024 * 1024,
                 min_read_rate_bps=None,
                 max_read_rate_bps=None,
                 min_write_rate_bps="1G",
                 max_write_rate_bps=None,
                 directory="AUTO",
                 test_duration="5m",
                 upstream_port="eth1",
                 num_ports=1,
                 server_mount="10.40.0.1:/var/tmp/test",
                 macvlan_parent=None,
                 first_mvlan_ip=None,
                 netmask=None,
                 gateway=None,
                 shelf=1,
                 resource=1,
                 dhcp=True,
                 use_macvlans=False,
                 use_test_groups=False,
                 write_only_test_group=None,
                 read_only_test_group=None,
                 port_list=None,
                 ip_list=None,
                 connections_per_port=1,
                 mode="both",
                 update_group_args=None,
                 test_rig=None,
                 test_tag=None,
                 dut_hw_version=None,
                 dut_sw_version=None,
                 dut_model_num=None,
                 dut_serial_num=None,
                 test_id=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        if port_list is None:
            port_list = []
        if update_group_args is None:
            update_group_args = {"name": None, "action": None, "cxs": None}
        self.host = host
        self.port = port
        self.radio = radio
        self.upstream_port = upstream_port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.number_template = number_template
        self.test_duration = test_duration
        self.port_list = []
        self.connections_per_port = connections_per_port
        self.use_macvlans = use_macvlans
        self.mode = mode.lower()
        self.ip_list = ip_list
        self.netmask = netmask
        self.gateway = gateway
        if self.use_macvlans:
            if macvlan_parent:
                self.macvlan_parent = macvlan_parent
                self.port_list = port_list
        else:
            self.port_list = port_list

        self.use_test_groups = use_test_groups
        if self.use_test_groups:
            if self.mode == "write":
                if write_only_test_group:
                    self.write_only_test_group = write_only_test_group
                else:
                    raise ValueError("--write_only_test_group must be used to set test group name")
            if self.mode == "read":
                if read_only_test_group:
                    self.read_only_test_group = read_only_test_group
                else:
                    raise ValueError("--read_only_test_group must be used to set test group name")
            if self.mode == "both":
                if write_only_test_group and read_only_test_group:
                    self.write_only_test_group = write_only_test_group
                    self.read_only_test_group = read_only_test_group
                else:
                    raise ValueError("--write_only_test_group and --read_only_test_group "
                                     "must be used to set test group names")

        self.wo_profile = self.new_fio_endp_profile()
        self.mvlan_profile = self.new_mvlan_profile()

        if not self.use_macvlans and len(self.port_list) > 0:
            self.station_profile = self.new_station_profile()
            self.station_profile.lfclient_url = self.lfclient_url
            self.station_profile.ssid = self.ssid
            self.station_profile.ssid_pass = self.password
            self.station_profile.security = self.security
            self.station_profile.number_template_ = self.number_template
            self.station_profile.mode = 0

        self.wo_profile.fs_type = fs_type
        self.wo_profile.min_rw_size = LFUtils.parse_size(min_rw_size)
        self.wo_profile.max_rw_size = LFUtils.parse_size(max_rw_size)
        self.wo_profile.min_file_size = LFUtils.parse_size(min_file_size)
        self.wo_profile.max_file_size = LFUtils.parse_size(max_file_size)
        self.wo_profile.min_read_rate_bps = LFUtils.parse_size(min_read_rate_bps)
        self.wo_profile.max_read_rate_bps = LFUtils.parse_size(max_read_rate_bps)
        self.wo_profile.min_write_rate_bps = LFUtils.parse_size(min_write_rate_bps)
        self.wo_profile.max_write_rate_bps = LFUtils.parse_size(max_write_rate_bps)
        self.wo_profile.directory = directory
        self.wo_profile.server_mount = server_mount
        self.wo_profile.num_connections_per_port = connections_per_port

        self.ro_profile = self.wo_profile.create_ro_profile()

        if self.use_macvlans:
            self.mvlan_profile.num_macvlans = int(num_ports)
            self.mvlan_profile.desired_macvlans = self.port_list
            self.mvlan_profile.macvlan_parent = self.macvlan_parent
            self.mvlan_profile.dhcp = dhcp
            self.mvlan_profile.netmask = netmask
            self.mvlan_profile.first_ip_addr = first_mvlan_ip
            self.mvlan_profile.gateway = gateway
            self.mvlan_profile.shelf = shelf
            self.mvlan_profile.resource = resource

        self.created_ports = []
        if self.use_test_groups:
            if self.mode:
                if self.mode == "write":
                    self.wo_tg_profile = self.new_test_group_profile()
                    self.wo_tg_profile.group_name = self.write_only_test_group
                elif self.mode == "read":
                    self.ro_tg_profile = self.new_test_group_profile()
                    self.ro_tg_profile.group_name = self.read_only_test_group
                elif self.mode == "both":
                    self.wo_tg_profile = self.new_test_group_profile()
                    self.ro_tg_profile = self.new_test_group_profile()
                    self.wo_tg_profile.group_name = self.write_only_test_group
                    self.ro_tg_profile.group_name = self.read_only_test_group
                else:
                    raise ValueError("Unknown mode given ", self.mode)
            else:
                raise ValueError("Mode ( read, write, or both ) must be specified")

        if update_group_args and update_group_args['name']:
            temp_tg = self.new_test_group_profile()
            temp_cxs = update_group_args['cxs'].split(',')
            if update_group_args['action'] == "add":
                temp_tg.group_name = update_group_args['name']
                if not temp_tg.check_group_exists():
                    temp_tg.create_group()
                for cx in temp_cxs:
                    if "CX_" not in cx:
                        cx = "CX_" + cx
                    temp_tg.add_cx(cx)
            if update_group_args['action'] == "del":
                temp_tg.group_name = update_group_args['name']
                if temp_tg.check_group_exists():
                    for cx in temp_cxs:
                        temp_tg.rm_cx(cx)
            time.sleep(5)

        self.wo_tg_exists = False
        self.ro_tg_exists = False
        self.wo_tg_cx_exists = False
        self.ro_tg_cx_exists = False
        print("Checking for pre-existing test groups and cxs")
        if self.use_test_groups:
            if self.mode == "write":
                if self.wo_tg_profile.check_group_exists():
                    self.wo_tg_exists = True
                    if len(self.wo_tg_profile.list_cxs()) > 0:
                        self.wo_tg_cx_exists = True
            elif self.mode == "read":
                if self.ro_tg_profile.check_group_exists():
                    self.ro_tg_exists = True
                    if len(self.ro_tg_profile.list_cxs()) > 0:
                        self.ro_tg_cx_exists = True
            elif self.mode == "both":
                if self.wo_tg_profile.check_group_exists():
                    self.wo_tg_exists = True
                    if len(self.wo_tg_profile.list_cxs()) > 0:
                        self.wo_tg_cx_exists = True
                if self.ro_tg_profile.check_group_exists():
                    self.ro_tg_exists = True
                    if len(self.ro_tg_profile.list_cxs()) > 0:
                        self.ro_tg_cx_exists = True

        self.report = lf_report.lf_report(_results_dir_name="test_l4", _output_html="ftp_test.html", _output_pdf="ftp_test.pdf")

        kpi_path = self.report.get_report_path()
        self.kpi_csv = lf_kpi_csv.lf_kpi_csv(
            _kpi_path=kpi_path,
            _kpi_test_rig=test_rig,
            _kpi_test_tag=test_tag,
            _kpi_dut_hw_version=dut_hw_version,
            _kpi_dut_sw_version=dut_sw_version,
            _kpi_dut_model_num=dut_model_num,
            _kpi_dut_serial_num=dut_serial_num,
            _kpi_test_id=test_id)

    def __compare_vals(self, val_list):
        passes = 0
        expected_passes = 0
        for item in val_list:
            expected_passes += 1
            if val_list[item]['read-bps'] + val_list[item]['write-bps'] > 0:
                if item[0] == 'r':
                    if int(val_list[item]['read-bps']) > int(self.wo_profile.min_read_rate_bps):
                        print('%s Pass: %s' % (item, val_list[item]))
                        passes += 1
                    else:
                        print('%s Fail: %s' % (item, val_list[item]))
                        print(int(val_list[item]['read-bps']) / int(self.wo_profile.min_read_rate_bps))
                if item[0] == 'w':
                    if int(val_list[item]['write-bps']) > int(self.wo_profile.min_write_rate_bps):
                        print('%s Pass: %s' % (item, val_list[item]))
                        passes += 1
                    else:
                        print('%s Fail: %s' % (item, val_list[item]))
                        print(int(val_list[item]['write-bps']) / int(self.wo_profile.min_write_rate_bps))
            else:
                return True
        if passes == expected_passes:
            return True
        else:
            if self.debug:
                print('passes: %s, expected passes: %s' % (passes, expected_passes))
                print('FAIL')
                print(val_list)
                print(self.wo_profile.min_read_rate_bps)
                print(self.wo_profile.min_write_rate_bps)
            return False

    def __get_values(self):
        time.sleep(3)
        if self.mode == "write":
            cx_list = self.json_get("fileio/%s?fields=write-bps" % (
                ','.join(self.wo_profile.created_cx.keys())), debug_=self.debug)
        elif self.mode == "read":
            cx_list = self.json_get("fileio/%s?fields=read-bps" % (
                ','.join(self.ro_profile.created_cx.keys())), debug_=self.debug)
        else:
            cx_list = self.json_get("fileio/%s,%s?fields=write-bps,read-bps" % (
                ','.join(self.wo_profile.created_cx.keys()),
                ','.join(self.ro_profile.created_cx.keys())), debug_=self.debug)
        cx_map = {}
        if cx_list:
            cx_list = cx_list['endpoint']
            for i in cx_list:
                for item, value in i.items():
                    cx_map[self.name_to_eid(item)[2]] = {"read-bps": value['read-bps'],
                                                         "write-bps": value['write-bps']}
        return cx_map

    def build(self):
        # Build stations
        if self.use_macvlans:
            self.mvlan_profile.create(admin_down=False, sleep_time=.5, debug=self.debug)
            self._pass("PASS: MACVLAN build finished")
            self.created_ports += self.mvlan_profile.created_macvlans
        elif not self.use_macvlans and self.ip_list is None:
            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template(self.number_template)
            print("Creating stations")
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=self.radio, sta_names_=self.port_list, debug=self.debug)
            self._pass("PASS: Station build finished")
            self.created_ports += self.station_profile.station_names

        if len(self.ip_list) > 0:
            for num_port in range(len(self.port_list)):
                if self.ip_list[num_port] != 0:
                    if self.gateway and self.netmask:
                        shelf = self.name_to_eid(self.port_list[num_port])[0]
                        resource = self.name_to_eid(self.port_list[num_port])[1]
                        port = self.name_to_eid(self.port_list[num_port])[2]
                        req_url = "/cli-json/set_port"
                        data = {
                            "shelf": shelf,
                            "resource": resource,
                            "port": port,
                            "ip_addr": self.ip_list[num_port],
                            "netmask": self.netmask,
                            "gateway": self.gateway
                        }
                        self.json_post(req_url, data)
                        self.created_ports.append("%s.%s.%s" % (shelf, resource, port))
                    else:
                        raise ValueError("Netmask and gateway must be specified")

        # if use test groups and test group do not exist, create cxs, create test group, assign to test group
        # if use test groups and test group exist and no cxs, create cxs, assign to test group
        # if use test groups and test group exist and cxs exist, do nothing
        # if not use test groups, create cxs
        if self.mode:
            if self.use_test_groups:
                if self.mode == "write":
                    if self.wo_tg_exists and not self.wo_tg_cx_exists:
                        print("Creating Write Only CXs")
                        self.wo_profile.create(ports=self.created_ports,
                                               connections_per_port=self.connections_per_port,
                                               sleep_time=.5, debug_=self.debug,
                                               suppress_related_commands_=None)
                        time.sleep(1)
                        print("Adding cxs to %s" % self.wo_tg_profile.group_name)
                        for cx in self.wo_profile.created_cx.values():
                            self.wo_tg_profile.add_cx(cx)
                    else:
                        print("Creating Write Only CXs")
                        self.wo_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                               sleep_time=.5, debug_=self.debug,
                                               suppress_related_commands_=None)
                        time.sleep(1)
                        print("Creating Write Only test group")
                        self.wo_tg_profile.create_group()
                        print("Adding cxs to %s" % self.wo_tg_profile.group_name)
                        for cx in self.wo_profile.created_cx.values():
                            self.wo_tg_profile.add_cx(cx)
                elif self.mode == "read":
                    if self.ro_tg_exists:
                        if not self.ro_tg_cx_exists:
                            print("Creating Read Only CXs")
                            self.ro_profile.create(ports=self.created_ports,
                                                   connections_per_port=self.connections_per_port,
                                                   sleep_time=.5, debug_=self.debug,
                                                   suppress_related_commands_=None)
                            time.sleep(1)
                            print("Adding cxs to %s" % self.ro_tg_profile.group_name)
                            for cx in self.ro_profile.created_cx.values():
                                self.ro_tg_profile.add_cx(cx)
                    else:
                        print("Creating Read Only CXs")
                        self.ro_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                               sleep_time=.5, debug_=self.debug,
                                               suppress_related_commands_=None)
                        time.sleep(1)
                        print("Creating Read Only test group")
                        self.ro_tg_profile.create_group()
                        print("Adding cxs to %s" % self.ro_tg_profile.group_name)
                        for cx in self.ro_profile.created_cx.values():
                            self.ro_tg_profile.add_cx(cx)
                elif self.mode == "both":
                    if self.wo_tg_exists:
                        if not self.wo_tg_cx_exists:
                            print("Creating Write Only CXs")
                            self.wo_profile.create(ports=self.created_ports,
                                                   connections_per_port=self.connections_per_port,
                                                   sleep_time=.5, debug_=self.debug,
                                                   suppress_related_commands_=None)
                            time.sleep(1)
                            print("Adding cxs to %s" % self.wo_tg_profile.group_name)
                            for cx in self.wo_profile.created_cx.values():
                                self.wo_tg_profile.add_cx(cx)
                    else:
                        print("Creating Write Only CXs")
                        self.wo_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                               sleep_time=.5, debug_=self.debug,
                                               suppress_related_commands_=None)
                        time.sleep(1)
                        print("Creating Write Only test group")
                        self.wo_tg_profile.create_group()
                        print("Adding cxs to %s" % self.wo_tg_profile.group_name)
                        for cx in self.wo_profile.created_cx.values():
                            self.wo_tg_profile.add_cx(cx)
                    if self.ro_tg_exists:
                        if not self.ro_tg_cx_exists:
                            print("Creating Read Only CXs")
                            self.ro_profile.create(ports=self.created_ports,
                                                   connections_per_port=self.connections_per_port,
                                                   sleep_time=.5, debug_=self.debug,
                                                   suppress_related_commands_=None)
                            time.sleep(1)
                            print("Adding cxs to %s" % self.ro_tg_profile.group_name)
                            for cx in self.ro_profile.created_cx.values():
                                self.ro_tg_profile.add_cx(cx)
                    else:
                        print("Creating Read Only CXs")
                        self.ro_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                               sleep_time=.5, debug_=self.debug,
                                               suppress_related_commands_=None)
                        time.sleep(1)
                        print("Creating Read Only test group")
                        self.ro_tg_profile.create_group()
                        print("Adding cxs to %s" % self.ro_tg_profile.group_name)
                        for cx in self.ro_profile.created_cx.values():
                            self.ro_tg_profile.add_cx(cx)
                else:
                    raise ValueError("Unknown mode used, must be (read, write, both)")
            else:
                if self.mode == "write":
                    print("Creating Write Only CXs")
                    self.wo_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                           sleep_time=.5, debug_=self.debug,
                                           suppress_related_commands_=None)
                elif self.mode == "read":
                    print("Creating Read Only CXs")
                    self.ro_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                           sleep_time=.5, debug_=self.debug,
                                           suppress_related_commands_=None)
                elif self.mode == "both":
                    print("Creating Write Only CXs")
                    self.wo_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                           sleep_time=.5, debug_=self.debug,
                                           suppress_related_commands_=None)
                    print("Creating Read Only CXs")
                    self.ro_profile.create(ports=self.created_ports, connections_per_port=self.connections_per_port,
                                           sleep_time=.5, debug_=self.debug,
                                           suppress_related_commands_=None)
                else:
                    raise ValueError("Unknown mode used, must be (read, write, both)")
        else:
            raise ValueError("Mode must be set (read, write, both)")

    def start(self, print_pass=False, print_fail=False):
        temp_ports = self.created_ports.copy()
        if not self.use_macvlans:
            self.station_profile.admin_up()
        else:
            self.mvlan_profile.admin_up()
        if self.wait_for_ip(temp_ports, debug=self.debug):
            self._pass("All ports got IPs", print_pass)
        else:
            self._fail("Ports failed to get IPs", print_fail)
        cur_time = datetime.datetime.now()
        # print("Got Values")
        end_time = self.parse_time(self.test_duration) + cur_time
        if self.use_test_groups:
            if self.mode == "write":
                self.wo_tg_profile.start_group()
            elif self.mode == "read":
                self.ro_tg_profile.start_group()
            else:
                self.wo_tg_profile.start_group()
                time.sleep(2)
                self.ro_tg_profile.start_group()
        else:
            if self.mode == "write":
                self.wo_profile.start_cx()
            elif self.mode == "read":
                self.ro_profile.start_cx()
            else:
                self.wo_profile.start_cx()
                time.sleep(2)
                self.ro_profile.start_cx()

        passes = 0
        expected_passes = 0
        print("Starting Test...")
        write_bps = 0
        read_bps = 0
        while cur_time < end_time:
            write_bps = 0
            read_bps = 0
            interval_time = cur_time + datetime.timedelta(seconds=1)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                time.sleep(1)
            new_rx_values = self.__get_values()
            for key, value in new_rx_values.items():
                write_bps += value['write-bps']
                read_bps += value['read-bps']

            expected_passes += 1
            if self.__compare_vals(new_rx_values):
                passes += 1
            else:
                self._fail("FAIL: Not all stations increased traffic", print_fail)
                # break
            # old_rx_values = new_rx_values
            cur_time = datetime.datetime.now()


        self.kpi_csv.kpi_csv_get_dict_update_time()
        self.kpi_csv.kpi_dict['Graph-Group'] = 'Total write BPS'
        self.kpi_csv.kpi_dict['short-description'] = "write-bps %s" % self.wo_profile.fs_type
        self.kpi_csv.kpi_dict['numeric-score'] = write_bps
        self.kpi_csv.kpi_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(self.kpi_csv.kpi_dict)

        self.kpi_csv.kpi_csv_get_dict_update_time()
        self.kpi_csv.kpi_dict['Graph-Group'] = 'Total read BPS'
        self.kpi_csv.kpi_dict['short-description'] = "read-bps %s" % self.wo_profile.fs_type
        self.kpi_csv.kpi_dict['numeric-score'] = read_bps
        self.kpi_csv.kpi_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(self.kpi_csv.kpi_dict)

        if passes == expected_passes:
            self._pass("PASS: All tests passes", print_pass)

    def stop(self):
        if self.use_test_groups:
            if self.mode == "write":
                self.wo_tg_profile.stop_group()
            elif self.mode == "read":
                self.ro_tg_profile.stop_group()
            else:
                self.wo_tg_profile.stop_group()
                time.sleep(2)
                self.ro_tg_profile.stop_group()
        else:
            if self.mode == "write":
                self.wo_profile.stop_cx()
            elif self.mode == "read":
                self.ro_profile.stop_cx()
            else:
                self.wo_profile.stop_cx()
                time.sleep(2)
                self.ro_profile.stop_cx()

        if not self.use_macvlans:
            self.station_profile.admin_down()
        else:
            self.mvlan_profile.admin_down()

    def cleanup(self, port_list=None):
        if self.use_test_groups:
            if self.mode == "read":
                if not self.ro_tg_exists:
                    if self.ro_tg_profile.check_group_exists():
                        self.ro_tg_profile.rm_group()
                if not self.ro_tg_cx_exists:
                    self.ro_profile.cleanup()

            elif self.mode == "write":
                if not self.wo_tg_exists:
                    if self.wo_tg_profile.check_group_exists():
                        self.wo_tg_profile.rm_group()
                if not self.wo_tg_cx_exists:
                    self.wo_profile.cleanup()

            elif self.mode == "both":
                if not self.ro_tg_exists:
                    if self.ro_tg_profile.check_group_exists():
                        self.ro_tg_profile.rm_group()
                if not self.ro_tg_cx_exists:
                    self.ro_profile.cleanup()

                if not self.wo_tg_exists:
                    if self.wo_tg_profile.check_group_exists():
                        self.wo_tg_profile.rm_group()
                if not self.wo_tg_cx_exists:
                    self.wo_profile.cleanup()
        else:
            if self.mode == "read":
                self.ro_profile.cleanup()
            elif self.mode == "write":
                self.wo_profile.cleanup()
            elif self.mode == "both":
                self.ro_profile.cleanup()
                self.wo_profile.cleanup()

        if not self.use_macvlans and self.ip_list is None:
            self.station_profile.cleanup(port_list)
        elif self.use_macvlans:
            self.mvlan_profile.cleanup()

        # LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=port_list, debug=self.debug)


def main():
    parser = Realm.create_bare_argparse(
        prog='test_fileio.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Creates FileIO endpoints which can be NFS, CIFS or iSCSI endpoints.''',

        description='''\
test_fileio.py:
--------------------
Generic command layout:
./test_fileio.py --macvlan_parent <port> --num_ports <num ports> --use_macvlans 
                 --first_mvlan_ip <first ip in series> --netmask <netmask to use> --gateway <gateway ip addr>

./test_fileio.py --macvlan_parent eth2 --num_ports 3 --use_macvlans --first_mvlan_ip 192.168.92.13 
                 --netmask 255.255.255.0 --gateway 192.168.92.1
                 
./test_fileio.py --radio 1.wiphy0 --test_duration 1m --macvlan_parent eth1 --num_ports 3 --use_macvlans  
                 --use_ports eth1#0,eth1#1,eth1#2 --connections_per_port 2 --mode write
                 
./test_fileio.py --radio 1.wiphy0 --test_duration 1m --macvlan_parent eth1 --num_ports 3 --use_macvlans  
                 --first_mvlan_ip 10.40.3.100 --netmask 255.255.240.0 --gateway 10.40.0.1  
                 --use_test_groups --write_only_test_group test_wo --read_only_test_group test_ro 
                 --add_to_group test_wo --cxs test_wo0000,test_wo0001,test_wo0002

./test_fileio.py --radio 1.wiphy0 --test_duration 1m --macvlan_parent eth1 --num_ports 3 --use_macvlans
                 --use_ports eth1#0=10.40.3.103,eth1#1,eth1#2 --connections_per_port 2 
                 --netmask 255.255.240.0 --gateway 10.40.0.1

''')
    parser.add_argument('--num_stations', help='Number of stations to create', default=0)
    parser.add_argument('--radio', help='radio EID, e.g: 1.wiphy2')
    parser.add_argument('--ssid', help='SSID for stations to associate to')
    parser.add_argument('--passwd', '--password', '--key', help='WiFi passphrase/password/key')
    parser.add_argument('--security', help='security type to use for ssid { wep | wpa | wpa2 | wpa3 | open }')
    parser.add_argument('-u', '--upstream_port',
                        help='non-station port that generates traffic: <resource>.<port>, e.g: 1.eth1',
                        default='1.eth1')
    parser.add_argument('--test_duration', help='sets the duration of the test', default="5m")
    parser.add_argument('--fs_type', help='endpoint type', default="fe_nfs4")
    parser.add_argument('--min_rw_size', help='minimum read/write size', default=64 * 1024)
    parser.add_argument('--max_rw_size', help='maximum read/write size', default=64 * 1024)
    parser.add_argument('--min_file_size', help='minimum file size', default=50 * 1024 * 1024)
    parser.add_argument('--max_file_size', help='maximum file size', default=50 * 1024 * 1024)
    parser.add_argument('--min_read_rate_bps', help='minimum bps read rate', default=10e6)
    parser.add_argument('--max_read_rate_bps', help='maximum bps read rate', default=10e6)
    parser.add_argument('--min_write_rate_bps', help='minimum bps write rate', default=10e6)
    parser.add_argument('--max_write_rate_bps', help='maximum bps write rate', default="1G")
    parser.add_argument('--directory', help='--directory directory to read/write in. Absolute path suggested',
                        default="AUTO")
    parser.add_argument('--server_mount', help='--server_mount The server to mount, ex: 192.168.100.5/exports/test1',
                        default="10.40.0.1:/var/tmp/test")

    parser.add_argument('--macvlan_parent', help='specifies parent port for macvlan creation', default=None)
    parser.add_argument('--first_port', help='specifies name of first port to be used', default=None)
    parser.add_argument('--num_ports', help='number of ports to create', default=1)
    parser.add_argument('--connections_per_port', help='specifies number of connections to be used per port', default=1,
                        type=int)
    parser.add_argument('--use_ports', help='list of comma separated ports to use with ips, \'=\' separates name and ip'
                                            '{ port_name1=ip_addr1,port_name1=ip_addr2 }. '
                                            'Ports without ips will be left alone', default=None)
    parser.add_argument('--use_macvlans', help='will create macvlans', action='store_true', default=False)
    parser.add_argument('--first_mvlan_ip', help='specifies first static ip address to be used or dhcp', default=None)
    parser.add_argument('--netmask', help='specifies netmask to be used with static ip addresses', default=None)
    parser.add_argument('--gateway', help='specifies default gateway to be used with static addressing', default=None)
    parser.add_argument('--use_test_groups', help='will use test groups to start/stop instead of single endps/cxs',
                        action='store_true', default=False)
    parser.add_argument('--read_only_test_group', help='specifies name to use for read only test group', default=None)
    parser.add_argument('--write_only_test_group', help='specifies name to use for write only test group', default=None)
    parser.add_argument('--mode', help='write,read,both', default='both', type=str)
    # kpi_csv arguments
    parser.add_argument(
        "--test_rig",
        default="",
        help="test rig for kpi.csv, testbed that the tests are run on")
    parser.add_argument(
        "--test_tag",
        default="",
        help="test tag for kpi.csv,  test specific information to differentiate the test")
    parser.add_argument(
        "--dut_hw_version",
        default="",
        help="dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument(
        "--dut_sw_version",
        default="",
        help="dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument(
        "--dut_model_num",
        default="",
        help="dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument(
        "--dut_serial_num",
        default="",
        help="dut serial for kpi.csv, serial number / serial number of the device under test")
    parser.add_argument(
        "--test_priority",
        default="",
        help="dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument(
        '--csv_outfile',
        help="--csv_outfile <Output file for csv data>",
        default="")
    tg_group = parser.add_mutually_exclusive_group()
    tg_group.add_argument('--add_to_group', help='name of test group to add cxs to', default=None)
    tg_group.add_argument('--del_from_group', help='name of test group to delete cxs from', default=None)
    parser.add_argument('--cxs',
                        help='list of cxs to add/remove depending on use of --add_to_group or --del_from_group',
                        default=None)
    args = parser.parse_args()

    parent = LFUtils.name_to_eid(args.macvlan_parent)
    shelf = parent[0]
    resource = parent[1]
    macvlan_parent = parent[2]
    update_group_args = {
        "name": None,
        "action": None,
        "cxs": None
    }
    if args.add_to_group and args.cxs:
        update_group_args['name'] = args.add_to_group
        update_group_args['action'] = "add"
        update_group_args['cxs'] = args.cxs
    elif args.del_from_group and args.cxs:
        update_group_args['name'] = args.del_from_group
        update_group_args['action'] = "del"
        update_group_args['cxs'] = args.cxs

    port_list = []
    ip_list = []
    if args.first_port and args.use_ports:
        if args.first_port.startswith("sta"):
            if args.num_ports and (int(args.num_ports) > 0):
                start_num = int(args.first_port[3:])
                num_ports = int(args.num_ports)
                port_list = LFUtils.port_name_series(prefix="sta", start_id=start_num, end_id=start_num + num_ports - 1,
                                                     padding_number=10000,
                                                     radio=args.radio)
        else:
            if args.num_ports and macvlan_parent and (int(args.num_ports) > 0) \
                    and macvlan_parent in args.first_port:
                start_num = int(args.first_port[args.first_port.index('#') + 1:])
                num_ports = int(args.num_ports)
                port_list = LFUtils.port_name_series(prefix=macvlan_parent + "#", start_id=start_num,
                                                     end_id=start_num + num_ports - 1, padding_number=100000,
                                                     radio=args.radio)
            else:
                raise ValueError("Invalid values for num_ports [%s], macvlan_parent [%s], and/or first_port [%s].\n"
                                 "first_port must contain parent port and num_ports must be greater than 0"
                                 % (args.num_ports, macvlan_parent, args.first_port))
    else:
        if args.use_ports is None:
            num_ports = int(args.num_ports)
            if not args.use_macvlans:
                port_list = LFUtils.port_name_series(prefix="sta", start_id=0, end_id=num_ports - 1,
                                                     padding_number=10000,
                                                     radio=args.radio)
            else:
                port_list = LFUtils.port_name_series(prefix=macvlan_parent + "#", start_id=0,
                                                     end_id=num_ports - 1, padding_number=100000,
                                                     radio=args.radio)
        else:
            temp_list = args.use_ports.split(',')
            for port in temp_list:
                port_list.append(port.split('=')[0])
                if '=' in port:
                    ip_list.append(port.split('=')[1])
                else:
                    ip_list.append(0)

            if len(port_list) != len(ip_list):
                raise ValueError(temp_list, " ports must have matching ip addresses!")

    if args.first_mvlan_ip:
        if args.first_mvlan_ip.lower() == "dhcp":
            dhcp = True
        else:
            dhcp = False
    else:
        dhcp = True
    if 'nfs' in args.fs_type:
        if len(os.popen('mount -l | grep nfs').read()) > 0:
            print('Success')
        else:
            raise ValueError("No nfs share is mounted")
    else:
        exit(1)

    ip_test = FileIOTest(args.mgr,
                         args.mgr_port,
                         ssid=args.ssid,
                         password=args.passwd,
                         security=args.security,
                         port_list=port_list,
                         ip_list=ip_list,
                         test_duration=args.test_duration,
                         upstream_port=args.upstream_port,
                         _debug_on=args.debug,
                         macvlan_parent=macvlan_parent,
                         use_macvlans=args.use_macvlans,
                         first_mvlan_ip=args.first_mvlan_ip,
                         netmask=args.netmask,
                         gateway=args.gateway,
                         shelf=shelf,
                         resource=resource,
                         dhcp=dhcp,
                         fs_type=args.fs_type,
                         min_rw_size=args.min_rw_size,
                         max_rw_size=args.max_rw_size,
                         min_file_size=args.min_file_size,
                         max_file_size=args.max_file_size,
                         min_read_rate_bps=args.min_read_rate_bps,
                         max_read_rate_bps=args.max_read_rate_bps,
                         min_write_rate_bps=args.min_write_rate_bps,
                         max_write_rate_bps=args.max_write_rate_bps,
                         directory=args.directory,
                         server_mount=args.server_mount,
                         num_ports=args.num_ports,
                         use_test_groups=args.use_test_groups,
                         write_only_test_group=args.write_only_test_group,
                         read_only_test_group=args.read_only_test_group,
                         update_group_args=update_group_args,
                         connections_per_port=args.connections_per_port,
                         mode=args.mode
                         # want a mount options param
                         )

    ip_test.cleanup(port_list)
    ip_test.build()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
    ip_test.start(False, False)
    ip_test.stop()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
        # exit(1)
    time.sleep(30)
    ip_test.cleanup(port_list)
    if ip_test.passes():
        print("Full test passed, all endpoints had increased bytes-rd throughout test duration")


if __name__ == "__main__":
    main()
