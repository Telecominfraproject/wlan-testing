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
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2
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
             "appliedRadios": ["2G"],
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
        ]
    },
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
@pytest.mark.usefixtures("setup_configuration")
class TestEmpsk6GBridgeWPA2(object):

    @pytest.mark.wpa2
    @pytest.mark.wpa3
    @pytest.mark.sixg
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14423", name="WIFI-14423")
    @allure.title("Test E-MPSK with WPA2 to WPA3 on 6GHz")
    def test_client_wpa2_wpa3_6g_empsk(self, get_test_library,get_target_object,
                                        setup_configuration, check_connectivity, get_testbed_details):
        """
        Verify E-MPSK working in BRIDGE mode:
        - Client connects on 2.4/5GHz (WPA2)
        - Encryption is changed from WPA2 to WPA3
        - Verify client successfully get an IP and associate to AP
        """
        profile_data = {
            "ssid_name": "OpenWifi-roam",
            "appliedRadios": ["2G", "5G"],
            "security": "psk2",
            "security_key": "OpenWifi",
            "multi-psk": [
                {"key": "aaaaaaaa"},
                {"key": "bbbbbbbb"}
            ]
        }
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        num_sta = 1

        device_name = get_testbed_details['device_under_tests'][0]['identifier']

        empsk_config = {
    "interfaces": [
        {
            "ethernet": [
                {
                    "select-ports": [
                        "WAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "dynamic"
            },
            "name": "WAN",
            "role": "upstream",
            "services": [
                "lldp"
            ],
            "ssids": [
                {
                    "bss-mode": "ap",
                    "encryption": {
                        "ieee80211w": "optional",
                        "key": "OpenWifi",
                        "proto": "psk2"
                    },
                    "multi-psk": [
                        {
                            "key": "aaaaaaaa"
                        },
                        {
                            "key": "bbbbbbbb"
                        }
                    ],
                    "name": "OpenWifi-roam",
                    "roaming": True,
                    "rrm": {
                        "reduced-neighbor-reporting": True
                    },
                    "wifi-bands": [
                        "2G",
                        "5G"
                    ]
                },
                {
                    "bss-mode": "ap",
                    "encryption": {
                        "ieee80211w": "required",
                        "key": "OpenWifi",
                        "proto": "sae"
                    },
                    "name": "OpenWifi-roam",
                    "roaming": True,
                    "rrm": {
                        "reduced-neighbor-reporting": True
                    },
                    "wifi-bands": [
                        "6G"
                    ]
                }
            ]
        },
        {
            "ethernet": [
                {
                    "select-ports": [
                        "LAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "static",
                "dhcp": {
                    "lease-count": 100,
                    "lease-first": 10,
                    "lease-time": "6h"
                },
                "subnet": "192.168.1.1/24"
            },
            "name": "LAN",
            "role": "downstream",
            "services": [
                "ssh",
                "lldp"
            ]
        }
    ],
    "metrics": {
        "health": {
            "interval": 120
        },
        "statistics": {
            "interval": 120,
            "types": [
                "ssids",
                "lldp",
                "clients"
            ]
        }
    },
    "radios": [
        {
            "band": "2G",
            "channel": "auto",
            "channel-mode": "EHT",
            "channel-width": 20,
            "country": "US"
        },
        {
            "band": "5G",
            "channel": 36,
            "channel-mode": "EHT",
            "channel-width": 80,
            "country": "US"
        },
        {
            "band": "6G",
            "channel": 33,
            "channel-mode": "EHT",
            "channel-width": 320,
            "country": "US"
        }
    ],
    "services": {
        "lldp": {
            "describe": "uCentral",
            "location": "universe"
        },
        "ssh": {
            "port": 22
        }
    },
    "uuid": 1739265165
}
        payload = {"configuration": json.dumps(empsk_config), "serialNumber": device_name, "UUID": 2}

        path = "device/" + device_name + "/configure"
        uri = get_target_object.controller_library_object.build_uri(path)
        logging.info(f"uri::{uri}")
        resp = requests.post(uri, data=json.dumps(payload, indent=2),
                             headers=get_target_object.controller_library_object.make_headers(), verify=False,
                             timeout=120)

        logging.info(f"response:,{resp}")
        if resp.status_code == 200:
            logging.info("Empsk configuration applied successfully")
            allure.attach(name=f"Response for Reconfiguration - {resp.status_code} {resp.reason}",
                          body=str(resp.json()))
        else:
            allure.attach(name=f"Response for Reconfiguration - {resp.status_code} {resp.reason}",
                          body=f"TEST FAILED, Reconfiguration is not successful {str(resp.json())}")


        sta_data = get_test_library.empsk_test(ssid=ssid, passkey=security_key, security=security,
                                                   mode=mode, band=band, pre_cleanup=False, num_sta=num_sta,
                                                   scan_ssid=True,
                                                   station_data=["ip", "alias", "mac","channel", "port type","security", "ap", "parent dev"],
                                                   allure_attach=True, allure_name="station data for 2G band", dut_data=setup_configuration)

        logging.info(f"sta_data{sta_data}")