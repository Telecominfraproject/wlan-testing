"""
    Create VLAN ,connect stations and flow traffic through it : vlan Mode
    pytest -m TestVlanConfigRadioFiveg
"""

import time
import allure
import pytest

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something", "vlan": 125}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something", "vlan": 200}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something", "vlan": 150}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.parametrize(
    "create_vlan",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.TestVlanConfigRadioFiveg
class TestVlanConfigFivegRadio(object):

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @pytest.mark.valid_client_ip_wpa_fiveg  # wifi-2169
    @allure.testcase(name="test_station_ip_wpa_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2169")
    def test_station_ip_wpa_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test, lf_tools,
                                    get_vlan_list, update_report, station_names_fiveg,
                                    test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa, fiveg
            pytest -m valid_client_ip_wpa_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        vlan = 125
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        print("upstream_port: ",upstream_port)
        port_resources = upstream_port.split(".")
        vlan_list = get_vlan_list
        print(vlan_list)
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = station_ip.split(".")
            vlan_ip = vlan_ip.split(".")

            print(station_ip[:2], vlan_ip[:2])
            for i, j in zip(station_ip[:2], vlan_ip[:2]):
                if i != j:
                    assert False

            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("station got IP as per VLAN. Test passed")
                assert True
            else:
                assert False
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.valid_client_ip_wpa2_fiveg  # wifi-2157
    @allure.testcase(name="test_station_ip_wpa2_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2157")
    def test_station_ip_wpa2_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test, lf_tools,
                                     update_report, station_names_fiveg,
                                     test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m valid_client_ip_wpa2_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 200
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = station_ip.split(".")
            vlan_ip = vlan_ip.split(".")

            print(station_ip[:2], vlan_ip[:2])
            for i, j in zip(station_ip[:2], vlan_ip[:2]):
                if i != j:
                    assert False

            print("station got IP as per VLAN. Test passed")
            assert True
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.disable_vlan_fiveg  # wifi-2174
    @allure.testcase(name="test_disable_vlan_wpa2_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2174")
    def test_disable_vlan_wpa2_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test, lf_tools,
                                       update_report, station_names_fiveg,
                                       test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m disable_vlan_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 200
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")

        vlan_alias = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                       port_resources[2] + "." + str(vlan))["interface"]["alias"]

        req_url = "cli-json/set_port"
        lf_tools.json_post(req_url, port_resources[0], port_resources[1], vlan_alias, 1, 8388608)
        down = False
        while not down:
            down = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                     port_resources[2] + "." + str(vlan))["interface"]["down"]
            time.sleep(1)

        passes = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                        passkey=security_key, mode=mode, band=band,
                                        station_name=station_names_fiveg, vlan_id=vlan)

        if not passes:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            print("station did not get an IP. Test passed")
            print("station ip: ", station_ip)
            assert True
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass

    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.valid_client_ip_open_fiveg  # wifi-2161
    @allure.testcase(name="test_station_ip_open_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2161")
    def test_station_ip_open_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test, lf_tools,
                                     get_vlan_list, update_report, station_names_fiveg,
                                     test_cases, get_configuration):
        """
            Client connectivity using vlan, open, fiveg
            pytest -m valid_client_ip_open_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")
        vlan_list = get_vlan_list
        print("vlan_list", vlan_list)
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = station_ip.split(".")
            vlan_ip = vlan_ip.split(".")

            print(station_ip[:2], vlan_ip[:2])
            for i, j in zip(station_ip[:2], vlan_ip[:2]):
                if i != j:
                    assert False

            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("station got IP as per VLAN. Test passed")
                assert True
            else:
                assert False
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @pytest.mark.test_station_ip_wpa_wpa2_ssid_5g  # wifi-2167
    @allure.testcase(name="test_station_ip_wpa_wpa2_personal_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2167")
    def test_station_ip_wpa_wpa2_personal_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test,
                                                  lf_tools, get_vlan_list, update_report, station_names_fiveg,
                                                  test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa, wpa2, fiveg
            pytest -m test_station_ip_wpa_wpa2_ssid_5g
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = 150
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")
        vlan_list = get_vlan_list
        print(vlan_list)
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = station_ip.split(".")
            vlan_ip = vlan_ip.split(".")

            print(station_ip[:2], vlan_ip[:2])
            for i, j in zip(station_ip[:2], vlan_ip[:2]):
                if i != j:
                    assert False

            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("station got IP as per VLAN. Test passed")
                assert True
            else:
                assert False
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.valid_client_ip_wpa2_personal  # wifi-2172
    @allure.testcase(name="test_station_ip_wpa2_personal_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2172")
    def test_station_ip_wpa2_personal_ssid_5g(self, get_lanforge_data, setup_profiles, create_vlan, lf_test, lf_tools,
                                              get_vlan_list, update_report, station_names_fiveg,
                                              test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m valid_client_ip_wpa2_personal
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 200
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")
        vlan_list = get_vlan_list
        print(vlan_list)
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            station_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                           station_names_fiveg[0])["interface"]["ip"]
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = station_ip.split(".")
            vlan_ip = vlan_ip.split(".")

            print(station_ip[:2], vlan_ip[:2])
            for i, j in zip(station_ip[:2], vlan_ip[:2]):
                if i != j:
                    assert False

            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("station got IP as per VLAN. Test passed")
                assert True
            else:
                assert False
        else:
            assert False
        try:
            lf_test.Client_disconnect(station_names_fiveg)
        except:
            pass