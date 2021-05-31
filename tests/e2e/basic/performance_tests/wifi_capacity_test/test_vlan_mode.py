import pytest
import sys
import time
from lf_wifi_capacity_test import WiFiCapacityTest
from create_station import CreateStation
pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.vlan]

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *
from sta_connect2 import StaConnect2
from eap_connect import EAPConnect
import allure

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


def lanforge_ip(args):
    pass


@pytest.mark.basic
@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestWifiCapacityVlanMode(object):

    @pytest.mark.wpa
    @pytest.mark.mutto
    @pytest.mark.twog
    def test_client_wpa_2g(self, test_cases,lf_test):
        print("**********  test_client_wpa_2g  ***********")
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        print(profile_data)

        '''create_station = CreateStation(_host = lf_test.lanforge_ip,
                                       _port = lf_test.lanforge_port,
                                       _ssid = profile_data["ssid_name"],
                                       _password = profile_data["security_key"],
                                       _security = "wpa",
                                       _sta_list = ['1.1.sta0000','1.1.sta0001'],
                                       _radio = lf_test.twog_radios)
        create_station.build()
        time.sleep(20)'''
        PASS = lf_test.wifi_capacity(ssid = profile_data["ssid_name"], paswd = profile_data["security_key"],
                              security = "wpa", mode = "VLAN", band = "twog", instance_name = "wct_instance", )
        assert PASS

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_client_wpa_5g(self, test_cases, lf_test):
        print("**********  test_client_wpa_5g  ***********")
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        print(profile_data)

        '''create_station = CreateStation(_host=lf_test.lanforge_ip,
                                       _port=lf_test.lanforge_port,
                                       _ssid=profile_data["ssid_name"],
                                       _password=profile_data["security_key"],
                                       _security="wpa",
                                       _sta_list=['1.1.sta0000', '1.1.sta0001'],
                                       _radio=lf_test.fiveg_radios)
        create_station.build()
        time.sleep(20)'''
        PASS = lf_test.wifi_capacity(ssid=profile_data["ssid_name"], paswd=profile_data["security_key"],
                                     security="wpa", mode="VLAN", band="fiveg",
                                     instance_name="wct_instance", )
        assert PASS


    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, test_cases,lf_test):
        print("**********  test_client_wpa2_personal_2g  ***********")
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        print(profile_data)

        '''create_station = CreateStation(_host = lf_test.lanforge_ip,
                                       _port = lf_test.lanforge_port,
                                       _ssid = profile_data["ssid_name"],
                                       _password = profile_data["security_key"],
                                       _security = "wpa2",
                                       _sta_list = ['1.1.sta0000','1.1.sta0001'],
                                       _radio = lf_test.twog_radios)
        create_station.build()
        time.sleep(20)'''
        PASS = lf_test.wifi_capacity( ssid = profile_data["ssid_name"], paswd = profile_data["security_key"],
                              security = "wpa2", mode = "VLAN", band = "twog",
                              instance_name = "wct_instance", )
        assert PASS

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, test_cases, lf_test):
        print("**********  test_client_wpa2_personal_5g  ***********")
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        print(profile_data)

        '''create_station = CreateStation(_host=lf_test.lanforge_ip,
                                       _port=lf_test.lanforge_port,
                                       _ssid=profile_data["ssid_name"],
                                       _password=profile_data["security_key"],
                                       _security="wpa2",
                                       _sta_list=['1.1.sta0000', '1.1.sta0001'],
                                       _radio=lf_test.fiveg_radios)
        create_station.build()
        time.sleep(20)'''
        PASS = lf_test.wifi_capacity(ssid=profile_data["ssid_name"], paswd=profile_data["security_key"],
                                     security="wpa2", mode="VLAN", band="fiveg",
                                     instance_name="wct_instance", )
        assert PASS


