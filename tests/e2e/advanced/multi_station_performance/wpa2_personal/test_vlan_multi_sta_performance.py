"""
    Test Multi-Station Performance: Vlan Mode
    pytest -m multistaperf
"""
import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.vlan]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ]
    },
    "rf": {
        "5G": {
            "channel-width": 80},
        "2G": {
            "channel-width": 20}
    },
    "radius": False
}


@allure.feature("VLAN MODE MULTI-STATION PERFORMANCE")
@allure.parent_suite("MULTI STATION PERFORMANCE")
@allure.suite(suite_name="VLAN MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal MULTI STATION PERFORMANCE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiStaPerfVlan(object):

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5942", name="WIFI-5942")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                            get_test_device_logs, get_dut_logs_per_test_case,
                                                            check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=35,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5944", name="WIFI-5944")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library,
                                                                 num_stations,
                                                                 get_test_device_logs, get_dut_logs_per_test_case,
                                                                 check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,38dB,48DdB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5945", name="WIFI-5945")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library,
                                                                      num_stations,
                                                                      get_test_device_logs, get_dut_logs_per_test_case,
                                                                      check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5949", name="WIFI-5949")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                              get_test_device_logs, get_dut_logs_per_test_case,
                                                              check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=35,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5950", name="WIFI-5950")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library,
                                                                   num_stations,
                                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                                   check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,38dB,48DdB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6085", name="WIFI-6085")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library,
                                                                        num_stations,
                                                                        get_test_device_logs,
                                                                        get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6092", name="WIFI-6092")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                                            get_test_device_logs, get_dut_logs_per_test_case,
                                                            check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6093", name="WIFI-6093")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library,
                                                                 num_stations,
                                                                 get_test_device_logs, get_dut_logs_per_test_case,
                                                                 check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6094", name="WIFI-6094")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library,
                                                                      num_stations,
                                                                      get_test_device_logs, get_dut_logs_per_test_case,
                                                                      check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5946", name="WIFI-5946")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                                              get_test_device_logs, get_dut_logs_per_test_case,
                                                              check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5947", name="WIFI-5947")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library,
                                                                   num_stations,
                                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                                   check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5948", name="WIFI-5948")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library,
                                                                        num_stations,
                                                                        get_test_device_logs,
                                                                        get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5951", name="WIFI-5951")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                            get_test_device_logs, get_dut_logs_per_test_case,
                                                            check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5966", name="WIFI-5966")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library,
                                                                 num_stations,
                                                                 get_test_device_logs, get_dut_logs_per_test_case,
                                                                 check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5954", name="WIFI-5954")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library,
                                                                      num_stations,
                                                                      get_test_device_logs, get_dut_logs_per_test_case,
                                                                      check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5969", name="WIFI-5969")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                              get_test_device_logs, get_dut_logs_per_test_case,
                                                              check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5968", name="WIFI-5968")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library,
                                                                   num_stations,
                                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                                   check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5967", name="WIFI-5967")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library,
                                                                        num_stations,
                                                                        get_test_device_logs,
                                                                        get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5952", name="WIFI-5952")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                                            get_test_device_logs, get_dut_logs_per_test_case,
                                                            check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5953", name="WIFI-5953")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library,
                                                                 num_stations,
                                                                 get_test_device_logs, get_dut_logs_per_test_case,
                                                                 check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,40dB,50dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5973", name="WIFI-5973")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_40dB_50dB_dis_nss2_5g(self, setup_configuration, get_test_library,
                                                                      num_stations,
                                                                      get_test_device_logs, get_dut_logs_per_test_case,
                                                                      check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400,
                                                                         traffic_type="udp_upload"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5971", name="WIFI-5971")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                                              get_test_device_logs, get_dut_logs_per_test_case,
                                                              check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5970", name="WIFI-5970")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library,
                                                                   num_stations,
                                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                                   check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title(
        "VLAN Mode Multi Station Performance Test with 10dB,40dB,50dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5972", name="WIFI-5972")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_40dB_50dB_dis_nss2_5g(self, setup_configuration, get_test_library,
                                                                        num_stations,
                                                                        get_test_device_logs,
                                                                        get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400,
                                                                         traffic_type="udp_download"
                                                                         , create_vlan=False,
                                                                         dut_data=setup_configuration
                                                                         , sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

