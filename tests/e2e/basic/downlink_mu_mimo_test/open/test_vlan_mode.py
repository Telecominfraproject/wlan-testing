"""

    Performance Test: Downlink MU-MIMO Test: Bridge Mode
    pytest -m "downlink_mu_mimo and Vlan and open and fiveg"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.downlink_mu_mimo, pytest.mark.vlan, pytest.mark.open]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "mu-mimo-5g", "appliedRadios": ["5G"]},
            {"ssid_name": "mu-mimo-2g", "appliedRadios": ["2G"]}
        ]
    },
    "rf": [],
    "radius": False
}


@allure.suite("performance")
@allure.feature("NAT MODE open security and Downlink MU_MIMO Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMuMimoVlan(object):
    """
    Downlink MU-MIMO Test: Bridge Mode
    pytest -m downlink_mu_mimo and Vlan
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6849",
                     name="WIFI-6849")
    @pytest.mark.open
    @pytest.mark.fiveg
    def test_mu_mimo_open_bridge_5g(self, lf_tools, lf_test, create_lanforge_chamberview_dut):
        """
            Downlink MU-MIMO Test: Bridge Mode
            pytest -m downlink_mu_mimo and Bridge and open and fiveg
            """
        print('lf tool')
        dut_name = create_lanforge_chamberview_dut
        mode = "VLAN"
        upstream_port = "1.1.eth2"
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
        mimo_obj = lf_test.downlink_mu_mimo(upstream_port=upstream_port, mode=mode, vlan_id=vlan, dut_name=dut_name, dut_5g=dut_5g, dut_2g=dut_2g)
        report_name = mimo_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Downlink MU-MIMO Test")
        assert True
