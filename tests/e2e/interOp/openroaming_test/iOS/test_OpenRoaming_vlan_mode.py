"""
    EAP Passpoint VLAN Mode
    Run wpa2_eap & Run wpa2_only_eap:
    pytest -m "OpenRoaming and interop_ios and fiveg and wpa2_eap and vlan" -s -vvv --testbed interop --skip-upgrade
    pytest -m "OpenRoaming and interop_ios and twog and wpa2_eap and vlan" -s -vvv --testbed interop --skip-upgrade
    pytest -m "OpenRoaming and interop_ios and fiveg and wpa2_only_eap and vlan" -s -vvv --testbed interop --skip-upgrade
    pytest -m "OpenRoaming and interop_ios and twog and wpa2_only_eap and vlan" -s -vvv --testbed interop --skip-upgrade
    Run all:
    pytest -m "openRoaming and interop_ios and vlan" -s -vvv --testbed interop --skip-upgrade --skip-testrail --collect-only
"""

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

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.interop_ios, pytest.mark.ios, pytest.mark.openRoaming, pytest.mark.vlan]
# pytestmark = [pytest.mark.openRoaming]

from iOS_lib import closeApp, openApp, ForgetProfileWifiConnection, deleteOpenRoamingInstalledProfile, verifyUploadDownloadSpeediOS, downloadInstallOpenRoamingProfile, ForgetWifiConnection, Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown

setup_params_eap = {
    "mode": "VLAN",
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

@allure.feature("VLAN MODE EAP PASSPOINT SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_eap],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestOpenRoamingBridgeVLAN(object):

    @pytest.mark.wpa2_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_2g_WPA2_EAP_VLAN(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_iOS):
       
        result = push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_config']
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
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        #profileDownloadURL = passpoint_profile_info["profile_download_url_ios"]
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
  
        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_iOS, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_iOS, connData)
     
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, downloadProfileSSID, connData)

        try: 
            assert verify_APconnMobileDevice_iOS(request, profileNameSSID, setup_perfectoMobile_iOS, connData)
            #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData) 
            assert False
            
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    

    @pytest.mark.wpa2_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_5g_WPA2_EAP_VLAN(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_iOS):
 
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
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        #profileDownloadURL = passpoint_profile_info["profile_download_url_ios"]
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Setting Perfecto ReportClient....
        #SSID to download profile ::  passpoint_profile_download
        #SSID to validate connectivity ::  ssid_wpa2_eap_passpoint_5g
        #Profile download URL ::  https://onboard.almondlabs.net/ios.html
        #Profile name to remove ::  AmeriBand
      
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
  
        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_iOS, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_iOS, connData)
     
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, downloadProfileSSID, connData)

        try: 
            assert verify_APconnMobileDevice_iOS(request, profileNameSSID, setup_perfectoMobile_iOS, connData)
            #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData) 
            assert False
            
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
  
    @pytest.mark.wpa2_only_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_wpa2_only_eap_2g_VLAN(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

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
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        #profileDownloadURL = passpoint_profile_info["profile_download_url_ios"]
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

      #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
  
        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_iOS, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_iOS, connData)
     
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, downloadProfileSSID, connData)

        try: 
            assert verify_APconnMobileDevice_iOS(request, profileNameSSID, setup_perfectoMobile_iOS, connData)
            #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData) 
            assert False
            
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    

    @pytest.mark.wpa2_only_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_OpenRoaming_wpa2_only_eap_5g_VLAN(self, passpoint_profile_info, push_ap_profile, request, get_APToMobileDevice_data, setup_perfectoMobile_iOS):
      
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
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        downloadProfileSSID = setup_params_eap["ssid_modes"]["open"][0]["ssid_name"]
        downloadProfileSSIDPass = ""
        #profileDownloadURL = passpoint_profile_info["profile_download_url_ios"]
        profileDownloadURL = "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig"
        profileName = passpoint_profile_info["profile_name_on_device"]
        profileNameSSID = setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"]

        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
  
        #Set Wifi/AP Mode
        set_APconnMobileDevice_iOS(request, downloadProfileSSID, downloadProfileSSIDPass, setup_perfectoMobile_iOS, connData)

        #Install Profile 
        downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile_iOS, connData)
     
        #ForgetWifi Original
        ForgetWifiConnection(request, setup_perfectoMobile_iOS, downloadProfileSSID, connData)

        try: 
            assert verify_APconnMobileDevice_iOS(request, profileNameSSID, setup_perfectoMobile_iOS, connData)
            #Verify Upload download Speed from device Selection
            verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
        except Exception as e:
            deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData) 
            assert False
            
        #Delete Profile Under Settings
        deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile_iOS, connData)    
