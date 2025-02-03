"""

   Dynamic_Vlan: VLAN Mode
    pytest -m "dynamic_vlan_tests and wpa3_enterprise and vlan"

"""

import allure
import pytest
import time
import importlib
import logging

lf_library = importlib.import_module("configuration")
DYNAMIC_VLAN_RADIUS_SERVER_DATA = lf_library.DYNAMIC_VLAN_RADIUS_SERVER_DATA
DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA = lf_library.DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.dynamic_vlan_tests,
              pytest.mark.vlan, pytest.mark.ow_sanity_lf]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3e_2g", "appliedRadios": ["2G"],
             "security_key": "something",
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             "vlan": 100
             },
            {"ssid_name": "ssid_wpa3e_6g", "appliedRadios": ["6G"],
             "security_key": "something",
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             "vlan": 100
             }]},
    "rf": {
       "6G": {
            "band": "6G",
            "channel-mode": "EHT",
            "channel-width": 80,
            }
    },
    "radius": True
}

@allure.parent_suite("Dynamic VLAN Test")
@allure.suite("WPA3 Enterprise Security")
@allure.sub_suite("6 GHz Band")
@allure.feature("Dynamic VLAN Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_enterprise
@pytest.mark.twog
class TestDynamicVlan6GWpa3(object):
    @pytest.mark.absence_of_radius_vlan_identifier
    @pytest.mark.wpa3_enterprise
    @pytest.mark.sixg
    @allure.testcase(name="test_ssid_vlan_in_the_absence_of_radius_vlan_identifier",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-14368")
    @allure.title("Test for ssid vlan in the absence of radius vlan identifier")
    def test_ssid_vlan_in_the_absence_of_radius_vlan_identifier_6g_wpa3(self, get_test_library,
                                                                        get_dut_logs_per_test_case,
                                                                        get_test_device_logs, num_stations,
                                                                        setup_configuration, check_connectivity):
        """
                pytest -m "absence_of_radius_vlan_identifier and wpa3_enterprise and vlan and sixg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[1]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "sixg"
        mode = "VLAN"
        vlan = [100]
        ttls_passwd = "passwordvlannotsentuser"
        eap = "TTLS"
        identity = "vlannotsentuser"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu, vlan_id=vlan,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              key_mgmt="WPA-EAP-SHA256",
                                                                              dut_data=setup_configuration)
        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                                "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]

        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                           "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = station_ip.split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        logging.info(f"station ip...{sta_ip_1}\neth.{vlan[0]}...{eth_vlan_ip}\neth_upstream_ip...{eth_ip}")
        if sta_ip_1[0] == "0":
            assert False, result
        elif eth_vlan_ip[0] == "0":
            assert False, result
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            elif i == j:
                val = True
        if val:
            assert True, result
        elif not val:
            assert False, result