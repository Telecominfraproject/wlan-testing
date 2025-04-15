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
        "wpa2_personal": [{"ssid_name": "bandsteering_2", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "bandsteering_2", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}

@allure.feature("Band Steering")
@allure.parent_suite("Band Steering Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="General security mode Band Steering")
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
        """ wpa2 personal
            pytest -m "band_steering_tests and bridge and wpa2_personal"
        """
        profile_data = {"ssid_name": "bandsteering_2", "appliedRadios": ["2G", "5G"]}
        ssid = profile_data["ssid_name"]
        security = "wpa2"
        security_key = "password@123"
        mode = "BRIDGE"
        band = "twog"
        num_sta = 1

        #BandSteering Configuration
        test_file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(test_file_dir, 'bandsteer_config.json')
        with open(file_path, 'r') as file:
            json_string = file.read()
            config_data = json.loads(json_string)

        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {"configuration": json.dumps(config_data), "serialNumber": device_name, "UUID": 2}

        path = "device/" + device_name + "/configure"
        uri = get_target_object.controller_library_object.build_uri(path)
        logging.info(f"uri::{uri}")
        resp = requests.post(uri, data=json.dumps(payload, indent=2),
                             headers=get_target_object.controller_library_object.make_headers(), verify=False,
                             timeout=120)

        logging.info(f"response:,{resp}")
        if resp.status_code == 200:
            logging.info("BandSteering configuration applied successfully")
            allure.attach(name=f"Response for Configuration - {resp.status_code} {resp.reason}",
                          body=str(resp.json()))
        else:
            allure.attach(name=f"Response for Configuration - {resp.status_code} {resp.reason}",
                          body=f"TEST FAILED, Configuration is not applied successful {str(resp.json())}")

        pass_fail, message = get_test_library.band_steering_test(ssid=ssid, passkey=security_key, security=security,
                                       mode=mode, band=band, pre_cleanup=False, num_sta=num_sta, scan_ssid=True,
                                       station_data=["ip", "alias", "mac", "channel", "port type", "security",
                                                             "ap", "parent dev"],
                                       allure_attach=True, dut_data=setup_configuration,
                                       get_target_object=get_target_object, config_data=config_data)

        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True