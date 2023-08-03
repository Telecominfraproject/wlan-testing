"""

    Advanced Captive Portal Test: BRIDGE Mode
    pytest -m "advanced_captive_portal_tests and bridge"

"""
import logging

import allure
import pytest

pytestmark = [pytest.mark.advanced_captive_portal_tests, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_captive_portal_open_dual_br", "appliedRadios": ["2G"], "security_key": "something",
             "captive": {
                 "auth-mode": "click-to-continue",
                 "walled-garden-fqdn": [
                     "*.google.com",
                     "telecominfraproject.com"
                 ]
             }
             }
        ]},
    "rf": {},
    "radius": False
}


@allure.feature("Advanced Captive Portal Test")
@allure.parent_suite("Advanced Captive Portal Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="Click-to-continue mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeadvancedcaptiveportal(object):
    """
        Advanced Captive Portal Test: BRIDGE Mode
        pytest -m "advanced_captive_portal_tests and bridge"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.click_to_continue
    @allure.title("Click-to-continue mode with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10977", name="WIFI-10977")
    def test_bridge_open_2g_click_to_continue(self, get_test_library, get_dut_logs_per_test_case,
                                              get_test_device_logs, num_stations, check_connectivity,
                                              setup_configuration):
        """
            BRIDGE Mode Advanced Captive Portal Test with open encryption 2.4 GHz Band
            pytest -m "advanced_captive_portal_tests and open and twog and bridge and click_to_continue"
        """
        profile_data = {"ssid_name": "ssid_captive_portal_open_dual_br", "appliedRadios": ["2G"], "security_key": "something",
             "captive": {
                 "auth-mode": "click-to-continue",
                 "walled-garden-fqdn": [
                     "*.google.com",
                     "telecominfraproject.com"
                 ]
             }
             }
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result
