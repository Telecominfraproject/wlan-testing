"""

    Performance Test: Dataplane Throughput Test: VLAN Mode
    pytest -m "dataplane_tests and vlan"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.vlan, pytest.mark.dataplane_tests, pytest.mark.wpa]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa": [
            {"ssid_name": "wpa_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "wpa_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}


@allure.feature("Dataplane Tests")
@allure.parent_suite("Dataplane Tests")
@allure.suite(suite_name="WPA Personal Security")
@allure.sub_suite(sub_suite_name="VLAN Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputVLAN(object):
    """Dataplane THroughput VLAN Mode
       pytest -m "dataplane_tests and wpa and vlan"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @allure.title("Test for TCP UDP Download 2.4 GHz")
    def test_tcp_upd_wpa_vlan_2g_band(self, get_test_library, get_dut_logs_per_test_case,
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
        in the VLAN mode scenario with WPA-Personal security.

        Unique Marker:
        dataplane_tests and vlan and wpa and twog

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        profile_data = {"ssid_name": "wpa_dataplane_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        security_key = profile_data["security_key"]
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        influx_tags = "dataplane-tcp-udp-vlan-wpa-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band, vlan_id=vlan,
                                                   instance_name="TIP_DPT_DPT_WPA_2G_VLAN",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.wpa_personal
    @pytest.mark.fiveg
    @allure.title("Test for TCP UDP Download 5 GHz")
    def test_tcp_upd_wpa_vlan_5g_band(self, get_test_library, get_dut_logs_per_test_case,
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
        in the VLAN mode scenario with WPA-Personal security.

        Unique Marker:
        dataplane_tests and vlan and wpa and fiveg

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        profile_data = {"ssid_name": "wpa_dataplane_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        security_key = profile_data["security_key"]
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        influx_tags = "dataplane-tcp-udp-vlan-wpa-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security, passkey=security_key,
                                                   num_sta=1, mode=mode,
                                                   band=band, vlan_id=vlan,
                                                   instance_name="TIP_DPT_DPT_WPA_5G_VLAN",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   dut_data=setup_configuration,
                                                   client_type=client_type
                                                   )
