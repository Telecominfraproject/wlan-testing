"""
       Dual Band Performance Test : NAT Mode
       pytest -m "performance and dual_band_tests and nat"


"""

import os
import allure
import pytest

pytestmark = [pytest.mark.performance, pytest.mark.dual_band_tests, pytest.mark.nat,
              pytest.mark.single_station_dual_band_throughput]
setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_personal_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
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
@allure.suite("NAT Mode")
@allure.sub_suite("wpa2_personal security")
@allure.feature("Dual band performance test")
@pytest.mark.usefixtures("setup_configuration")
class TestWpa2DualbandPerformanceNat(object):
    """
         pytest -m "performance and dual_band_tests and nat and wpa2_personal and twog  and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3918", name="WIFI-3918")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("Test Dual Band with ApAuto test of NAT mode")
    def test_client_wpa2_personal_bridge(self, get_test_library, setup_configuration, check_connectivity):
        """
                                    Dual Band Test with wpa2_personal encryption
                                    pytest -m "dual_band_tests and wpa2_personal"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]
        ssid_2G, ssid_5G = profile_data[0]["ssid_name"], profile_data[0]["ssid_name"]
        dut_name = list(setup_configuration.keys())[0]
        mode = "NAT-WAN"
        vlan = 1
        dut_5g, dut_2g = "", ""
        influx_tags = "dual-band-nat-wpa2"
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
