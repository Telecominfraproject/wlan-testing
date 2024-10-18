"""

    Client Connectivity Hot Reload Configuration: BRIDGE Mode
    pytest -m "client_connectivity_tests and bridge and general"

"""
import json
import logging
import time

import allure
import pytest
import requests
import threading

pytestmark = [pytest.mark.hot_reload, pytest.mark.bridge, pytest.mark.general]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "OpenWifi", "appliedRadios": ["5G"], "security_key": "OpenWifi"}]},
    "rf": {},
    "radius": False
}


@allure.feature("Hot Reload")
@allure.parent_suite("Hot Configuration Reloads")
@allure.suite(suite_name="WPA2 PERSONAL")
@allure.sub_suite(sub_suite_name="Test Hot Config Reload")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestHotReloadConfigSuite(object):
    """
        Bridge Client Connectivity Hot Reload (wpa2_personal) (fiveg)
        pytest -m "hot_reload and bridge and general"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.band
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Hot Reload with wpa2_personal encryption 5 GHz Band(Band Parameter)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14137", name="WIFI-14137")
    def test_hot_config_reload_band(self, get_test_library, get_test_device_logs,
                                              get_testbed_details,
                                              get_dut_logs_per_test_case, get_target_object,
                                              num_stations, check_connectivity, setup_configuration,
                                              client_type):
        """
            Test Description: The hot reload config feature allows real-time configuration updates without restarting services, minimizing downtime and service disruptions. It’s essential for maintaining continuous operation, especially in critical systems or environments with frequent updates. This feature enhances flexibility, improves scalability, and reduces the risk of human error. Here Band parameter comes under radio (PHY level) of AP, hence it’s modification should restart the service

            Marker:
            hot_reload and bridge and general and wpa2_personal and fiveg and band
        """

        print("----------------setup_configuration in test_hot_config_reload_band:", setup_configuration)
        profile_data = {"ssid_name": "OpenWifi", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        reconfig = "band"

        # Hot Reload Configuration
        passes, result = get_test_library.hot_config_reload_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=num_stations, tip_2x_obj=get_target_object, reconfig = reconfig)

        assert passes == "PASS", result



    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.channel_width
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Hot Reload with wpa2_personal encryption 5 GHz Band(Channel width Parameter)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14138", name="WIFI-14138")
    def test_hot_config_reload_channel_width(self, get_test_library, get_test_device_logs,
                                             get_testbed_details,
                                             get_dut_logs_per_test_case, get_target_object,
                                             num_stations, check_connectivity, setup_configuration,
                                             client_type):
        """
            Test Description: The hot reload config feature allows real-time configuration updates without restarting services, minimizing downtime and service disruptions. It’s essential for maintaining continuous operation, especially in critical systems or environments with frequent updates. This feature enhances flexibility, improves scalability, and reduces the risk of human error. Here Channel Width parameter comes under radio (PHY level) of AP, hence it’s modification should restart the service
            Marker:
            hot_reload and bridge and general and wpa2_personal and fiveg and channel_width
        """

        print("----------------setup_configuration:", setup_configuration)
        profile_data = {"ssid_name": "OpenWifi", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        reconfig = "channel_width"

        # Hot Reload Configuration
        passes, result = get_test_library.hot_config_reload_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=num_stations, tip_2x_obj=get_target_object,
                                                                 reconfig=reconfig)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Hot Reload with wpa2_personal encryption 5 GHz Band(DFS Parameter)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14186", name="WIFI-14186")
    def test_hot_config_reload_dfs(self, get_test_library, get_test_device_logs,
                                   get_testbed_details,
                                   get_dut_logs_per_test_case, get_target_object,
                                   num_stations, check_connectivity, setup_configuration,
                                   client_type):
        """
            Test Description: The hot reload config feature allows real-time configuration updates without restarting services, minimizing downtime and service disruptions. It’s essential for maintaining continuous operation, especially in critical systems or environments with frequent updates. This feature enhances flexibility, improves scalability, and reduces the risk of human error. Here DFS feature comes under radio (PHY level) of AP, hence it’s modification should restart the service

            Marker:
            hot_reload and bridge and general and wpa2_personal and fiveg and dfs
        """

        print("----------------setup_configuration:", setup_configuration)
        profile_data = {"ssid_name": "OpenWifi", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        reconfig = "dfs"

        # Hot Reload Configuration
        passes, result = get_test_library.hot_config_reload_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=num_stations, tip_2x_obj=get_target_object,
                                                                 reconfig=reconfig)

        assert passes == "PASS", result

