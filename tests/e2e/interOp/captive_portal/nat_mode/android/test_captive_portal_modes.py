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

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_and, verifyUploadDownloadSpeed_android, wifi_connect, wifi_disconnect_and_forget, captive_portal_and

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.captive_portal
              ,pytest.mark.regression_interop, pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "nat_captive_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "nat_captive_open_5g", "appliedRadios": ["5G"]}],
        "wpa": [{"ssid_name": "nat_captive_wpa_2g", "appliedRadios": ["2G"], "security_key": "lanforge"},
                {"ssid_name": "nat_captive_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "lanforge"}],
        "wpa2_personal": [{"ssid_name": "nat_captive_wpa2_2g", "appliedRadios": ["2G"], "security_key": "lanforge"},
                {"ssid_name": "nat_captive_wpa2_5g", "appliedRadios": ["5G"],
                 "security_key": "lanforge"}],
        "wpa3_personal": [
            {"ssid_name": "nat_captive_wpa3_2g", "appliedRadios": ["2G"], "security_key": "lanforge"},
            {"ssid_name": "nat_captive_wpa3_5g", "appliedRadios": ["5G"],
             "security_key": "lanforge"}]},
    "rf": {},
    "radius": False,
    "captive_portal": True
}

for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Nat Mode Captive Portal : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("NAT MODE CAPTIVE PORTAL")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeCaptivePortalSuiteOneNAT(object):
    """ Captive Portal SuiteA
        pytest -m "captive portal and nat and InteropsuiteA"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5178", name="WIFI-5178")
    @pytest.mark.twog
    @pytest.mark.open
    def test_Captive_Portal_Open_2g_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                               setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5141", name="WIFI-5141")
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_Captive_Portal_Open_5g_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                               setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5180", name="WIFI-5180")
    @pytest.mark.twog
    @pytest.mark.wpa
    def test_Captive_Portal_WPA_2g_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                         setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5144", name="WIFI-5144")
    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_Captive_Portal_WPA_5g_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                         setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5184", name="WIFI-5184")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_Captive_Portal_WPA2_2g_Personal_NAT(self, request, get_vif_state, get_ap_logs,
                                                   get_APToMobileDevice_data,
                                                   setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5147", name="WIFI-5147")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_Captive_Portal_WPA2_5g_Personal_NAT(self, request, get_vif_state, get_ap_logs,
                                                    get_APToMobileDevice_data,
                                                    setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5129", name="WIFI-5129")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_Captive_Portal_WPA3_2g_Personal_NAT(self, request, get_vif_state, get_ap_logs,
                                                    get_APToMobileDevice_data,
                                                    setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5137", name="WIFI-5137")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_Captive_Portal_WPA3_5g_Personal_NAT(self, request, get_vif_state, get_ap_logs,
                                                    get_APToMobileDevice_data,
                                                    setup_perfectoMobile_android):

        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = captive_portal_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False