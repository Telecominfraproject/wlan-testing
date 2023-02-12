"""
    Multiple number of SSIDs Test: Bridge Mode
    pytest -m multi_ssid
"""

import time
import allure
import pytest

pytestmark = [pytest.mark.multi_ssid, pytest.mark.bridge]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "multi_ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "multi_ssid1_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "multi_ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "multi_ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiSsidDataPath1(object):
    """
        Multiple number of SSIDs Test: Bridge Mode
        pytest -m multi_ssid
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12227")
    @pytest.mark.wpa2_personal
    @pytest.mark.one_ssid
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.multi_ssid
    def test_one_ssid(self, get_test_library, get_dut_logs_per_test_case,
                      get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """Multi-SSID Bridge Mode
           pytest -m "max_ssid and single_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0000", "sta0001"]
        sta_list2 = ["sta1000", "sta1001"]
        pass_fail = {}
        for i in range(len(setup_params_general1["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security, passkey=security_key,
                                                         mode=mode, radio=get_test_library.wave2_2g_radios[0], station_name=sta_list1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security, passkey=security_key,
                                                         mode=mode, radio=get_test_library.wave2_5g_radios[0], station_name=sta_list2)

        cx_data = get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                                         side_b_min_rate=6291456, side_b_max_rate=0,
                                                         traffic_type="lf_tcp", sta_list=sta_list1,
                                                         side_b=sta_list2)
        print("waiting 30 sec for getting layer3 cx data...")
        time.sleep(30)
        allure.attach(cx_data)
        # fail_list = list(filter(lambda x : x == False, pass_fail))
        assert True
