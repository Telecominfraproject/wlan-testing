"""

    Performance Test: Dataplane Throughput Test: BRIDGE Mode
    pytest -m "dataplane_tests wpa3_personal security and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_tests,
              pytest.mark.bridge, pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]},
    "rf": {},
    "radius": False
}


@allure.feature("Dataplane Tests")
@allure.parent_suite("Dataplane Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
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
    @pytest.mark.sixg
    @pytest.mark.performance
    @allure.title("Test for TCP UDP Download 6 GHz")
    def test_tcp_udp_wpa3_personal_bridge_6g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, setup_configuration):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_tests and bridge and wpa3_personal and sixg"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        band = "sixg"
        influx_tags = "dataplane-tcp-udp-bridge-wpa3_personal-6G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=num_stations, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA_6G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )
