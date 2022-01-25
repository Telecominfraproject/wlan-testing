import pytest
import allure
import os

pytestmark = [pytest.mark.mesh, pytest.mark.bridge]

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
class TestMesh(object):

    @pytest.mark.wpa2_personal
    def testmesh_2g(self, setup_mesh_profile_fix, lf_test, lf_tools):
        raw_lines = [['selected_dut2: tip-node-2 ssid_wpa2_2g_1 90:3c:b3:9d:69:2f (2)'], ['selected_dut5: tip-node-2 ssid_wpa2_5g_1 90:3c:b3:9d:69:2e (1)'], ['sta_amount-2: 2'], ['radios-2-0: 1.4.6 wiphy0'],
               ['ap_arrangements: Current Position'], ['sta_position: Current Position'],['chamber-0: RootAP'],['chamber-1: Node1'],
               ['chamber-2: Node2'],['chamber-4: MobileStations'],
               ['path: Orbit Current'], ['traffic_types: TCP'], ['direction: Both'], ['tests: Throughput'], ['traf_combo: N2'],
                     ["skip_dhcp: 1"], ["skip_5: 1"] ]

        mesh_o = lf_test.mesh_test(instance_name="test_mesh1_1", raw_lines=raw_lines,duration="5m")
        report_name = mesh_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        print("report name ", report_name)
        entries = os.listdir("../reports/" + report_name + '/')
        print("entries", entries)
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Basic Mesh Test")

        assert True
