"""

    Performance Test: Dataplane Throughput Test: BRIDGE Mode
    pytest -m "dataplane_tests wpa3_personal security and bridge"

"""
import logging
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_tests,
              pytest.mark.bridge, pytest.mark.wpa3_personal]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]},
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "HE",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 160,
            "channel-mode": "HE",
            "channel": 33
        }
    },
    "radius": False
},
setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]},
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 40,
            "channel-mode": "HE",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 160,
            "channel-mode": "HE",
            "channel": 33
        }
    },
    "radius": False
},
setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]},
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 40,
            "channel-mode": "EHT",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "EHT",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 320,
            "channel-mode": "EHT",
            "channel": 33
        }
    },
    "radius": False
}

testbed_details_global = None
setup_params_general = None
dut_data = {}

@pytest.fixture(scope="class")
def initialize_testbed(request):
    """Calls setup_testbed automatically before tests"""
    global testbed_details_global
    global setup_params_general
    global dut_data
    selected_tb = request.getfixturevalue("selected_testbed")
    print(f"Selected Testbed: {selected_tb}")
    testbed_details_global = request.getfixturevalue("get_testbed_details")
    assert testbed_details_global is not None, "Testbed details should not be None"
    print(f"Initialized Testbed Details: {testbed_details_global}")

    # Extract 'mode' from the first device in 'device_under_tests'
    ap_mode = testbed_details_global["device_under_tests"][0].get("mode", "")

    # Assign setup_params_general based on mode
    if ap_mode == "wifi6":
        setup_params_general = setup_params_general1
    elif ap_mode == "wifi6e":
        setup_params_general = setup_params_general2
    elif ap_mode == "wifi7":
        setup_params_general = setup_params_general3
    else:
        print(f"Unknown mode: {ap_mode}. Defaulting to None")

    print(f"Setup Params Assigned: {setup_params_general}")

    get_marker = request.getfixturevalue("get_markers")
    requested_combination = []
    for key in get_marker:
        if get_marker[key]:
            requested_combination.append(get_marker[key])

    logging.info(f"requested_combination:::{requested_combination}")
    get_target_obj = request.getfixturevalue("get_target_object")
    logging.info("ready to start setup_basic_configuration")
    logging.info(f"setup_params_general value before start:{setup_params_general}")
    if isinstance(setup_params_general, tuple):
        setup_params_general = setup_params_general[0]
    dut_data = get_target_obj.setup_basic_configuration(configuration=setup_params_general,
                                                       requested_combination=requested_combination)

    logging.info(f"setup_basic_configuration dut data:{dut_data}")

@allure.feature("Dataplane Tests")
@allure.parent_suite("Dataplane Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
class TestDataplaneThroughputBRIDGE(object):
    """Dataplane THroughput BRIDGE Mode
       pytest -m "dataplane_tests and wpa3_personal and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.title("Test for TCP UDP Download 2.4 GHz")
    def test_tcp_udp_wpa3_personal_bridge_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, setup_configuration):
        """Dataplane THroughput BRIDGE Mode.
           pytest -m "dataplane_tests and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-bridge-wpa3_personal-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA_2G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.title("Test for TCP UDP Download 5 GHz")
    def test_tcp_udp_wpa3_personal_bridge_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, setup_configuration):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_tests and bridge and wpa3_personal and fiveg"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-bridge-wpa3_personal-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA_5G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Test for TCP UDP Download 6 GHz")
    def test_tcp_udp_wpa3_personal_bridge_6g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, initialize_testbed):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_tests and bridge and wpa3_personal and sixg"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        band = "sixg"
        ap_mode = testbed_details_global["device_under_tests"][0].get("mode", "")
        logging.info(f"ap_mode value:{ap_mode}")
        influx_tags = "dataplane-tcp-udp-bridge-wpa3_personal-6G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=num_stations, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA_6G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=dut_data,
                                                   client_type=client_type, duration="30s", path_loss=10,
                                                   download_rate="85%", upload_rate="0", ap_mode =ap_mode
                                                   )
