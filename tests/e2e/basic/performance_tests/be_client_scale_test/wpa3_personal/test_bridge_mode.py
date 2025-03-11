"""

    Performance Test:  BE Client Scale Test : BRIDGE Mode
    pytest -m "be_client_scale_tests and bridge"

"""
import logging
import os
import pytest
import allure

pytestmark = [pytest.mark.bridge, pytest.mark.be_client_scale_tests]

setup_params_general_6G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]
    },
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


@allure.feature("BE Client Scale Tests")
@allure.parent_suite("BE Client Scale Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_6G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.performance
class TestWifiCapacityBRIDGEMode6G(object):
    """ BE Client Scale Test BRIDGE mode
           be_client_scale_tests and bridge and wpa3_personal and sixg"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    @pytest.mark.sixg
    @allure.title("Test for TCP Download 6 GHz")
    def test_be_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations, get_lab_info, selected_testbed):
        """ BE Client Scale Test BRIDGE mode
            pytest -m "be_client_scale_tests and bridge and wpa3_personal and sixg and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        if dut_mode.lower() == "wifi6":
            logging.info("AP does not support BE mode, so skipping this test.")
            pytest.skip("AP does not support BE mode, so skipping this test")
        get_test_library.wifi_capacity(instance_name="test_be_client_wpa3_BRIDGE_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations}, is_wifi7=True, is_bw320=True)
        assert True

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3659", name="WIFI-3659")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    @pytest.mark.sixg
    @allure.title("Test for UDP Download 6 GHz")
    def test_be_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations, get_lab_info, selected_testbed):
        """ BE Client Scale Test BRIDGE mode
            pytest -m "be_client_scale_tests and bridge and wpa3_personal and sixg and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        if dut_mode.lower() == "wifi6":
            logging.info("AP does not support BE mode, so skipping this test.")
            pytest.skip("AP does not support BE mode, so skipping this test")
        get_test_library.wifi_capacity(instance_name="test_be_client_wpa3_BRIDGE_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations}, is_wifi7=True, is_bw320=True)
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_upload
    @pytest.mark.sixg
    @allure.title("Test for TCP Upload 6 GHz")
    def test_be_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations, get_lab_info, selected_testbed):
        """ BE Client Scale Test BRIDGE mode
            pytest -m "be_client_scale_tests and bridge and wpa3_personal and sixg and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        if dut_mode.lower() == "wifi6":
            logging.info("AP does not support BE mode, so skipping this test.")
            pytest.skip("AP does not support BE mode, so skipping this test")
        get_test_library.wifi_capacity(instance_name="test_be_client_wpa3_BRIDGE_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations}, is_wifi7=True, is_bw320=True)
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.udp_upload
    @pytest.mark.sixg
    @allure.title("Test for UDP Upload 6 GHz")
    def test_be_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations, get_lab_info, selected_testbed):
        """ BE Client Scale Test BRIDGE mode
            pytest -m "be_client_scale_tests and bridge and wpa3_personal and sixg and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        if dut_mode.lower() == "wifi6":
            logging.info("AP does not support BE mode, so skipping this test.")
            pytest.skip("AP does not support BE mode, so skipping this test")
        get_test_library.wifi_capacity(instance_name="test_be_client_wpa3_BRIDGE_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations}, is_wifi7=True, is_bw320=True)
        assert True
