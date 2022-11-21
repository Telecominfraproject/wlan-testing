#!/usr/bin/env python3
# Class: FIOEndpProfile(LFCliBase)

# Written by Candela Technologies Inc.
#  Updated by:
import sys
import os
import importlib
import time
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase

logger = logging.getLogger(__name__)


class FIOEndpProfile(LFCliBase):
    """
    Very often you will create the FileIO writer profile first so that it creates the data
    that a reader profile will subsequently use.
    """

    def __init__(self, lfclient_host, lfclient_port, local_realm, io_direction="write", debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.local_realm = local_realm
        self.fs_type = "fe_nfsv4"
        self.min_rw_size = 128 * 1024
        self.max_rw_size = 128 * 1024
        self.min_file_size = 10 * 1024 * 1024
        self.max_file_size = 10 * 1024 * 1024

        self.min_read_rate_bps = 10 * 1000 * 1000
        self.max_read_rate_bps = 10 * 1000 * 1000
        self.min_write_rate_bps = 1000 * 1000 * 1000
        self.max_write_rate_bps = 1000 * 1000 * 1000

        self.file_num = 10  # number of files to write
        self.directory = None  # directory like /mnt/lf/$endp_name

        # this refers to locally mounted directories presently used for writing
        # you would set this when doing read tests simultaneously to write tests
        # so like, if your endpoint names are like wo_300GB_001, your Directory value
        # defaults to /mnt/lf/wo_300GB_001; but reader enpoint would be named
        # /mnt/lf/ro_300GB_001, this overwrites a readers directory name to wo_300GB_001
        self.mount_dir = "AUTO"

        self.server_mount = None  # like cifs://10.0.0.1/bashful or 192.168.1.1:/var/tmp
        self.mount_options = None
        self.iscsi_vol = None
        self.retry_timer_ms = 2000
        self.io_direction = io_direction  # read / write
        self.quiesce_ms = 3000
        self.pattern = "increasing"
        self.file_prefix = "AUTO"  # defaults to endp_name
        self.cx_prefix = "wo_"

        self.created_cx = {}
        self.created_endp = []

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

    def create_ro_profile(self):
        ro_profile = self.local_realm.new_fio_endp_profile()
        ro_profile.realm = self.local_realm

        ro_profile.fs_type = self.fs_type
        ro_profile.min_read_rate_bps = self.min_write_rate_bps
        ro_profile.max_read_rate_bps = self.max_write_rate_bps
        ro_profile.min_write_rate_bps = self.min_read_rate_bps
        ro_profile.max_write_rate_bps = self.max_read_rate_bps
        ro_profile.file_num = self.file_num
        ro_profile.directory = self.directory
        ro_profile.mount_dir = self.directory
        ro_profile.server_mount = self.server_mount
        ro_profile.mount_options = self.mount_options
        ro_profile.iscsi_vol = self.iscsi_vol
        ro_profile.retry_timer_ms = self.retry_timer_ms
        ro_profile.io_direction = "read"
        ro_profile.quiesce_ms = self.quiesce_ms
        ro_profile.pattern = self.pattern
        ro_profile.file_prefix = self.file_prefix
        ro_profile.cx_prefix = "ro_"
        return ro_profile

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
                # pprint(data)
                req_url = "cli-json/rm_endp"
                data = {
                    "endp_name": cx_name
                }
                self.json_post(req_url, data)
                # pprint(data)

    def create(self, ports=None, connections_per_port=1, sleep_time=.5, debug_=False, suppress_related_commands_=None):
        if ports is None:
            ports = []
        cx_post_data = []
        for port_name in ports:
            for num_connection in range(connections_per_port):
                # 
                if len(self.local_realm.name_to_eid(port_name)) >= 3:
                    shelf = self.local_realm.name_to_eid(port_name)[0]
                    resource = self.local_realm.name_to_eid(port_name)[1]
                    name = self.local_realm.name_to_eid(port_name)[2]
                else:
                    logger.critical("Unexpected name for port_name %s" % port_name)
                    raise ValueError("Unexpected name for port_name %s" % port_name)
                if self.directory is None or self.server_mount is None or self.fs_type is None:
                    logger.critical("directory [%s], server_mount [%s], and type [%s] must not be None" % (
                        self.directory, self.server_mount, self.fs_type))
                    raise ValueError("directory [%s], server_mount [%s], and type [%s] must not be None" % (
                        self.directory, self.server_mount, self.fs_type))
                endp_data = {
                    "alias": self.cx_prefix + name + "_" + str(num_connection) + "_fio",
                    "shelf": shelf,
                    "resource": resource,
                    "port": name,
                    "type": self.fs_type,
                    "min_read_rate": self.min_read_rate_bps,
                    "max_read_rate": self.max_read_rate_bps,
                    "min_write_rate": self.min_write_rate_bps,
                    "max_write_rate": self.max_write_rate_bps,
                    "directory": self.directory,
                    "server_mount": self.server_mount,
                    "mount_dir": self.mount_dir,
                    "prefix": self.file_prefix,
                    "payload_pattern": self.pattern,

                }
                # Read direction is copy of write only directory
                if self.io_direction == "read":
                    endp_data["prefix"] = "wo_" + name + "_" + str(num_connection) + "_fio"
                    endp_data["directory"] = "/mnt/lf/wo_" + name + "_" + str(num_connection) + "_fio"

                url = "cli-json/add_file_endp"
                self.local_realm.json_post(url, endp_data, debug_=False,
                                           suppress_related_commands_=suppress_related_commands_)
                time.sleep(sleep_time)

                data = {
                    "name": self.cx_prefix + name + "_" + str(num_connection) + "_fio",
                    "io_direction": self.io_direction,
                    "num_files": 5
                }
                self.local_realm.json_post("cli-json/set_fe_info", data, debug_=debug_,
                                           suppress_related_commands_=suppress_related_commands_)

        self.local_realm.json_post("/cli-json/nc_show_endpoints", {"endpoint": "all"})
        for port_name in ports:
            for num_connection in range(connections_per_port):
                name = self.local_realm.name_to_eid(port_name)[2]

                endp_data = {
                    "alias": "CX_" + self.cx_prefix + name + "_" + str(num_connection) + "_fio",
                    "test_mgr": "default_tm",
                    "tx_endp": self.cx_prefix + name + "_" + str(num_connection) + "_fio",
                    "rx_endp": "NA"
                }
                cx_post_data.append(endp_data)
                self.created_cx[self.cx_prefix + name + "_" + str(
                    num_connection) + "_fio"] = "CX_" + self.cx_prefix + name + "_" + str(num_connection) + "_fio"

        for cx_data in cx_post_data:
            url = "/cli-json/add_cx"
            self.local_realm.json_post(url, cx_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands_)
            time.sleep(sleep_time)
