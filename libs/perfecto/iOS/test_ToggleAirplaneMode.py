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
from conftest import closeApp, openApp, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, tearDown
#from conftest import 

class TestToggleAirplaneMode(object):

    #@pytest.mark.sanity
    #@pytest.mark.wpa2_personal
    #@pytest.mark.VerifyApTo_MobileDeviceWeb
    #@pytest.mark.parametrize('bundleID-iOS', [net.techet.netanalyzerlite])
    def test_ToogleAirplaneMode(self, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        
        try:
            report = setup_perfectoMobile_iOS[1]
            driver = setup_perfectoMobile_iOS[0]
            connData = get_ToggleAirplaneMode_data

            #Set Wifi/AP Mode
            set_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, get_ToggleAirplaneMode_data)

            #Toggle AirplaneMode
            Toggle_AirplaneMode_iOS(setup_perfectoMobile_iOS, get_ToggleAirplaneMode_data)
       
            #Verify AP After AirplaneMode
            assert verify_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, get_ToggleAirplaneMode_data)
         

        except exception as e:
            print (e.message)
            tearDown(setup_perfectoMobile_iOS)
     