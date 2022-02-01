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

from android_lib import set_APconnMobileDevice_android, ForgetWifiConnection, expressWifi, wifi_connect, wifi_disconnect_and_forget

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "XWF-OWF_DSx", "appliedRadios": ["2G"]}]
    },
    "rf": {},
    "radius": False,
    "express-wifi": True
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestExpressWifiAndroid(object):

    @pytest.mark.twog
    @pytest.mark.open
    def test_ExpressWifi_Android(self, request, get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = ""
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        #Set Wifi/AP Mode
        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        #Express Wifi
        if expressWifi(request, ssidName, setup_perfectoMobile_android, connData):
            assert True
        else:
            assert False
        #ForgetWifi
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

  
    
