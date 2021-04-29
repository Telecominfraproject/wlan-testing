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
from urllib3 import exceptions
from conftest import closeApp, openApp, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, tearDown
#from conftest import 

class TestPassPointConnection(object):

    #@pytest.mark.sanity
    #@pytest.mark.wpa2_personal
    #@pytest.mark.VerifyApTo_MobileDeviceWeb
    #@pytest.mark.parametrize('bundleID-iOS', [net.techet.netanalyzerlite])
    def test_PassPointConnection_Mobile(self, setup_perfectoMobile_iOS, get_PassPointConniOS_data):
        
        #bundleId-iOS=net.techet.netanalyzerlite
        #Wifi-5G or 2G Verification
        try:
            report = setup_perfectoMobile_iOS[1]
            driver = setup_perfectoMobile_iOS[0]
            connData = get_PassPointConniOS_data

            #Set Wifi Access Mode to #Default-SSID-5gl-perfecto-b/#Default-SSID-2gl-perfecto-b
            set_APconnMobileDevice_iOS("Default-SSID-5gl-perfecto-b", setup_perfectoMobile_iOS, get_PassPointConniOS_data)

            #Toggle Airplane Mode and Ensure Wifi Connection. 
            Toggle_AirplaneMode_iOS(setup_perfectoMobile_iOS, get_PassPointConniOS_data)

            #Close Settings App
            closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile_iOS)

        except exceptions as e:
            print (e.message)
            tearDown(setup_perfectoMobile_iOS)
           
        #except exception as ex