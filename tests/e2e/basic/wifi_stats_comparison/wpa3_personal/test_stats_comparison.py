"""

    Comparison of iwinfo with controller stats
    pytest -m "stats_comparison and bridge and wap3_personal"

"""
import json
import logging
import time

import allure
import pytest


pytestmark = [pytest.mark.ow_sanity_lf, pytest.mark.stats_comparison, pytest.mark.bridge, pytest.mark.wap3_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "OpenWifi_2G", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi_5G", "appliedRadios": ["5G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi_6G", "appliedRadios": ["6G"], "security_key": "OpenWifi"}]},
    "rf":{
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "EHT",
            "channel": 6,
            "country": "US"
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36,
            "country": "US"
        },
        "6G": {
            "band": "6G",
            "channel-width": 320,
            "channel-mode": "EHT",
            "channel": 33,
            "country": "US"
        }
    },
    "radius": False
}


@allure.feature("Wifi_stats_comparison")
@allure.parent_suite("Wifi_stats_comparison")
@allure.suite(suite_name="WPA3 PERSONAL")
@allure.sub_suite(sub_suite_name="Test Wifi stats comparison")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestStatsComparisonSuite(object):
    """
        Comparison of iwinfo with controller stats
        pytest -m "stats_comparison and bridge and wap3_personal"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.sixg
    @allure.story('wpa3_personal')
    @allure.title("Comparison of iwinfo with controller stats")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14639", name="WIFI-14639")
    def test_stats_comparison(self, get_test_library, get_test_device_logs,
                                              get_testbed_details,
                                              get_dut_logs_per_test_case, get_target_object,
                                              num_stations, check_connectivity, setup_configuration,
                                              client_type):
        """
            Test Description: The iwinfo command on the AP side displays key wireless parameters such as configured SSIDs, BSSIDs, operating channels, channel bandwidth, frequency, encryption, etc. Verify that these parameters shown in iwinfo accurately reflect in the controller’s stats.

            Marker:
            "stats_comparison and bridge and wap3_personal"
        """

        # check for the AP band support
        get_test_library.check_band_ap(band="sixg")
        ssid_names = []
        bands = ["twog","fiveg","sixg"]
        for i in range(0,3):
            ssid_names.append(setup_params_general["ssid_modes"]["wpa3_personal"][i]["ssid_name"])
        #     bands.append(setup_params_general["ssid_modes"]["wpa3_personal"][i]["appliedRadios"][0])
        # logging.info(f"ssid_names:{ssid_names} and bands: {bands}")

        security_key = "OpenWifi"
        security = "wpa3"
        mode = "BRIDGE"

        get_test_library.wifi_stats_comparison(ssid_list=ssid_names, bands=bands, security=security,
                                                                 dut_data=setup_configuration,passkey=security_key,
                                                                 mode=mode, num_sta=num_stations,
                                               sta_rows=["ssid", "ip", "mode", "channel", "signal", "mac", "parent dev"],
                                               get_target_object=get_target_object)

        assert True