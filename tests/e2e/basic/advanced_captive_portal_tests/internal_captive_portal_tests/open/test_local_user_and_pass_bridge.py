"""

    Advanced Captive Portal Test: BRIDGE Mode
    pytest -m "advanced_captive_portal_tests and bridge"

"""
import copy
import logging

import allure
import pytest

pytestmark = [pytest.mark.advanced_captive_portal_tests, pytest.mark.bridge, pytest.mark.internal_captive_portal_tests,
              pytest.mark.local_user_and_pass]

captive = {
                 "auth-mode": "credentials",
                 "credentials": [
                     {
                         "username": "abc",
                         "password": "def"
                     }
                 ],
                 "walled-garden-fqdn": [
                     "*.google.com",
                     "telecominfraproject.com"
                 ]
             }
setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_captive_portal_open_2g_br", "appliedRadios": ["2G"], "security_key": "something",
             "captive": captive
             },
            {"ssid_name": "ssid_captive_portal_open_5g_br", "appliedRadios": ["5G"], "security_key": "something",
             "captive": captive
             }
        ],
        "owe": [
            {"ssid_name": "int_cap_portal_2g_lup", "appliedRadios": ["2G"], "security_key": "something",
             "captive": captive
             },
            {"ssid_name": "int_cap_portal_6g_lup", "appliedRadios": ["6G"], "security_key": "something",
             "captive": captive
             }
        ]},
    "rf": {
        "2G": {
            "band": "2G",
            "channel": 6,
            "channel-mode": "HE"
        },
        "5G": {
            "band": "5G",
            "channel": 36,
            "channel-mode": "HE"
        },
        "6G": {
            "band": "6G",
            "channel": 33,
            "channel-width": 160,
            "channel-mode": "HE"
        }
    },
    "radius": False
}

# Deep copy the original dictionary to avoid modifying it
setup_params_general_wifi7 = copy.deepcopy(setup_params_general)

# Update channel-mode to 'EHT' for all bands
for band in setup_params_general_wifi7["rf"]:
    setup_params_general_wifi7["rf"][band]["channel-mode"] = "EHT"
    if band == "6G":
        setup_params_general_wifi7["rf"][band]["channel-width"] = 320

testbed_details_global = None
dut_data = {}
is_bw320 = False
is_ht160 = False

@pytest.fixture(scope="class")
def setup_initial_configuration(request):
    """Calls setup_testbed automatically before tests"""
    global testbed_details_global
    global setup_params_general
    global dut_data
    global is_bw320
    global is_ht160
    selected_tb = request.getfixturevalue("selected_testbed")
    print(f"Selected Testbed: {selected_tb}")
    testbed_details_global = request.getfixturevalue("get_testbed_details")
    assert testbed_details_global is not None, "Testbed details should not be None"
    print(f"Initialized Testbed Details: {testbed_details_global}")

    # Extract 'mode' from the first device in 'device_under_tests'
    ap_mode = testbed_details_global["device_under_tests"][0].get("mode", "")
    if ap_mode == "wifi7":
        is_bw320 = True
    if ap_mode == "wifi6e":
        is_ht160 = True
    # Assign setup_params_general based on mode
    if ap_mode == "wifi6" or ap_mode == "wifi6e":
        setup_params_general = setup_params_general
    elif ap_mode == "wifi7":
        setup_params_general = setup_params_general_wifi7
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

@allure.feature("Advanced Captive Portal Test")
@allure.parent_suite("Advanced Captive Portal Tests")
@allure.suite(suite_name="Internal Captive Portal")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
class TestBridgeModeadvancedcaptiveportal(object):
    """
        Advanced Captive Portal Test: BRIDGE Mode
        pytest -m "advanced_captive_portal_tests and bridge and internal_captive_portal_tests"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.ow_regression_lf
    @allure.title("Local user/pass mode with open encryption 2.4 GHz Band Bridge mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10991", name="WIFI-10991")
    def test_bridge_open_2g_local_user_and_pass(self, setup_initial_configuration, get_test_library,
                                                get_dut_logs_per_test_case,get_test_device_logs,
                                                num_stations,check_connectivity,get_testbed_details, get_target_object):
        """
            BRIDGE Mode Advanced Captive Portal Test with open encryption 2.4 GHz Band
            pytest -m "advanced_captive_portal_tests and internal_captive_portal_tests and open and twog and bridge and local_user_and_pass"
        """
        profile_data = {"ssid_name": "ssid_captive_portal_open_2g_br", "appliedRadios": ["2G"],
                        "security_key": "something",
                        "captive": {
                            "auth-mode": "credentials",
                            "credentials": [
                                {
                                    "username": "abc",
                                    "password": "def"
                                }
                            ],
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
        json_post_data = 'username=abc&password=def&action=credentials'
        allure.attach(name="Definition",
                      body="Local user/pass mode (Captive-Credentials): In this mode the client needs to "
                           "enter the valid credentials that are configured in the AP to get the internet access.")
        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                  dut_data=dut_data,
                                                                  passkey=security_key, mode=mode, band=band,
                                                                  num_sta=num_stations, json_post_data=json_post_data,
                                                                  get_testbed_details=get_testbed_details,
                                                                  tip_2x_obj=get_target_object)
        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.ow_regression_lf
    @allure.title("Local user/pass mode with open encryption 5 GHz Band Bridge mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14498", name="WIFI-14498")
    def test_bridge_open_5g_local_user_and_pass(self, setup_initial_configuration, get_test_library,
                                                get_dut_logs_per_test_case, get_test_device_logs,
                                                num_stations, check_connectivity, get_testbed_details,
                                                get_target_object):
        """
            BRIDGE Mode Advanced Captive Portal Test with open encryption 5 GHz Band
            pytest -m "advanced_captive_portal_tests and internal_captive_portal_tests and open and fiveg and bridge and local_user_and_pass"
        """
        profile_data = {"ssid_name": "ssid_captive_portal_open_5g_br", "appliedRadios": ["5G"],
                        "security_key": "something",
                        "captive": {
                            "auth-mode": "credentials",
                            "credentials": [
                                {
                                    "username": "abc",
                                    "password": "def"
                                }
                            ],
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
        band = "fiveg"
        # json post data for API
        json_post_data = 'username=abc&password=def&action=credentials'
        allure.attach(name="Definition",
                      body="Local user/pass mode (Captive-Credentials): In this mode the client needs to "
                           "enter the valid credentials that are configured in the AP to get the internet access.")
        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                  dut_data=dut_data,
                                                                  passkey=security_key, mode=mode, band=band,
                                                                  num_sta=num_stations, json_post_data=json_post_data,
                                                                  get_testbed_details=get_testbed_details,
                                                                  tip_2x_obj=get_target_object)
        assert passes == "PASS", result

    @pytest.mark.owe
    @pytest.mark.twog
    @pytest.mark.sixg
    @pytest.mark.ow_regression_lf
    @allure.title("Local user/pass mode with owe encryption 6 GHz Band Bridge mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14498", name="WIFI-14498")
    def test_bridge_6g_local_user_and_pass(self, setup_initial_configuration, get_test_library,
                                                get_dut_logs_per_test_case, get_test_device_logs,
                                                num_stations, check_connectivity, get_testbed_details,
                                                get_target_object):
        """
            BRIDGE Mode Advanced Captive Portal Test with owe encryption 6 GHz Band
            pytest -m "advanced_captive_portal_tests and internal_captive_portal_tests and owe and sixg and bridge and local_user_and_pass"
        """
        profile_data = {"ssid_name": "int_cap_portal_6g_lup", "appliedRadios": ["6G"],
                        "security_key": "something",
                        "captive": {
                            "auth-mode": "credentials",
                            "credentials": [
                                {
                                    "username": "abc",
                                    "password": "def"
                                }
                            ],
                            "walled-garden-fqdn": [
                                "*.google.com",
                                "telecominfraproject.com"
                            ]
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "sixg"
        # json post data for API
        json_post_data = 'username=abc&password=def&action=credentials'
        allure.attach(name="Definition",
                      body="Local user/pass mode (Captive-Credentials): In this mode the client needs to "
                           "enter the valid credentials that are configured in the AP to get the internet access.")
        passes, result = get_test_library.advanced_captive_portal(ssid=ssid_name, security=security,
                                                                  dut_data=dut_data,
                                                                  passkey=security_key, mode=mode, band=band,
                                                                  num_sta=num_stations, json_post_data=json_post_data,
                                                                  get_testbed_details=get_testbed_details,
                                                                  tip_2x_obj=get_target_object, enable_owe=True, is_bw320=is_bw320,is_ht160=is_ht160)
        assert passes == "PASS", result


