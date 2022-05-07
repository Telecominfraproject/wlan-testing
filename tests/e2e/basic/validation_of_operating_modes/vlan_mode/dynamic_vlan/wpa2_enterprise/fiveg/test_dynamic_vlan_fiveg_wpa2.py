"""

   Dynamic_Vlan: VLAN Mode
    pytest -m "dynamic_vlan and wpa2_enterprise and vlan"

"""

import os
import allure
import pytest
import time
from configuration import DYNAMIC_VLAN_RADIUS_SERVER_DATA
from configuration import DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.regression, pytest.mark.dynamic_vlan, pytest.mark.wpa2_enterprise, pytest.mark.vlan,
              pytest.mark.fiveg]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2e_5g", "appliedRadios": ["5G"],
             "security_key": "something",
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             "vlan": 100
             }]},
    "rf": {},
    "radius": True
}


@allure.suite("regression")
@allure.feature("VLAN MODE wpa2_enterprise Dynamic Vlan")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDynamicVlan5GWpa2(object):

    @pytest.mark.absence_of_radius_vlan_identifier
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_ssid_vlan_in_the_absence_of_radius_vlan_identifier",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5704")
    def test_ssid_vlan_in_the_absence_of_radius_vlan_identifier_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs, get_ap_logs,
                                                                create_lanforge_chamberview_dut, lf_test,
                                                                get_configuration,
                                                                station_names_fiveg):
        """
                pytest -m " absence_of_radius_vlan_identifier and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan_id = 100
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan_id])
        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg",
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordvlannotsentuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="vlannotsentuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan_id))["interface"]["ip"]

        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_fiveg[0]].split('.')
        print(sta_ip_1)
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        # eth_ip_1 = eth_ip.split('.')
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_vlan_ip[0] == "0":
            print("ssid configured vlan didnt recieved ip")
            assert False
        print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        print("upstream ip...", eth_ip)
        print("ssid configured vlan ip", eth_vlan_ip)
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            elif i == j:
                val = True
        allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan_id)))
        allure.attach(name="ssid configured vlan ip..", body=str(eth_vlan_ip))
        allure.attach(name="upstream port....", body=str(port_resources[2]))
        allure.attach(name="upstream ip....", body=str(eth_ip))
        if val:
            assert True
            print("Station ip assigned as per ssid vlan")
        elif not val:
            print("Station ip not assigned as per ssid vlan")
            assert False

    @pytest.mark.invalidradiusvlan
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_dynamic_invalid_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5706")
    def test_dynamic_invalid_vlan_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs, get_ap_logs,
                                  create_lanforge_chamberview_dut, lf_test, get_configuration,
                                  station_names_fiveg):
        """
                pytest -m "invalidradiusvlan and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan_id = 100
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan_id])

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=vlan_id,
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordinvalidvlanuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="invalidvlanuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan_id))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_fiveg[0]].split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_vlan_ip[0] == "0":
            print("ssid configured vlan didnt recieved ip")
            assert False
        print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        print("ssid vlan ip...", eth_vlan_ip)
        print("upstream ip..", eth_ip)
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan_id)))
        allure.attach(name="ssid configured vlan ip..", body=str(eth_vlan_ip))
        allure.attach(name="upstream port....", body=str(port_resources[2]))
        allure.attach(name="upstream ip....", body=str(eth_ip))
        if val:
            assert True
            print("Station ip assigned as per ssid vlan")
        elif not val:
            print("Station ip not assigned as per ssid vlan")
            assert False

    @pytest.mark.periodic_reauthentication
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_radius_vlan_info_retained_after_periodic_reauthentication",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5707")
    def test_radius_vlan_info_retained_after_periodic_reauthentication_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs,
                                                                       get_ap_logs,
                                                                       create_lanforge_chamberview_dut, lf_test,
                                                                       get_configuration,
                                                                       station_names_fiveg):
        """
                pytest -m "periodic_reauthentication and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = [100, 200]
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=vlan)

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=vlan[1],
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordB", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="userB", d_vlan=True, cleanup=False)

        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]
        sta_ip = lf_test.station_ip[station_names_fiveg[0]]

        count = 0
        # print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        # print("vlan ip...", eth_vlan_ip)
        # print("eth_vlan_ip..", eth_ip)
        eth_ssid_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                             "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
        eth_rad_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                            "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_vlan_ip_1 = eth_rad_vlan_ip.split('.')
        sta_ip_1 = sta_ip.split('.')
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_vlan_ip_1[0] == "0":
            print("radius configured vlan didnt recieved ip")
            assert False
        print(sta_ip_1)
        for k in range(0, 2):
            for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    break
                else:
                    if count == 2:
                        break  # allure.attach(name="station ip",body=str(sta_ip))
                    continue
            count = count + 1
            time.sleep(30)
            lf_tools.admin_up_down([station_names_fiveg[0]], option="up")

            sta_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                       "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_ip_1 = sta_ip.split('.')
            print(sta_ip)
        allure.attach(name="station ip....", body=str(sta_ip))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan[0])))
        allure.attach(name="ssid configured vlan ip..", body=str(eth_ssid_vlan_ip))
        allure.attach(name="radius configured vlan..", body=str(port_resources[2] + "." + str(vlan[1])))
        allure.attach(name="radius configured vlan ip....", body=str(eth_rad_vlan_ip))
        allure.attach(name="upstream port....", body=str(port_resources[2]))
        allure.attach(name="upstream ip....", body=str(eth_ip))
        if count == 2:
            assert True
            print("Station ip assigned as per dynamic vlan")
        elif count == 0:
            print("Station ip not assigned as per dynamic vlan")
            assert False

    @pytest.mark.absenceofvlanid
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_ssid_vlan_used_in_absence_of_radius_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5708")
    def test_ssid_vlan_used_in_absence_of_radius_vlan_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs, get_ap_logs,
                                                      create_lanforge_chamberview_dut, lf_test, get_configuration,
                                                      station_names_fiveg):
        """
                pytest -m "absenceofvlanid and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = 100
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan])

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=vlan,
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordvlannotsentuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="vlannotsentuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_fiveg[0]].split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        print("ssid configured vlan ip...", eth_vlan_ip)
        print("upstream ip..", eth_ip)
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_vlan_ip[0] == "0":
            print("ssid configured vlan didnt recieved ip")
            assert False

        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan)))
        allure.attach(name="ssid configured vlan ip..", body=str(eth_vlan_ip))
        allure.attach(name="upstream port....", body=str(port_resources[2]))
        allure.attach(name="upstream ip....", body=str(eth_ip))
        if val:
            assert True
            print("Station ip assigned as per ssid configured vlan")
        elif not val:
            print("Station ip not assigned as per ssid configured vlan")
            assert False

    '''
    @pytest.mark.unsupported
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_dynamic_unsupported_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5710")
    def test_dynamic_unsupported_vlan(self, get_vif_state, lf_tools,
                                      create_lanforge_chamberview_dut, lf_test, get_configuration,
                                      station_names_fiveg):
        """
                pytest -m "unsupported and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = 100
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan])

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=100,
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordinvalidvlanuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="invalidvlanuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_fiveg[0]].split('.')
        eth_vlan_ip_1 = eth_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        print("vlan ip...", eth_vlan_ip)
        print("eth_vlan_ip..", eth_ip)
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
                allure.attach(name="vlan ip....", body=str(eth_vlan_ip))
                print("Station ip not assigned as per vlan")
                assert False
            else:
                assert True
                allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
                allure.attach(name="vlan ip....", body=str(eth_vlan_ip))
                allure.attach(name="vlan ip....", body=str(eth_ip))
                print("Station ip assigned as per vlan")
    '''

    @pytest.mark.outofboundvlanid
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_outof_bound_vlanid",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5711")
    def test_out_of_bound_vlanid_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs, get_ap_logs,
                                create_lanforge_chamberview_dut, lf_test, get_configuration,
                                station_names_fiveg):
        """
                pytest -m "outofboundvlanid and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = 100
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan])

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=vlan,
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordoutofboundvlanuser", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="outofboundvlanuser", d_vlan=True)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        if lf_test.station_ip[station_names_fiveg[0]] == "0.0.0.0":
            print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
            assert True
            allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
            allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan)))
            allure.attach(name="ssid configured vlan ip..", body=str(eth_vlan_ip))
            allure.attach(name="upstream port....", body=str(port_resources[2]))
            allure.attach(name="upstream ip....", body=str(eth_ip))
            allure.attach(name="out of bound vlan id..", body=str(7000))
            print("Test Passsed...Client Connection failed")

    @pytest.mark.client_association_ap_with_dynamic_vlan
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_client_association_ap_with_dynamic_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5712")
    def test_client_association_ap_with_dynamic_vlan_5g_wpa2(self, get_vif_state, lf_tools, get_ap_logs, get_lf_logs,
                                                     create_lanforge_chamberview_dut, lf_test, get_configuration,
                                                     station_names_fiveg):
        """
                pytest -m "client_association_ap_with_dynamic_vlan and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = [100, 200]
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=vlan)

        lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                            mode=mode, band="fiveg", vlan_id=vlan[0],
                            station_name=station_names_fiveg, key_mgmt="WPA-EAP",
                            pairwise="NA", group="NA", wpa_psk="DEFAULT",
                            ttls_passwd="passwordB", ieee80211w=0,
                            wep_key="NA", ca_cert="NA", eap="TTLS", identity="userB", d_vlan=True)

        eth_ssid_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                             "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]

        eth_radius_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                               "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = lf_test.station_ip[station_names_fiveg[0]].split('.')
        eth_radius_vlan_ip_1 = eth_radius_vlan_ip.split('.')
        print("station ip...", lf_test.station_ip[station_names_fiveg[0]])
        print("radius vlan ip...", eth_radius_vlan_ip)
        print("eth_upstream_ip..", eth_ip)
        if sta_ip_1[0] == "0":
            print("station didnt received any ip")
            allure.attach("station didnt recieved ip..")
            assert False
        elif eth_radius_vlan_ip_1[0] == "0":
            print("ssid configured vlan didnt recieved ip")
            assert False

        for i, j in zip(sta_ip_1[0:2], eth_radius_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        allure.attach(name="station ip....", body=str(lf_test.station_ip[station_names_fiveg[0]]))
        allure.attach(name="ssid configured vlan..", body=str(port_resources[2] + "." + str(vlan[0])))
        allure.attach(name="ssid configured vlan ip....", body=str(eth_ssid_vlan_ip))
        allure.attach(name="radius configured vlan..", body=str(port_resources[2] + "." + str(vlan[1])))
        allure.attach(name="radius configured vlan ip....", body=str(eth_radius_vlan_ip))
        allure.attach(name="Upstream ip....", body=str(eth_ip))
        if val:
            assert True
            print("Station ip assigned as per radius vlan")
        elif not val:
            print("Station ip not assigned as per radius vlan")
            assert False

    @pytest.mark.subsequent_user_for_same_user_account
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_subsequent_user_for_same_user_account",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5713")
    def test_subsequent_user_for_same_user_account_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs,
                                                   get_ap_logs,
                                                   create_lanforge_chamberview_dut, lf_test,
                                                   get_configuration,
                                                   station_names_fiveg):
        """
                pytest -m "subsequent_user_for_same_user_account and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = 100
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=[vlan])

        station_list = []
        sta_ip = []
        for i in range(0, 2):
            station_list.append(lf_tools.fiveg_prefix + str(i))
        print(station_list)
        print([station_list[0]])

        for m in range(0, len(station_list)):
            lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                                mode=mode, band="fiveg", vlan_id=100,
                                station_name=[station_list[m]], key_mgmt="WPA-EAP",
                                pairwise="NA", group="NA", wpa_psk="DEFAULT",
                                ttls_passwd="passwordA", ieee80211w=0,
                                wep_key="NA", ca_cert="NA", eap="TTLS", identity="userA", d_vlan=True, cleanup=False)
            lf_tools.admin_up_down([station_list[m]], option="up")
            sta_ip.append(lf_test.station_ip[station_list[m]])
            if sta_ip[m] == "0.0.0.0":
                allure.attach("station didnt recieved ip..")
                assert False
            print(sta_ip)
            time.sleep(30)

        eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan))["interface"]["ip"]
        eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        for n in range(0, len(station_list)):
            sta_ip_1 = sta_ip[n].split('.')
            print("station ip...", sta_ip[n])
            print("vlan ip...", eth_vlan_ip)
            print("eth_vlan_ip..", eth_ip)
            for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    val = False
                else:
                    val = True
            allure.attach(name="station ip....", body=str(sta_ip[n]))
            allure.attach(name="radius configured vlan..", body=str(port_resources[2] + "." + str(vlan)))
            allure.attach(name="radius configured vlan ip..", body=str(eth_vlan_ip))
            allure.attach(name="upstream port....", body=str(port_resources[2]))
            allure.attach(name="upstream ip....", body=str(eth_ip))
            if val:
                assert True
                print("Station ip assigned as per radius vlan")
            elif not val:
                print("Station ip not assigned as per radius vlan")
                assert False

    @pytest.mark.subsequent_user_for_different_user_account
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_subsequent_user_for_different_user_account_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5714")
    def test_subsequent_user_for_different_user_account_5g_wpa2(self, get_vif_state, lf_tools, get_lf_logs,
                                                        get_ap_logs,
                                                        create_lanforge_chamberview_dut, lf_test,
                                                        get_configuration,
                                                        station_names_fiveg):
        """
                pytest -m "subsequent_user_for_different_user_account and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_5G = profile_data[0]["ssid_name"]
        mode = "VLAN"
        vlan = [100, 200]
        val = ""
        upstream_port = lf_tools.upstream_port
        print(upstream_port)
        port_resources = upstream_port.split(".")
        print(lf_tools.dut_idx_mapping)
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=vlan)

        station_list = []
        sta_ip = []
        dynamic_vlan_user = ["userA", "userB"]
        dynamic_vlan_pass = ["passwordA", "passwordB"]
        for i in range(0, 2):
            station_list.append(lf_tools.fiveg_prefix + str(i))

        for user_id, user_pass, sta in zip(dynamic_vlan_user, dynamic_vlan_pass, range(0, len(station_list))):
            lf_test.EAP_Connect(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
                                mode=mode, band="fiveg", vlan_id=vlan[sta],
                                station_name=[station_list[sta]], key_mgmt="WPA-EAP",
                                pairwise="NA", group="NA", wpa_psk="DEFAULT",
                                ttls_passwd=user_pass, ieee80211w=0,
                                wep_key="NA", ca_cert="NA", eap="TTLS", identity=user_id, d_vlan=True, cleanup=False)

            sta_ip.append(lf_test.station_ip[station_list[sta]])

            eth_vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                            "/" + port_resources[2] + "." + str(vlan[sta]))["interface"]["ip"]

            eth_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                       "/" + port_resources[2])["interface"]["ip"]
            eth_vlan_ip_1 = eth_vlan_ip.split('.')
            print(sta_ip)
            sta_ip_1 = sta_ip[sta].split('.')
            if sta_ip_1 == "0.0.0.0":
                allure.attach("station didn't received ip..")
                assert False
            print("station ip...", lf_test.station_ip[station_list[sta]])
            print("vlan ip...", eth_vlan_ip)
            print("eth_vlan_ip..", eth_ip)
            for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    val = False
                else:
                    val = True
            allure.attach(name="station ip....", body=str(sta_ip[sta]))
            allure.attach(name="radius configured vlan..", body=str(port_resources[2] + "." + str(vlan[sta])))
            allure.attach(name="radius configured vlan ip..", body=str(eth_vlan_ip))
            allure.attach(name="upstream port....", body=str(port_resources[2]))
            allure.attach(name="upstream ip....", body=str(eth_ip))
            if val:
                assert True
                print(f"{station_list[sta]} ip assigned as per radius vlan")
            elif not val:
                print(f"{station_list[sta]} ip not assigned as per radius vlan")
                assert False
            lf_tools.admin_up_down([station_list[sta]], option="up")
            time.sleep(5)

