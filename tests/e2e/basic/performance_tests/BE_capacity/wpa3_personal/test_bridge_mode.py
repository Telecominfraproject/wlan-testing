"""

    Performance Test: Single BE client Wifi capacity with Channel and Channel-width Test: Bridge Mode
    pytest -m "wifi_capacity_be_tests and bridge"

"""
import logging

import allure
import pytest

pytestmark = [pytest.mark.wifi_capacity_be_tests, pytest.mark.bridge, pytest.mark.sixg,
              pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}

                          ]},
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 40,
            "channel-mode": "EHT",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "EHT",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 320,
            "channel-mode": "EHT",
            "channel": 33
        }
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
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @allure.title("Single BE client TCP Download wifi capacity 320Mhz Bw")
    def test_be_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_be_tests and sixg and tcp_download and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        sets = [["UDP-Burst", "1"], ["UDP-GRO", "1"], ["Multiple Endpoints:", "10"]]
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_download", mode=mode,
                                       download_rate="10Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True , is_wifi7=True, is_bw320=True,
                                       sets_=sets)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_download
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single BE client UDP Download wifi capacity 320Mhz Bw")
    def test_be_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_be_tests and sixg and udp_download and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        sets = [["UDP-Burst", "1"], ["UDP-GRO", "1"], ["Multiple Endpoints:", "10"]]
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_dl", mode=mode,
                                       download_rate="10Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True, is_wifi7=True, is_bw320=True,
                                       sets_=sets)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_upload
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single BE client TCP Upload wifi capacity 320Mhz Bw")
    def test_be_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_be_tests and sixg and tcp_upload and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        # val = [['modes: Auto'], ['bandw_options: 320Mhz']]
        sets = [["UDP-Burst", "1"], ["UDP-GRO", "1"], ["Multiple Endpoints:", "10"]]
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="10Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True, is_wifi7=True, is_bw320=True,
                                       sets_=sets)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_upload
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Single BE client UDP Upload wifi capacity 320Mhz Bw")
    def test_be_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, get_lab_info, selected_testbed, check_connectivity):
        """ Single BE client Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_be_tests and sixg and udp_upload and bridge"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        sets = [["UDP-Burst", "1"], ["UDP-GRO", "1"], ["Multiple Endpoints:", "10"]]
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="10Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True, is_wifi7=True, is_bw320=True,
                                       sets_=sets)
        assert True
