"""

   Dynamic_Vlan: Bridge Mode
    pytest -m "dynamic_vlan and wpa2_personal and bridge"

"""

import os
import allure
import pytest

pytestmark = [pytest.mark.regression, pytest.mark.dynamic_vlan, pytest.mark.wpa2_enterprise, pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2e_2g", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {},
    "radius": True
}


@allure.suite("regression")
@allure.feature("NAT MODE wpa2_enterprise Dynamic Vlan")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDynamicVlan(object):

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_vlan_5710",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5710")
    def test_dynamic_vlan_5710(self, get_vif_state, lf_tools,
                               create_lanforge_chamberview_dut, lf_test, get_configuration, station_names_twog):
        """
                pytest -m "dynamic_vlan and wpa2_personal and bridge"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        password_2G = profile_data[0]["security_key"]
        security_2g = setup_params_general["ssid_modes"]

        dut_name = create_lanforge_chamberview_dut
        mode = "NAT"
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        # for i in lf_tools.dut_idx_mapping:
        #
        #     if lf_tools.dut_idx_mapping[i][3] == "2G":
        #         dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
        #         print(dut_2g)
        # if ssid_2G not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        eap_obj = lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                                      mode=mode, band="twog", vlan_id=100,
                                      station_name=station_names_twog, key_mgmt="WPA-EAP",
                                      pairwise="NA", group="NA", wpa_psk="DEFAULT",
                                      ttls_passwd="passwordA", ieee80211w=0,
                                      wep_key="NA", ca_cert="NA", eap="TTLS", identity="userA")

        station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                       station_names_twog[0])["interface"]["ip"]
        print(station_ip)

        print(eap_obj)

        # report_name = eap_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        # lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True
