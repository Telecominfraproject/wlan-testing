"""
    Toggle Wifi Mode : VLAN Mode
    pytest -m "toggle_wifi_mode and vlan and general"

"""
import random
import string
import time
import allure
import pytest

pytestmark = [pytest.mark.toggle_wifi_mode, pytest.mark.vlan, pytest.mark.general]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}

for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@pytest.mark.InteropsuiteA
@allure.feature("VLAN MODE TOGGLE WIFI MODE")
@allure.parent_suite("Toggle Wifi Mode Tests")
@allure.suite("General Security Modes")
@allure.sub_suite("NAT Mode: Suite-One")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestToggleWifiModeVlanModeSuiteOne(object):

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa2 encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6511", name="WIFI-6511")
    def test_ToggleWifiMode_WPA2_Personal_2g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa2 encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6510", name="WIFI-6510")
    def test_ToggleWifiMode_WPA2_Personal_5g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6513", name="WIFI-6513")
    def test_ToggleWifiMode_WPA_2g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6512", name="WIFI-6512")
    def test_ToggleWifiMode_WPA_5g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.open
    @allure.title("VLAN Mode Toggle Wifi Button Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6515", name="WIFI-6515")
    def test_ToggleWifiMode_open_2g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.open
    @allure.title("VLAN Mode Toggle Wifi Button Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6514", name="WIFI-6514")
    def test_ToggleWifiMode_open_5g_Vlan(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

setup_params_general_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}]
    },
    "rf": {},
    "radius": False
}

for sec_modes in setup_params_general_two['ssid_modes'].keys():
    for i in range(len(setup_params_general_two['ssid_modes'][sec_modes])):
        N = 2
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'].replace("ssid_","") + "_"+ rand_string

@pytest.mark.InteropsuiteB
@allure.feature("VLAN MODE TOGGLE WIFI MODE")
@allure.parent_suite("Toggle Wifi Mode Tests")
@allure.suite("General Security Modes")
@allure.sub_suite("VLAN Mode: Suite-Two")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestToggleWifiModeVlanModeSuiteTwo(object):
    """
        Vlan Toggle Wifi-Mode (wpa3_personal. wpa3_personal_mixed. wpa_wpa2_personal_mixed) (twog, fiveg)
        pytest -m "toggle_wifi_mode and vlan and SuiteTwo"
    """
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa3_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6517", name="WIFI-6517")
    def test_ToggleWifiMode_WPA3_Personal_2g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6516", name="WIFI-6516")
    def test_ToggleWifiMode_WPA3_Personal_5g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6519", name="WIFI-6519")
    def test_ToggleWifiMode_WPA3_Personal_Mixed_2g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa3_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6518", name="WIFI-6518")
    def test_ToggleWifiMode_WPA3_Personal_Mixed_5g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6521", name="WIFI-6521")
    def test_ToggleWifiMode_wpa_wpa2_personal_mixed_2g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    @allure.title("VLAN Mode Toggle Wifi Button Test with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6520", name="WIFI-6520")
    def test_ToggleWifiMode_wpa_wpa2_personal_mixed_5g_Vlan(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

