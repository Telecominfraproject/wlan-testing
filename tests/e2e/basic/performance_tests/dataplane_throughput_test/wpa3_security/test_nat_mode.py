"""

    Performance Test: Dataplane Throughput Test: NAT Mode
    pytest -m "dataplane_tests wpa3_personal security and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_tests,
              pytest.mark.nat, pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("NAT MODE wpa3_personal security and Dataplane Throughput Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputNAT(object):
    """Dataplane THroughput NAT Mode
       pytest -m "dataplane_tests and wpa3_personal and nat"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.twog
    def test_tcp_upd_wpa3_personal_nat_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, client_type,
                                               get_target_object,
                                               num_stations, setup_configuration):
        """Dataplane THroughput NAT Mode.
           pytest -m "dataplane_tests and nat and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "NAT-WAN"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-nat-wpa3_personal-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA3_PERSONAL_2G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.fiveg
    def test_tcp_upd_wpa3_personal_nat_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, client_type,
                                               get_target_object,
                                               num_stations, setup_configuration):
        """Dataplane THroughput NAT Mode
           pytest -m "dataplane_tests and nat and wpa3_personal and fiveg"
        """
        profile_data = {"ssid_name": "wpa3_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        security_key = profile_data["security_key"]
        mode = "NAT-WAN"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-nat-wpa3_personal-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA3_PERSONAL_5G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration
                                                   )
