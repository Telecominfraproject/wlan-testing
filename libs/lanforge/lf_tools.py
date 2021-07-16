from create_chamberview import CreateChamberview
from create_chamberview_dut import DUT
import time
from LANforge.lfcli_base import LFCliBase
import json
import os
import pandas as pd

class ChamberView:

    def __init__(self, lanforge_data=None, access_point_data=None, debug=True, testbed=None):
        self.lanforge_ip = lanforge_data["ip"]
        self.lanforge_port = lanforge_data["port"]
        self.twog_radios = lanforge_data["2.4G-Radio"]
        self.fiveg_radios = lanforge_data["5G-Radio"]
        self.ax_radios = lanforge_data["AX-Radio"]
        self.upstream_port = lanforge_data["upstream"]
        self.twog_prefix = lanforge_data["2.4G-Station-Name"]
        self.fiveg_prefix = lanforge_data["5G-Station-Name"]
        self.ax_prefix = lanforge_data["AX-Station-Name"]
        self.uplink_port = lanforge_data["uplink"]  # eth2
        self.upstream_subnet = lanforge_data["upstream_subnet"]
        self.testbed = testbed
        self.upstream_resources = self.upstream_port.split(".")[0] + "." + self.upstream_port.split(".")[1]
        self.uplink_resources = self.uplink_port.split(".")[0] + "." + self.uplink_port.split(".")[1]
        self.delete_old_scenario = True
        # For chamber view
        self.scenario_name = "TIP-" + self.testbed
        self.debug = debug
        self.exit_on_error = False

        self.raw_line = [
            ["profile_link " + self.upstream_resources + " upstream-dhcp 1 NA NA " + self.upstream_port.split(".")
            [2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resources + " uplink-nat 1 'DUT: upstream LAN " + self.upstream_subnet
             + "' NA " + self.uplink_port.split(".")[2] + "," + self.upstream_port.split(".")[2] + " -1 NA"]
        ]

        # This is for rawline input | see create_chamberview_dut.py for more details

        self.CreateChamberview = CreateChamberview(self.lanforge_ip, self.lanforge_port)

        if access_point_data:
            # for DUT
            self.dut_name = testbed
            self.ap_model = access_point_data[0]["model"]
            self.version = access_point_data[0]["version"].split("/")[-1]
            self.serial = access_point_data[0]["serial"]

            self.CreateDut = DUT(lfmgr=self.lanforge_ip,
                                 port=self.lanforge_port,
                                 dut_name=self.testbed,
                                 sw_version=self.version,
                                 hw_version=self.ap_model,
                                 model_num=self.ap_model,
                                 serial_num=self.serial
                                 )
            self.CreateDut.ssid = []

    def Chamber_View(self):
        if self.delete_old_scenario:
            self.CreateChamberview.clean_cv_scenario(type="Network-Connectivity", scenario_name=self.scenario_name)
        self.CreateChamberview.setup(create_scenario=self.scenario_name,
                                     raw_line=self.raw_line
                                     )
        self.CreateChamberview.build(self.scenario_name)
        self.CreateChamberview.sync_cv()
        time.sleep(2)
        self.CreateChamberview.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateChamberview.sync_cv()
        return self.CreateChamberview, self.scenario_name

    def Create_Dut(self):
        self.CreateDut.setup()
        self.CreateDut.add_ssids()
        self.CreateDut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateDut.cv_test.sync_cv()
        time.sleep(2)
        self.CreateDut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateDut.cv_test.sync_cv()
        return self.CreateDut, self.dut_name

    def update_ssid(self, ssid_data=[]):
        self.CreateDut.ssid = ssid_data
        self.CreateDut.add_ssids()
        # SSID data should be in this format
        # [
        # ['ssid_idx=0 ssid=Default-SSID-2g security=WPA|WEP| password=12345678 bssid=90:3c:b3:94:48:58'],
        # ['ssid_idx=1 ssid=Default-SSID-5gl password=12345678 bssid=90:3c:b3:94:48:59']
        #  ]
        pass

    def json_get(self, _req_url="/"):
        cli_base = LFCliBase(_lfjson_host=self.lanforge_ip, _lfjson_port=self.lanforge_port, )
        json_response = cli_base.json_get(_req_url=_req_url)
        return json_response

    def json_post(self, req_url, shelf, resources, port, current, intrest):
        data = {
            "shelf": shelf,
            "resource": resources,
            "port": port,
            "current_flags": current,
            "interest": intrest
        }
        cli_base = LFCliBase(_lfjson_host=self.lanforge_ip, _lfjson_port=self.lanforge_port, )
        return cli_base.json_post(req_url, data)

    def read_kpi_file(self, column_name, dir_name ):
        if column_name == None:
            df = pd.read_csv("../reports/" + str(dir_name) + "/kpi.csv", sep=r'\t', engine='python')
            if df.empty == True:
                return "empty"
            else:
                return df
        else:
            df = pd.read_csv("../reports/" + str(dir_name) + "/kpi.csv", sep=r'\t', usecols=column_name, engine='python')
            if df.empty == True:
                return "empty"
            else:
                return df






