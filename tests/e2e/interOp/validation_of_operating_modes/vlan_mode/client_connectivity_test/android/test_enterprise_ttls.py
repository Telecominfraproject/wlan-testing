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

import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.client_connectivity
              ,pytest.mark.interop_uc_sanity, pytest.mark.vlan, pytest.mark.enterprise]

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_eap_and, verifyUploadDownloadSpeed_android, wifi_connect_eap, wifi_disconnect_and_forget

setup_params_enterprise = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g_vlan", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_eap_5g_vlan", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g_vlan", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g_vlan", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g_vlan", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g_vlan", "appliedRadios": ["5G"], "vlan": 100}]},

    "rf": {},
    "radius": True
}

@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Vlan Mode EAP Client Connectivity : Suite-A")
@pytest.mark.suiteA
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestVlanModeEnterpriseTTLSSuiteA(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4679", name="WIFI-4679")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_enterprise
    def test_ClientConnectivity_5g_WPA2_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                              , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print ("SSID_NAME: " + ssidName)
        #print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4678", name="WIFI-4678")
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    def test_ClientConnectivity_2g_WPA2_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                                   , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android,
                                                 connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4683", name="WIFI-4683")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_enterprise
    def test_ClientConnectivity_5g_WPA3_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                                   , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android,
                                                 connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4682", name="WIFI-4682")
    @pytest.mark.twog
    @pytest.mark.wpa3_enterprise
    def test_ClientConnectivity_2g_WPA3_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                                   , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android,
                                                 connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4681", name="WIFI-4681")
    @pytest.mark.fiveg
    @pytest.mark.wpa_enterprise
    def test_ClientConnectivity_5g_WPA_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                                        , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android,
                                                 connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4680", name="WIFI-4680")
    @pytest.mark.twog
    @pytest.mark.wpa_enterprise
    def test_ClientConnectivity_2g_WPA_enterprise_Vlan(self, request, get_vif_state, get_ToggleAirplaneMode_data
                                                        , setup_perfectoMobile_android, radius_info, get_ap_logs):

        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ["BLANK"]
        print("SSID_NAME: " + ssidName)
        # print ("SSID_PASS: " + ssidPassword)
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip, is_internet = get_ip_address_eap_and(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android,
                                                 connData)
        # Set Wifi/AP Mode
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect_eap(request, ssidName, identity, ttls_passwd, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False