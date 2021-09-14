"""

    Performance Test: Wifi Capacity Test : VLAN Mode
    pytest -m "wifi_capacity_test and VLAN"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.VLAN]
# """pytest.mark.usefixtures("setup_test_run")"""]


setup_params_general_dual_band = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_dual_band],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.dual_band
class TestWifiCapacityVLANModeDualBand(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3693", name="WIFI-3693")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_vlan_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                    lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and dual_band"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
        
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3694", name="WIFI-3694")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_vlan_udp_dl(self, get_vif_state, lf_tools,
                                    lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and dual_band"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3691", name="WIFI-3691")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa_vlan_tcp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test vlan mode
            pytest -m "wifi_capacity_test and VLAN and wpa3_personal and dual_band"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3692", name="WIFI-3692")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_vlan_udp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and dual_band"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa_VLAN_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

setup_params_general_2G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityVLANMode2G(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3651", name="WIFI-3651")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_vlan_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                    lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3658", name="WIFI-3658")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_vlan_udp_dl(self, get_vif_state, lf_tools,
                                    lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3668", name="WIFI-3668")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_vlan_tcp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3662", name="WIFI-3662")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_vlan_udp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

setup_params_general_5G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_personal": [
            {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityVLANMode5G(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3653", name="WIFI-3653")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    def test_client_wpa3_vlan_tcp_dl(self, get_vif_state, lf_tools, setup_profiles,
                                    lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3659", name="WIFI-3659")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    def test_client_wpa3_vlan_udp_dl(self, get_vif_state, lf_tools,
                                    lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3669", name="WIFI-3669")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_vlan_tcp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3663", name="WIFI-3663")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_vlan_udp_bidirectional(self, get_vif_state, lf_tools,
                                               lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                               get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and vlan and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa3_VLAN_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True