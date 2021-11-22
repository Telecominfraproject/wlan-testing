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
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    verifyUploadDownloadSpeediOS, get_ip_address_ios, captive_portal, wifi_disconnect_and_forget

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.client_connectivity, pytest.mark.interop_uc_sanity, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "lanforge": [{"ssid_name": "lanforge", "appliedRadios": ["2G,5G"]},
                 {"ssid_name": "lanforge", "appliedRadios": ["5G"]}]},
    "rf": {},
    "radius": False
}


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode Client Connectivity : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("BRIDGE MODE CLIENT CAPTIVE PORTAL")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
#@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeCaptivePortalSuiteOneBridge(object):
    """ Client Connectivity SuiteA
        pytest -m "captive portal and bridge and InteropsuiteA"
    """
    @pytest.mark.sg345
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_Captive_Portal_Open_BRIDGE(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                               setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["lanforge"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            captive_portal(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False
    #
    # @pytest.mark.twog
    # @pytest.mark.open
    # def test_Captive_Portal_2g_Open_BRIDGE(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
    #                                            setup_perfectoMobile_iOS):
    #
    #     profile_data = setup_params_general["ssid_modes"]["open"][0]
    #     ssidName = profile_data["ssid_name"]
    #     ssidPassword = "[BLANK]"
    #     print("SSID_NAME: " + ssidName)
    #     print("SSID_PASS: " + ssidPassword)
    #     get_vif_state.append(ssidName)
    #     if ssidName not in get_vif_state:
    #         allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
    #         pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
    #
    #     report = setup_perfectoMobile_iOS[1]
    #     driver = setup_perfectoMobile_iOS[0]
    #     connData = get_APToMobileDevice_data
    #
    #     # Set Wifi/AP Mode
    #     ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
    #     if is_internet:
    #         if ip:
    #             text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
    #         else:
    #             text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
    #         print(text_body)
    #         allure.attach(name="Connection Status: ", body=str(text_body))
    #
    #         captive_portal(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
    #         assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
    #         wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
    #     else:
    #         allure.attach(name="Connection Status: ", body=str("No Internet access"))
    #         assert False
