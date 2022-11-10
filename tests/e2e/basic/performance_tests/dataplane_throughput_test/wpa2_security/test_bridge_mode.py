"""

    Performance Test: Dataplane Throughput Test: BRIDGE Mode
    pytest -m "dataplane_tests wpa2_personal security and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_tests,
              pytest.mark.bridge, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "wpa2_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa2_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("BRIDGE MODE wpa2_personal security and Dataplane Throughput Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputBRIDGE(object):
    """Dataplane THroughput BRIDGE Mode
       pytest -m "dataplane_tests and wpa2_personal and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.twog
    def test_tcp_upd_wpa2_personal_bridge_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, setup_configuration):
        """Dataplane THroughput BRIDGE Mode.
           pytest -m "dataplane_tests and bridge and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "wpa2_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-bridge-wpa2_personal-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_2G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.fiveg
    def test_tcp_upd_wpa2_personal_bridge_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, client_type,
                                                  get_target_object,
                                                  num_stations, setup_configuration):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_tests and bridge and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "wpa2_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        mode = "BRIDGE"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-bridge-wpa2_personal-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_5G_BRIDGE",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration
                                                   )
