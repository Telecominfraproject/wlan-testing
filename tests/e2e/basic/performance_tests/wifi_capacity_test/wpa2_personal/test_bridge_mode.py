"""

    Performance Test: Wifi Capacity Test : BRIDGE Mode
    pytest -m "wifi_capacity_test and BRIDGE"

"""
import logging
import allure
import pytest

LOGGER = logging.getLogger(__name__)

pytestmark = [pytest.mark.performance, pytest.mark.bridge]
# """pytest.mark.usefixtures("setup_test_run")"""]


setup_params_general_dual_band = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE WIFI CAPACITY TEST")
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
@pytest.mark.wpa2_personal
@pytest.mark.wifi_capacity_test
class TestWifiCapacityBRIDGEModeDualBand(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3926", name="WIFI-3926")
    @pytest.mark.tcp_download
    def test_client_wpa2_BRIDGE_tcp_dl(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        LOGGER.info('test_client_wpa2_BRIDGE_tcp_dl Test Setup Finished, Starting test now...')
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "tcp-download-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        LOGGER.info('test_client_wpa2_BRIDGE_tcp_dl Test Finished')
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3927", name="WIFI-3927")
    @pytest.mark.udp_download
    def test_client_wpa2_BRIDGE_udp_dl(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "udp-download-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3932", name="WIFI-3932")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_BRIDGE_tcp_bidirectional(self, lf_tools, get_apnos_max_clients,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "tcp-bidirectional-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3933", name="WIFI-3933")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_BRIDGE_udp_bidirectional(self, lf_tools, get_apnos_max_clients,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "udp-bidirectional-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7127", name="WIFI-7127")
    @pytest.mark.tcp_upload
    def test_client_wpa2_bridge_tcp_ul(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "tcp-upload-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_ul", mode=mode, vlan_id=vlan,
                                        download_rate="0", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7128", name="WIFI-7128")
    @pytest.mark.udp_upload
    def test_client_wpa2_bridge_udp_ul(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "udp-upload-bridge-wpa2-2.4G-5G"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_ul", mode=mode, vlan_id=vlan,
                                        download_rate="0", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True


setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE Wifi Capacity")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityBRIDGEMode2G(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3928", name="WIFI-3928")
    @pytest.mark.tcp_download
    def test_client_wpa2_BRIDGE_tcp_dl(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["tcp", "download", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", influx_tags=influx_tags,
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3930", name="WIFI-3930")
    @pytest.mark.udp_download
    def test_client_wpa2_BRIDGE_udp_dl(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["udp", "download", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", influx_tags=influx_tags,
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3934", name="WIFI-3934")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_BRIDGE_tcp_bidirectional(self, lf_tools, get_apnos_max_clients,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["udp", "bidirectional", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3935", name="WIFI-3935")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_BRIDGE_udp_bidirectional(self, lf_tools, get_apnos_max_clients,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["tcp", "bidirectional", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7127", name="WIFI-7127")
    @pytest.mark.tcp_upload
    def test_client_wpa2_bridge_tcp_ul(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["tcp", "upload", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_ul", mode=mode, vlan_id=vlan,
                                        download_rate="0", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7128", name="WIFI-7128")
    @pytest.mark.udp_upload
    def test_client_wpa2_bridge_udp_ul(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = ["udp", "upload", "2.4G"]
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_ul", mode=mode, vlan_id=vlan,
                                        download_rate="0", batch_size="1,5,10,20,40,64,128,256",
                                        influx_tags=influx_tags,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True


setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
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
@pytest.mark.wpa2_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityBRIDGEMode5G(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3929", name="WIFI-3929")
    @pytest.mark.tcp_download
    def test_client_wpa2_BRIDGE_tcp_dl(self, lf_tools, get_apnos_max_clients,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3931", name="WIFI-3931")
    @pytest.mark.udp_download
    def test_client_wpa2_BRIDGE_udp_dl(self, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3936", name="WIFI-3936")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_BRIDGE_tcp_bidirectional(self, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3937", name="WIFI-3937")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_BRIDGE_udp_bidirectional(self, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
