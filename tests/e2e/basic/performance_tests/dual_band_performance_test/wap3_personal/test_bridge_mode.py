"""
       Dual Band Performance Test : BRIDGE Mode
       pytest -m "performance and dual_band_tests and bridge"


"""

import allure
import pytest

pytestmark = [pytest.mark.dual_band_tests, pytest.mark.bridge,
              pytest.mark.single_station_dual_band_throughput]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_personal_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
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
@allure.suite("Bridge Mode")
@allure.sub_suite("wpa3_personal security")
@allure.feature("Dual band performance test")
@pytest.mark.usefixtures("setup_configuration")
class TestWpa3DualbandPerformanceBridge(object):
    """
         pytest -m "performance and dual_band_tests and bridge and wpa3_personal and twog  and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3728", name="WIFI-3728")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.title("Test Dual Band with ApAuto test of bridge mode")
    def test_client_wpa3_personal_bridge(self, get_test_library, setup_configuration, check_connectivity):
        """
        The Dual-band Throughput Test is intended to measure the throughput the DUT can support when concurrently
        connected to multiple stations on both the 2.4 and 5 GHz bands, each operating with two spatial streams.
        The purpose of these additional test cases is to detect cross band interference of the DUT's transmitter
        on the receiver. The weak link is needed to ensure DUT and STA are transmitting at the highest power and
        causing the most potential interference when the receiver is more susceptible to noise (low SNR). Note,
        each station is connected using either the 2.4 or 5 GHz band, but not both bands simultaneously. This test
        requires at least 2 stations, located 2m from the DUT. The DUT will need to support at least 4 independent
        radio chains for this test case, two operating in the 2.4 GHz band and two operating in the 5 GHz band.

        Unique Marker:
        dual_band_tests and bridge and wpa3_personal
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"]
        ssid_2G, ssid_5G = profile_data[0]["ssid_name"], profile_data[0]["ssid_name"]
        dut_name = list(setup_configuration.keys())[0]
        mode = "BRIDGE"
        vlan = 1
        dut_5g, dut_2g = "", ""
        influx_tags = "dual-band-bridge-wpa3"
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
