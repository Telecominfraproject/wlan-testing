"""

    Performance Test: Multi-psk Test: NAT-WAN Mode
     pytest -m "multipsk and wpa2_personal and twog" -s -vvv --skip-testrail --testbed=basic-03 --alluredir=../allure_reports
        wifi-3493
"""
import allure
import pytest

pytestmark = [pytest.mark.multi_psk_tests,
              pytest.mark.nat,
              pytest.mark.wpa2_personal,
              pytest.mark.ow_sanity_lf,
              pytest.mark.twog, pytest.mark.ow_regression_lf]

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
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("Multi-PSK Test")
@allure.parent_suite("Multi-PSK Tests")
@allure.suite("WPA2 Personal Security")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultipskNAT(object):

    @pytest.mark.vlan1
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3495", name="WIFI-3495")
    @allure.title("Test for Client Connect with 1 VLAN")
    def test_client_wpa2_2g_vlan1(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
        To verify a client operating on NAT Mode Multipsk Test with wpa encryption 2.4 GHz Band is connecting or not.

        Unique Marker:
        multi_psk_tests and nat and wpa2_personal and twog and vlan1
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
        mode = "NAT-WAN"
        band = "twog"
        mpsk_data = {"default": {"num_stations": 1, "passkey": profile_data["security_key"]},
                     100: {"num_stations": 1, "passkey": profile_data["multi-psk"][0]["key"]}}

        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)
        assert True

    @pytest.mark.vlan2
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10061", name="WIFI-10061")
    @allure.title("Test for Client Connect with 2 VLAN's")
    def test_client_wpa2_2g_vlan2(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
        To verify the client operating on NAT Mode Multipsk Test with WPA encryption 2.4 GHz Band.

        Unique Marker:
        multi_psk_tests and nat and wpa2_personal and twog and vlan2
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
        mode = "NAT-WAN"
        band = "twog"
        mpsk_data = {"default": {"num_stations": 1, "passkey": profile_data["security_key"]},
                     100: {"num_stations": 1, "passkey": profile_data["multi-psk"][0]["key"]},
                     200: {"num_stations": 1, "passkey": profile_data["multi-psk"][1]["key"]}}
        get_test_library.multi_psk_test(band=band, mpsk_data=mpsk_data, ssid=ssid, bssid="['BLANK']",
                                        passkey=security_key,
                                        encryption=security, mode=mode, num_sta=1, dut_data=setup_configuration)
        assert True