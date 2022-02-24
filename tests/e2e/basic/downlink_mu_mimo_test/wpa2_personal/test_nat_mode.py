"""

    Performance Test: Downlink MU-MIMO Test: NAT Mode
    pytest -m "downlink_mu_mimo and nat and wpa2_personal and fiveg"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.downlink_mu_mimo, pytest.mark.nat, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "mu-mimo-5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "mu-mimo-2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": [],
    "radius": False
}


@allure.suite("performance")
@allure.feature("NAT MODE wpa2_personal security and Downlink MU_MIMO Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMuMimoNat(object):
    """
    Downlink MU-MIMO Test: nat Mode
    pytest -m downlink_mu_mimo and nat
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6849",
                     name="WIFI-6849")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_mu_mimo_wpa2_personal_nat_5g(self, lf_tools, lf_test, create_lanforge_chamberview_dut):
        """
            Downlink MU-MIMO Test: nat Mode
            pytest -m downlink_mu_mimo and nat and wpa2_personal and fiveg
            """
        dut_name = create_lanforge_chamberview_dut
        mode = "NAT"
        vlan = 1
        dut_5g = ""
        dut_2g = ""
        print(lf_tools.dut_idx_mapping)
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4] + ' (1)'
                print(dut_5g)
            if lf_tools.dut_idx_mapping[i][3] == "2G":
                dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4] + ' (2)'
                print(dut_2g)
        tr398_obj = lf_test.tr398Test(mode=mode, vlan_id=vlan, dut_name=dut_name, dut_5g=dut_5g, dut_2g=dut_2g)
        report_name = tr398_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Downlink MU-MIMO Test")
        assert True
