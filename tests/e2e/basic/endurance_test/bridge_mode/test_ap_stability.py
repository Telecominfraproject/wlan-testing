"""

    Stability Test: Bridge Mode
    pytest -m "regression and bridge"

"""

import os
import allure
import pytest

pytestmark = [pytest.mark.regression, pytest.mark.bridge, pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.regression
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestAPStabilityBridge(object):
    """
         pytest -m "regression and bridge and wpa2_personal and twog  and fiveg"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @allure.testcase(name="test_ap_stability_wpa2_personal",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3035")
    def test_ap_stability_wpa2_personal(self, lf_tools,
                                        create_lanforge_chamberview_dut, lf_test, get_configuration):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)
            if lf_tools.dut_idx_mapping[i][3] == "2G":
                dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_2g)
        apstab_obj = lf_test.apstabilitytest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                             instance_name="stability_instance_wpa2p_bridge",
                                             vlan_id=vlan, dut_5g=dut_5g, dut_2g=dut_2g)

        report_name = apstab_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="AP Stability Test")
        assert True
