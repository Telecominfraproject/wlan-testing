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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.interop_ios, pytest.mark.ClientConnectivity]

from iOS_lib import closeApp, openApp, verifyUploadDownloadSpeediOS, ForgetWifiConnection, Toggle_AirplaneMode_iOS, \
    set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeMode(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ClientConnectivity_5g_WPA2_Personal_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                                 setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ClientConnectivity_2g_WPA2_Personal_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                                 setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ClientConnectivity_2g_WPA_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                       setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ClientConnectivity_5g_WPA_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                       setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.twog
    @pytest.mark.open
    def test_ClientConnectivity_2g_OPEN_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                       setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)

    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ClientConnectivity_5g_OPEN_Bridge(self, request, get_vif_state, get_APToMobileDevice_data,
                                       setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        # Verify Upload download Speed from device Selection
        verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)

        # ForgetWifi
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, ssidName, connData)