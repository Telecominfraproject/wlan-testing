"""

    Performance Test: Wifi Capacity Test : BRIDGE Mode
    pytest -m "wifi_capacity_test and BRIDGE"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.bridge]
# """pytest.mark.usefixtures("setup_test_run")"""]


setup_params_general_dual_band = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_dual_band],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.bridge
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.dual_band
@pytest.mark.wpa3_personal
@pytest.mark.wifi_capacity_test
class TestWifiCapacityBRIDGEModeDualBand(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3693", name="WIFI-3693")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_bridge_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and dual_band"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["tcp", "download", "2.4G-5G Combined"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3694", name="WIFI-3694")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_bridge_udp_dl(self, get_vif_state, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and dual_band"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["udp", "download", "2.4G-5G Combined"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3691", name="WIFI-3691")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and dual_band"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["tcp", "bidirectional", "2.4G-5G Combined"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3692", name="WIFI-3692")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_bridge_udp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and dual_band"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["udp", "bidirectional", "2.4G-5G Combined"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityBRIDGEMode2G(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3651", name="WIFI-3651")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_bridge_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3658", name="WIFI-3658")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_bridge_udp_dl(self, get_vif_state, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3668", name="WIFI-3668")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3662", name="WIFI-3662")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_bridge_udp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa3_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityBRIDGEMode5G(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3653", name="WIFI-3653")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_bridge_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                       lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3659", name="WIFI-3659")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_bridge_udp_dl(self, get_vif_state, lf_tools,
                                       lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3669", name="WIFI-3669")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3663", name="WIFI-3663")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_bridge_udp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True