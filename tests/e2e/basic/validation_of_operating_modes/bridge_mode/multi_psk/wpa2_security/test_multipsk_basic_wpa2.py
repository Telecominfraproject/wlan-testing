"""

    Performance Test: Multi-psk Test: Bridge Mode
     pytest -m "multipsk and wpa2_personal and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
        wifi-3493
"""
import json
import logging
from datetime import time

import allure
import pytest
import requests

pytestmark = [pytest.mark.multi_psk_tests,
              pytest.mark.bridge,
              pytest.mark.wpa2_personal,
              pytest.mark.twog]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "MDU-Wi-Fi-2g",
             "appliedRadios": ["2G"],
             "security": "psk2",
             "security_key": "OpenWifi",
             "multi-psk": [
                 {
                     "key": "OpenWifi1",
                     "vlan-id": 100
                 },
                 {
                     "key": "OpenWifi2",
                     "vlan-id": 200
                 }
             ],
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("MultiPsk Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.parent_suite("MultiPsk Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA2 Security")
@pytest.mark.ow_regression_lf
@pytest.mark.usefixtures("setup_configuration")
class TestMultipskBridgeWPA2(object):

    @pytest.mark.vlan1
    @pytest.mark.wpa2
    @pytest.mark.ow_sanity_lf
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3493", name="WIFI-3493")
    @allure.title("Test for Client Connect with 1 VLAN")
    def test_client_wpa2_2g_vlan1(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                    To verify a client operating on BRIDGE Mode Multipsk Test with wpa encryption 2.4 GHz Band is connecting or not.
                    pytest -m "ow_sanity_lf and vlan1 and wpa2 and multipsk"
        """
        profile_data = {"ssid_name": "MDU-Wi-Fi-2g",
                        "appliedRadios": ["2G"],
                        "security": "psk2",
                        "security_key": "OpenWifi",
                        "multi-psk": [
                            {
                                "key": "OpenWifi1",
                                "vlan-id": 100
                            },
                            {
                                "key": "OpenWifi2",
                                "vlan-id": 200
                            }
                        ],
                        }
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        mpsk_data = {"default": {"num_stations": 1, "passkey": profile_data["security_key"]},
                     100: {"num_stations": 1, "passkey": profile_data["multi-psk"][0]["key"]}}

        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)
        assert True

    @pytest.mark.vlan2
    @pytest.mark.ow_sanity_lf
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10657", name="WIFI-10657")
    @allure.title("Test for Client Connect with 2 VLAN's")
    def test_client_wpa2_2g_vlan2(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            To verify a client operating on BRIDGE Mode Multipsk Test with wpa encryption 2.4 GHz Band is connecting or not.
            pytest -m "multi_psk_tests and bridge and wpa2_personal and vlan2 and twog"
        """
        profile_data = {"ssid_name": "MDU-Wi-Fi-2g",
                        "appliedRadios": ["2G"],
                        "security": "psk2",
                        "security_key": "OpenWifi",
                        "multi-psk": [
                            {
                                "key": "OpenWifi1",
                                "vlan-id": 100
                            },
                            {
                                "key": "OpenWifi2",
                                "vlan-id": 200
                            }
                        ],
                        }
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        mpsk_data = {"default": {"num_stations": 1, "passkey": profile_data["security_key"]},
                     100: {"num_stations": 1, "passkey": profile_data["multi-psk"][0]["key"]},
                     200: {"num_stations": 1, "passkey": profile_data["multi-psk"][1]["key"]}}
        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)
        assert True



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
    """Calls setup_testbed automatically before tests"""
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
@allure.sub_suite("WPA2 Security")
class TestEmpsk6GBridgeWPA2(object):

    @pytest.mark.wpa3_personal
    @pytest.mark.wpa2_personal
    @pytest.mark.sixg
    @pytest.mark.twog
    @pytest.mark.fiveg
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
                                                   mode=mode, band=band, pre_cleanup=False, num_sta=num_sta,
                                                   scan_ssid=True, dut_data=dut_data, extra_securities = ["wpa3"],
                                                   allure_attach=True, allure_name="station data for 2G band")

        logging.info(f"sta_data{sta_data}")