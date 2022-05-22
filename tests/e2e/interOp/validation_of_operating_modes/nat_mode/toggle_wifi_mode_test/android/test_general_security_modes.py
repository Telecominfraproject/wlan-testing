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

pytestmark = [pytest.mark.regression, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.ToggleWifiMode, pytest.mark.client_reconnect]

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_WifiMode_android, ForgetWifiConnection, openApp,\
    gets_ip_add_for_checking_and_forgets_ssid, verifyUploadDownloadSpeed_android, wifi_connect, wifi_disconnect_and_forget, gets_ip_add_and_does_not_forget_ssid

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}

for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop regression")
@allure.sub_suite(sub_suite_name="Nat Mode Client ReConnect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("NAT MODE CLIENT RECONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestToggleWifiModeAndroidNatModeSuiteOne(object):
    """ Client ReConnect SuiteA
        pytest -m "client_reconnect and bridge and InteropsuiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6491", name="WIFI-6491")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ToogleWifiMode_5g_WPA2_Personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6492", name="WIFI-6492")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ToogleWifiMode_2g_WPA2_Personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6493", name="WIFI-6493")
    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ToogleWifiMode_5g_WPA_Personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                  get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6494", name="WIFI-6494")
    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ToogleWifiMode_2g_WPA_Personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                  get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6495", name="WIFI-6495")
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ToogleWifiMode_5g_Open_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6496", name="WIFI-6496")
    @pytest.mark.twog
    @pytest.mark.open
    def test_ToogleWifiMode_2g_Open_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

setup_params_general_two = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]
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

@allure.suite(suite_name="interop regression")
@allure.sub_suite(sub_suite_name="Nat Mode Client ReConnect : Suite-B")
@pytest.mark.InteropsuiteB
@allure.feature("NAT MODE CLIENT RECONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestToggleWifiModeAndroidNatModeSuiteTwo(object):
    """ Client ReConnect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteB"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6497", name="WIFI-6497")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_ToogleWifiMode_5g_wpa3_personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6498", name="WIFI-6498")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_ToogleWifiMode_2g_wpa3_personal_Nat(self, request, get_vif_state, get_ap_logs,
                                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6499", name="WIFI-6499")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    def test_ToogleWifiMode_5g_wpa3_personal_mixed_Nat(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6500", name="WIFI-6500")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    def test_ToogleWifiMode_2g_wpa3_personal_mixed_Nat(self, request, get_vif_state, get_ap_logs,
                                                         get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6501", name="WIFI-6501")
    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ToogleWifiMode_5g_wpa_wpa2_personal_mixed_Nat(self, request, get_vif_state, get_ap_logs,
                                                             get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6502", name="WIFI-6502")
    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ToogleWifiMode_2g_wpa_wpa2_personal_mixed_Nat(self, request, get_vif_state, get_ap_logs,
                                                             get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = gets_ip_add_and_does_not_forget_ssid(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
            ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_android, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False