"""
    Toggle Wifi Mode : NAT Mode
    pytest -m "toggle_wifi_mode and nat and general"

"""
import random
import string
import time
import allure
import pytest

pytestmark = [pytest.mark.toggle_wifi_mode, pytest.mark.nat, pytest.mark.general]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
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
@allure.feature("NAT MODE TOGGLE WIFI MODE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestToggleWifiModeNatModeSuiteOne(object):

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa2 encryption 2.4 GHz Band")
    def test_ToggleWifiMode_WPA2_Personal_2g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa2 encryption 5 GHz Band")
    def test_ToggleWifiMode_WPA2_Personal_5g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa encryption 2.4 GHz Band")
    def test_ToggleWifiMode_WPA_2g_Nat(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa encryption 5 GHz Band")
    def test_ToggleWifiMode_WPA_5g_Nat(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.open
    @allure.title("NAT Mode Toggle Wifi Mode Test with open encryption 2.4 GHz Band")
    def test_ToggleWifiMode_open_2g_Nat(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.open
    @allure.title("NAT Mode Toggle Wifi Mode Test with open encryption 5 GHz Band")
    def test_ToggleWifiMode_open_5g_Nat(self, get_dut_logs_per_test_case, get_test_device_logs,
                                                    num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

setup_params_general_two = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"], "security_key": "something"}]
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
@allure.feature("NAT MODE TOGGLE WIFI MODE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestToggleWifiModeNatModeSuiteTwo(object):
    """
        Nat Toggle Wifi-Mode (wpa3_personal. wpa3_personal_mixed. wpa_wpa2_personal_mixed) (twog, fiveg)
        pytest -m "toggle_wifi_mode and nat and SuiteTwo"
    """
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa3_personal encryption 2.4 GHz Band")
    def test_ToggleWifiMode_WPA3_Personal_2g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa3_personal encryption 5 GHz Band")
    def test_ToggleWifiMode_WPA3_Personal_5g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    def test_ToggleWifiMode_WPA3_Personal_Mixed_2g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa3_personal_mixed encryption 5 GHz Band")
    def test_ToggleWifiMode_WPA3_Personal_Mixed_5g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    def test_ToggleWifiMode_wpa_wpa2_personal_mixed_2g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result

    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    @allure.title("NAT Mode Toggle Wifi Mode Test with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    def test_ToggleWifiMode_wpa_wpa2_personal_mixed_5g_Nat(self,get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        profile_data = setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        passes, result = get_test_library.toggle_wifi_mode_test(ssid=ssid_name, passkey=security_key)
        allure.attach(name="Test result", body=str(result))
        assert passes == "PASS", result



