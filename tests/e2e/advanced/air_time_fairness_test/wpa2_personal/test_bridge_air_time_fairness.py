"""

    Airtime Fairness Tests: BRIDGE Mode
    pytest -m "airtime_fairness_tests and wpa2_personal and bridge"

"""

import pytest
import allure
import os
import time
import logging

pytestmark = [pytest.mark.advance, pytest.mark.airtime_fairness_tests, pytest.mark.wpa2_personal, pytest.mark.bridge]

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
@allure.parent_suite("Airtime Fairness Tests")
@allure.suite("WPA2 Personal Security")
@allure.sub_suite("Bridge Mode")
@allure.feature("green field & medium distanced & legacy stations")
@pytest.mark.usefixtures("setup_configuration")
class TestAtfBridge(object):
    """
                        BRIDGE Mode Airtime Fairness Test with wpa2 personal encryption
                        pytest -m "airtime_fairness_tests and bridge and wpa2_personal"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6394", name="WIFI-6394")
    @pytest.mark.twog
    @pytest.mark.atf_2g
    @allure.title("Test for Airtime fairness of 2.4G")
    def test_atf_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                    BRIDGE Mode Airtime Fairness Test with wpa2 personal encryption 2.4 GHz Band
                    pytest -m "airtime_fairness_tests and bridge and twog and wpa2_personal and atf_2g"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        vlan = 1
        band = 'twog'
        result, description = get_test_library.air_time_fairness(ssid=ssid_name, passkey=security_key, security="wpa2",
                                                                 mode=mode, band=band, vlan_id=vlan,atn=380,
                                                                 pass_value=[80,80,48], dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False, description

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6394", name="WIFI-6394")
    @pytest.mark.fiveg
    @pytest.mark.atf_5g
    @allure.title("Test for Airtime fairness of 5G")
    def test_atf_5g(self, get_test_library, setup_configuration, check_connectivity):
        """
                            BRIDGE Mode Airtime Fairness Test with wpa2 personal encryption 5 GHz Band
                            pytest -m "airtime_fairness_tests and bridge and fiveg and wpa2_personal and atf_5g"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        vlan = 1
        band = 'fiveg'

        result, description = get_test_library.air_time_fairness(ssid=ssid_name, passkey=security_key, security="wpa2",
                                                                 mode=mode, band=band, vlan_id=vlan, atn=250,
                                                                 pass_value=[500,470,260], dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False, description