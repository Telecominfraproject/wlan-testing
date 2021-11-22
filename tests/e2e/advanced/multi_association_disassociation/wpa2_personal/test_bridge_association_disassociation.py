import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.multiassodisasso, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultiAssoDisassoBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5691", name="WIFI-5691")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up
    def test_multi_station_udp_upload_2g(self, lf_test, lf_tools, create_lanforge_chamberview_dut):
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = []
        ssid_name.append(profile_data["ssid_name"])
        print(ssid_name)
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations=16, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        # sta_list = lf_tools.get_station_list()
        # print(sta_list)
        # lf_tools.admin_up_down(sta_list=sta_list, option="up")
        # sel_stations = ",".join(sta_list[0:8])
        # val = [['dl_rate_sel: Per-Station Downliad Rate:']]
        # wct_obj = lf_test.wifi_capacity(instance_name="udp_upload_2g", mode=mode, vlan_id=vlan,
        #                                 download_rate="0Gbps", stations=sel_stations, raw_lines=val, batch_size="8",
        #                                 upload_rate="4Mbps", protocol="UDP-IPv4", duration="120000", create_stations=False)
        # time.sleep(30)
        # lf_tools.admin_up_down(sta_list=sta_list[8:16], option="down")
        # time.sleep(10)
        # lf_tools.admin_up_down(sta_list=sta_list[8:16], option="up")
        #
        #
        #
        # report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        #
        # lf_tools.attach_report_graphs(report_name=report_name)
        # print("Test Completed... Cleaning up Stations")
        # assert True

