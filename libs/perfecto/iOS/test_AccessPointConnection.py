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
from conftest import closeApp, openApp, ping_deftapps_iOS, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, get_WifiIPAddress_iOS
#from conftest import 

class TestAccessPointConnection(object):

    #@pytest.mark.sanity
    #@pytest.mark.wpa2_personal
    #@pytest.mark.VerifyApTo_MobileDeviceWeb
    #@pytest.mark.parametrize('bundleID-iOS', [net.techet.netanalyzerlite])
    def test_AccessPointConnection(self, get_AccessPointConn_data, setup_perfectoMobile_iOS):
        
        try:
            report = setup_perfectoMobile_iOS[1]
            driver = setup_perfectoMobile_iOS[0]
            connData = get_AccessPointConn_data

            #Set Wifi/AP Mode
            set_APconnMobileDevice_iOS(connData["Default-SSID-perfecto-b"], setup_perfectoMobile_iOS, connData)

            #Need An ip To ping
            wifi_ip = get_WifiIPAddress_iOS(setup_perfectoMobile_iOS, connData)

            #Open Ping Application
            openApp(connData["bundleId-iOS-Ping"], setup_perfectoMobile_iOS)

            ping_deftapps_iOS(setup_perfectoMobile_iOS, wifi_ip)



            #Toggle AirplaneMode
            #Toggle_AirplaneMode_iOS(setup_perfectoMobile_iOS, get_ToggleAirplaneMode_data)
       
            #Verify AP After AirplaneMode
            #assert verify_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, get_ToggleAirplaneMode_data)
         

        except NoSuchElementException as ex:
            self.currentResult = False
            #report.test_stop(TestResultFactory.create_failure("NoSuchElementException", ex))
            print (ex.message)
            self.currentResult = True
     