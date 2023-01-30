"""
    Test Multi-Station Performance: Bridge Mode
    pytest -m multistaperf
"""
import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
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

@allure.feature("BRIDGE MODE MULTI-STATION PERFORMANCE")
@allure.parent_suite("MULTI STATION PERFORMANCE")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal MULTI STATION PERFORMANCE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiStaPerfBridge(object):
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.bridge_tsm
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name, security_key=profile_data["security_key"],
                                                                         mode=mode,vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps",batch_size="3",
                                                                         protocol="UDP-IPv4",duration="120000",
                                                                         expected_throughput=35,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5844", name="WIFI-5844")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_38dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5877", name="WIFI-5877")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5881", name="WIFI-5881")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=35, traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5882", name="WIFI-5882")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_38dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6083", name="WIFI-6083")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6086", name="WIFI-6086")
    @pytest.mark.bridge_tsm
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6087", name="WIFI-6087")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_25dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6088", name="WIFI-6088")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5878", name="WIFI-5878")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5879", name="WIFI-5879")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_25dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5880", name="WIFI-5880")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200, traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5883", name="WIFI-5883")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70, traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5887", name="WIFI-5887")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_38dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5886", name="WIFI-5886")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5890", name="WIFI-5890")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70, traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description
            

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5889", name="WIFI-5889")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_38dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5888", name="WIFI-5888")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5884", name="WIFI-5884")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5885", name="WIFI-5885")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_25dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5896", name="WIFI-5896")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400,traffic_type="udp_upload")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5892", name="WIFI-5892")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5891", name="WIFI-5891")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg12
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_25dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description


    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5895", name="WIFI-5895")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400, traffic_type="udp_download")
        if result:
            assert True
        else:
            assert False, description

