"""
       Dual Band Performance Test : NAT Mode
       pytest -m "performance and dual_band_tests and nat"


"""

import allure
import pytest

pytestmark = [pytest.mark.dual_band_tests, pytest.mark.nat, pytest.mark.performance_release]#,

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_wpa2p_2g", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ]},
    "rf": {},
    "radius": False
}


@pytest.mark.dual_band_tests
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.parent_suite("Dual Band Tests")
@allure.suite("Dual Band Tests: NAT mode")
@allure.sub_suite("Open security")
@allure.feature("Dual band performance test")
@pytest.mark.usefixtures("setup_configuration")
class TestOpenDualbandPerformanceNat(object):
    """
         pytest -m "performance and dual_band_tests and nat and open and twog  and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3724", name="WIFI-3724")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("Test Dual Band with ApAuto test of NAT mode")
    def test_client_open_bridge(self, get_test_library, setup_configuration, check_connectivity):
        """
                    Dual Band Test with open encryption
                    pytest -m "dual_band_tests and open"
        """
        profile_data = setup_params_general["ssid_modes"]["open"]
        ssid_2G, ssid_5G = profile_data[0]["ssid_name"], profile_data[0]["ssid_name"]
        dut_name = list(setup_configuration.keys())[0]
        mode = "NAT-WAN"
        vlan = 1
        dut_5g, dut_2g = "", ""
        influx_tags = "dual-band-bridge-open"
        for i in setup_configuration[dut_name]['ssid_data']:
            get_test_library.dut_idx_mapping[str(i)] = list(setup_configuration[dut_name]['ssid_data'][i].values())
            if get_test_library.dut_idx_mapping[str(i)][3] == "5G":
                dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + \
                         get_test_library.dut_idx_mapping[str(i)][4]
            if get_test_library.dut_idx_mapping[str(i)][3] == "2G":
                dut_2g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + \
                         get_test_library.dut_idx_mapping[str(i)][4]

        get_test_library.dual_band_performance_test(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G, vlan_id=vlan,
                                                    dut_5g=dut_5g, dut_2g=dut_2g, influx_tags=influx_tags,
                                                    move_to_influx=False, dut_data=setup_configuration)

        assert True
