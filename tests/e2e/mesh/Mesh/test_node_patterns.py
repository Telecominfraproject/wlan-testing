import pytest
import allure
import os

pytestmark = [pytest.mark.mesh, pytest.mark.bridge, pytest.mark.node_patterns]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g_1", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "mesh": "yes",
    "rf": {},
    "radius": False
}


@allure.feature("MESH BASIC")
@pytest.mark.parametrize(
    'setup_mesh_profile_fix',
    [setup_params_general],
    indirect=True,
    scope="class"
)
# @pytest.mark.usefixtures("setup_profiles")
class TestNodePatters(object):

    @pytest.mark.wpa2_personal
    def test_throughput_latency_2g_5g_ap_chamber_pos_ABC(self, setup_mesh_profile_fix, lf_test, lf_tools):
        #lf_tools.reset_scenario()
        raw_lines = [['selected_dut2: tip-root ssid_wpa2_2g_1 34:ef:b6:af:4a:7d (2)'], ['selected_dut5: tip-root ssid_wpa2_5g_1 34:ef:b6:af:4a:7e (1)'],
                    ['sta_amount-4: 1'], ['radios-0-0: 1.2.6 wiphy0'], ['radios-0-3: 1.2.7 wiphy1'], ['radios-1-0: 1.3.6 wiphy0'],
                    ['radios-1-3: 1.3.7 wiphy1'], ['radios-2-0: 1.4.6 wiphy0'], ['radios-2-3: 1.4.7 wiphy1'],
                    ['radios-4-0: 1.1.6 wiphy2'], ['radios-4-3: 1.1.7 wiphy3'], ['ap_arrangements: ABC'],
                    ['sta_position: Current Position'], ['chamber-0: Root'], ['chamber-1: Node1'],
                    ['chamber-2: Node2'], ['chamber-4: Mobile-Sta'],
                    ['path: Orbit Current'], ['traffic_types: UDP'], ['direction: Both'], ['tests: Throughput'], ['traf_combo: STA']]

        mesh_o = lf_test.mesh_test(instance_name="node_patterns_ABC", raw_lines=raw_lines)
        report_name = mesh_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        print("report name ", report_name)
        entries = os.listdir("../reports/" + report_name + '/')
        print("entries", entries)
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Node patterns")

        assert True