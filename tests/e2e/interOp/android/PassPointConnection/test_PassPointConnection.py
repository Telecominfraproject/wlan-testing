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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.PassPointConnection]

from android_lib import closeApp, set_APconnMobileDevice_android, verifyUploadDownloadSpeed_android, Toggle_WifiMode_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, setup_perfectoMobile_android

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

@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)

@pytest.mark.usefixtures("setup_profiles")
class TestPassPointConnection(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_PassPointConnection_5g_WPA2_Personal(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_android):
        
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1] 
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_PassPointConnection_2g_WPA2_Personal(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0] 
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_PassPointConnection_5g_WPA(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_params_general["ssid_modes"]["wpa"][1] 
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_PassPointConnection_2g_WPA(self, request, get_vif_state, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)