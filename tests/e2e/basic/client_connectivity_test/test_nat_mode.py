"""
    Test Case Module:  Client Connectivity Test
    Mode:       NAT

"""

import pytest
import sys

pytestmark = [pytest.mark.client_connectivity_test, pytest.mark.nat]

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')

from sta_connect2 import StaConnect2
from eap_connect import EAPConnect
import time


#

@pytest.mark.sanity
@pytest.mark.nat
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["NAT"], ["NAT"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestNatModeClientConnectivity(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_wpa_2g(self, request, get_lanforge_data, setup_profile_data, instantiate_testrail,
                           instantiate_controller, instantiate_project, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_2dot4g_prefix"] + "0" + str(i))
        print(profile_data, get_lanforge_data)
        staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
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
        staConnect.runtime_secs = 40
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
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='2G WPA Client Connectivity Passed successfully - nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='2G WPA Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert staConnect.passes()
        # C2420

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_client_wpa_5g(self, request, get_lanforge_data, setup_profile_data, instantiate_project,
                           instantiate_controller, instantiate_testrail, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_5g_prefix"] + "0" + str(i))
        staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
                                 debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        staConnect.radio = get_lanforge_data["lanforge_5g"]
        staConnect.resource = 1
        staConnect.dut_ssid = profile_data["ssid_name"]
        staConnect.dut_passwd = profile_data["security_key"]
        staConnect.dut_security = "wpa"
        staConnect.station_names = station_names
        staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
        staConnect.runtime_secs = 40
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
            instantiate_testrail.update_testrail(case_id=test_cases["5g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='5G WPA Client Connectivity Passed successfully - nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["5g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='5G WPA Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert staConnect.passes()
        # C2419

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, request, get_lanforge_data, setup_profile_data, instantiate_project,
                                    instantiate_controller, instantiate_testrail, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["2G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_2dot4g_prefix"] + "0" + str(i))
        staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
                                 debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        staConnect.radio = get_lanforge_data["lanforge_2dot4g"]
        staConnect.resource = 1
        staConnect.dut_ssid = profile_data["ssid_name"]
        staConnect.dut_passwd = profile_data["security_key"]
        staConnect.dut_security = "wpa2"
        staConnect.station_names = station_names
        staConnect.sta_prefix = get_lanforge_data["lanforge_2dot4g_prefix"]
        staConnect.runtime_secs = 40
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
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='2G WPA2 Client Connectivity Passed successfully - nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["2g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='2G WPA2 Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert staConnect.passes()
        # C2237

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, request, get_lanforge_data, setup_profile_data, instantiate_project,
                                    instantiate_controller, instantiate_testrail, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["5G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_5g_prefix"] + "0" + str(i))
        staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
                                 debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        staConnect.radio = get_lanforge_data["lanforge_5g"]
        staConnect.resource = 1
        staConnect.dut_ssid = profile_data["ssid_name"]
        staConnect.dut_passwd = profile_data["security_key"]
        staConnect.dut_security = "wpa2"
        staConnect.station_names = station_names
        staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
        staConnect.runtime_secs = 40
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
            instantiate_testrail.update_testrail(case_id=test_cases["5g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='5G WPA2 Client Connectivity Passed successfully - nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["5g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='5G WPA2 Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert staConnect.passes()
        # C2236

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_client_wpa2_enterprise_2g(self, request, get_lanforge_data, setup_profile_data, instantiate_project,
                                      instantiate_controller, instantiate_testrail, radius_info, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA2_E"]["2G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_2dot4g_prefix"] + "0" + str(i))
        eap_connect = EAPConnect(get_lanforge_data["lanforge_ip"], get_lanforge_data["lanforge-port-number"])
        eap_connect.upstream_resource = 1
        eap_connect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        eap_connect.security = "wpa2"
        eap_connect.sta_list = station_names
        eap_connect.station_names = station_names
        eap_connect.sta_prefix = get_lanforge_data["lanforge_2dot4g_prefix"]
        eap_connect.ssid = profile_data["ssid_name"]
        eap_connect.radio = get_lanforge_data["lanforge_2dot4g"]
        eap_connect.eap = "TTLS"
        eap_connect.identity = radius_info["user"]
        eap_connect.ttls_passwd = radius_info["password"]
        eap_connect.runtime_secs = 40
        eap_connect.setup()
        eap_connect.start()
        print("napping %f sec" % eap_connect.runtime_secs)
        time.sleep(eap_connect.runtime_secs)
        eap_connect.stop()
        try:
            eap_connect.cleanup()
            eap_connect.cleanup()
        except:
            pass
        run_results = eap_connect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", eap_connect.passes)
        if eap_connect.passes():
            instantiate_testrail.update_testrail(case_id=test_cases["2g_eap_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='5G WPA2 ENTERPRISE Client Connectivity Passed successfully - '
                                                     'nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["2g_eap_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='5G WPA2 ENTERPRISE Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert eap_connect.passes()
        # C5214

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_client_wpa2_enterprise_5g(self, request, get_lanforge_data, setup_profile_data, instantiate_project,
                                      instantiate_controller, instantiate_testrail, radius_info, test_cases, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA2_E"]["5G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_5g_prefix"] + "0" + str(i))
        eap_connect = EAPConnect(get_lanforge_data["lanforge_ip"], get_lanforge_data["lanforge-port-number"])
        eap_connect.upstream_resource = 1
        eap_connect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        eap_connect.security = "wpa2"
        eap_connect.sta_list = station_names
        eap_connect.station_names = station_names
        eap_connect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
        eap_connect.ssid = profile_data["ssid_name"]
        eap_connect.radio = get_lanforge_data["lanforge_5g"]
        eap_connect.eap = "TTLS"
        eap_connect.identity = radius_info["user"]
        eap_connect.ttls_passwd = radius_info["password"]
        eap_connect.runtime_secs = 40
        eap_connect.setup()
        eap_connect.start()
        print("napping %f sec" % eap_connect.runtime_secs)
        time.sleep(eap_connect.runtime_secs)
        eap_connect.stop()
        try:
            eap_connect.cleanup()
            eap_connect.cleanup()
        except:
            pass
        run_results = eap_connect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", eap_connect.passes)
        if eap_connect.passes():
            instantiate_testrail.update_testrail(case_id=test_cases["5g_eap_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='5G WPA2 ENTERPRISE Client Connectivity Passed successfully - '
                                                     'nat mode' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["5g_eap_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='5G WPA2 ENTERPRISE Client Connectivity Failed - nat mode' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert eap_connect.passes()

    @pytest.mark.modify_ssid
    @pytest.mark.parametrize(
        'update_ssid',
        (["NAT, WPA, 5G, Sanity-updated-5G-WPA-NAT"]),
        indirect=True
    )
    def test_modify_ssid(self, request, update_ssid, get_lanforge_data, setup_profile_data, instantiate_testrail,
                         instantiate_project, test_cases, instantiate_controller, exit_on_fail):
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_5g_prefix"] + "0" + str(i))
        staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
                                 debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
        staConnect.radio = get_lanforge_data["lanforge_5g"]
        staConnect.resource = 1
        staConnect.dut_ssid = profile_data["ssid_name"]
        staConnect.dut_passwd = profile_data["security_key"]
        staConnect.dut_security = "wpa"
        staConnect.station_names = station_names
        staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
        staConnect.runtime_secs = 40
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
            instantiate_testrail.update_testrail(case_id=test_cases["nat_ssid_update"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='5G WPA Client Connectivity Passed successfully - nat mode '
                                                     'updated ssid' + str(run_results))
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["nat_ssid_update"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='5G WPA Client Connectivity Failed - nat mode updated ssid' + str(run_results))
            if exit_on_fail:
                pytest.exit("Test Case Failed! exit_on_fail Exit")
        instantiate_controller.refresh_instance()
        assert staConnect.passes()
