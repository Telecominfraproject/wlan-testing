"""

    Performance Test: Multi-psk Test: NAT Mode
     pytest -m "multipsk and wpa2_personal and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
        wifi-3495
"""
import time
import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.ow_sanity_lf,
              pytest.mark.ow_multipsk_tests_lf,
              pytest.mark.nat]


setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "MDU Wi-Fi",
             "appliedRadios": ["2G"],
             "security": "psk2",
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
             },
            ]},
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@allure.parent_suite("OpenWifi Multi PSK Test")
@allure.suite("NAT Mode")
@allure.sub_suite("WPA2 Personal Security")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultipskNAT(object):

    @pytest.mark.multipsk
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.twogvlan1
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3495", name="WIFI-3495")
    @allure.title("Test for 2.4GHz one SSID with two keys (1 -- vlan 100, 2 -- without vlan id)")
    def test_client_wpa2_2g_vlan1(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        lf_tools.reset_scenario()
        print(profile_data)
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        security_key = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][2]["key"]
        vlan_id = []
        vlan_id.append(profile_data["multi-psk"][0]['vlan-id'])
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        # create vlan
        lf_tools.add_vlan(vlan_ids=[int(vlan_id[0])])
        time.sleep(10)
        station_name = []
        station_name.append("sta" + str(vlan_id[0]))
        station_name.append("sta00")
        print(station_name)
        multipsk_obj = lf_test.multipsk(ssid=ssid_name,  security="wpa2", mode="NAT",
                                        vlan_id=vlan_id, key1=key1, key2=key2, band=band, station_name=station_name, n_vlan="1")
        if multipsk_obj == True:
            assert True
        else:
            assert False, "Expected and Attained IP's of Station are Different"

    @pytest.mark.multipsk
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.twogvlan2
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3495", name="WIFI-3495")
    @allure.title("Test for 2.4 GHz one SSID with two keys (1 -- vlan 100, 2 -- vlan 200)")
    def test_client_wpa2_2g_vlan2(self, lf_test, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
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

        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        # create vlan
        station_name = []
        for i in vlan_id:
            lf_tools.add_vlan(vlan_ids=[int(i)])
            station_name.append("sta" + str(i))
        time.sleep(10)


        station_name.append("sta00")
        print(station_name)
        multipsk_obj = lf_test.multipsk(ssid=ssid_name, security="wpa2", mode="NAT",
                                        vlan_id=vlan_id, key1=key1, key2=key2, band=band,
                                        station_name=station_name, n_vlan="2", key3=key3)
        if multipsk_obj == True:
            assert True
        else:
            assert False, "Expected and Attained IP's of Station are Different"


