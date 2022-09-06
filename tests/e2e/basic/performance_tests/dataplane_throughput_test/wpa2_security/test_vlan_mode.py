"""

    Performance Test: Dataplane Throughput Test: VLAN Mode
    pytest -m "dataplane_throughput_test and vlan"


"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance,
              pytest.mark.vlan, pytest.mark.dataplane_throughput_test]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("VLAN MODE Dataplane Throughput Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputVLAN(object):
    """Dataplane THroughput VLAN Mode
       pytest -m "dataplane_throughput_test and vlan"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3913", name="WIFI-3913")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_tcp_upd_wpa2_personal_vlan_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs,
                                                get_target_object,
                                                num_stations, setup_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "dataplane_throughput_test and vlan and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        influx_tags = "dataplane-tcp-udp-vlan-wpa2-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security,
                                                   num_sta=1, mode=mode, passkey=security_key,
                                                   band=band, vlan_id=vlan,
                                                   instance_name="TIP_DPT_DPT_WPA2_2G_VLAN",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3914", name="WIFI-3914")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_tcp_upd_wpa2_personal_vlan_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs,
                                                get_target_object,
                                                num_stations, setup_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "dataplane_throughput_test and vlan and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        influx_tags = "dataplane-tcp-udp-vlan-wpa2-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security,
                                                   num_sta=1, mode=mode, passkey=security_key,
                                                   band=band, vlan_id=vlan,
                                                   instance_name="TIP_DPT_DPT_WPA2_5G_VLAN",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

