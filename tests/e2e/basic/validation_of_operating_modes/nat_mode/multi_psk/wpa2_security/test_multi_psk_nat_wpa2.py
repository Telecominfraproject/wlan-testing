"""
     Multi-psk Test: NAT Mode
     pytest -m "multipsk and wpa2_personal and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
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
             },
            ]},
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE MULTIPSK")
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
    def test_client_wpa_2g_vlan1(self, get_test_library, get_dut_logs_per_test_case,
                                 get_test_device_logs, num_stations, setup_configuration):
        """
                    NAT Mode Multipsk Test with wpa encryption 2.4 GHz Band
                    pytest -m "ow_multipsk_tests_lf and nat and wpa2_personal and twogvlan1 and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa"][0]
        ssid=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa2"
        mode="NAT"
        band="twog"
        mpsk_data={profile_data["multi-psk"][0]["vlan-id"]: {"num_stations": 1,
                                                             "passkey": profile_data["multi-psk"][0]["key"]}}
        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)

    @pytest.mark.multipsk
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.twogvlan2
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3495", name="WIFI-3495")
    def test_client_wpa_2g_vlan2(self, get_test_library, get_dut_logs_per_test_case,
                                 get_test_device_logs, num_stations, setup_configuration):
        """
                NAT Mode Multipsk Test with wpa2 personal encryption 2.4 GHz Band
                pytest -m "ow_multipsk_tests_lf and nat and wpa2_personal and twogvlan2 and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa"][0]
        ssid=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa2"
        mode="NAT"
        band="twog"
        mpsk_data={profile_data["multi-psk"][0]["vlan-id"]: {"num_stations": 1,
                                                             "passkey": profile_data["multi-psk"][0]["key"]},
                   profile_data["multi-psk"][1]["vlan-id"]: {"num_stations": 1,
                                                             "passkey": profile_data["multi-psk"][1]["key"]}}
        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)

