from logging import exception
import unittest
import warnings
from perfecto.test import TestResultFactory
import pytest
import sys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
import string
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios, pytest.mark.interop_country_code_CA, pytest.mark.interop_country_code,
               pytest.mark.bridge]


from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    verifyUploadDownloadSpeediOS, get_ip_address_ios


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 36},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 1}
           },
    "radius": False
}

for sec_modes in setup_params_general1['ssid_modes'].keys():
    for i in range(len(setup_params_general1['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general1['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general1['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteOne(object):
    """ Client Connect SuiteOne    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7667", name="WIFI-7667")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn36_80Mhz_CA_5g(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn1_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 52},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 2}
           },
    "radius": False
}

for sec_modes in setup_params_general2['ssid_modes'].keys():
    for i in range(len(setup_params_general2['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general2['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general2['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteTwo(object):
    """ Client Connect SuiteTwo    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7667", name="WIFI-7667")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn52_80Mhz_CA_5g(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn2_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 100},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 3}
           },
    "radius": False
}

for sec_modes in setup_params_general3['ssid_modes'].keys():
    for i in range(len(setup_params_general3['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general3['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general3['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteThree(object):
    """ Client Connect SuiteThree    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7667", name="WIFI-7667")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn100_80Mhz_CA_5g(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn3_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 132},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 4}
           },
    "radius": False
}

for sec_modes in setup_params_general4['ssid_modes'].keys():
    for i in range(len(setup_params_general4['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general4['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general4['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteFour(object):
    """ Client Connect SuiteFour    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7667", name="WIFI-7667")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn132_80Mhz_CA_5g(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn4_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 52},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 5}
           },
    "radius": False
}

for sec_modes in setup_params_general5['ssid_modes'].keys():
    for i in range(len(setup_params_general5['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general5['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general5['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteFive(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn5_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 56},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 6}
           },
    "radius": False
}

for sec_modes in setup_params_general6['ssid_modes'].keys():
    for i in range(len(setup_params_general6['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general6['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general6['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteSix(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn6_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 60},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 7}
           },
    "radius": False
}

for sec_modes in setup_params_general7['ssid_modes'].keys():
    for i in range(len(setup_params_general7['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general7['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general7['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteSeven(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn7_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 64},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 8}
           },
    "radius": False
}

for sec_modes in setup_params_general8['ssid_modes'].keys():
    for i in range(len(setup_params_general8['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general8['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general8['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteEight(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn8_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

setup_params_general9 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 100},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 9}
           },
    "radius": False
}

for sec_modes in setup_params_general9['ssid_modes'].keys():
    for i in range(len(setup_params_general9['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general9['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general9['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteNine(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn9_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general9["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


setup_params_general10 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 104},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 10}
           },
    "radius": False
}

for sec_modes in setup_params_general10['ssid_modes'].keys():
    for i in range(len(setup_params_general10['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general10['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general10['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general10],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteTen(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn10_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general10["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

setup_params_general11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 108},
        "2G":
        {'band': '2G',
        'country': 'CA',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 11}
           },
    "radius": False
}

for sec_modes in setup_params_general11['ssid_modes'].keys():
    for i in range(len(setup_params_general11['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general11['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general11['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop country code")
@allure.sub_suite(sub_suite_name="Bridge Mode country code(CA)")
@allure.feature("BRIDGE MODE CLIENT CONNECT WITH COUNTRY CODE CA")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteEleven(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7646", name="WIFI-7646")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    def test_ClientConnect_bridge_wpa2_chn11_80Mhz_CA_2g(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general11["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


