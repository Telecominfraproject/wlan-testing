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
    @pytest.mark.advance_ac
    @allure.title("Maximum Throughput Test for AC Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13330", name="WIFI-13330")
    def test_maximum_throughput_ac_bridge(self, get_test_library, setup_configuration, check_connectivity,
                                          selected_testbed):
        """
            Test Description:
            The Maximum throughput test intends to measure the maximum throughput performance of the DUT with
            a single station active. The test uses TCP connections and the attenuation is adjusted to emulate a
            distance of 2 meters. The 2.4Ghz station is configured for 20Mhz bandwidth and the 5Ghz station is
            configured for 80Mhz bandwidth. In 6Ghz, the station is configured for 160Mhz bandwidth. In both cases
            the station is configured for a maximum of two spatial streams.

            Marker:
            advance_ac and maximum_throughput and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 0"], ["skip_ax: 1"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="max_tput",
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
    @allure.title("Maximum Throughput Test for AX Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13330", name="WIFI-13330")
    def test_maximum_throughput_ax_bridge(self, get_test_library, setup_configuration, check_connectivity,
                                          selected_testbed):
        """
            Test Description:
            The Maximum throughput test intends to measure the maximum throughput performance of the DUT with
            a single station active. The test uses TCP connections and the attenuation is adjusted to emulate a
            distance of 2 meters. The 2.4Ghz station is configured for 20Mhz bandwidth and the 5Ghz station is
            configured for 80Mhz bandwidth. In 6Ghz, the station is configured for 160Mhz bandwidth. In both cases
            the station is configured for a maximum of two spatial streams.

            Marker:
            advance_ax and maximum_throughput and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 1"], ["skip_ax: 0"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="max_tput",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description
