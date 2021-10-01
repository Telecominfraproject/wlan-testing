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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios, pytest.mark.expressWifiConnection]

from iOS_lib import closeApp, ForgetWifiConnection, set_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, verifyUploadDownloadSpeediOS, expressWifi


class TestExpressWifi(object):

    def test_ExpressWifi(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):

        ssidName = "XWF-OWF_DSx"
        ssidPassword = ""
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        #Express Wifi
        expressWifi(request, setup_perfectoMobile_iOS, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

  
    
