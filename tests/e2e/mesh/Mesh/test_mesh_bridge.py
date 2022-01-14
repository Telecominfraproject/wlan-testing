import pytest
import allure
import os

pytestmark = [pytest.mark.mesh, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
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
        raw_lines = [['selected_dut2: tip-node2 OpenWifi123 90:3c>b3:9d:69:36(1)'], ['selected_dut5: tip-node2 OpenWifi 90:3c:b3:9d:69:2f(2)'], ['sta_amount-2: 2'], ['radios-2-0: 1.4.6 wiphy0'],
               ['radios-2-3: 1.4.7 wiphy1'], ['ap_arrangements: Current Position'], ['sta_position: Current Position'],
               ['path: Orbit Current'], ['traffic_types: UDP;TCP'], ['direction: Both'], ['tests: Throughput'], ['traf_combo: N2']]

        mesh_o = lf_test.mesh_test(instance_name="meshtest-01", raw_lines=raw_lines)
        report_name = mesh_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        print("report name ", report_name)
        entries = os.listdir("../reports/" + report_name + '/')
        print("entries", entries)
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Basic Mesh Test")

        assert True