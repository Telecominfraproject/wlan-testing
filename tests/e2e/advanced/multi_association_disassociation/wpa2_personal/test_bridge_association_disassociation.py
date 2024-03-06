"""

    Multi Association and Disassociation: BRIDGE Mode
    pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge"

"""

import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multi_assoc_disassoc_tests, pytest.mark.bridge]

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


@allure.feature("Multi Association and Disassociation")
@allure.parent_suite("Multi Association and Disassociation Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_MultiAssoc_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.advance_ac
    @allure.title("Multi Association and Disassociation Test for AC Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13339", name="WIFI-13339")
    def test_multi_assoc_disassoc_ac_bridge(self, get_test_library, setup_configuration, check_connectivity,
                                            selected_testbed):
        """
            Test Description:
            Multiple association / disassociation stability test intends to measure stability of Wi-Fi device under a
            dynamic environment with frequent change of connection status.

            Marker:
            advance_ac and multi_assoc_disassoc_tests and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 0"], ["skip_ax: 1"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="reset",
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
    @allure.title("Multi Association and Disassociation Test for AX Clients in BRIDGE Mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13339", name="WIFI-13339")
    def test_multi_assoc_disassoc_ax_bridge(self, get_test_library, setup_configuration, check_connectivity,
                                            selected_testbed):
        """
            Test Description:
            Multiple association / disassociation stability test intends to measure stability of Wi-Fi device under a
            dynamic environment with frequent change of connection status.

            Marker:
            advance_ax and multi_assoc_disassoc_tests and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        raw_line = [["skip_ac: 1"], ["skip_ax: 0"]]
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="reset",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed, extra_raw_lines=raw_line)
        if result:
            assert True
        else:
            assert False, description
