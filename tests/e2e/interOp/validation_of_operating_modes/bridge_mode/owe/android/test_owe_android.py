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
import random
import sys
import allure
import string

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and,
              pytest.mark.OWE, pytest.mark.bridge]

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_and, wifi_connect, wifi_disconnect_and_forget
setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "owe": [
            {"ssid_name": "OWE_Enhanced_2G",
             "appliedRadios": ["2G"],
             "ieee80211w": "required"
             },
            {"ssid_name": "OWE_Enhanced_5G",
             "appliedRadios": ["5G"],
             "ieee80211w": "required"
             }
        ],
    },
    "rf": {},
    "radius": False
}

for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.feature("Bridge MODE OWE")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestOWEBridge(object):

    @pytest.mark.twog
    @pytest.mark.ow_sanity_interop
    def test_owe_android_2g(self, request, get_vif_state, get_ap_logs,
                               get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["owe"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.fiveg
    @pytest.mark.ow_sanity_interop
    @pytest.mark.owe
    def test_owe_android_5g(self, request, get_vif_state, get_ap_logs,
                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["owe"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        ip, is_internet = get_ip_address_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False



