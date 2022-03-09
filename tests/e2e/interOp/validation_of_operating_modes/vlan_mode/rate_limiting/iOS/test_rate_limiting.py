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
import random
import string
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    return_upload_download_speed_iOS, get_ip_address_ios, wifi_connect, wifi_disconnect_and_forget

pytestmark = [pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.rate_limiting, pytest.mark.vlan]
setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa2_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ],
        "wpa": [
            {"ssid_name": "ssid_wpa_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ],
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa3_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ]
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


@allure.feature("VLAN MODE Rate Limiting")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRateLimitingVLAN(object):


    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_rate_limiting_wpa2_2g(self, request, get_vif_state, get_ap_logs,
                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_rate_limiting_wpa2_5g(self, request, get_vif_state, get_ap_logs,
                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_rate_limiting_wpa_2g(self, request, get_vif_state, get_ap_logs,
                                  get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_rate_limiting_wpa_5g(self, request, get_vif_state, get_ap_logs,
                                  get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    def test_rate_limiting_wpa3_2g(self, request, get_vif_state, get_ap_logs,
                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    def test_rate_limiting_wpa3_5g(self, request, get_vif_state, get_ap_logs,
                                   get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        print("Upload rate:" + (str)(up_rate))
        print("Download rate:" + (str)(down_rate))
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        down_speed, up_speed = return_upload_download_speed_iOS(request, setup_perfectoMobile_iOS, connData)
        wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        print(down_speed, up_speed)
        if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
            assert True
        else:
            assert False