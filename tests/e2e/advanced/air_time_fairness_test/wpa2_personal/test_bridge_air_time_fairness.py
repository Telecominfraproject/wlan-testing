"""

    Airtime Fairness Tests: BRIDGE Mode
    pytest -m "atf and wpa2_personal and bridge"

"""

import pytest
import allure
import os
import time
import logging

pytestmark = [pytest.mark.advance, pytest.mark.atf, pytest.mark.wpa2_personal, pytest.mark.bridge]

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


@allure.feature("Airtime Fairness")
@allure.parent_suite("Airtime Fairness Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_Atf_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ac
    @allure.title("Airtime Fairness Test for AC Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13341", name="WIFI-13341")
    def test_atf_ac_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Airtime Fairness Test intends to verify the capability of Wi-Fi device to ensure the fairness of airtime usage.
            This test uses two stations at a time, with one station running in optimum configuration. The second station
            varies between optimum configuration, weaker signal, and legacy mode configurations. In each setting,
            TCP traffic is used to determine maximum capacity of each station running by itself. Then, UDP traffic is
            created on STA1 to run at 75% of the TCP throughput and UDP traffic is created on the second station at
            50% of the TCP throughput for that station. This overdrives the AP and causes it to drop frames. The
            pass/fail criteria is that each station gets at least 45% of the TCP throughput when both stations are
            running the prescribed UDP traffic.

            Marker:
            advance_ac and atf and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 0"], ["skip_ax: 1"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="atf3",
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
    @allure.title("Airtime Fairness Test for AX Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13341", name="WIFI-13341")
    def test_atf_ax_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Airtime Fairness Test intends to verify the capability of Wi-Fi device to ensure the fairness of airtime usage.
            This test uses two stations at a time, with one station running in optimum configuration. The second station
            varies between optimum configuration, weaker signal, and legacy mode configurations. In each setting,
            TCP traffic is used to determine maximum capacity of each station running by itself. Then, UDP traffic is
            created on STA1 to run at 75% of the TCP throughput and UDP traffic is created on the second station at
            50% of the TCP throughput for that station. This overdrives the AP and causes it to drop frames. The
            pass/fail criteria is that each station gets at least 45% of the TCP throughput when both stations are
            running the prescribed UDP traffic.

            Marker:
            advance_ax and atf and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 1"], ["skip_ax: 0"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="atf3",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description
