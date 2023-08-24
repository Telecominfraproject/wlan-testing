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
            {"ssid_name": "ssid_captive_portal_open_2g_br", "appliedRadios": ["2G"], "security_key": "something",
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
                                              setup_configuration, get_testbed_details, get_target_object):
        """
            BRIDGE Mode Advanced Captive Portal Test with open encryption 2.4 GHz Band
            pytest -m "advanced_captive_portal_tests and open and twog and bridge and click_to_continue"
        """
        profile_data = {"ssid_name": "ssid_captive_portal_open_2g_br", "appliedRadios": ["2G"],
                        "security_key": "something",
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
        # json post data for API
        json_post_data = 'action=click&accept_terms=clicked'
        allure.attach(name="Definition",
                      body="Click-to-continue mode: In this mode the client will be redirected to the page where "
                           "the client needs to accept the terms of service before getting internet.")
        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                  dut_data=setup_configuration,
                                                                  passkey=security_key, mode=mode, band=band,
                                                                  num_sta=num_stations, json_post_data=json_post_data,
                                                                  get_testbed_details=get_testbed_details,
                                                                  tip_2x_obj=get_target_object)
        assert passes == "PASS", result
