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
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}


@allure.suite(suite_name="interop")
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
    def test_ClientConnect_5g_WPA2_Eap(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS, radius_info):
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
    def test_ClientConnect_2g_WPA2_Eap(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS, radius_info):

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
    def test_ClientConnect_5g_WPA3_Eap(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS, radius_info):
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
    def test_ClientConnect_2g_WPA3_Eap(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS, radius_info):

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
