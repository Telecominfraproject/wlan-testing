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

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from android_lib import closeApp, set_APconnMobileDevice_android, verifyUploadDownloadSpeed_android, Toggle_WifiMode_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, setup_perfectoMobile_android

@pytest.mark.PassPointConnectionAndroid
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["NAT"], ["NAT"])],
    indirect=True,
    scope="class"
)

@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestPassPointConnection(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_PassPointConnection_5g_WPA2_Personal(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobile_android):
        
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["5G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_PassPointConnection_2g_WPA2_Personal(self, setup_profile_data, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["2G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_PassPointConnection_5g_WPA(self, setup_profile_data, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobile_android, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_PassPointConnection_2g_WPA(self, setup_profile_data, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        
        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

         #Set Wifi/AP Mode
        set_APconnMobileDevice_android(ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Verify Upload download Speed from device Selection
        assert verifyUploadDownloadSpeed_android(setup_perfectoMobile_android, connData)

        #Toggle Wifi Mode
        assert Toggle_WifiMode_android(setup_perfectoMobile_android, ssidName, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobile_android, ssidName, connData)