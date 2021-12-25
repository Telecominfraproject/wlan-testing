import pytest
import allure

pytestmark = [pytest.mark.mesh, pytest.mark.bridge]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
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
    def testmesh(self, setup_mesh_profile_fix):
        #setup_mesh_scenario):
        pass