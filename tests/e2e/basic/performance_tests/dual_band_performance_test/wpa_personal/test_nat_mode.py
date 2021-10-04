"""
       Dual Band Performance Test : NAT Mode
       pytest -m "performance and dual_band_test and nat"


"""

import os
import allure
import pytest

pytestmark = [pytest.mark.dual_band_test, pytest.mark.nat,
              pytest.mark.single_station_dual_band_throughput]
setup_params_general = {
    "mode": "NAT",
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
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDualbandPerformanceNat(object):
    """
         pytest -m "performance and dual_band_test and nat and wpa_personal and twog  and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3726", name="WIFI-3726")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa_personal_nat(self, get_vif_state, lf_tools,
                                  create_lanforge_chamberview_dut, lf_test, get_configuration):
        profile_data = setup_params_general["ssid_modes"]["wpa"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "NAT"
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
        if ssid_2G and ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        dbpt_obj = lf_test.dualbandperformancetest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                                   instance_name="dbp_instance_wpap_nat_p",
                                                   vlan_id=vlan, dut_5g=dut_5g, dut_2g=dut_2g)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dual Band Performance Wpa Nat Test")
        assert True