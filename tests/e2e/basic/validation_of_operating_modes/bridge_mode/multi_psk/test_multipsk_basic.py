"""

    Performance Test: Multi-psk Test: Bridge Mode
     pytest -m "multipsk and wpa2_personal and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
        wifi-3492
"""
import os
import time

import pytest
import allure

pytestmark = [pytest.mark.multipsk, pytest.mark.bridge]
# pytest.mark.usefixtures("setup_test_run")]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security": "psk2",
             "security_key": "something",
             "multi-psk": [
                 {
                     "key": "password@123",
                     "vlan-id": 100
                 },
                 {
                     "key": "lanforge@123"
                 }
             ],
             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultipskBridge(object):

    @pytest.mark.multipsk
    @pytest.mark.wpa
    def test_client_wpa(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        print(profile_data)
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        security_key = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        vlan_id = profile_data["multi-psk"][0]['vlan-id']
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        # create vlan
        lf_tools.add_vlan(vlan_ids=[int(vlan_id)])

        # input data
        input_data = [{
            "password": key1,
            "upstream": "eth2." + str(vlan_id),
            "mac": "",
            "num_station": 1,
            "radio": "wiphy4"
        },
            {
                "password": key2,
                "upstream": "eth2",
                "mac": "",
                "num_station": 1,
                "radio": "wiphy4"
            },

        ]
        multipsk_obj = lf_test.multipsk(ssid=ssid_name, input_dataset=input_data, security="wpa", mode="BRIDGE", vlan_id=int(vlan_id))

        if multipsk_obj == True:
            assert True
        else:
            assert False

    @pytest.mark.multipsk
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_2g(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        print(profile_data)
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        security_key = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        vlan_id = profile_data["multi-psk"][0]['vlan-id']
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        # create vlan
        lf_tools.add_vlan(vlan_ids=[int(vlan_id)])
        time.sleep(10)
        station_name = []
        station_name.append("sta" + str(vlan_id))
        station_name.append("sta00")
        print(station_name)
        multipsk_obj = lf_test.multipsk(ssid=ssid_name,  security="wpa2", mode="BRIDGE",
                                        vlan_id=int(vlan_id), key1=key1, key2=key2, band=band, station_name=station_name)
        if multipsk_obj == True:
            assert True
        else:
            assert False
