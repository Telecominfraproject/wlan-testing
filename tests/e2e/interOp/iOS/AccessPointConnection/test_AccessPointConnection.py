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

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ping_deftapps_iOS, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

@pytest.mark.TestPassPointConnectivetyIOS
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
class TestPassPointConnectivetyIOS(object):

    def test_AccessPointConnection(self, setup_profile_data, get_AccessPointConn_data, setup_perfectoMobile_iOS):
        
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]  
        #profile_data = setup_profile_data["NAT"]["WPA"]["2G"]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
      
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_AccessPointConn_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(ssidName, setup_perfectoMobile_iOS, connData)

        #Need An ip To ping
        wifi_ip = get_WifiIPAddress_iOS(setup_perfectoMobile_iOS, connData)

        #Open Ping Application
        openApp(connData["bundleId-iOS-Ping"], setup_perfectoMobile_iOS)

        ping_deftapps_iOS(setup_perfectoMobile_iOS, wifi_ip)
