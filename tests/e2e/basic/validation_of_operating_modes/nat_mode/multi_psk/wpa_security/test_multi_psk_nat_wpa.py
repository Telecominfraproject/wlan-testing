"""

    Performance Test: Multi-psk Test: NAT Mode
     pytest -m "multipsk and wpa and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
        wifi-3494
"""
import os
import time

import pytest
import allure

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.ow_sanity_lf,
              pytest.mark.ow_multipsk_tests_lf,
              pytest.mark.nat]


setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa": [
            {"ssid_name": "MDU Wi-Fi",
             "appliedRadios": ["2G"],
             "security": "psk",
             "security_key": "something",
             "multi-psk": [
                 {
                     "key": "lanforge1",
                     "vlan-id": 100
                 },
                 {
                     "key": "lanforge2",
                     "vlan-id": 200
                 },
                 {
                     "key": "lanforge3"
                 }
             ],
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultipskNAT(object):

    @pytest.mark.multipsk
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.twogvlan1
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3494", name="WIFI-3494")
    def test_client_wpa_2g_vlan1(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        lf_tools.reset_scenario()
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        security_key = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][2]["key"]
        vlan_id = []
        vlan_id.append(profile_data["multi-psk"][0]['vlan-id'])
        security = "wpa"
        mode = "NAT"
        band = "twog"
        # create vlan
        lf_tools.add_vlan(vlan_ids=[int(vlan_id[0])])
        time.sleep(10)
        station_name = []
        station_name.append("sta" + str(vlan_id[0]))
        station_name.append("sta00")
        print(station_name)
        multipsk_obj = lf_test.multipsk(ssid=ssid_name,  security="wpa", mode="NAT",
                                        vlan_id=vlan_id, key1=key1, key2=key2, band=band, station_name=station_name, n_vlan="1")
        if multipsk_obj == True:
            assert True
        else:
            assert False

    @pytest.mark.multipsk
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.twogvlan2
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3494", name="WIFI-3494")
    def test_client_wpa_2g_vlan2(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        lf_tools.reset_scenario()
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        security_key = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        vlan_id = []
        vlan_id.append(profile_data["multi-psk"][0]['vlan-id'])
        vlan_id.append(profile_data["multi-psk"][1]['vlan-id'])

        security = "wpa"
        mode = "NAT"
        band = "twog"
        # create vlan
        station_name = []
        for i in vlan_id:
            lf_tools.add_vlan(vlan_ids=[int(i)])
            station_name.append("sta" + str(i))
        time.sleep(10)


        station_name.append("sta00")
        print(station_name)
        multipsk_obj = lf_test.multipsk(ssid=ssid_name, security="wpa", mode="NAT",
                                        vlan_id=vlan_id, key1=key1, key2=key2, band=band,
                                        station_name=station_name, n_vlan="2", key3=key3)
        if multipsk_obj == True:
            assert True
        else:
            assert False

