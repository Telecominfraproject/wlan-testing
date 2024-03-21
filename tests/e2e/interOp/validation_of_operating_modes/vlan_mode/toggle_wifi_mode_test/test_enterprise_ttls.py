"""
    Toggle Wifi Mode : VLAN Mode
    pytest -m "toggle_wifi_mode and vlan and enterprise"

"""
import random
import string
import time
import allure
import pytest

pytestmark = [pytest.mark.toggle_wifi_mode, pytest.mark.vlan, pytest.mark.enterprise]

setup_params_enterprise = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]},

    "rf": {},
    "radius": True
}

for sec_modes in setup_params_enterprise['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@pytest.mark.InteropsuiteA
@allure.feature("VLAN MODE TOGGLE WIFI MODE")
@allure.parent_suite("Toggle Wifi Mode Tests")
@allure.suite("Enterprise TTLS")
@allure.sub_suite("VLAN Mode: Suite-One")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestToggleWifiModeVlanModeSuiteOne(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa2 encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6524", name="WIFI-6524")
    def test_ToggleWifiMode_WPA2_enterprise_5g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa2 encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6525", name="WIFI-6525")
    def test_ToggleWifiMode_WPA2_enterprise_2g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                  num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6522", name="WIFI-6522")
    def test_ToggleWifiMode_WPA_enterprise_5g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6523", name="WIFI-6523")
    def test_ToggleWifiMode_WPA_enterprise_2g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                        num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa3_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6526", name="WIFI-6526")
    def test_ToggleWifiMode_wpa3_enterprise_5g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa3_enterprise
    @allure.title("VLAN Mode Toggle Wifi Button Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6527", name="WIFI-6527")
    def test_ToggleWifiMode_wpa3_enterprise_2g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        identity = radius_info['user']
        ttls_passwd = radius_info["password"]

        passes, result = get_test_library.enterprise_toggle_wifi_mode_test(ssid=ssid_name, identity=identity,
                                                                           ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result
