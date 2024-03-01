"""

    Test Maximum Connection : Bridge Mode
    pytest -m "maximum_connection"
"""
import sys

import pytest
import allure
import json
import os

pytestmark = [pytest.mark.advance, pytest.mark.maximum_connection, pytest.mark.bridge]

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


@allure.feature("Maximum Connection")
@allure.parent_suite("Maximum Connection Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_MaxConnection_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Maximum Connection Test")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13328", name="WIFI-13328")
    def test_max_connection_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            The Maximum Connection test intends to verify that the Wi-Fi AP can support 32 STAs simultaneously
            connected with minimal packet loss and no disassociations taking place.

            Marker:
            advance and maximum_connection and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="max_cx",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed)
        if result:
            assert True
        else:
            assert False, description

