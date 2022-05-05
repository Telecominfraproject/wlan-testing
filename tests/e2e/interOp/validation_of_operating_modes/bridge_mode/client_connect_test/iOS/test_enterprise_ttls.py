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
    verifyUploadDownloadSpeediOS, get_ip_address_eap_ios

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios, pytest.mark.client_connect
              ,pytest.mark.interop_uc_sanity, pytest.mark.bridge, pytest.mark.enterprise]

setup_params_enterprise = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}],
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}

# class TestUniqueSSIDEnterpriseBridgeIOS(object):
#
#     @pytest.mark.unique_ssid_enterprise_bridge_ios
#     def test_unique_ssid_enterprise_bridge_ios(self):
#         for sec_modes in setup_params_enterprise['ssid_modes'].keys():
#             for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
#                 N = 3
#                 rand_string = (''.join(random.choices(string.ascii_uppercase +
#                                                       string.digits, k=N))) + str(int(time.time_ns()) % 10000)
#                 setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = \
#                     setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string
#             assert True

for sec_modes in setup_params_enterprise['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client Connect : Suite-A")
@pytest.mark.suiteA
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeEnterpriseTTLSSuiteA(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connect and bridge and enterprise and ttls and interop and suiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4691", name="WIFI-4691")
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_ClientConnect_5g_WPA2_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):
        """ wpa2 enterprise 5g
            pytest -m "client_connect and bridge and enterprise and ttls and wpa_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4690", name="WIFI-4690")
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    def test_ClientConnect_2g_WPA2_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4695", name="WIFI-4695")
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_ClientConnect_5g_WPA3_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):
        """ wpa2 enterprise 5g
            pytest -m "client_connect and bridge and enterprise and ttls and wpa_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4694", name="WIFI-4694")
    @pytest.mark.twog
    @pytest.mark.wpa3_enterprise
    def test_ClientConnect_2g_WPA3_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4693", name="WIFI-4693")
    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_ClientConnect_5g_WPA_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):
        """ wpa enterprise 5g
            pytest -m "client_connect and bridge and enterprise and ttls and wpa_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4692", name="WIFI-4692")
    @pytest.mark.twog
    @pytest.mark.wpa_enterprise
    def test_ClientConnect_2g_WPA_Eap_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                       , setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS, connData)

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


setup_params_enterprise_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "wpa_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "wpa3_mixed_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "wpa3_mixed_eap_5g", "appliedRadios": ["5G"]}]
    },
    "rf": {},
    "radius": True
}
# class TestUniqueSSIDBridgeEnterpriseTwoAnd(object):
#
#     @pytest.mark.unique_ssid_enterprise_two_bridge_and
#     def test_unique_ssid_bridge_and(self):
for sec_modes in setup_params_enterprise_two['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise_two['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_enterprise_two['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_enterprise_two['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string
            # assert True


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client Connect : Suite-B")
@pytest.mark.suiteB
@pytest.mark.mixed_eap
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeEnterpriseTTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity and bridge and enterprise and ttls and suiteB"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7414", name="WIFI-7414")
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    def test_ClientConnect_2g_wpa_wpa2_eap_mixed_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data,
                                       setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS, connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7413", name="WIFI-7413")
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    def test_ClientConnect_5g_wpa_wpa2_eap_mixed_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data,
                                                        setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7416", name="WIFI-7416")
    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    def test_ClientConnect_2g_wpa3_eap_mixed_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data,
                                                   setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7415", name="WIFI-7415")
    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_ClientConnect_5g_wpa3_eap_mixed_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data,
                                                    setup_perfectoMobile_iOS, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssidName = profile_data["ssid_name"]
        # ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_eap_ios(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_iOS,
                                                 connData)

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