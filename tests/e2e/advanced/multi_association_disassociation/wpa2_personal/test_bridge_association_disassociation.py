import pytest
import allure
import os
import time
import pandas as pd
import threading

pytestmark = [pytest.mark.advance, pytest.mark.multiassodisasso, pytest.mark.bridge, pytest.mark.report]

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
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiAssoDisassoBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5691", name="WIFI-5691")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_2g
    @pytest.mark.karthika_new
    def test_multi_asso_disasso_udp_upload_nss2_2g(self, get_test_library, setup_configuration, get_target_object):
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16, dut_data=setup_configuration,
                                                            mode = mode, vlan=vlan, instance_name="udp_upload_2g",
                                                            traffic_direction="upload", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5692", name="WIFI-5692")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_2g
    def test_multi_asso_disasso_udp_download_nss2_2g(self, get_test_library, setup_configuration):
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_2g",
                                                                  traffic_direction="download", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5693", name="WIFI-5693")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_5g
    def test_multi_asso_disasso_udp_upload_nss2_5g(self, get_test_library, setup_configuration):
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_upload_5g",
                                                                  traffic_direction="upload", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5694", name="WIFI-5694")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_5g
    def test_multi_asso_disasso_udp_download_nss2_5g(self, get_test_library, setup_configuration):
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_5g",
                                                                  traffic_direction="download", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription


