import logging
import os
import importlib
import allure
import pytest

pytestmark = [pytest.mark.mbssid_tests, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "OpenWifi-6G-1", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-2", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-3", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-4", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-5", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-6", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-7", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-8", "appliedRadios": ["6G"], "security_key": "OpenWifi"},

            {"ssid_name": "OpenWifi-2G-1", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-2", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-3", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-4", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-5", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-6", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-7", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-8", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ],
        "owe": [
            {"ssid_name": "OpenWifi-6G-1", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-2", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-3", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-4", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-5", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-6", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-7", "appliedRadios": ["6G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-6G-8", "appliedRadios": ["6G"], "security_key": "OpenWifi"},

            {"ssid_name": "OpenWifi-2G-1", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-2", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-3", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-4", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-5", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-6", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-7", "appliedRadios": ["2G"], "security_key": "OpenWifi"},
            {"ssid_name": "OpenWifi-2G-8", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel": "auto",
            "channel-width": 40,
            "channel-mode": "EHT"
        },
        "5G": {
            "band": "5G",
            "channel": "auto",
            "channel-width": 80,
            "channel-mode": "EHT"
        },
        "6G": {
            "band": "6G",
            "channel": "auto",
            "channel-width": 160,
            "channel-mode": "EHT",
            "he-settings": {"multiple-bssid": True}
        }
    },
    "radius": False
}


@allure.feature("mbssid_tests")
@allure.parent_suite("MBSSID Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="MBSSID Client Connectivity Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMbssidConnectivity(object):
    """
        MBSSID Connectivity Test
        pytest -m "mbssid_tests and bridge"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @pytest.mark.twog
    @pytest.mark.transmit
    @allure.story("MBSSID Connectivity Test WPA3 personal")
    @allure.title("BRIDGE Mode Transmitting ssid Client Connectivity Test with WPA3 Personal in 6GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14642", name="WIFI-14642")
    def test_mbssid_connectivity_wpa3_personal_6g_transmit(self, setup_configuration, get_test_library, check_connectivity,
                                                  get_target_object, get_testbed_details):
        """
            Test Description: Test Description: MBSSID is a Wi-Fi feature that allows an AP to advertise multiple SSIDs using a single transmitted beacon frame, instead of sending separate beacons for each SSID. In the 6 GHz band, clients are required to discover networks passively and to reduce power usage and airtime consumption, it's inefficient for APs to transmit beacons for every SSID.
            MBSSID Connectivity Test WPA3 personal (6G)
            pytest -m "mbssid_tests and wpa3_personal and sixg and transmit"
        """
        profile_data = {"ssid_name": "OpenWifi-6G-1", "appliedRadios": ["6G", "2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "sixg"
        result = get_test_library.mbssid_test(ssid=ssid_name, security=security,
                                                      dut_data=setup_configuration,
                                                      passkey=security_key, mode=mode, band=band,
                                                      num_sta=1, tip_2x_obj=get_target_object, is_ht160=True,
                                                      is_mbssid=True, search_type="transmit")
        logging.info(f"result from testcase:{result}")

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @pytest.mark.twog
    @pytest.mark.non_transmit
    @allure.story("MBSSID Connectivity Test WPA3 personal")
    @allure.title("BRIDGE Mode Non-transmitting ssid Client Connectivity Test with WPA3 Personal in 6GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14614", name="WIFI-14614")
    def test_mbssid_connectivity_wpa3_personal_6g_non_transmit(self, setup_configuration, get_test_library, check_connectivity,
                                                  get_target_object, get_testbed_details):
        """
            Test Description: Test Description: MBSSID is a Wi-Fi feature that allows an AP to advertise multiple SSIDs using a single transmitted beacon frame, instead of sending separate beacons for each SSID. In the 6 GHz band, clients are required to discover networks passively and to reduce power usage and airtime consumption, it's inefficient for APs to transmit beacons for every SSID.
            MBSSID Connectivity Test WPA3 personal (6G)
            pytest -m "mbssid_tests and wpa3_personal and sixg and non_transmit"
        """
        profile_data = {"ssid_name": "OpenWifi-6G-2", "appliedRadios": ["6G", "2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "sixg"
        result = get_test_library.mbssid_test(ssid=ssid_name, security=security,
                                              dut_data=setup_configuration,
                                              passkey=security_key, mode=mode, band=band,
                                              num_sta=1, tip_2x_obj=get_target_object, is_ht160=True,
                                              is_mbssid=True, search_type="non-transmit")
        logging.info(f"result from testcase:{result}")

    @pytest.mark.owe
    @pytest.mark.sixg
    @pytest.mark.twog
    @pytest.mark.transmit
    @allure.story("MBSSID Connectivity Test OWE")
    @allure.title("BRIDGE Mode Transmitting ssid Client Connectivity Test with OWE in 6GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14664", name="WIFI-14664")
    def test_mbssid_connectivity_wpa3_personal_6g(self, setup_configuration, get_test_library, check_connectivity,
                                                  get_target_object, get_testbed_details):
        """
            Test Description: Test Description: MBSSID is a Wi-Fi feature that allows an AP to advertise multiple SSIDs using a single transmitted beacon frame, instead of sending separate beacons for each SSID. In the 6 GHz band, clients are required to discover networks passively and to reduce power usage and airtime consumption, it's inefficient for APs to transmit beacons for every SSID.
            MBSSID Connectivity Test OWE (6G)
            pytest -m "mbssid_tests and owe and sixg and transmit"
        """
        profile_data = {"ssid_name": "OpenWifi-6G-1", "appliedRadios": ["6G", "2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "owe"
        mode = "BRIDGE"
        band = "sixg"
        result = get_test_library.mbssid_test(ssid=ssid_name, security=security,
                                              dut_data=setup_configuration,
                                              passkey=security_key, mode=mode, band=band,
                                              num_sta=1, tip_2x_obj=get_target_object, is_ht160=True,
                                              is_mbssid=True, search_type="transmit")
        logging.info(f"result from testcase:{result}")

