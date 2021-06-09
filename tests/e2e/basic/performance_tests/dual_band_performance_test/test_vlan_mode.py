import pytest

pytestmark = [pytest.mark.dual_band_performance_test, pytest.mark.vlan]
import sys

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')
import lf_ap_auto_test
import time
from lf_ap_auto_test import ApAutoTest

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2p_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2p_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.dual_band_performance_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDualbandPerformanceVlan(object):

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_open(self, get_lanforge_data, testbed, lf_tools):
        profile_data = setup_params_general["ssid_modes"]["open"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[1]["ssid_name"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio_2G = []
        radio_2G.append(get_lanforge_data["lanforge_2dot4g"])
        radio_5G = []
        radio_5G.append(get_lanforge_data["lanforge_5g"])
        dut_name = testbed

        CV_Test = ApAutoTest(lf_host=lanforge_ip,
                             lf_port=lanforge_port,
                             lf_user="lanforge",
                             lf_password="lanforge",
                             instance_name="dbp_instance_open_vlan",
                             config_name="dbp_config",
                             upstream=upstream,
                             pull_report=True,
                             dut5_0=dut_name + ' ' + ssid_5G,
                             dut2_0=dut_name + ' ' + ssid_2G,
                             load_old_cfg=False,
                             max_stations_2=1,
                             max_stations_5=1,
                             max_stations_dual=2,
                             radio2=[["1.1.wiphy0"]],
                             radio5=[["1.1.wiphy1"]],
                             sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '1'],
                                   ['Throughput vs Pkt Size', '0'], ['Capacity', '0'], ['Stability', '0'],
                                   ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                   ['Long-Term', '0']]
                             )
        CV_Test.setup()
        CV_Test.run()

        @pytest.mark.wpa
        @pytest.mark.twog
        @pytest.mark.fiveg
        def test_client_wpa(self, get_lanforge_data, testbed, lf_tools):
            profile_data = setup_params_general["ssid_modes"]["wpa"]
            ssid_2G = profile_data[0]["ssid_name"]
            ssid_5G = profile_data[1]["ssid_name"]
            lanforge_ip = get_lanforge_data["lanforge_ip"]
            lanforge_port = int(get_lanforge_data["lanforge-port-number"])
            upstream = get_lanforge_data["lanforge_bridge_port"]
            radio_2G = []
            radio_2G.append(get_lanforge_data["lanforge_2dot4g"])
            radio_5G = []
            radio_5G.append(get_lanforge_data["lanforge_5g"])
            dut_name = testbed

            CV_Test = ApAutoTest(lf_host=lanforge_ip,
                                 lf_port=lanforge_port,
                                 lf_user="lanforge",
                                 lf_password="lanforge",
                                 instance_name="dbp_instance_wpa_vlan",
                                 config_name="dbp_config",
                                 upstream=upstream,
                                 pull_report=True,
                                 dut5_0=dut_name + ' ' + ssid_5G,
                                 dut2_0=dut_name + ' ' + ssid_2G,
                                 load_old_cfg=False,
                                 max_stations_2=1,
                                 max_stations_5=1,
                                 max_stations_dual=2,
                                 radio2=[["1.1.wiphy0"]],
                                 radio5=[["1.1.wiphy1"]],
                                 sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '1'],
                                       ['Throughput vs Pkt Size', '0'], ['Capacity', '0'], ['Stability', '0'],
                                       ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                       ['Long-Term', '0']]
                                 )
            CV_Test.setup()
            CV_Test.run()

    @pytest.mark.wpa2_personal
    def test_client_wpa2_personal(self, get_lanforge_data, testbed, lf_tools):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[1]["ssid_name"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio_2G = []
        radio_2G.append(get_lanforge_data["lanforge_2dot4g"])
        radio_5G = []
        radio_5G.append(get_lanforge_data["lanforge_5g"])
        dut_name = testbed

        CV_Test = ApAutoTest(lf_host=lanforge_ip,
                             lf_port=lanforge_port,
                             lf_user="lanforge",
                             lf_password="lanforge",
                             instance_name="dbp_instance_wpa2p_vlan",
                             config_name="dbp_config",
                             upstream="1.1." + upstream,
                             pull_report=True,
                             dut5_0=dut_name + ' ' + ssid_5G,
                             dut2_0=dut_name + ' ' + ssid_2G,
                             load_old_cfg=False,
                             max_stations_2=1,
                             max_stations_5=1,
                             max_stations_dual=2,
                             radio2=[["1.1.wiphy0"]],
                             radio5=[["1.1.wiphy1"]],
                             sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '1'],
                                   ['Throughput vs Pkt Size', '0'], ['Capacity', '0'], ['Stability', '0'],
                                   ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                   ['Long-Term', '0']]
                             )
        CV_Test.setup()
        CV_Test.run()
