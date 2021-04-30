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

from iOS_lib import closeApp, openApp, verifyUploadDownloadSpeediOS, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

@pytest.mark.APToMobileDevice
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
class TestVerifyAPToMobileDevice(object):

    def test_VerifyApTo_MobileDeviceWeb(self, setup_profile_data, get_APToMobileDevice_data, setup_perfectoMobileWeb):
        
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]
        ssidName = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]
        ssidPassword = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
      
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobileWeb[1]
        driver = setup_perfectoMobileWeb[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobileWeb, connData)

        #Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(setup_perfectoMobileWeb, connData)

        
        
      
     