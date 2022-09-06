"""

    Performance Test: Dataplane Throughput Test: nat Mode
    pytest -m "dataplane_throughput_test and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.dataplane_throughput_test,
              pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("BRIDGE MODE Dataplane Throughput Test")
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputNAT(object):
    """Dataplane THroughput nat Mode
       pytest -m "dataplane_throughput_test and nat"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3913", name="WIFI-3913")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_tcp_udp_wpa2_personal_nat_2g_band_ac_station(self, get_test_library, get_dut_logs_per_test_case,
                                                          get_test_device_logs,
                                                          get_target_object,
                                                          num_stations, setup_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-nat-wpa2-2.4G-ac"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_2G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3914", name="WIFI-3914")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_tcp_udp_wpa2_personal_nat_5g_band_ac_station(self, get_test_library, get_dut_logs_per_test_case,
                                                          get_test_device_logs,
                                                          get_target_object,
                                                          num_stations, setup_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-nat-wpa2-5G-ac"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_WPA2_5G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

    # @pytest.mark.wpa2_personal
    # @pytest.mark.twog
    # def test_tcp_udp_wpa2_personal_nat_2g_band_ax_station(self, get_test_library, get_dut_logs_per_test_case,
    #                                                       get_test_device_logs,
    #                                                       get_target_object,
    #                                                       num_stations):
    #     """Dataplane THroughput nat Mode
    #        pytest -m "dataplane_throughput_test and nat and wpa2_personal and twog"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "ax"
    #     influx_tags = "dataplane-tcp-udp-nat-wpa2-2.4G-ax"
    #     get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
    #                                                num_sta=1, mode=mode,
    #                                                band=band,
    #                                                instance_name="TIP_DPT_DPT_WPA2_2G_NAT_AX",
    #                                                influx_tags=influx_tags, move_to_influx=False,
    #                                                )
    #
    # @pytest.mark.wpa2_personal
    # @pytest.mark.fiveg
    # def test_tcp_udp_wpa2_personal_nat_5g_band_aX_station(self, get_test_library, get_dut_logs_per_test_case,
    #                                                       get_test_device_logs,
    #                                                       get_target_object,
    #                                                       num_stations):
    #     """Dataplane THroughput nat Mode
    #        pytest -m "dataplane_throughput_test and nat and wpa2_personal and fiveg"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "ax"
    #     influx_tags = "dataplane-tcp-udp-nat-wpa2-5G-ax"
    #     get_test_library.dataplane_throughput_test(ssid=ssid_name, passkey=security_key, security=security,
    #                                                num_sta=1, mode=mode,
    #                                                band=band,
    #                                                instance_name="TIP_DPT_DPT_WPA2_5G_NAT_AX",
    #                                                influx_tags=influx_tags, move_to_influx=False,
    #                                                )
    #
