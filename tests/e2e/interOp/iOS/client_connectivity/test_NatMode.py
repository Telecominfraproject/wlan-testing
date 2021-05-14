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
#pytestmark = [pytest.mark.ClientConnectivity, pytest.mark.nat, pytest.mark.interop]

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from iOS_lib import closeApp, openApp, verifyUploadDownloadSpeediOS, ForgetWifiConnection, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

@pytest.mark.ClientConnectivity
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
class TestNatMode(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ClientConnectivity_5g_WPA2_Personal(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobile_iOS):
        
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["5G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        #Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(setup_perfectoMobile_iOS, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ClientConnectivity_2g_WPA2_Personal(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobileWeb):
            
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["2G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobileWeb[1]
        driver = setup_perfectoMobileWeb[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(ssidName, ssidPassword, setup_perfectoMobileWeb, connData)

        #Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(setup_perfectoMobileWeb, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobileWeb, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ClientConnectivity_2g_WPA(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobileWeb):
            
        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobileWeb[1]
        driver = setup_perfectoMobileWeb[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(ssidName, ssidPassword, setup_perfectoMobileWeb, connData)

        #Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(setup_perfectoMobileWeb, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobileWeb, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ClientConnectivity_5g_WPA(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobileWeb):
            
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]  
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobileWeb[1]
        driver = setup_perfectoMobileWeb[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(ssidName, ssidPassword, setup_perfectoMobileWeb, connData)

        #Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(setup_perfectoMobileWeb, connData)

        #ForgetWifi
        ForgetWifiConnection(setup_perfectoMobileWeb, ssidName, connData)