"""

    Test Rate v/s Range : Bridge Mode
    pytest -m "rate_vs_range"
"""
import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.rate_vs_range, pytest.mark.bridge]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}

@allure.feature("RATE VS RANGE")
@allure.parent_suite("Rate vs Range Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_RatevsRange_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test Download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2495", name="WIFI-2495")
    def test_rvr_bridge_dl_wpa2_personal_2g(self,get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1

        result, description = get_test_library.rate_vs_range(ssid_name=ssid_name, security_key=security_key,
                                                                  security=security, mode=mode, band=band, vlan=vlan,
                                                                  dut_data=setup_configuration, num_sta=1,
                                                                  direction="DUT Transmit",
                                                                  instance_name="BRIDGE_RVR_TWOG_DL",
                                                                  pass_value={"strong": 100, "medium": 95, "weak": 14},
                                                                  attenuations=[0, 10, 21, 24, 27, 30, 33, 36, 39, 42,
                                                                                45, 48, 51, 54, 57, 60, 63])
        if result:
            assert True
        else:
            assert False, description


    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test Upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2495", name="WIFI-2495")
    def test_rvr_bridge_ul_wpa2_personal_2g(self, get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1

        result, description = get_test_library.rate_vs_range(ssid_name=ssid_name, security_key=security_key,
                                                                  security=security, mode=mode, band=band, vlan=vlan,
                                                                  dut_data=setup_configuration, num_sta=1,
                                                                  direction="DUT Receive",
                                                                  instance_name="BRIDGE_RVR_TWOG_UL",
                                                                  pass_value={"strong": 100, "medium": 95, "weak": 14},
                                                                  attenuations=[0, 10, 21, 24, 27, 30, 33, 36, 39, 42,
                                                                                45, 48, 51, 54, 57, 60, 63])
        if result:
            assert True
        else:
            assert False, description

    @pytest.mark.performance_advanced
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test Download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2499", name="WIFI-2499")
    def test_rvr_bridge_dl_wpa2_personal_5g(self,get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1

        result, description = get_test_library.rate_vs_range(ssid_name=ssid_name, security_key=security_key,
                                                                  security=security, mode=mode, band=band, vlan=vlan,
                                                                  dut_data=setup_configuration, num_sta=1,
                                                                  direction="DUT Transmit",
                                                                  instance_name="BRIDGE_RVR_FIVEG_DL",
                                                                  pass_value={"strong": 560, "medium": 220, "weak": 5},
                                                                  attenuations=[0, 10, 21, 24, 27, 30, 33, 36, 39, 42,
                                                                                45, 48, 51, 54])
        if result:
            assert True
        else:
            assert False, description


    @pytest.mark.performance_advanced
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test Upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2499", name="WIFI-2499")
    def test_rvr_bridge_ul_wpa2_personal_5g(self, get_test_library, setup_configuration, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1

        result, description = get_test_library.rate_vs_range(ssid_name=ssid_name, security_key=security_key,
                                                                  security=security, mode=mode, band=band, vlan=vlan,
                                                                  dut_data=setup_configuration, num_sta=1,
                                                                  direction="DUT Receive",
                                                                  instance_name="BRIDGE_RVR_FIVEG_UL",
                                                                  pass_value={"strong": 560, "medium": 220, "weak": 5},
                                                                  attenuations=[0, 10, 21, 24, 27, 30, 33, 36, 39, 42,
                                                                                45, 48, 51, 54])
        if result:
            assert True
        else:
            assert False, description