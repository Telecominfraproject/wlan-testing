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
    @allure.title("BRIDGE Mode Airtime Fairness Test")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13341", name="WIFI-13341")
    def test_rvr_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        mode = "BRIDGE"
        vlan = 1
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="atf",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed)
        if result:
            assert True
        else:
            assert False, description
