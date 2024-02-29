"""

    Maximum Throughput Test : Bridge Mode
    pytest -m "maximum_throughput"
"""
import sys

import pytest
import allure
import json
import os

pytestmark = [pytest.mark.advance, pytest.mark.maximum_throughput, pytest.mark.bridge]

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


@allure.feature("Maximum Throughput")
@allure.parent_suite("Maximum Throughput Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_MaxThroughput_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Maximum Throughput Test")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13330", name="WIFI-13330")
    def test_rvr_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        mode = "BRIDGE"
        vlan = 1
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="max_tput",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed)
        if result:
            assert True
        else:
            assert False, description