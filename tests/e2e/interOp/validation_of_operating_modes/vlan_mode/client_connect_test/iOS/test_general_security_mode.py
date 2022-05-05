from logging import exception
import io
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

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    verifyUploadDownloadSpeediOS, get_ip_address_ios

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.client_connect, pytest.mark.interop_uc_sanity, pytest.mark.vlan]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_vlan", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid_open_5g_vlan", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa": [{"ssid_name": "ssid_wpa_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid_wpa_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g_vlan", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}
# class TestUniqueSSIDGeneralOneVLANiOS(object):
#
#     @pytest.mark.unique_ssid_general_one_vlan_ios
#     def test_unique_ssid_general_one_vlan_ios(self):
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
@allure.sub_suite(sub_suite_name="Vlan Mode Client Connect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("VLAN MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestVlanModeConnectSuiteOneVlan(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and vlan and InteropsuiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4594", name="WIFI-4594")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ClientConnect_5g_WPA2_Personal_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                          setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4593", name="WIFI-4593")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ClientConnect_2g_WPA2_Personal_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4586", name="WIFI-4586")
    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ClientConnect_5g_WPA_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4585", name="WIFI-4585")
    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ClientConnect_2g_WPA_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4583", name="WIFI-4583")
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ClientConnect_5g_Open_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

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
        # assert Toggle_AirplaneMode_android(request, setup_perfectoMobile_iOS, connData)

        #ForgetWifi
        # ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4581", name="WIFI-4581")
    @pytest.mark.twog
    @pytest.mark.open
    def test_ClientConnect_2g_Open_VLAN(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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

setup_params_general_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_p_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "wpa3_p_5g_vlan", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}],
        "wpa3_personal_mixed": [
            {"ssid_name": "wpa3_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "wpa3_p_m_5g_vlan", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "wpa_wpa2_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "wpa_wpa2_p_m_5g_vlan", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}]
    },
    "rf": {},
    "radius": False
}

# class TestUniqueSSIDGeneralTwoVLANiOS(object):
#
#     @pytest.mark.unique_ssid_general_two_vlan_ios
#     def test_unique_ssid_general_two_vlan_ios(self):
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
@allure.sub_suite(sub_suite_name="Vlan Mode Client Connect : Suite-B")
@pytest.mark.InteropsuiteB
@allure.feature("VLAN MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestVlanModeConnectSuiteTwo(object):
    """ Client Connect SuiteB
        pytest -m "client_connect and vlan and InteropsuiteB"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4596", name="WIFI-4596")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_ClientConnect_5g_wpa3_personal_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4595", name="WIFI-4595")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_ClientConnect_2g_wpa3_personal_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4598", name="WIFI-4598")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_5g_wpa3_personal_mixed_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4597", name="WIFI-4597")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_2g_wpa3_personal_mixed_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4600", name="WIFI-4600")
    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_5g_wpa_wpa2_personal_mixed_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4599", name="WIFI-4599")
    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_2g_wpa_wpa2_personal_mixed_Vlan(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

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