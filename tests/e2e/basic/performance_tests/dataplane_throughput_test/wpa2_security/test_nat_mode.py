"""

    Performance Test: Dataplane Throughput Test: NAT Mode
    pytest -m "dataplane_tests wpa2_personal security and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_tests,
              pytest.mark.nat, pytest.mark.wpa2_personal, pytest.mark.performance]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "wpa2_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa2_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("Dataplane Tests")
@allure.parent_suite("Dataplane Tests")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputNAT(object):
    """Dataplane THroughput NAT Mode
       pytest -m "dataplane_tests and wpa2_personal and nat"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("Test for TCP UDP Download 2.4 GHz")
    def test_tcp_upd_wpa2_personal_nat_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, client_type,
                                               get_target_object,
                                               num_stations, setup_configuration):
        """
        The WiFi data plane test is designed to conduct on automatic testing of combinations of station types,
        MIMO types, Channel Bandwidths. Traffic types. Traffic direction, Frame sizes etc. It will run a quick
        throughput test at every combination of these test variables and plot at the results in a set of
        charts to compare performance. The user is allowed to define an intended load as a percentage of the
        max theoretical PHY rate for every test combination.
        The expected behavior is that for every test combination the achieved throughput should be at least 70% of
        the theoretical max PHY rate under ideal test conditions.
        Objective of this test plan is to check the throughput on the single station with different frame sizes
        in the NAT mode scenario with WPA2-Personal security.

        Unique Marker:
        dataplane_tests and nat and wpa2_personal and twog

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        profile_data = {"ssid_name": "wpa2_personal_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        mode = "NAT-WAN"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-nat-wpa2_personal-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_2G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.title("Test for TCP UDP Download 5 GHz")
    def test_tcp_upd_wpa2_personal_nat_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, client_type,
                                               get_target_object,
                                               num_stations, setup_configuration):
        """
        The WiFi data plane test is designed to conduct on automatic testing of combinations of station types,
        MIMO types, Channel Bandwidths. Traffic types. Traffic direction, Frame sizes etc. It will run a quick
        throughput test at every combination of these test variables and plot at the results in a set of
        charts to compare performance. The user is allowed to define an intended load as a percentage of the
        max theoretical PHY rate for every test combination.
        The expected behavior is that for every test combination the achieved throughput should be at least 70% of
        the theoretical max PHY rate under ideal test conditions.
        Objective of this test plan is to check the throughput on the single station with different frame sizes
        in the NAT mode scenario with WPA2-Personal security.

        Unique Marker:
        dataplane_tests and nat and wpa2_personal and fiveg

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        profile_data = {"ssid_name": "wpa2_personal_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        mode = "NAT-WAN"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-nat-wpa2_personal-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_5G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )
