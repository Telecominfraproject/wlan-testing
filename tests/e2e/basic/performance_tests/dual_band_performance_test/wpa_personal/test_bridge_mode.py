"""
       Dual Band Performance Test : BRIDGE Mode
       pytest -m "performance and dual_band_test and bridge"


"""

import os
import allure
import pytest

pytestmark = [pytest.mark.dual_band_test, pytest.mark.bridge,
              pytest.mark.single_station_dual_band_throughput]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa": [
            {"ssid_name": "ssid_wpa_personal_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
            ]},
    "rf": {},
    "radius": False
}


@pytest.mark.dual_band_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestWpaDualbandPerformanceBridge(object):
    """
         pytest -m "performance and dual_band_test and bridge and wpa_personal and twog  and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3726", name="WIFI-3726")
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa_personal_bridge(self, get_test_library, setup_configuration, check_connectivity):
        profile_data = setup_params_general["ssid_modes"]["wpa"]
        ssid_2G, ssid_5G = profile_data[0]["ssid_name"], profile_data[0]["ssid_name"]
        dut_name = list(setup_configuration.keys())[0]
        mode = "BRIDGE"
        vlan = 1
        dut_5g, dut_2g = "", ""
        influx_tags = "dual-band-bridge-wpa"
        for i in setup_configuration[dut_name]['ssid_data']:
            get_test_library.dut_idx_mapping[str(i)] = list(setup_configuration[dut_name]['ssid_data'][i].values())
            if get_test_library.dut_idx_mapping[str(i)][3] == "5G":
                dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + get_test_library.dut_idx_mapping[str(i)][4]
            if get_test_library.dut_idx_mapping[str(i)][3] == "2G":
                dut_2g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' + get_test_library.dut_idx_mapping[str(i)][4]

        dbpt_obj = get_test_library.dualbandperformancetest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G, vlan_id=vlan,
                                                            dut_5g=dut_5g, dut_2g=dut_2g, influx_tags=influx_tags,
                                                            move_to_influx=False, dut_data=setup_configuration)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name, pdf_name="Dual Band Performance Test")
        get_test_library.attach_report_kpi(report_name=report_name)
        assert True
