"""

    Test Spatial Consistency: Bridge Mode
    pytest -m spatial_consistency
"""

import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.spatial_consistency, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            'band': '5G',
            "channel": 36,
            "channel-width": 80
        },
        "2G": {
            'band': '2G',
            "channel": 6,
            "channel-width": 20

        }

    },
    "radius": False
}


@allure.feature("Spatial Consistency")
@allure.feature("Spatial Consistency")
@allure.parent_suite("Spatial Consistency Test")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="Bridge Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_SpatialConsistency_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ac
    @allure.title("Spatial Consistency Test for AC Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13336", name="WIFI-13336")
    def test_spatial_consistency_ac_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Spatial consistency test intends to verify the Wi-Fi signal consistency in spatial
            domain by testing throughput with DUT at different angles to the Station and at different
            emulated distance. The angles are changed with a programmable turn-table.
            The distance is emulated by adjusting attenuation.

            Marker:
            advance_ac and spatial_consistency and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 0"], ["skip_ax: 1"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="spatial",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ax
    @allure.title("Spatial Consistency Test for AX Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13336", name="WIFI-13336")
    def test_spatial_consistency_ax_bridge(self, get_test_library, setup_configuration, check_connectivity,
                                           selected_testbed):
        """
            Test Description:
            Spatial consistency test intends to verify the Wi-Fi signal consistency in spatial
            domain by testing throughput with DUT at different angles to the Station and at different
            emulated distance. The angles are changed with a programmable turn-table.
            The distance is emulated by adjusting attenuation.

            Marker:
            advance_ax and spatial_consistency and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 1"], ["skip_ax: 0"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="spatial",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description
