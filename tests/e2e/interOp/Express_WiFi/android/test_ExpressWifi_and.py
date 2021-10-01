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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_android, pytest.mark.expressWifiConnection]

from android_lib import set_APconnMobileDevice_android, ForgetWifiConnection, expressWifi


class TestExpressWifiAndroid(object):

    def test_ExpressWifi_Android(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

        ssidName = "XWF-OWF_DSx"
        ssidPassword = ""
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Express Wifi
        expressWifi(request, setup_perfectoMobile_android, connData)

        #ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_android, ssidName, connData)

  
    
