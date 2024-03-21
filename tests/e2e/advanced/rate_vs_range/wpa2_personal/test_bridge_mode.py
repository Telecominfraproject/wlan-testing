"""

    Test Rate v/s Range : Bridge Mode
    pytest -m "rate_vs_range"
"""
import sys

import pytest
import allure
import json
import os

pytestmark = [pytest.mark.advance, pytest.mark.rate_vs_range, pytest.mark.bridge]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            'band': '5G',
            "channel": 36,
            "channel-width": 80
        },
        "2G": {
            'band': '2G',
            "channel": 6,
            "channel-width": 20

        }

    },
    "radius": False
}

@allure.feature("Rate v/s Range")
@allure.parent_suite("Rate v/s Range Test")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="Bridge Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_RatevsRange_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ac
    @allure.title("Rate vs Range Test for AC Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13335", name="WIFI-13335")
    def test_rvr_ac_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Range versus rate test intends to measure the rate-control,
            baseband and RF chain performance of Wi-Fi device at different signal levels.
            The attenuation of signals due to range increase is achieved by
            adjusting the attenuator.

            Marker:
            advance_ac and rate_vs_range and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 0"], ["skip_ax: 1"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="rvr",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ax
    @allure.title("Rate vs Range Test for AX Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13335", name="WIFI-13335")
    def test_rvr_ax_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Range versus rate test intends to measure the rate-control,
            baseband and RF chain performance of Wi-Fi device at different signal levels.
            The attenuation of signals due to range increase is achieved by
            adjusting the attenuator.

            Marker:
            advance_ax and rate_vs_range and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 1"], ["skip_ax: 0"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="rvr",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description
