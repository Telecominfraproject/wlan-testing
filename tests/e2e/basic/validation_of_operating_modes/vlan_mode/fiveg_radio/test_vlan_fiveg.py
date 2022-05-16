"""
    Create VLAN ,connect stations and flow traffic through it : vlan Mode
    pytest -m test_vlan_config_5g_radio
"""

import time
import allure
import pytest

pytestmark = [pytest.mark.ow_sanity_lf,
              pytest.mark.multi_vlan,
              pytest.mark.fiveg]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something", "vlan": 125}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 200}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
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
@pytest.mark.usefixtures("setup_profiles")
class TestVlanConfigFivegRadio(object):

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @pytest.mark.valid_client_ip_wpa_fiveg  # wifi-2169
    @allure.testcase(name="test_station_ip_wpa_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2169")
    def test_station_ip_wpa_ssid_5g(self, lf_test, lf_tools,
                                    station_names_fiveg,
                                    test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa, fiveg
            pytest -m valid_client_ip_wpa_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        vlan = 125
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        print("upstream_port: ", upstream_port)
        port_resources = upstream_port.split(".")
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]
            vlan_list = list(
                map(lambda y: int(list(y.values())[0]['alias'][list(y.values())[0]['alias'].find('.') + 1:]),
                    list(filter(lambda x: x if list(x.values())[0]['port type'].endswith('VLAN') else None,
                                lf_tools.json_get("/port/?fields=port+type,alias")['interfaces']))))
            station_ip = lf_test.station_ip
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
    def test_station_ip_wpa2_ssid_5g(self, lf_test, lf_tools,
                                     station_names_fiveg,
                                     test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m valid_client_ip_wpa2_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
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
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]

            station_ip = lf_test.station_ip
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
    def test_disable_vlan_wpa2_ssid_5g(self, lf_test, lf_tools,
                                       station_names_fiveg,
                                       test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m disable_vlan_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
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
        count = 0
        while not down:
            down = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                     port_resources[2] + "." + str(vlan))["interface"]["down"]
            time.sleep(1)
            count += 1
            if count == 30:
                break

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
    def test_station_ip_open_ssid_5g(self, lf_test, lf_tools,
                                     station_names_fiveg,
                                     test_cases, get_configuration):
        """
            Client connectivity using vlan, open, fiveg
            pytest -m valid_client_ip_open_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]
            vlan_list = list(
                map(lambda y: int(list(y.values())[0]['alias'][list(y.values())[0]['alias'].find('.') + 1:]),
                    list(filter(lambda x: x if list(x.values())[0]['port type'].endswith('VLAN') else None,
                                lf_tools.json_get("/port/?fields=port+type,alias")['interfaces']))))
            station_ip = lf_test.station_ip
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
    def test_station_ip_wpa_wpa2_personal_ssid_5g(self, lf_test,
                                                  lf_tools, station_names_fiveg,
                                                  test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa, wpa2, fiveg
            pytest -m test_station_ip_wpa_wpa2_ssid_5g
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
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
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]
            vlan_list = list(
                map(lambda y: int(list(y.values())[0]['alias'][list(y.values())[0]['alias'].find('.') + 1:]),
                    list(filter(lambda x: x if list(x.values())[0]['port type'].endswith('VLAN') else None,
                                lf_tools.json_get("/port/?fields=port+type,alias")['interfaces']))))

            station_ip = lf_test.station_ip
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
    @pytest.mark.enable_vlan_fiveg  # wifi-2172
    @allure.testcase(name="test_station_ip_wpa2_personal_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2172")
    def test_enable_vlan_wpa2_ssid_5g(self, lf_test, lf_tools,
                                      station_names_fiveg,
                                      test_cases, get_configuration):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m enable_vlan_fiveg
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 200
        lanforge_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lanforge_data["upstream"]
        port_resources = upstream_port.split(".")
        lf_test.Client_disconnect(station_names_fiveg)
        vlan_alias = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                       port_resources[2] + "." + str(vlan))["interface"]["alias"]
        lf_tools.json_post("cli-json/set_port", port_resources[0], port_resources[1], vlan_alias, 0, 8388610)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            vlan_ip = lf_tools.json_get("/port/" + port_resources[0] + "/" + port_resources[1] + "/" +
                                        port_resources[2] + "." + str(vlan))["interface"]["ip"]
            vlan_list = list(
                map(lambda y: int(list(y.values())[0]['alias'][list(y.values())[0]['alias'].find('.') + 1:]),
                    list(filter(lambda x: x if list(x.values())[0]['port type'].endswith('VLAN') else None,
                                lf_tools.json_get("/port/?fields=port+type,alias")['interfaces']))))

            station_ip = lf_test.station_ip
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
