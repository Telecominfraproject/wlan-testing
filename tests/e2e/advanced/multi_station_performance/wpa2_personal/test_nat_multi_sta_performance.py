"""
    Test Multi-Station Performance: Nat Mode
    pytest -m multistaperf
"""
import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G":{
            "channel-width": 80},
        "2G":{
            "channel-width": 20}
    },
    "radius": False
}

@allure.feature("MULTI-STATION PERFORMANCE")
@allure.parent_suite("Multi Station Performance Test")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="WPA2 Personal")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiStaPerfNat(object):

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5897", name="WIFI-5897")
    @pytest.mark.nat_tsm
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss1_2g
    def test_multi_station_NAT_udp_upload_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=35, traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5898", name="WIFI-5898")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss1_2g
    def test_multi_station_NAT_udp_upload_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                                get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30, traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5901", name="WIFI-5901")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_NAT_udp_upload_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                                     get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5905", name="WIFI-5905")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss1_2g
    def test_multi_station_NAT_udp_download_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                             get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=35,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "NAT Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5906", name="WIFI-5906")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss1_2g
    def test_multi_station_NAT_udp_download_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                                  get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=30,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "NAT Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6084", name="WIFI-6084")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_NAT_udp_download_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                                                       get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=1,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss1_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=25,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6089", name="WIFI-6089")
    @pytest.mark.nat_tsm
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss1_5g
    def test_multi_station_NAT_udp_upload_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6090", name="WIFI-6090")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss1_5g
    def test_multi_station_NAT_udp_upload_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6091", name="WIFI-6091")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_NAT_udp_upload_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5902", name="WIFI-5902")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss1_5g
    def test_multi_station_NAT_udp_download_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_dis_nss1_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5903", name="WIFI-5903")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss1_5g
    def test_multi_station_NAT_udp_download_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=250,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5904", name="WIFI-5904")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_NAT_udp_download_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=1,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss1_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=200,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5907", name="WIFI-5907")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss2_2g
    def test_multi_station_NAT_udp_upload_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations, get_test_device_logs,
                                                           get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5911", name="WIFI-5911")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss2_2g
    def test_multi_station_NAT_udp_upload_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                                get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5910", name="WIFI-5910")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_NAT_udp_upload_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                                     get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_upload_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50, traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5914", name="WIFI-5914")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss2_2g
    def test_multi_station_NAT_udp_download_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                             get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_2g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=70,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5913", name="WIFI-5913")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss2_2g
    def test_multi_station_NAT_udp_download_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                                                  get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=60,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5912", name="WIFI-5912")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_NAT_udp_download_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library,
                                                                       num_stations, get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="twog", antenna=4,
                                                                         instance_name="udp_download_10dB_38dB_48dB_dis_nss2_2g",
                                                                         set_att_db="10db,38db,48db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=50,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5908", name="WIFI-5908")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss2_5g
    def test_multi_station_NAT_udp_upload_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5909", name="WIFI-5909")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss2_5g
    def test_multi_station_NAT_udp_upload_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5918", name="WIFI-5918")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_NAT_udp_upload_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_upload_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="0Gbps",
                                                                         upload_rate="1Gbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400,traffic_type="udp_upload"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5916", name="WIFI-5916")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss2_5g
    def test_multi_station_NAT_udp_download_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_dis_nss2_5g",
                                                                         set_att_db="10db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5915", name="WIFI-5915")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss2_5g
    def test_multi_station_NAT_udp_download_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db", download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=500,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5917", name="WIFI-5917")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_NAT_udp_download_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        vlan = 1

        result, description = get_test_library.multi_station_performance(ssid_name=ssid_name,
                                                                         security_key=profile_data["security_key"],
                                                                         mode=mode, vlan=vlan, band="fiveg", antenna=4,
                                                                         instance_name="udp_download_10dB_25dB_35dB_dis_nss2_5g",
                                                                         set_att_db="10db,25db,35db",
                                                                         download_rate="1Gbps",
                                                                         upload_rate="9.6Kbps", batch_size="3,6,9",
                                                                         protocol="UDP-IPv4", duration="120000",
                                                                         expected_throughput=400,traffic_type="udp_download"
                                                                         ,dut_data=setup_configuration,sniff_radio=True)
        if result:
            assert True
        else:
            assert False, description

