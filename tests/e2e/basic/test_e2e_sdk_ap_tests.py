import sys
import time
from datetime import datetime

import allure
import pytest

setup_params = [
    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_psk_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk"},
            {"ssid_name": "ssid_psk_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_psk2_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk2"},
            {"ssid_name": "ssid_psk2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_sae_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "sae"},
            {"ssid_name": "ssid_sae_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "sae"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "none"},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "none"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa2"},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa2"}],
        "radius": True
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa3"},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa3"}],
        "radius": True
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_psk_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk"},
            {"ssid_name": "ssid_psk_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_psk2_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk2"},
            {"ssid_name": "ssid_psk2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_sae_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "sae"},
            {"ssid_name": "ssid_sae_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "sae"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "none"},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "none"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa2"},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa2"}],
        "radius": True
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa3"},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa3"}],
        "radius": True
    },
    ##########
{
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_psk_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk", "vlan": 100},
            {"ssid_name": "ssid_psk_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk", "vlan": 100}],
        "radius": False
    },

    {
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_psk2_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk2", "vlan": 100},
            {"ssid_name": "ssid_psk2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2", "vlan": 100}],
        "radius": False
    },

    {
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_sae_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "sae", "vlan": 100},
            {"ssid_name": "ssid_sae_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "sae", "vlan": 100}],
        "radius": False
    },

    {
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "none", "vlan": 100},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "none", "vlan": 100}],
        "radius": False
    },

    {
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa2", "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa2", "vlan": 100}],
        "radius": True
    },

    {
        "mode": "VLAN",
        "ssids": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa3", "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa3", "vlan": 100}],
        "radius": True
    },

]


@pytest.mark.ow_config_load_test
@pytest.mark.ow_sdk_load_tests
@allure.parent_suite("OpenWifi SDK E2E Tests")
@allure.parent_suite("OpenWifi Gateway E2E Configuration Test")
class TestBulkConfigTest(object):

    @allure.sub_suite("Back to Back config Apply test on single AP")
    def test_config_apply_test(self, setup_controller, instantiate_profile, get_configuration, radius_info,
                               radius_accounting_info):
        """
            Test the system endpoints to verify list of services present
            WIFI-3449
        """
        PASS = []
        SERIAL = get_configuration["access_point"][0]["serial"]
        for i in range(0, 100):
            for config in setup_params:
                profile_obj = instantiate_profile(sdk_client=setup_controller)
                profile_obj.set_mode(config["mode"])
                profile_obj.set_radio_config()
                radius = config["radius"]
                for ssid in config["ssids"]:
                    if radius:
                        profile_obj.add_ssid(ssid_data=ssid, radius=radius, radius_auth_data=radius_info,
                                             radius_accounting_data=radius_accounting_info)
                    else:
                        profile_obj.add_ssid(ssid_data=ssid)
                status = profile_obj.push_config(serial_number=SERIAL)
                if status.status_code != 200:
                    allure.attach("Configure command Failed: ", SERIAL, " Time: " + str(datetime.utcnow()))
                    print(str(status.status_code) + ":\t" + str(status.json()))
                    allure.attach(name=str(status.status_code), body=str(status.json()))
                    print("Configure command success: ", SERIAL, " Time: " + str(datetime.utcnow()))
                    PASS.append(False)
                if status.status_code == 200:
                    print(str(status.status_code) + ":\t" + str(status.json()))
                    allure.attach(name=str(status.status_code), body=str(status.json()))
                    allure.attach("Configure command success: ", SERIAL, " Time: " + str(datetime.utcnow()))
                    print("Configure command success: ", SERIAL, " Time: " + str(datetime.utcnow()))
                    PASS.append(True)
                print("Sleeping 30 Sec before Next Config")
                time.sleep(30)

        assert False not in PASS
