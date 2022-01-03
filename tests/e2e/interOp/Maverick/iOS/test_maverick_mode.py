from logging import exception
import io
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

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown, \
    verifyUploadDownloadSpeediOS, get_ip_address_ios, set_maverick_ios, verifyMaverickWebpageiOS

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.client_connect, pytest.mark.interop_uc_sanity, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "Maverick", "appliedRadios": ["2G"]}]},
    "rf": {},
    "radius": False
}


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Maverick Mode Client Connect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("MAVERICK MODE")
# @pytest.mark.parametrize(
#     'set_maverick_mode_all',
#     # [setup_params_general],
#     indirect=True,
#     scope="class"
# )

class TestMavericMode(object):

    @pytest.mark.maverick123
    def test_Maverick(self, request, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS,
                      set_maverick_mode_all):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Get Maverick Mode
        set_maverick_ios(request, ssidName, setup_perfectoMobile_iOS, connData)

        # Verify Maverick Webpage
        verifyMaverickWebpageiOS(request, setup_perfectoMobile_iOS, get_APToMobileDevice_data)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)
