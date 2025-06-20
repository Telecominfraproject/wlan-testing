import json
import logging
import os
import allure
import pytest
import requests

pytestmark = [pytest.mark.band_steering_tests, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "bandsteering_2",
             "appliedRadios": ["2G", "5G"],
             "security": "psk2",
             "security_key": "password@123",
            "roaming": True,
            "wifi-steering":
            {
			    "mode": "local",
			    "network": "upstream",
			    "assoc-steering": True,
			    "required-snr": -85,
			    "required-probe-snr": -80,
			    "required-roam-snr": -80,
			    "load-kick-threshold": 90
		    }
            }
            ]},
    "rf": {
        "2G": {
            "band": "2G",
            "country": "CA",
            "channel-width": 80,
            "channel-mode": "HE"
        },
        "5G": {
            "band": "5G",
            "country": "CA",
            "channel-width": 80,
            "channel-mode": "HE"
        },
        "6G": {
            "band": "6G",
            "channel-mode": "HE"
        }
    },
    "radius": False
}

@allure.feature("Band Steering")
@allure.parent_suite("Band Steering Tests")
@allure.suite(suite_name="WPA2 PERSONAL")
@allure.sub_suite(sub_suite_name="Test Band Steering with WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBandSteering(object):
    """
        Bridge Band Steering (wpa2_personal) (twog, fiveg)
        pytest -m "band_steering_tests and bridge and wpa2_personal"
    """

    @pytest.mark.band_steering_tests
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @allure.story('WAP2 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Band Steering Test with wap2 encryption")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14518", name="JIRA LINK")
    def test_band_steering_wpa2_personal(self, get_test_library, get_target_object, check_connectivity,
                                                setup_configuration, client_type, get_testbed_details):
        """ Validate steering and data path connectivity
            pytest -m "band_steering_tests and bridge and wpa2_personal"
        """
        profile_data = {"ssid_name": "bandsteering_2", "appliedRadios": ["2G", "5G"]}
        ssid = profile_data["ssid_name"]
        security = "wpa2"
        security_key = "password@123"
        mode = "BRIDGE"
        band = "twog"
        num_sta = 1
        pass_fail, message = get_test_library.band_steering_test(ssid=ssid, passkey=security_key, security=security,
                                       mode=mode, band=band, pre_cleanup=False, num_sta=num_sta, scan_ssid=True,
                                       station_data=["ip", "alias", "mac", "channel", "port type", "security",
                                                             "ap", "parent dev"],
                                       allure_attach=True, dut_data=setup_configuration,
                                       get_target_object=get_target_object, get_testbed_details=get_testbed_details)

        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True