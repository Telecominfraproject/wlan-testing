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

pytestmark = [pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and
              ,pytest.mark.multi_psk, pytest.mark.bridge]

from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_and, verifyUploadDownloadSpeed_android, wifi_connect, wifi_disconnect_and_forget

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa": [
            {"ssid_name": "ssid_2g_mpsk",
             "appliedRadios": ["2G"],
             "security": "psk",
             "security_key": "something",
             "multi-psk": [
                 {
                     "key": "lanforge1",
                     "vlan-id": 100
                 },
                 {
                     "key": "lanforge2",
                     "vlan-id": 150
                 },
                 {
                     "key": "lanforge3",
                     "vlan-id": 200
                 },
                 {
                     "key": "lanforge4",
                     "vlan-id": 250
                 },
                 {
                     "key": "lanforge5",
                     "vlan-id": 300
                 },
                 {
                     "key": "lanforge6",
                     "vlan-id": 350
                 },
                 {
                     "key": "lanforge7",
                     "vlan-id": 400
                 },
                 {
                     "key": "lanforge8",
                     "vlan-id": 450
                 },
                 {
                     "key": "lanforge9",
                     "vlan-id": 500
                 },
                 {
                     "key": "lanforge10",
                     "vlan-id": 550
                 },
                 {
                     "key": "lanforge11",
                     "vlan-id": 600
                 },
                 {
                     "key": "lanforge12",
                     "vlan-id": 650
                 },
                 {
                     "key": "lanforge13",
                     "vlan-id": 700
                 },
                 {
                     "key": "lanforge14",
                     "vlan-id": 750
                 },
                 {
                     "key": "lanforge15",
                     "vlan-id": 800
                 },
                 {
                     "key": "lanforge16",
                     "vlan-id": 850
                 }
             ],
             },
            {"ssid_name": "ssid_5g_mpsk",
             "appliedRadios": ["5G"],
             "security": "psk",
             "security_key": "something",
             "multi-psk": [
                 {
                     "key": "lanforge1",
                     "vlan-id": 100
                 },
                 {
                     "key": "lanforge2",
                     "vlan-id": 150
                 },
                 {
                     "key": "lanforge3",
                     "vlan-id": 200
                 },
                 {
                     "key": "lanforge4",
                     "vlan-id": 250
                 },
                 {
                     "key": "lanforge5",
                     "vlan-id": 300
                 },
                 {
                     "key": "lanforge6",
                     "vlan-id": 350
                 },
                 {
                     "key": "lanforge7",
                     "vlan-id": 400
                 },
                 {
                     "key": "lanforge8",
                     "vlan-id": 450
                 },
                 {
                     "key": "lanforge9",
                     "vlan-id": 500
                 },
                 {
                     "key": "lanforge10",
                     "vlan-id": 550
                 },
                 {
                     "key": "lanforge11",
                     "vlan-id": 600
                 },
                 {
                     "key": "lanforge12",
                     "vlan-id": 650
                 },
                 {
                     "key": "lanforge13",
                     "vlan-id": 700
                 },
                 {
                     "key": "lanforge14",
                     "vlan-id": 750
                 },
                 {
                     "key": "lanforge15",
                     "vlan-id": 800
                 },
                 {
                     "key": "lanforge16",
                     "vlan-id": 850
                 }
             ],
             }
            ]},
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.feature("BRIDGE MODE Multi PSK")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultipskBridge(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_multi_psk_wpa_2g_2vlans(self, request, get_vif_state, get_ap_logs, lf_tools, get_configuration,
                            get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        print(vlan1)
        print(vlan2)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1."+ str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1."+ str(vlan2))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_multi_psk_wpa_5g_2vlans(self, request, get_vif_state, get_ap_logs, lf_tools,
                            get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        print(vlan1)
        print(vlan2)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    #-------------4 Vlans----------------------------------
    @pytest.mark.wpa
    @pytest.mark.twog
    def test_multi_psk_wpa_2g_4vlans(self, request, get_vif_state, get_ap_logs, lf_tools, get_configuration,
                                      get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_multi_psk_wpa_5g_4vlans(self, request, get_vif_state, get_ap_logs, lf_tools,
                                      get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    # -------------8 Vlans----------------------------------
    @pytest.mark.wpa
    @pytest.mark.twog
    def test_multi_psk_wpa_2g_8vlans(self, request, get_vif_state, get_ap_logs, lf_tools, get_configuration,
                                      get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        key5 = profile_data["multi-psk"][4]["key"]
        key6 = profile_data["multi-psk"][5]["key"]
        key7 = profile_data["multi-psk"][6]["key"]
        key8 = profile_data["multi-psk"][7]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        vlan5 = profile_data["multi-psk"][4]["vlan-id"]
        vlan6 = profile_data["multi-psk"][5]["vlan-id"]
        vlan7 = profile_data["multi-psk"][6]["vlan-id"]
        vlan8 = profile_data["multi-psk"][7]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        print(vlan5)
        print(vlan6)
        print(vlan7)
        print(vlan8)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        vlan_ip5 = lf_tools.json_get("/port/1/1/eth1." + str(vlan5))["interface"]["ip"]
        vlan_ip6 = lf_tools.json_get("/port/1/1/eth1." + str(vlan6))["interface"]["ip"]
        vlan_ip7 = lf_tools.json_get("/port/1/1/eth1." + str(vlan7))["interface"]["ip"]
        vlan_ip8 = lf_tools.json_get("/port/1/1/eth1." + str(vlan8))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print(vlan_ip5)
        print(vlan_ip6)
        print(vlan_ip7)
        print(vlan_ip8)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip5, is_internet5 = get_ip_address_and(request, ssidName, key5, setup_perfectoMobile_android, connData)
        #
        if ip5:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip5 = ip5.split(".")
            vlan_ip5 = vlan_ip5.split(".")
            print(ip5[:2], vlan_ip5[:2])
            for i, j in zip(ip5[:2], vlan_ip5[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip6, is_internet6 = get_ip_address_and(request, ssidName, key6, setup_perfectoMobile_android, connData)
        #
        if ip6:
            if is_internet6:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip6 = ip6.split(".")
            vlan_ip6 = vlan_ip6.split(".")
            print(ip6[:2], vlan_ip6[:2])
            for i, j in zip(ip6[:2], vlan_ip6[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip7, is_internet7 = get_ip_address_and(request, ssidName, key7, setup_perfectoMobile_android, connData)
        #
        if ip7:
            if is_internet7:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip7 = ip7.split(".")
            vlan_ip7 = vlan_ip7.split(".")
            print(ip7[:2], vlan_ip7[:2])
            for i, j in zip(ip7[:2], vlan_ip7[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip8, is_internet8 = get_ip_address_and(request, ssidName, key8, setup_perfectoMobile_android, connData)
        #
        if ip8:
            if is_internet8:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip8 = ip8.split(".")
            vlan_ip8 = vlan_ip8.split(".")
            print(ip8[:2], vlan_ip8[:2])
            for i, j in zip(ip8[:2], vlan_ip8[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_multi_psk_wpa_5g_8vlans(self, request, get_vif_state, get_ap_logs, lf_tools,
                                      get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        key5 = profile_data["multi-psk"][4]["key"]
        key6 = profile_data["multi-psk"][5]["key"]
        key7 = profile_data["multi-psk"][6]["key"]
        key8 = profile_data["multi-psk"][7]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        vlan5 = profile_data["multi-psk"][4]["vlan-id"]
        vlan6 = profile_data["multi-psk"][5]["vlan-id"]
        vlan7 = profile_data["multi-psk"][6]["vlan-id"]
        vlan8 = profile_data["multi-psk"][7]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        print(vlan5)
        print(vlan6)
        print(vlan7)
        print(vlan8)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        vlan_ip5 = lf_tools.json_get("/port/1/1/eth1." + str(vlan5))["interface"]["ip"]
        vlan_ip6 = lf_tools.json_get("/port/1/1/eth1." + str(vlan6))["interface"]["ip"]
        vlan_ip7 = lf_tools.json_get("/port/1/1/eth1." + str(vlan7))["interface"]["ip"]
        vlan_ip8 = lf_tools.json_get("/port/1/1/eth1." + str(vlan8))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print(vlan_ip5)
        print(vlan_ip6)
        print(vlan_ip7)
        print(vlan_ip8)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip5, is_internet5 = get_ip_address_and(request, ssidName, key5, setup_perfectoMobile_android, connData)
        #
        if ip5:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip5 = ip5.split(".")
            vlan_ip5 = vlan_ip5.split(".")
            print(ip5[:2], vlan_ip5[:2])
            for i, j in zip(ip5[:2], vlan_ip5[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip6, is_internet6 = get_ip_address_and(request, ssidName, key6, setup_perfectoMobile_android, connData)
        #
        if ip6:
            if is_internet6:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip6 = ip6.split(".")
            vlan_ip6 = vlan_ip6.split(".")
            print(ip6[:2], vlan_ip6[:2])
            for i, j in zip(ip6[:2], vlan_ip6[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip7, is_internet7 = get_ip_address_and(request, ssidName, key7, setup_perfectoMobile_android, connData)
        #
        if ip7:
            if is_internet7:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip7 = ip7.split(".")
            vlan_ip7 = vlan_ip7.split(".")
            print(ip7[:2], vlan_ip7[:2])
            for i, j in zip(ip7[:2], vlan_ip7[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip8, is_internet8 = get_ip_address_and(request, ssidName, key8, setup_perfectoMobile_android, connData)
        #
        if ip8:
            if is_internet8:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip8 = ip8.split(".")
            vlan_ip8 = vlan_ip8.split(".")
            print(ip8[:2], vlan_ip8[:2])
            for i, j in zip(ip8[:2], vlan_ip8[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    # -------------16 Vlans----------------------------------
    @pytest.mark.wpa
    @pytest.mark.twog
    def test_multi_psk_wpa_2g_16vlans(self, request, get_vif_state, get_ap_logs, lf_tools, get_configuration,
                                      get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        key5 = profile_data["multi-psk"][4]["key"]
        key6 = profile_data["multi-psk"][5]["key"]
        key7 = profile_data["multi-psk"][6]["key"]
        key8 = profile_data["multi-psk"][7]["key"]
        key9 = profile_data["multi-psk"][8]["key"]
        key10 = profile_data["multi-psk"][9]["key"]
        key11 = profile_data["multi-psk"][10]["key"]
        key12 = profile_data["multi-psk"][11]["key"]
        key13 = profile_data["multi-psk"][12]["key"]
        key14 = profile_data["multi-psk"][13]["key"]
        key15 = profile_data["multi-psk"][14]["key"]
        key16 = profile_data["multi-psk"][15]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        vlan5 = profile_data["multi-psk"][4]["vlan-id"]
        vlan6 = profile_data["multi-psk"][5]["vlan-id"]
        vlan7 = profile_data["multi-psk"][6]["vlan-id"]
        vlan8 = profile_data["multi-psk"][7]["vlan-id"]
        vlan9 = profile_data["multi-psk"][8]["vlan-id"]
        vlan10 = profile_data["multi-psk"][9]["vlan-id"]
        vlan11 = profile_data["multi-psk"][10]["vlan-id"]
        vlan12 = profile_data["multi-psk"][11]["vlan-id"]
        vlan13 = profile_data["multi-psk"][12]["vlan-id"]
        vlan14 = profile_data["multi-psk"][13]["vlan-id"]
        vlan15 = profile_data["multi-psk"][14]["vlan-id"]
        vlan16 = profile_data["multi-psk"][15]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        print(vlan5)
        print(vlan6)
        print(vlan7)
        print(vlan8)
        print(vlan9)
        print(vlan10)
        print(vlan11)
        print(vlan12)
        print(vlan13)
        print(vlan14)
        print(vlan15)
        print(vlan16)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        vlan_ip5 = lf_tools.json_get("/port/1/1/eth1." + str(vlan5))["interface"]["ip"]
        vlan_ip6 = lf_tools.json_get("/port/1/1/eth1." + str(vlan6))["interface"]["ip"]
        vlan_ip7 = lf_tools.json_get("/port/1/1/eth1." + str(vlan7))["interface"]["ip"]
        vlan_ip8 = lf_tools.json_get("/port/1/1/eth1." + str(vlan8))["interface"]["ip"]
        vlan_ip9 = lf_tools.json_get("/port/1/1/eth1." + str(vlan9))["interface"]["ip"]
        vlan_ip10 = lf_tools.json_get("/port/1/1/eth1." + str(vlan10))["interface"]["ip"]
        vlan_ip11 = lf_tools.json_get("/port/1/1/eth1." + str(vlan11))["interface"]["ip"]
        vlan_ip12 = lf_tools.json_get("/port/1/1/eth1." + str(vlan12))["interface"]["ip"]
        vlan_ip13 = lf_tools.json_get("/port/1/1/eth1." + str(vlan13))["interface"]["ip"]
        vlan_ip14 = lf_tools.json_get("/port/1/1/eth1." + str(vlan14))["interface"]["ip"]
        vlan_ip15 = lf_tools.json_get("/port/1/1/eth1." + str(vlan15))["interface"]["ip"]
        vlan_ip16 = lf_tools.json_get("/port/1/1/eth1." + str(vlan16))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print(vlan_ip5)
        print(vlan_ip6)
        print(vlan_ip7)
        print(vlan_ip8)
        print(vlan_ip9)
        print(vlan_ip10)
        print(vlan_ip11)
        print(vlan_ip12)
        print(vlan_ip13)
        print(vlan_ip14)
        print(vlan_ip15)
        print(vlan_ip16)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip5, is_internet5 = get_ip_address_and(request, ssidName, key5, setup_perfectoMobile_android, connData)
        #
        if ip5:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip5 = ip5.split(".")
            vlan_ip5 = vlan_ip5.split(".")
            print(ip5[:2], vlan_ip5[:2])
            for i, j in zip(ip5[:2], vlan_ip5[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip6, is_internet6 = get_ip_address_and(request, ssidName, key6, setup_perfectoMobile_android, connData)
        #
        if ip6:
            if is_internet6:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip6 = ip6.split(".")
            vlan_ip6 = vlan_ip6.split(".")
            print(ip6[:2], vlan_ip6[:2])
            for i, j in zip(ip6[:2], vlan_ip6[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip7, is_internet7 = get_ip_address_and(request, ssidName, key7, setup_perfectoMobile_android, connData)
        #
        if ip7:
            if is_internet7:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip7 = ip7.split(".")
            vlan_ip7 = vlan_ip7.split(".")
            print(ip7[:2], vlan_ip7[:2])
            for i, j in zip(ip7[:2], vlan_ip7[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip8, is_internet8 = get_ip_address_and(request, ssidName, key8, setup_perfectoMobile_android, connData)
        #
        if ip8:
            if is_internet8:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip8 = ip8.split(".")
            vlan_ip8 = vlan_ip8.split(".")
            print(ip8[:2], vlan_ip8[:2])
            for i, j in zip(ip8[:2], vlan_ip8[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip9, is_internet9 = get_ip_address_and(request, ssidName, key9, setup_perfectoMobile_android, connData)
        #
        if ip9:
            if is_internet9:
                text_body = ("connected to " + ssidName + " (" + ip9 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip9 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip9 = ip9.split(".")
            vlan_ip = vlan_ip9.split(".")
            print(ip9[:2], vlan_ip9[:2])
            for i, j in zip(ip9[:2], vlan_ip9[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip10, is_internet10 = get_ip_address_and(request, ssidName, key10, setup_perfectoMobile_android, connData)
        #
        if ip10:
            if is_internet10:
                text_body = ("connected to " + ssidName + " (" + ip10 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip10 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip10 = ip10.split(".")
            vlan_ip10 = vlan_ip10.split(".")
            print(ip10[:2], vlan_ip10[:2])
            for i, j in zip(ip10[:2], vlan_ip10[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip11, is_internet11 = get_ip_address_and(request, ssidName, key11, setup_perfectoMobile_android, connData)
        #
        if ip11:
            if is_internet11:
                text_body = ("connected to " + ssidName + " (" + ip11 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip11 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip11 = ip11.split(".")
            vlan_ip11 = vlan_ip11.split(".")
            print(ip11[:2], vlan_ip11[:2])
            for i, j in zip(ip11[:2], vlan_ip11[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip12, is_internet12 = get_ip_address_and(request, ssidName, key12, setup_perfectoMobile_android, connData)
        #
        if ip12:
            if is_internet12:
                text_body = ("connected to " + ssidName + " (" + ip12 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip12 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip12 = ip12.split(".")
            vlan_ip12 = vlan_ip12.split(".")
            print(ip12[:2], vlan_ip12[:2])
            for i, j in zip(ip12[:2], vlan_ip12[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip13, is_internet13 = get_ip_address_and(request, ssidName, key13, setup_perfectoMobile_android, connData)
        #
        if ip13:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip13 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip13 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip13 = ip13.split(".")
            vlan_ip13 = vlan_ip13.split(".")
            print(ip13[:2], vlan_ip13[:2])
            for i, j in zip(ip13[:2], vlan_ip13[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip14, is_internet14 = get_ip_address_and(request, ssidName, key14, setup_perfectoMobile_android, connData)
        #
        if ip14:
            if is_internet14:
                text_body = ("connected to " + ssidName + " (" + ip14 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip14 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip14 = ip14.split(".")
            vlan_ip14 = vlan_ip14.split(".")
            print(ip14[:2], vlan_ip14[:2])
            for i, j in zip(ip14[:2], vlan_ip14[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip15, is_internet15 = get_ip_address_and(request, ssidName, key15, setup_perfectoMobile_android, connData)
        #
        if ip15:
            if is_internet15:
                text_body = ("connected to " + ssidName + " (" + ip15 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip15 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip15 = ip15.split(".")
            vlan_ip15 = vlan_ip15.split(".")
            print(ip15[:2], vlan_ip15[:2])
            for i, j in zip(ip15[:2], vlan_ip15[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip16, is_internet16 = get_ip_address_and(request, ssidName, key16, setup_perfectoMobile_android, connData)
        #
        if ip16:
            if is_internet16:
                text_body = ("connected to " + ssidName + " (" + ip16 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip16 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip16 = ip16.split(".")
            vlan_ip16 = vlan_ip16.split(".")
            print(ip16[:2], vlan_ip16[:2])
            for i, j in zip(ip16[:2], vlan_ip16[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_multi_psk_wpa_5g_16vlans(self, request, get_vif_state, get_ap_logs, lf_tools, get_configuration,
                                       get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        key1 = profile_data["multi-psk"][0]["key"]
        key2 = profile_data["multi-psk"][1]["key"]
        key3 = profile_data["multi-psk"][2]["key"]
        key4 = profile_data["multi-psk"][3]["key"]
        key5 = profile_data["multi-psk"][4]["key"]
        key6 = profile_data["multi-psk"][5]["key"]
        key7 = profile_data["multi-psk"][6]["key"]
        key8 = profile_data["multi-psk"][7]["key"]
        key9 = profile_data["multi-psk"][8]["key"]
        key10 = profile_data["multi-psk"][9]["key"]
        key11 = profile_data["multi-psk"][10]["key"]
        key12 = profile_data["multi-psk"][11]["key"]
        key13 = profile_data["multi-psk"][12]["key"]
        key14 = profile_data["multi-psk"][13]["key"]
        key15 = profile_data["multi-psk"][14]["key"]
        key16 = profile_data["multi-psk"][15]["key"]
        vlan1 = profile_data["multi-psk"][0]["vlan-id"]
        vlan2 = profile_data["multi-psk"][1]["vlan-id"]
        vlan3 = profile_data["multi-psk"][2]["vlan-id"]
        vlan4 = profile_data["multi-psk"][3]["vlan-id"]
        vlan5 = profile_data["multi-psk"][4]["vlan-id"]
        vlan6 = profile_data["multi-psk"][5]["vlan-id"]
        vlan7 = profile_data["multi-psk"][6]["vlan-id"]
        vlan8 = profile_data["multi-psk"][7]["vlan-id"]
        vlan9 = profile_data["multi-psk"][8]["vlan-id"]
        vlan10 = profile_data["multi-psk"][9]["vlan-id"]
        vlan11 = profile_data["multi-psk"][10]["vlan-id"]
        vlan12 = profile_data["multi-psk"][11]["vlan-id"]
        vlan13 = profile_data["multi-psk"][12]["vlan-id"]
        vlan14 = profile_data["multi-psk"][13]["vlan-id"]
        vlan15 = profile_data["multi-psk"][14]["vlan-id"]
        vlan16 = profile_data["multi-psk"][15]["vlan-id"]
        print(vlan1)
        print(vlan2)
        print(vlan3)
        print(vlan4)
        print(vlan5)
        print(vlan6)
        print(vlan7)
        print(vlan8)
        print(vlan9)
        print(vlan10)
        print(vlan11)
        print(vlan12)
        print(vlan13)
        print(vlan14)
        print(vlan15)
        print(vlan16)
        vlan_ip1 = lf_tools.json_get("/port/1/1/eth1." + str(vlan1))["interface"]["ip"]
        vlan_ip2 = lf_tools.json_get("/port/1/1/eth1." + str(vlan2))["interface"]["ip"]
        vlan_ip3 = lf_tools.json_get("/port/1/1/eth1." + str(vlan3))["interface"]["ip"]
        vlan_ip4 = lf_tools.json_get("/port/1/1/eth1." + str(vlan4))["interface"]["ip"]
        vlan_ip5 = lf_tools.json_get("/port/1/1/eth1." + str(vlan5))["interface"]["ip"]
        vlan_ip6 = lf_tools.json_get("/port/1/1/eth1." + str(vlan6))["interface"]["ip"]
        vlan_ip7 = lf_tools.json_get("/port/1/1/eth1." + str(vlan7))["interface"]["ip"]
        vlan_ip8 = lf_tools.json_get("/port/1/1/eth1." + str(vlan8))["interface"]["ip"]
        vlan_ip9 = lf_tools.json_get("/port/1/1/eth1." + str(vlan9))["interface"]["ip"]
        vlan_ip10 = lf_tools.json_get("/port/1/1/eth1." + str(vlan10))["interface"]["ip"]
        vlan_ip11 = lf_tools.json_get("/port/1/1/eth1." + str(vlan11))["interface"]["ip"]
        vlan_ip12 = lf_tools.json_get("/port/1/1/eth1." + str(vlan12))["interface"]["ip"]
        vlan_ip13 = lf_tools.json_get("/port/1/1/eth1." + str(vlan13))["interface"]["ip"]
        vlan_ip14 = lf_tools.json_get("/port/1/1/eth1." + str(vlan14))["interface"]["ip"]
        vlan_ip15 = lf_tools.json_get("/port/1/1/eth1." + str(vlan15))["interface"]["ip"]
        vlan_ip16 = lf_tools.json_get("/port/1/1/eth1." + str(vlan16))["interface"]["ip"]
        print(vlan_ip1)
        print(vlan_ip2)
        print(vlan_ip3)
        print(vlan_ip4)
        print(vlan_ip5)
        print(vlan_ip6)
        print(vlan_ip7)
        print(vlan_ip8)
        print(vlan_ip9)
        print(vlan_ip10)
        print(vlan_ip11)
        print(vlan_ip12)
        print(vlan_ip13)
        print(vlan_ip14)
        print(vlan_ip15)
        print(vlan_ip16)
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        ip1, is_internet1 = get_ip_address_and(request, ssidName, key1, setup_perfectoMobile_android, connData)
        #
        if ip1:
            if is_internet1:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip1 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip1 = ip1.split(".")
            vlan_ip1 = vlan_ip1.split(".")
            print(ip1[:2], vlan_ip1[:2])
            for i, j in zip(ip1[:2], vlan_ip1[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip2, is_internet2 = get_ip_address_and(request, ssidName, key2, setup_perfectoMobile_android, connData)
        #
        if ip2:
            if is_internet2:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip2 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip2 = ip2.split(".")
            vlan_ip2 = vlan_ip2.split(".")
            print(ip2[:2], vlan_ip2[:2])
            for i, j in zip(ip2[:2], vlan_ip2[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip3, is_internet3 = get_ip_address_and(request, ssidName, key3, setup_perfectoMobile_android, connData)
        #
        if ip3:
            if is_internet3:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip3 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip3 = ip3.split(".")
            vlan_ip3 = vlan_ip3.split(".")
            print(ip3[:2], vlan_ip3[:2])
            for i, j in zip(ip3[:2], vlan_ip3[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip4, is_internet4 = get_ip_address_and(request, ssidName, key4, setup_perfectoMobile_android, connData)
        #
        if ip4:
            if is_internet4:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip4 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip4 = ip4.split(".")
            vlan_ip4 = vlan_ip4.split(".")
            print(ip4[:2], vlan_ip4[:2])
            for i, j in zip(ip4[:2], vlan_ip4[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip5, is_internet5 = get_ip_address_and(request, ssidName, key5, setup_perfectoMobile_android, connData)
        #
        if ip5:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip5 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip5 = ip5.split(".")
            vlan_ip5 = vlan_ip5.split(".")
            print(ip5[:2], vlan_ip5[:2])
            for i, j in zip(ip5[:2], vlan_ip5[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip6, is_internet6 = get_ip_address_and(request, ssidName, key6, setup_perfectoMobile_android, connData)
        #
        if ip6:
            if is_internet6:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip6 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip6 = ip6.split(".")
            vlan_ip6 = vlan_ip6.split(".")
            print(ip6[:2], vlan_ip6[:2])
            for i, j in zip(ip6[:2], vlan_ip6[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip7, is_internet7 = get_ip_address_and(request, ssidName, key7, setup_perfectoMobile_android, connData)
        #
        if ip7:
            if is_internet7:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip7 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip7 = ip7.split(".")
            vlan_ip7 = vlan_ip7.split(".")
            print(ip7[:2], vlan_ip7[:2])
            for i, j in zip(ip7[:2], vlan_ip7[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip8, is_internet8 = get_ip_address_and(request, ssidName, key8, setup_perfectoMobile_android, connData)
        #
        if ip8:
            if is_internet8:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip8 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip8 = ip8.split(".")
            vlan_ip8 = vlan_ip8.split(".")
            print(ip8[:2], vlan_ip8[:2])
            for i, j in zip(ip8[:2], vlan_ip8[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip9, is_internet9 = get_ip_address_and(request, ssidName, key9, setup_perfectoMobile_android, connData)
        #
        if ip9:
            if is_internet9:
                text_body = ("connected to " + ssidName + " (" + ip9 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip9 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip9 = ip9.split(".")
            vlan_ip = vlan_ip9.split(".")
            print(ip9[:2], vlan_ip9[:2])
            for i, j in zip(ip9[:2], vlan_ip9[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip10, is_internet10 = get_ip_address_and(request, ssidName, key10, setup_perfectoMobile_android, connData)
        #
        if ip10:
            if is_internet10:
                text_body = ("connected to " + ssidName + " (" + ip10 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip10 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip10 = ip10.split(".")
            vlan_ip10 = vlan_ip10.split(".")
            print(ip10[:2], vlan_ip10[:2])
            for i, j in zip(ip10[:2], vlan_ip10[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip11, is_internet11 = get_ip_address_and(request, ssidName, key11, setup_perfectoMobile_android, connData)
        #
        if ip11:
            if is_internet11:
                text_body = ("connected to " + ssidName + " (" + ip11 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip11 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip11 = ip11.split(".")
            vlan_ip11 = vlan_ip11.split(".")
            print(ip11[:2], vlan_ip11[:2])
            for i, j in zip(ip11[:2], vlan_ip11[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip12, is_internet12 = get_ip_address_and(request, ssidName, key12, setup_perfectoMobile_android, connData)
        #
        if ip12:
            if is_internet12:
                text_body = ("connected to " + ssidName + " (" + ip12 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip12 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip12 = ip12.split(".")
            vlan_ip12 = vlan_ip12.split(".")
            print(ip12[:2], vlan_ip12[:2])
            for i, j in zip(ip12[:2], vlan_ip12[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip13, is_internet13 = get_ip_address_and(request, ssidName, key13, setup_perfectoMobile_android, connData)
        #
        if ip13:
            if is_internet5:
                text_body = ("connected to " + ssidName + " (" + ip13 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip13 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip13 = ip13.split(".")
            vlan_ip13 = vlan_ip13.split(".")
            print(ip13[:2], vlan_ip13[:2])
            for i, j in zip(ip13[:2], vlan_ip13[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip14, is_internet14 = get_ip_address_and(request, ssidName, key14, setup_perfectoMobile_android, connData)
        #
        if ip14:
            if is_internet14:
                text_body = ("connected to " + ssidName + " (" + ip14 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip14 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip14 = ip14.split(".")
            vlan_ip14 = vlan_ip14.split(".")
            print(ip14[:2], vlan_ip14[:2])
            for i, j in zip(ip14[:2], vlan_ip14[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip15, is_internet15 = get_ip_address_and(request, ssidName, key15, setup_perfectoMobile_android, connData)
        #
        if ip15:
            if is_internet15:
                text_body = ("connected to " + ssidName + " (" + ip15 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip15 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip15 = ip15.split(".")
            vlan_ip15 = vlan_ip15.split(".")
            print(ip15[:2], vlan_ip15[:2])
            for i, j in zip(ip15[:2], vlan_ip15[:2]):
                if i != j:
                    assert False
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False
        time.sleep(5)
        ip16, is_internet16 = get_ip_address_and(request, ssidName, key16, setup_perfectoMobile_android, connData)
        #
        if ip16:
            if is_internet16:
                text_body = ("connected to " + ssidName + " (" + ip16 + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip16 + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            ip16 = ip16.split(".")
            vlan_ip16 = vlan_ip16.split(".")
            print(ip16[:2], vlan_ip16[:2])
            for i, j in zip(ip16[:2], vlan_ip16[:2]):
                if i != j:
                    assert False
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False