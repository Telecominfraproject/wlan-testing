"""

    Performance Test: Receiver Sensitivity Test: bridge Mode
    pytest -m "rx_sensitivity_tests and wpa2_personal and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.rx_sensitivity_tests, pytest.mark.bridge, pytest.mark.wpa2_personal]

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


@allure.feature("Receiver Sensitivity")
@allure.parent_suite("Receiver Sensitivity Test")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_RxSensitivitytests_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Receiver Sensitivity Test")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13329", name="WIFI-13329")
    def test_rx_sensitivity_tests_bridge(self, get_test_library, setup_configuration, check_connectivity, selected_testbed):
        """
            Test Description:
            Receiver Sensitivity is a receiver's ability to receive and correctly demodulate weak signals.
            This test provides a simplified measurement of the receiver's sensitivity, relative to the total
            attenuation inserted between the DUT and the STA. As that attenuation is increased, the STA is
            limited to a single coding scheme, eventually causing the connection to degrade.
            The point at which the connection degrades represents the receiver's approximate sensitivity.
            This is an approximate measurement only, where a detailed receiver sensitivity measurement would
            typically be performed in a conducted test environment with calibrated transmitter power levels.
            The test is repeated with multiple coding schemes, ensuring the DUT should smoothly
            transition between coding schedules as the attenuation increases in normal operation.

            Marker:
            advance and rx_sensitivity_tests and wpa2_personal and bridge

            Note: Please refer to the PDF report for the Test Procedure, Pass/Fail Criteria, and Candela Score.
        """
        mode = "BRIDGE"
        vlan = 1
        result, description = get_test_library.tr398v2(mode=mode, vlan_id=vlan, test="rxsens",
                                                       dut_data=setup_configuration, move_to_influx=False,
                                                       testbed=selected_testbed)
        if result:
            assert True
        else:
            assert False, description
