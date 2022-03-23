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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.openRoaming, pytest.mark.bridge]
# pytestmark = [pytest.mark.openRoaming]


from android_lib import closeApp, set_APconnMobileDevice_android, verify_APconnMobileDevice_Android, deleteOpenRoamingInstalledProfile, downloadInstallOpenRoamingProfile, verifyUploadDownloadSpeed_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp

"""
    EAP Passpoint Test: BRIDGE Mode
    pytest -m "interop_iOS and eap_passpoint and bridge"
"""

setup_params_eap = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "passpoint_profile_download", "appliedRadios": ["is2dot4GHz"]}
        ],
        "wpa2_eap": [
            {"ssid_name": "ssid_wpa2_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
        ],
        "wpa2_only_eap": [
            {"ssid_name": "ssid_wpa2_only_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_only_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
        ]
    }
}
 
@allure.feature("BRIDGE MODE EAP PASSPOINT SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_eap],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestOpenRoamingBridgeMode(object):

    @pytest.mark.wpa2_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_2g_WPA2_EAP(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_android):
        """
            EAP Passpoint BRIDGE Mode
            pytest -m "interop_iOS and eap_passpoint and bridge and wpa2_eap and twog"
        """

        result = push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_config']
        print(result)
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_2g failed", body="")
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result
        result = push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_2g failed", body="")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        #SSID to download profile ::  passpoint_profile_download
        #SSID to validate connectivity ::  ssid_wpa2_eap_passpoint_5g
        #Profile download URL ::  https://onboard.almondlabs.net/ios.html
        #Profile name to remove ::  AmeriBand

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/androidconfig.cfg"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_android, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_android, connData)
        
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_android, downloadProfileSSID, connData)

        try:
            verify_APconnMobileDevice_Android(request, profileNameSSID, setup_perfectoMobile_android, connData)
             #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
            assert False
     
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    


    @pytest.mark.wpa2_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_5g_WPA2_EAP(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_android):
        """
            EAP Passpoint BRIDGE Mode
            pytest -m "interop_iOS and eap_passpoint and bridge and wpa2_eap and fiveg"
        """
        result = push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_5g failed", body="")
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result
        result = push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_5g failed", body="")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])
        #SSID to download profile ::  passpoint_profile_download
        #SSID to validate connectivity ::  ssid_wpa2_eap_passpoint_5g
        #Profile download URL ::  https://onboard.almondlabs.net/ios.html
        #Profile name to remove ::  AmeriBand

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/androidconfig.cfg"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_android, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_android, connData)
        
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_android, downloadProfileSSID, connData)

        try:
            verify_APconnMobileDevice_Android(request, profileName, setup_perfectoMobile_android, connData)
             #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
            assert False
     
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
  
    @pytest.mark.wpa2_only_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_wpa2_only_eap_2g(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_android):
        """
             EAP Passpoint BRIDGE Mode
             pytest -m "interop_iOS and eap_passpoint and bridge and wpa2_only_eap and twog"
        """
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_2g failed", body="")
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_2g failed", body="")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        #profileDownloadURL = passpoint_profile_info["profile_download_url_ios"]
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/androidconfig.cfg"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    

        #ForgetWifi
        #ForgetWifiConnection(request, setup_perfectoMobile_android, profileNameSSID, connData)

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_android, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_android, connData)
        
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_android, downloadProfileSSID, connData)

        try:
            verify_APconnMobileDevice_Android(request, profileNameSSID, setup_perfectoMobile_android, connData)

             #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
            assert False
     
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)     

    @pytest.mark.wpa2_only_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_wpa2_only_eap_5g(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_android):
        """
             EAP Passpoint BRIDGE Mode
             pytest -m "interop_iOS and eap_passpoint and bridge and wpa2_only_eap and fiveg"
        """
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_5g failed", body="")
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_5g failed", body="")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/androidconfig.cfg"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    

        #Set Wifi/AP Mode
        set_APconnMobileDevice_android(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_android, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_android, connData)
        
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_android, downloadProfileSSID, connData)

        try:
            verify_APconnMobileDevice_Android(request, profileNameSSID, setup_perfectoMobile_android, connData)
             #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeed_android(request, setup_perfectoMobile_android, connData)

        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
            assert False
     
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_android, connData)    
