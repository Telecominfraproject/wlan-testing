import time

import pytest
import allure

pytestmark = [pytest.mark.client_connectivity, pytest.mark.bridge, pytest.mark.basic]

setup_params_general = {
    "mode": "BRIDGE",
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


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_client_connectivity',
    [setup_params_general],
    indirect=True,
    scope="package"
)
@pytest.mark.usefixtures("setup_client_connectivity")
class TestBridgeModeConnectivity(object):

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g(self):
        ssid_data = setup_params_general["ssid_modes"]["open"][0]
        print(ssid_data)
        assert "setup_client_connectivity"

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g(self):
        ssid_data = setup_params_general["ssid_modes"]["open"][1]
        print(ssid_data)
        assert "setup_client_connectivity"

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    def test_wpa_ssid_2g(self, request, get_lanforge_data, instantiate_project, instantiate_testrail,
                         client_connectivity, test_cases):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        print(profile_data)
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_2dot4g_prefix"] + "0" + str(i))
        print(profile_data, get_lanforge_data)
        staConnect = client_connectivity(get_lanforge_data["lanforge_ip"],
                                         int(get_lanforge_data["lanforge-port-number"]),
                                         debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        staConnect.radio = get_lanforge_data["lanforge_2dot4g"]
        staConnect.resource = 1
        staConnect.dut_ssid = profile_data["ssid_name"]
        staConnect.dut_passwd = profile_data["security_key"]
        staConnect.dut_security = "wpa"
        staConnect.station_names = station_names
        staConnect.sta_prefix = get_lanforge_data["lanforge_2dot4g_prefix"]
        staConnect.runtime_secs = 10
        staConnect.bringup_time_sec = 60
        staConnect.cleanup_on_exit = True
        # staConnect.cleanup()
        staConnect.setup()
        staConnect.start()
        print("napping %f sec" % staConnect.runtime_secs)
        time.sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()
        run_results = staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", staConnect.passes)
        if staConnect.passes():
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                                     run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                                     run_results))
        assert staConnect.passes()

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_wpa_ssid_5g(self):
        ssid_data = setup_params_general["ssid_modes"]["wpa"][1]
        print(ssid_data)
        assert "setup_client_connectivity"

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g(self):
        ssid_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        print(ssid_data)
        assert "setup_client_connectivity"

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g(self):
        ssid_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        print(ssid_data)
        assert "setup_client_connectivity"
