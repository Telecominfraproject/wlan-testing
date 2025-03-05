"""

    Performance Test: Single BE client Wifi capacity with Channel and Channel-width Test: Bridge Mode
    pytest -m "be_capacity_tests and bridge"

"""
import logging

import allure
import pytest

pytestmark = [pytest.mark.be_capacity_tests, pytest.mark.bridge, pytest.mark.sixg,
              pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}

                          ]},
    "rf": {
        "6G": {
            'band': '6G',
            'channel-width': 160,
            "channel-mode": "EHT"}
    },
    "radius": False
}


@allure.feature("Performance Test")
@allure.parent_suite("BE Capacity Test")
@allure.suite("6 GHz Band")
@allure.sub_suite("BRIDGE Mode")

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.usefixtures("setup_configuration")
class TestWifiCapacityBRIDGEModeBE6G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.sixg
    @pytest.mark.tcp_download
    @allure.title("Single BE client TCP Download wifi capacity")
    def test_be_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "ow_sanity_lf and be_capacity_tests and sixg and tcp_download and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_download", mode=mode,
                                       download_rate="10Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_download
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single client UDP Download wifi capacity 160Mhz Bw")
    def test_be_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "be_capacity_tests and sixg and udp_download and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_dl", mode=mode,
                                       download_rate="10Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_upload
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single BE client TCP Upload wifi capacity 160Mhz Bw")
    def test_be_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "be_capacity_tests and sixg and tcp_upload and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="10Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_upload
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single BE client UDP Upload wifi capacity 160Mhz Bw")
    def test_be_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "be_capacity_tests and sixg and udp_upload and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="10Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True
