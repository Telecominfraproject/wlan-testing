import json
import logging
from datetime import time

import allure
import pytest
import requests

pytestmark = [pytest.mark.multi_psk_tests,
              pytest.mark.bridge,
              pytest.mark.wpa3_personal,
              pytest.mark.sixg,
              pytest.mark.ow_sanity_lf]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "OpenWifi-roam",
             "appliedRadios": ["2G", "5G"],
             "security": "psk2",
             "security_key": "OpenWifi",
             "multi-psk": [
                 {"key": "aaaaaaaa"},
                 {"key": "bbbbbbbb"}
             ],
            "roaming": True,
            "rrm": {
            "reduced-neighbor-reporting": True
                    }
             }
        ],
        "wpa3_personal": [
            {"ssid_name": "OpenWifi-roam",
             "appliedRadios": ["6G"],
             "security": "sae",
             "security_key": "OpenWifi",
            "roaming": True,
            "rrm": {
            "reduced-neighbor-reporting": True
                    }
             }
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "EHT",
            "channel": "auto"
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "EHT",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 320,
            "channel-mode": "EHT",
            "channel": 33
        }
    },
    "radius": False
}

testbed_details_global = None
dut_data = {}

@pytest.fixture(scope="class")
def setup_initial_configuration(request):
    """Calls setup_initial_configuration automatically before tests"""
    global setup_params_general
    global dut_data
    logging.info(f"Setup Params Assigned: {setup_params_general}")

    requested_combination = [['2G', 'wpa2_personal'], ['5G', 'wpa2_personal'], ['6G', 'wpa3_personal']]

    logging.info(f"requested_combination:::{requested_combination}")
    get_target_obj = request.getfixturevalue("get_target_object")
    logging.info("ready to start setup_basic_configuration")
    logging.info(f"setup_params_general value before start:{setup_params_general}")
    dut_data = get_target_obj.setup_basic_configuration(configuration=setup_params_general,
                                                       requested_combination=requested_combination)

    logging.info(f"setup_basic_configuration dut data:{dut_data}")

@allure.feature("MultiPsk Test")
@allure.parent_suite("MultiPsk Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA3 Security")
class TestEmpsk6GBridgeWPA3(object):

    # @pytest.mark.wpa3_personal
    # @pytest.mark.wpa2_personal
    # @pytest.mark.sixg
    # @pytest.mark.twog
    # @pytest.mark.fiveg
    @pytest.mark.empsk
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14423", name="WIFI-14423")
    @allure.title("Test E-MPSK with WPA2 to WPA3 on 6GHz")
    def test_client_wpa2_wpa3_6g_empsk(self, setup_initial_configuration, get_test_library,get_target_object,
                                     check_connectivity, get_testbed_details):
        """
        Verify E-MPSK working in BRIDGE mode:
        - Client connects on 2.4/5GHz (WPA2 and WPA3)
        - Encryption is changed from WPA2 to WPA3 (disable WPA2)
        - Verify client successfully get an IP and associate to AP
        """
        profile_data = {
            "ssid_name": "OpenWifi-roam",
            "appliedRadios": ["2G"],
            "security": "psk2",
            "security_key": "OpenWifi",
            "multi-psk": [
                {"key": "aaaaaaaa"},
                {"key": "bbbbbbbb"}
            ]
        }
        ssid = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        num_sta = 1
        security_key = profile_data["multi-psk"][0]["key"]
        sta_data = get_test_library.empsk_test(ssid=ssid, passkey=security_key, security=security, is_bw320=True,
                                                   mode=mode, band=band, pre_cleanup=True, num_sta=num_sta,
                                                   scan_ssid=True, dut_data=dut_data, extra_securities = ["wpa3"],
                                                   allure_attach=True)

        logging.info(f"sta_data{sta_data}")