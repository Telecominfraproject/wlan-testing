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
              pytest.mark.vlan, pytest.mark.ow_regression_lf]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3e_5g", "appliedRadios": ["5G"],
             "security_key": "something",
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             "vlan": 100
             }]},
    "rf": {},
    "radius": True
}


@allure.parent_suite("Dynamic VLAN Test")
@allure.suite("WPA3 Enterprise Security")
@allure.sub_suite("5 GHz Band")
@allure.feature("Dynamic VLAN Test")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDynamicVlan5GWpa3(object):

    @pytest.mark.absence_of_radius_vlan_identifier
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_ssid_vlan_in_the_absence_of_radius_vlan_identifier",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6095")
    @allure.title("Test for ssid vlan in the absence of radius vlan identifier")
    def test_ssid_vlan_in_the_absence_of_radius_vlan_identifier_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m " absence_of_radius_vlan_identifier and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
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
                                                                    identity=identity, num_sta=1, key_mgmt="WPA-EAP-SHA256",
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

    @pytest.mark.invalidradiusvlan
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_dynamic_invalid_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6097")
    @allure.title("Test for invalid vlan identifier")
    def test_dynamic_invalid_vlan_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "invalidradiusvlan and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100]
        ttls_passwd = "passwordinvalidvlanuser"
        eap = "TTLS"
        identity = "invalidvlanuser"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')
        get_test_library.add_vlan(vlan_ids=[vlan])

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid = ssid_name, key_mgmt="WPA-EAP-SHA256",
                                        security = security, extra_securities = extra_secu, vlan_id = vlan,
                                        mode = mode, band = band, eap = eap, ttls_passwd = ttls_passwd,
                                        ieee80211w = 0, identity = identity, num_sta = 1, dut_data = setup_configuration)

        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = station_ip.split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        if sta_ip_1[0] == "0":
            assert False, result
        elif eth_vlan_ip[0] == "0":
            assert False, result
        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        if val:
            assert True, result
        elif not val:
            assert False, result

    @pytest.mark.periodic_reauthentication
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_radius_vlan_info_retained_after_periodic_reauthentication",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6098")
    @allure.title("Test for radius vlan information retained after periodic reauthentication")
    def test_radius_vlan_info_retained_after_periodic_reauthentication_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "periodic_reauthentication and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100, 200]
        ttls_passwd = "passwordB"
        eap = "TTLS"
        identity = "userB"

        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid = ssid_name, security = security,
                                        extra_securities = extra_secu, vlan_id = vlan,
                                        mode = mode, band = band, eap = eap,
                                        ttls_passwd = ttls_passwd, ieee80211w = 0,
                                        identity = identity, num_sta = 1, key_mgmt="WPA-EAP-SHA256",
                                        dut_data = setup_configuration, cleanup=False, d_vlan=True)

        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        eth_ssid_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                             "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
        eth_rad_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                            "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_vlan_ip_1 = eth_rad_vlan_ip.split('.')
        sta_ip = []
        sta_ip.append(station_ip.split('.'))
        for u in get_test_library.json_get("/port/?fields=port+type,alias")['interfaces']:
            if list(u.values())[0]['port type'] in ['WIFI-STA']:
                station_name = list(u.keys())[0]
        sta = station_name.split('.')
        get_test_library.local_realm.admin_up(sta)
        time.sleep(10)
        for i in range(5):
            x = get_test_library.json_get("/port/" + sta[0] + "/" + sta[1] + "/" + sta[2])["interface"]["ip"]
            if x == "0.0.0.0":
                time.sleep(10)
            else:
                break
        sta_ip.append(x.split('.'))
        for k in sta_ip:
            for i, j in zip(k[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    val = False
                    break
                else:
                    val = True
        if val:
            assert True, result
        else:
            assert False, result

            assert passes == "PASS", result

    @pytest.mark.absenceofvlanid
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_ssid_vlan_used_in_absence_of_radius_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6100")
    @allure.title("test for ssid vlan used in absence of radius vlan")
    def test_ssid_vlan_used_in_absence_of_radius_vlan_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "absenceofvlanid and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100]
        ttls_passwd = "passwordvlannotsentuser"
        eap = "TTLS"
        identity = "vlannotsentuser"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                          extra_securities=extra_secu, vlan_id=vlan, mode=mode, band=band, eap=eap,
                                          d_vlan=False, ttls_passwd=ttls_passwd, ieee80211w=0, identity=identity,
                                          num_sta=1, dut_data=setup_configuration, key_mgmt="WPA-EAP-SHA256")

        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = station_ip.split('.')
        eth_vlan_ip_1 = eth_vlan_ip.split('.')
        if sta_ip_1[0] == "0":
            assert False, result
        elif eth_vlan_ip[0] == "0":
            assert False, result

        for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        if val:
            assert True, result
        elif not val:
            assert False, result

    @pytest.mark.outofboundvlanid
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_outof_bound_vlanid",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6103")
    @allure.title("test for out of bound vlan identifier")
    def test_out_of_bound_vlanid_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "outofboundvlanid and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100]
        ttls_passwd = "passwordoutofboundvlanuser"
        eap = "TTLS"
        identity = "outofboundvlanuser"
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                  extra_securities=extra_secu, vlan_id=vlan,
                                                                  mode=mode, band=band, eap=eap,
                                                                  ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                  identity=identity, num_sta=1, key_mgmt="WPA-EAP-SHA256",
                                                                  dut_data=setup_configuration)
        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                        "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        if station_ip == "0.0.0.0":
            assert True, result

    @pytest.mark.client_association_ap_with_dynamic_vlan
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_client_association_ap_with_dynamic_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6104")
    @allure.title("test for client association ap with dynamic vlan")
    def test_client_association_ap_with_dynamic_vlan_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "client_association_ap_with_dynamic_vlan and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100, 200]
        ttls_passwd = "passwordB"
        eap = "TTLS"
        identity = "userB"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')

        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                  extra_securities=extra_secu, vlan_id=vlan,
                                                                  mode=mode, band=band, eap=eap,
                                                                  ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                  identity=identity, num_sta=1, key_mgmt="WPA-EAP-SHA256",
                                                                  dut_data=setup_configuration, d_vlan=True)

        station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
        eth_ssid_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                             "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]

        eth_radius_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                               "/" + port_resources[2] + "." + str(vlan[1]))["interface"]["ip"]
        eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                   "/" + port_resources[2])["interface"]["ip"]

        sta_ip_1 = station_ip.split('.')
        eth_radius_vlan_ip_1 = eth_radius_vlan_ip.split('.')
        if sta_ip_1[0] == "0":
            assert False, result
        elif eth_radius_vlan_ip_1[0] == "0":
            assert False, result

        for i, j in zip(sta_ip_1[0:2], eth_radius_vlan_ip_1[0:2]):
            if i != j:
                val = False
            else:
                val = True
        if val:
            assert True, result
        elif not val:
            assert False, result

        assert passes == "PASS", result

    @pytest.mark.subsequent_user_for_same_user_account
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_subsequent_user_for_same_user_account",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6105")
    @allure.title("test for subsequent user for same user account")
    def test_subsequent_user_for_same_user_account_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "subsequent_user_for_same_user_account and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100]
        ttls_passwd = "passwordA"
        eap = "TTLS"
        identity = "userA"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')
        sta_ip = []

        for m in range(2):
            passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                      extra_securities=extra_secu, vlan_id=vlan,
                                                                      mode=mode, band=band, eap=eap,
                                                                      ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                      identity=identity, num_sta=1,  key_mgmt="WPA-EAP-SHA256",
                                                                      dut_data=setup_configuration)
            station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
            sta_ip.append(station_ip)
            if sta_ip[m] == "0.0.0.0":
                assert False, result

            eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                            "/" + port_resources[2] + "." + str(vlan[0]))["interface"]["ip"]
            eth_vlan_ip_1 = eth_vlan_ip.split('.')
            # for n in range(2):
            sta_ip_1 = sta_ip[m].split('.')
            for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    val = False
                else:
                    val = True
            if val:
                assert True, result
            elif not val:
                assert False, result

    @pytest.mark.subsequent_user_for_different_user_account
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.testcase(name="test_subsequent_user_for_different_user_account_vlan",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-6106")
    @allure.title("test for subsequent user for different user account")
    def test_subsequent_user_for_different_user_account_5g_wpa3(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                pytest -m "subsequent_user_for_different_user_account and wpa3_enterprise and vlan and fiveg"
        """

        profile_data = setup_params_general["ssid_modes"]["wpa3_enterprise"]
        ssid_name = profile_data[0]["ssid_name"]
        security = "wpa3"
        extra_secu = []
        band = "fiveg"
        mode = "VLAN"
        vlan = [100, 200]
        eap = "TTLS"
        val = ""
        port_resources = list(get_test_library.lanforge_data['wan_ports'].keys())[0].split('.')
        sta_ip = []
        dynamic_vlan_user = ["userA", "userB"]
        dynamic_vlan_pass = ["passwordA", "passwordB"]

        for user_id, user_pass, cnt in zip(dynamic_vlan_user, dynamic_vlan_pass, range(0, len(vlan))):
            if cnt == 0:
                d_vlan = False
            else:
                d_vlan = True
            passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, passkey="[BLANK]",
                                security=security, extra_securities=extra_secu, mode=mode, band=band, vlan_id=vlan,
                                num_sta=1, ttls_passwd=user_pass, ieee80211w=0, dut_data=setup_configuration,
                                eap=eap, identity=user_id, key_mgmt="WPA-EAP-SHA256", d_vlan=d_vlan)

            station_ip = get_test_library.station_data[list(get_test_library.station_data.keys())[0]]['ip']
            sta_ip.append(station_ip)

            eth_vlan_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                            "/" + port_resources[2] + "." + str(vlan[cnt]))["interface"]["ip"]

            eth_ip = get_test_library.json_get("/port/" + port_resources[0] + "/" + port_resources[1] +
                                       "/" + port_resources[2])["interface"]["ip"]
            eth_vlan_ip_1 = eth_vlan_ip.split('.')
            sta_ip_1 = sta_ip[cnt].split('.')
            if sta_ip_1[0] == '0':
                allure.attach("station didn't received ip..")
                assert False, result
            for i, j in zip(sta_ip_1[0:2], eth_vlan_ip_1[0:2]):
                if i != j:
                    val = False
                else:
                    val = True
            if val:
                assert True, result
            elif not val:
                assert False, result

            assert passes == "PASS", result
