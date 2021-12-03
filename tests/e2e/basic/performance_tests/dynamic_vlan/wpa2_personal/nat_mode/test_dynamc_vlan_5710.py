"""

   Dynamic_Vlan: Bridge Mode
    pytest -m "dynamic_vlan and wpa2_personal and bridge"

"""

import os
import allure
import pytest

pytestmark = [pytest.mark.regression, pytest.mark.dynamic_vlan, pytest.mark.wpa2_enterprise, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2e_2g", "appliedRadios": ["2G"],
             "security_key": "something","vlan":300}]},
    "rf": {},
    "radius": True
}


@allure.suite("regression")
@allure.feature("BRIDGE MODE wpa2_enterprise Dynamic Vlan")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDynamicVlan(object):

    @pytest.mark.absenceofradiusvlanttidentifier
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_vlan_5704",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5704")
    def test_dynamic_vlan_5704(self, get_vif_state, lf_tools,
                               create_lanforge_chamberview_dut, lf_test, get_configuration, station_names_twog):
        """
                pytest -m "dynamic_vlan and wpa2_personal and bridge"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        mode = "BRIDGE"
        vlan_id = profile_data[0]["vlan"]
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.add_vlan(vlan_ids=[vlan_id])
        # for i in lf_tools.dut_idx_mapping:
        #
        #     if lf_tools.dut_idx_mapping[i][3] == "2G":
        #         dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
        #         print(dut_2g)
        # if ssid_2G not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="twog",vlan_id=vlan_id,
                            station_name=station_names_twog, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordvlannotsentuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="vlannotsentuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_twog[0]].split('.')
        print(sta_ip_1)
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_twog[0]])
        print("vlan ip...", eth_vlan_ip)
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                allure.attach("vlan ip....", eth_vlan_ip)
                allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
                print("Station ip not assigned as per ssid vlan")
                assert False
            else:
                assert True
                allure.attach("vlan ip....", eth_vlan_ip)
                allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
                print("Station ip assigned as per ssid configured vlan")


    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_vlan_5710",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5705")
    def test_dynamic_vlan_5705(self, get_vif_state, lf_tools,
                             create_lanforge_chamberview_dut, lf_test, get_configuration, station_names_twog):
        """
                pytest -m "dynamic_vlan and wpa2_personal and bridge"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        mode = "BRIDGE"
        vlan = "100"
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.add_vlan(vlan_ids=[vlan])
        # for i in lf_tools.dut_idx_mapping:
        #
        #     if lf_tools.dut_idx_mapping[i][3] == "2G":
        #         dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
        #         print(dut_2g)
        # if ssid_2G not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="twog", vlan_id=100,
                            station_name=station_names_twog, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordA", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="userA", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + vlan)["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_twog[0]].split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_twog[0]])
        print("vlan ip...", eth_vlan_ip)
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                allure.attach("vlan ip....", eth_vlan_ip)
                allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
                print("Station ip not assigned as per vlan")
                assert False
            else:
                assert True
                allure.attach("vlan ip....", eth_vlan_ip)
                allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
                print("Station ip assigned as per dynamic vlan")



    @pytest.mark.unsupported
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_unsupported_vlan_5710",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5710")
    def test_dynamic_unsupported_vlan_5711(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration,
                                                station_names_twog):
        """
                pytest -m "dynamic_vlan and wpa2_personal and bridge"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        mode = "BRIDGE"
        vlan = "ABC"
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.add_vlan(vlan_ids=[vlan])
        # for i in lf_tools.dut_idx_mapping:
        #
        #     if lf_tools.dut_idx_mapping[i][3] == "2G":
        #         dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
        #         print(dut_2g)
        # if ssid_2G not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="twog", vlan_id="ABC",
                            station_name=station_names_twog, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordinvalidvlanuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="invalidvlanuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + vlan)["interface"]["ip"]

        if lf_test.station_ip[station_names_twog[0]] == "0.0.0.0":
            print("station ip...", lf_test.station_ip[station_names_twog[0]])
            assert True
            allure.attach("vlan ip....", eth_vlan_ip)
            allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
            allure.attach("Client Connection failed for unsupported vlan id..", vlan)
            print("Test Passsed...Client Connection failed")

    @pytest.mark.outofboundvlanid
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.testcase(name="test_dynamic_outofboundvlanid_vlan_5711",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5711")
    def test_dynamic_outofboundvlanid_vlan_5711(self, get_vif_state, lf_tools,
                                       create_lanforge_chamberview_dut, lf_test, get_configuration, station_names_twog):
        """
                pytest -m "dynamic_vlan and wpa2_personal and bridge"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_2G = profile_data[0]["ssid_name"]
        mode = "BRIDGE"
        vlan = "7000"
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.add_vlan(vlan_ids=[vlan])
        # for i in lf_tools.dut_idx_mapping:
        #
        #     if lf_tools.dut_idx_mapping[i][3] == "2G":
        #         dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
        #         print(dut_2g)
        # if ssid_2G not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        lf_test.EAP_Connect(ssid=ssid_2G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="twog", vlan_id=7000,
                            station_name=station_names_twog, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordoutofboundvlanuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="outofboundvlanuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + vlan)["interface"]["ip"]

        if lf_test.station_ip[station_names_twog[0]] == "0.0.0.0":
            print("station ip...", lf_test.station_ip[station_names_twog[0]])
            assert True
            allure.attach("vlan ip....", eth_vlan_ip)
            allure.attach("station ip....", lf_test.station_ip[station_names_twog[0]])
            allure.attach("Client Connection failed for out of bound vlan id..",vlan)
            print("Test Passsed...Client Connection failed")
