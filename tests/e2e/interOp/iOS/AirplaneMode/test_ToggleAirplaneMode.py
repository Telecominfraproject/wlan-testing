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

from iOS_lib import closeApp, openApp, Toggle_AirplaneMode_iOS, ForgetWifiConnection, set_APconnMobileDevice_iOS, \
    verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],"security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],"security_key": "something"}]},
    "rf": {},
    "radius": False
}

@pytest.mark.ToggleAirplaneMode
@pytest.mark.interop_iOS
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)

@pytest.mark.usefixtures("setup_profiles")
class TestToggleAirplaneMode(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ToogleAirplaneMode_5g_WPA2_Personal(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #print("ReportFlag: " + resultFlag)
        #setReportResultFlag(resultFlag)
        
        # Toggle AirplaneMode
        Toggle_AirplaneMode_iOS(request, setup_perfectoMobile_iOS, connData)

        # Verify AP After AirplaneMode
        assert verify_APconnMobileDevice_iOS(request, ssidName, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ToogleAirplaneMode_2g_WPA2_Personal(self, request, get_ToggleAirplaneMode_data,setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #print("ResultFlag: " + resultFlag)
       # print(resultFlag)
       # reportResultFlag.reportFlag = resultFlag
        
        # Toggle AirplaneMode
        Toggle_AirplaneMode_iOS(request, setup_perfectoMobile_iOS, connData)

        # Verify AP After AirplaneMode
        assert verify_APconnMobileDevice_iOS(request, ssidName, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ToogleAirplaneMode_5g_WPA(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Toggle AirplaneMode
        Toggle_AirplaneMode_iOS(request, setup_perfectoMobile_iOS, connData)

        # Verify AP After AirplaneMode
        assert verify_APconnMobileDevice_iOS(request, ssidName, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ToogleAirplaneMode_2g_WPA(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Toggle AirplaneMode
        Toggle_AirplaneMode_iOS(request, setup_perfectoMobile_iOS, connData)

        # Verify AP After AirplaneMode
        assert verify_APconnMobileDevice_iOS(request, ssidName, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)
