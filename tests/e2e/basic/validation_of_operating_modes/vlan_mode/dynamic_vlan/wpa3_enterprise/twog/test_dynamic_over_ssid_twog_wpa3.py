"""

   Dynamic_Vlan: VLAN Mode
    pytest -m "dynamic_vlan and wpa3_enterprise and vlan"

"""

import os
import allure
import pytest
from configuration import DYNAMIC_VLAN_RADIUS_SERVER_DATA
from configuration import DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.regression, pytest.mark.dynamic_vlan, pytest.mark.wpa3_enterprise, pytest.mark.vlan,pytest.mark.twog]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3e_2g", "appliedRadios": ["2G"],
             "security_key": "something",
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             "vlan": 100
             }]},
    "rf": {},
    "radius": True
}


@allure.suite("regression")
@allure.feature("VLAN MODE wpa3_enterprise Dynamic Vlan")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDynamicVlanOverSsid2GWpa3(object):

    @pytest.mark.dynamic_precedence_over_ssid
    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_precedence_over_ssid_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6096")
    def test_dynamic_precedence_over_ssid_vlan_2g_wpa3(self, get_vif_state, lf_tools,get_ap_logs,get_lf_logs,
                                                    create_lanforge_chamberview_dut, lf_test, get_configuration,
                                                    station_names_twog):
        """
                pytest -m "dynamic_precedence_over_ssid and wpa3_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = [100,200]
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=vlan)

        lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa3", extra_securities=[],
                            mode=mode, band="twog", vlan_id=vlan[0],
                            station_name=station_names_twog, key_mgmt="WPA-EAP-SHA256",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordB", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="userB", d_vlan=True)

        eth_ssid_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                               "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]

        eth_radius_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_twog[0]].split('.')
        eth_vlan_ip_1 = eth_radius_vlan_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_twog[0]])
        print("vlan ip...", eth_radius_vlan_ip)
        print("eth_upstream_ip..", eth_ip)
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_vlan_ip_1[0] == "0":
            print("radius configured vlan didnt recieved ip")
            assert False
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True

        allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_twog[0]]))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan[0])))
        allure.attach(name="ssid configured vlan ip....", body=str(eth_ssid_vlan_ip))
        allure.attach(name="radius configured vlan..", body=str(port_resources[2] + "." + str(vlan[1])))
        allure.attach(name="radius configured vlan ip....", body=str(eth_radius_vlan_ip))
        allure.attach(name="upstream ip....", body=str(eth_ip))
        if val:
            assert True
            print("Station ip assigned as per dynamic vlan")
        elif not val:
            print("Station ip not assigned as per dynamic vlan")
            assert False