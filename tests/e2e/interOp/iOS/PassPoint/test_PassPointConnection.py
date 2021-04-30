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

from urllib3 import exceptions

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from iOS_lib import closeApp, openApp, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

@pytest.mark.PassPointConnection
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

    def test_PassPointConnection_Mobile(self,setup_profile_data, setup_perfectoMobile_iOS, get_PassPointConniOS_data):
        
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]
        ssidName = profile_data["ssid_name"]
        security_key = profile_data["security_key"]

        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]
        ssidPassword = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
      
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_PassPointConniOS_data

        #Set Wifi Access Mode to #Default-SSID-5gl-perfecto-b/#Default-SSID-2gl-perfecto-b
        set_APconnMobileDevice_iOS(ssidName, setup_perfectoMobile_iOS, connData)

        #Toggle Airplane Mode and Ensure Wifi Connection. 
        Toggle_AirplaneMode_iOS(setup_perfectoMobile_iOS, connData)

        #Close Settings App
        closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile_iOS)

    