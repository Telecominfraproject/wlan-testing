"""

   Dynamic_Vlan: VLAN Mode
    pytest -m "dynamic_vlan and wpa2_enterprise and vlan"

"""

import os
import allure
import pytest
from configuration import DYNAMIC_VLAN_RADIUS_SERVER_DATA
from configuration import DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.ow_dvlan_tests_lf,
              pytest.mark.wpa2_enterprise,
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
    "radius": "DVLAN"
}


@allure.suite("regression")
@allure.feature("VLAN MODE wpa2_enterprise Dynamic Vlan")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDynamicVlanOverSsid5GWpa2(object):

    @pytest.mark.dynamic_precedence_over_ssid
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_dynamic_precedence_over_ssid_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-5705")
    def test_dynamic_precedence_over_ssid_vlan_5g_wpa2(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration):
        """
                pytest -m "dynamic_precedence_over_ssid and wpa2_enterprise and vlan"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa2"
        extra_secu = []
        mode = "VLAN"
        band = "fiveg"
        vlan = [100,200]
        ttls_passwd = "passwordB" #radius_info["password"] #
        eap = "TTLS"
        identity = "userB" #radius_info['user'] #

        val = ""
        # upstream_port = lf_tools.upstream_port
        # print(upstream_port)
        # port_resources = upstream_port.split(".")
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')
        # print(lf_tools.dut_idx_mapping)
        # lf_tools.reset_scenario()
        # for i in vlan:
        get_test_library.add_vlan(vlan_ids=vlan)

        passes, result, station_ip = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu, vlan_id=vlan,
                                                                              mode=mode, band=band, eap=eap,d_vlan=True,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration)
        # get_test_library.enterprise_client_connectivity_test(ssid=ssid_5G, passkey="[BLANK]", security="wpa2", extra_securities=[],
        #                     mode=mode, band="fiveg", vlan_id=vlan[0],
        #                     station_name=station_names_fiveg, key_mgmt="WPA-EAP",
        #                     pairwise="NA", group="NA", wpa_psk="DEFAULT",
        #                     ttls_passwd="passwordB", ieee80211w=0,
        #                     wep_key="NA", ca_cert="NA", eap="TTLS", identity="userB", d_vlan=True)
        eth_ssid_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                               "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]

        eth_radius_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = station_ip.split('.')
        eth_vlan_ip_1 = eth_radius_vlan_ip.split('.')
        print("station ip...", sta_ip_1)
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

        allure.attach(name="station ip....", body=str(station_ip))
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