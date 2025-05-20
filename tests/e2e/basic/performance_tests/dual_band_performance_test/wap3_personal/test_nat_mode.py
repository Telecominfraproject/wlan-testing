"""
       Multi Band Performance Test : NAT Mode
       pytest -m "performance and multi_band_tests and nat"


"""
import logging
import allure
import pytest

pytestmark = [pytest.mark.performance, pytest.mark.nat, pytest.mark.muti_band_tests]

setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_personal_multi_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
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
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_personal_multi_band", "appliedRadios": ["2G", "5G", "6G"], "security_key": "something"}
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
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_personal_multi_band", "appliedRadios": ["2G", "5G", "6G"], "security_key": "something"}
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


@pytest.mark.multi_band_tests
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.wifi7
@allure.parent_suite("Multi Band Tests")
@allure.suite("Multi Band Tests: NAT mode")
@allure.sub_suite("wpa3_personal security")
@allure.feature("Multi band performance test")
class TestWpa3MultibandPerformanceNat(object):
    """
         pytest -m "performance and multi_band_tests and nat and wpa3_personal and twog  and fiveg."
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3728", name="WIFI-3728")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.sixg
    @allure.title("Test Multi Band with ApAuto test of NAT mode")
    def test_client_wpa3_personal_nat(self, initialize_testbed, get_test_library, check_connectivity):
        """
                            Multi Band Test with wpa3_personal encryption
                            pytest -m "multi_band_tests and wpa3_personal"
        """
        ap_mode = testbed_details_global["device_under_tests"][0].get("mode", "")
        logging.info(f"setup_params_general data:{setup_params_general}")
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"]
        logging.info(f"profile_data data:{profile_data}")

        ssid_2G, ssid_5G = profile_data[0]["ssid_name"], profile_data[0]["ssid_name"]
        dut_name = list(dut_data.keys())[0]
        mode = "NAT-WAN"
        vlan = 1
        dut_5g, dut_2g = "", ""
        if ap_mode == "wifi7" or ap_mode == "wifi6e":
            dut_6g = ""
            ssid_6G = profile_data[0]["ssid_name"]

        influx_tags = "dual-band-nat-wpa3"
        for i in dut_data[dut_name]['ssid_data']:
            get_test_library.dut_idx_mapping[str(i)] = list(dut_data[dut_name]['ssid_data'][i].values())
            if get_test_library.dut_idx_mapping[str(i)][3] == "5G":
                dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + \
                         get_test_library.dut_idx_mapping[str(i)][4]
            if get_test_library.dut_idx_mapping[str(i)][3] == "2G":
                dut_2g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + \
                         get_test_library.dut_idx_mapping[str(i)][4]

            if get_test_library.dut_idx_mapping[str(i)][3] == "6G" and (ap_mode == "wifi7" or ap_mode == "wifi6e"):
                dut_6g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + \
                         get_test_library.dut_idx_mapping[str(i)][4]
                logging.info(f"dut_6g value:{dut_6g}")

        if ap_mode == "wifi7" or ap_mode == "wifi6e":
            logging.info("ap mode is not wifi6 , ready to call triband")
            get_test_library.multi_band_performance_test(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                                        ssid_6G=ssid_6G, vlan_id=vlan,
                                                        dut_5g=dut_5g, dut_2g=dut_2g, dut_6g=dut_6g,
                                                        influx_tags=influx_tags,
                                                        move_to_influx=False, dut_data=dut_data)
        else:
            logging.info("ap mode is wifi6 , ready to call dualband")
            get_test_library.multi_band_performance_test(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G, vlan_id=vlan,
                                                        dut_5g=dut_5g, dut_2g=dut_2g, influx_tags=influx_tags,
                                                        move_to_influx=False, dut_data=dut_data)

        assert True
