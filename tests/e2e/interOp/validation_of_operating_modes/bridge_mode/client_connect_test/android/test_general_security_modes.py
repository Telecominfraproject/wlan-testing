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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.client_connect
              ,pytest.mark.interop_uc_sanity, pytest.mark.bridge]

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, get_ip_address_and

setup_params_general = {
    "mode": "BRIDGE",
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

# class TestUniqueSSIDGeneralBridgeAnd(object):
#
#     @pytest.mark.unique_ssid_general_one_bridge_and
#     def test_unique_ssid_general_one_bridge_and(self):
#         for sec_modes in setup_params_general['ssid_modes'].keys():
#             for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
#                 N = 3
#                 rand_string = (''.join(random.choices(string.ascii_uppercase +
#                                                       string.digits, k=N))) + str(int(time.time_ns()) % 10000)
#                 setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = \
#                 setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string
#             assert True

for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode Client Connect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("BRIDGE MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteOne(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4570", name="WIFI-4570")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ClientConnect_5g_WPA2_Personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4569", name="WIFI-4569")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ClientConnect_2g_WPA2_Personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4568", name="WIFI-4568")
    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ClientConnect_5g_WPA_Personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4567", name="WIFI-4567")
    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ClientConnect_2g_WPA_Personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4566", name="WIFI-4566")
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ClientConnect_5g_Open_Bridge(self, request, get_vif_state, get_ap_logs,
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

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

        #Toggle AirplaneMode
        # assert Toggle_AirplaneMode_android(request, setup_perfectoMobile_android, connData)

        #ForgetWifi
        # ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4565", name="WIFI-4565")
    @pytest.mark.twog
    @pytest.mark.open
    def test_ClientConnect_2g_Open_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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





setup_params_general_two = {
    "mode": "BRIDGE",
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

# class TestUniqueSSIDGeneralTwoBridgeAnd(object):
#
#     @pytest.mark.unique_ssid_general_two_bridge_and
#     def test_unique_ssid_general_two_bridge_and(self):
#         for sec_modes in setup_params_general_two['ssid_modes'].keys():
#             for i in range(len(setup_params_general_two['ssid_modes'][sec_modes])):
#                 N = 3
#                 rand_string = (''.join(random.choices(string.ascii_uppercase +
#                                                       string.digits, k=N))) + str(int(time.time_ns()) % 10000)
#                 setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] = \
#                 setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string
#
#         assert True

for sec_modes in setup_params_general_two['ssid_modes'].keys():
    for i in range(len(setup_params_general_two['ssid_modes'][sec_modes])):
        N = 2
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'].replace("ssid_","") + "_"+ rand_string

@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode Client Connect : Suite-B")
@pytest.mark.InteropsuiteB
@allure.feature("BRIDGE MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteTwo(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteB"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4572", name="WIFI-4572")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_ClientConnect_5g_wpa3_personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4571", name="WIFI-4571")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_ClientConnect_2g_wpa3_personal_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4574", name="WIFI-4574")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_5g_wpa3_personal_mixed_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4573", name="WIFI-4573")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_2g_wpa3_personal_mixed_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4576", name="WIFI-4576")
    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_5g_wpa_wpa2_personal_mixed_Bridge(self, request, get_vif_state, get_ap_logs,
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

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4575", name="WIFI-4575")
    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_2g_wpa_wpa2_personal_mixed_Bridge(self, request, get_vif_state, get_ap_logs,
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
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

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
