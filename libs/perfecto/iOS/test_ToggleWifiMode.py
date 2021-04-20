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
from conftest import closeApp, openApp, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS
#from conftest import 

class TestToggleAirplaneMode(object):

    #@pytest.mark.sanity
    #@pytest.mark.wpa2_personal
    #@pytest.mark.VerifyApTo_MobileDeviceWeb
    #@pytest.mark.parametrize('bundleID-iOS', [net.techet.netanalyzerlite])
    def test_ToogleWifiMode(self, get_ToggleWifiMode_data, setup_perfectoMobile_iOS):
        
        try:
            report = setup_perfectoMobile_iOS[1]
            driver = setup_perfectoMobile_iOS[0]
            connData = get_ToggleWifiMode_data

            #Set Wifi/AP Mode
            set_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, get_ToggleWifiMode_data)

            #Toggle WifiMode
            Toggle_WifiMode_iOS(setup_perfectoMobile_iOS, get_ToggleWifiMode_data)
       
            #Verify AP After AirplaneMode
            value = verify_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, connData)
            assert value
           

        except NoSuchElementException as ex:
            assert False
            print (ex.message)
          
     