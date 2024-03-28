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
        "wpa2_personal": [
            {"ssid_name": "ssid_captive_portal_wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something",
             "captive": {
                 "auth-mode": "radius",
                 "auth-server": "10.28.3.21",
                 "auth-port": 1812,
                 "auth-secret": "testing123",
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
@allure.suite(suite_name="Bridge Mode")
@allure.sub_suite(sub_suite_name="Radius user/pass mode")
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

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.radius_user_and_pass
    @pytest.mark.ow_regression_lf
    @allure.title("Radius user/pass mode with wpa2_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10996", name="WIFI-10996")
    def test_bridge_wpa2_2g_radius_user_and_pass(self, get_test_library, get_dut_logs_per_test_case,
                                                 get_test_device_logs, num_stations, check_connectivity,
                                                 setup_configuration, get_testbed_details, get_target_object,
                                                 radius_info):
        """
            Advanced Captive Portal provides a way to authenticate the clients before they get access to the internet.
            In the Advanced Captive Portal as soon as the clients get connected to the SSID, the client will be
            redirected to the captive Portal web page to authenticate or to accept the terms of service.

            Radius user/pass mode (Captive-Radius): In this mode the client needs to enter the valid credentials that
            are configured in the radius server being used to get the internet access.

            Unique Marker:
            advanced_captive_portal_tests and wpa2_personal and twog and bridge and radius_user_and_pass
        """
        profile_data = {"ssid_name": "ssid_captive_portal_wpa2_2g_br", "appliedRadios": ["2G"],
                        "security_key": "something",
                        "captive": {
                            "auth-mode": "radius",
                            "auth-server": "10.28.3.21",
                            "auth-port": 1812,
                            "auth-secret": "testing123",
                            "walled-garden-fqdn": [
                                "*.google.com",
                                "telecominfraproject.com"
                            ]
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        identity = radius_info['user']
        passwd = radius_info["password"]
        # json post data for API
        json_post_data = f"username={identity}&password={passwd}&action=radius"
        print("json_post_data", json_post_data)
        allure.attach(name="Definition",
                      body="Radius user/pass mode (Captive-Radius): In this mode the client needs to enter"
                           " the valid credentials that are configured in the radius server being used to get "
                           "the internet access.")
        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                  dut_data=setup_configuration,
                                                                  passkey=security_key, mode=mode, band=band,
                                                                  num_sta=num_stations, json_post_data=json_post_data,
                                                                  get_testbed_details=get_testbed_details,
                                                                  tip_2x_obj=get_target_object)
        assert passes == "PASS", result
