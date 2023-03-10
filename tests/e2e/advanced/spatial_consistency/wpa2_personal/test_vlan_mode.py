"""

    Test Spatial Consistency: Vlan Mode
    pytest -m spatial_consistency
"""

import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.spatial_consistency, pytest.mark.vlan]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan":100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan":100}
        ]
    },
    "rf": {
        "5G":{
            "channel-width": 80},
        "2G":{
            "channel-width": 20}
    },
    "radius": False
}
@allure.feature("SPATIAL CONSISTENCY")
@allure.parent_suite("Spatial Consistency Test")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_SpatialConsistency_Vlan(object):

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Vlan Mode Spatial Consistency Test (NSS-1) UDP-Download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5052", name="WIFI-5052")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss1
    def test_udp_download_nss1_wpa2_personal_2g(self, get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100

        result, description = get_test_library.spatial_consistency(ssid_name=ssid_name, security_key=security_key,
                                                                   security=security, mode=mode, band=band, vlan=vlan,
                                                                   dut_data=setup_configuration, num_sta=1,
                                                                   spatial_streams=1,
                                                                   instance_name="SPATIAL_NSS1_TWOG",
                                                                   pass_value={"strong": 45, "medium": 35, "weak": 17},
                                                                   attenuations=[10, 38, 48],create_vlan=False)
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Vlan Mode Spatial Consistency Test (NSS-2) UDP-Download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5068", name="WIFI-5068")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss2
    def test_udp_download_nss2_wpa2_personal_2g(self,get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100

        result, description = get_test_library.spatial_consistency(ssid_name=ssid_name, security_key=security_key,
                                                                   security=security, mode=mode, band=band, vlan=vlan,
                                                                   dut_data=setup_configuration, num_sta=1,
                                                                   spatial_streams=2,
                                                                   instance_name="SPATIAL_NSS2_TWOG",
                                                                   pass_value={"strong": 90, "medium": 70, "weak": 35},
                                                                   attenuations=[10, 38, 48],create_vlan=False)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Vlan Mode Spatial Consistency Test (NSS-1) UDP-Download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5067", name="WIFI-5067")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.nss1
    def test_udp_download_nss1_wpa2_personal_5g(self, get_test_library, setup_configuration, check_connectivity):
        profile_data =  {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100

        result, description = get_test_library.spatial_consistency(ssid_name=ssid_name, security_key=security_key,
                                                                   security=security, mode=mode, band=band, vlan=vlan,
                                                                   dut_data=setup_configuration, num_sta=1,
                                                                   spatial_streams=1,
                                                                   instance_name="SPATIAL_NSS1_FIVEG",
                                                                   pass_value={"strong": 250, "medium": 150,"weak": 75},
                                                                   attenuations=[10, 25, 35],create_vlan=False)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Vlan Mode Spatial Consistency Test (NSS-2) UDP-Download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5066", name="WIFI-5066")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.nss2
    def test_udp_download_nss2_wpa2_personal_5g(self,get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100

        result, description = get_test_library.spatial_consistency(ssid_name=ssid_name, security_key=security_key,
                                                                   security=security, mode=mode, band=band, vlan=vlan,
                                                                   dut_data=setup_configuration, num_sta=1,
                                                                   spatial_streams=2,
                                                                   instance_name="SPATIAL_NSS2_FIVEG",
                                                                   pass_value={"strong": 500, "medium": 300,"weak": 150},
                                                                   attenuations=[10, 25, 35],create_vlan=False)
        if result:
            assert True
        else:
            assert False, description


