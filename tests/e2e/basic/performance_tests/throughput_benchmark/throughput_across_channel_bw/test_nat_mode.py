"""

    Performance Test: Throughput  Across Bandwidth Test: NAT Mode
    pytest -m "throughput_across_bw_test and NAT"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_across_bw_test, pytest.mark.nat]
raw_lines = [['pkts: %s' % 1],
                         ['directions: DUT Transmit;DUT Receive'],
                         ['bandw_options: %s' % 1],
                         ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                         ["show_ll_graphs: 1"], ["show_log: 1"]]

setup_params_general_20Mhz = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {
        "5G": {
                "channel-width": 20,
                },
        "2G": {
                "channel-width": 20,
                }
    },
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput across channel-width Tests : WPA2 Personal Security")
@allure.suite("NAT Mode")
@allure.sub_suite("20Mhz Channel Bandwidth")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_20Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputAcrossBw20MhzNAT(object):
    """Throughput Across Bw NAT Mode
       pytest -m "throughput_across_bw_test and NAT"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2556", name="WIFI-2556")
    @pytest.mark.bw20Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, 
                                     lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and twog"
        """
        profile_data = setup_params_general_20Mhz["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, bw="20")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2556", name="WIFI-2556")
    @pytest.mark.bw20Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, 
                                     lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_20Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, bw="20")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False


setup_params_general_40Mhz = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {
        "5G": {
                "channel-width": 40,
                },
            "2G": {
                "channel-width": 40,
                }
    },
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput across channel-width Tests : WPA2 Personal Security")
@allure.suite("NAT Mode")
@allure.sub_suite("40Mhz Channel Bandwidth")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_40Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputAcrossBw40MhzNAT(object):
    """Throughput Across Bw NAT Mode
       pytest -m "throughput_across_bw_test and NAT"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2557", name="WIFI-2557")
    @pytest.mark.bw40Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, 
                                     lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and twog"
        """
        profile_data = setup_params_general_40Mhz["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, bw="40")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2557", name="WIFI-2557")
    @pytest.mark.bw40Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, 
                                     lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_40Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, bw="40")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

setup_params_general_80Mhz = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
                "channel-width": 80,
                }
    },
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput across channel-width Tests : WPA2 Personal Security")
@allure.suite("NAT Mode")
@allure.sub_suite("80Mhz Channel Bandwidth")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_80Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputAcrossBw80MhzNAT(object):
    """Throughput Across Bw NAT Mode
       pytest -m "throughput_across_bw_test and NAT"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2558", name="WIFI-2558")
    @pytest.mark.bw80Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, 
                                     lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, bw="80")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-9743", name="WIFI-9743")
    @pytest.mark.bw80Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.mmm
    @pytest.mark.tcp_download
    def test_client_wpa2_NAT_tcp_dl_80Mhz(self, lf_tools, get_apnos_max_clients,
                                    lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        vlan = 1
        max = int(get_apnos_max_clients[0])
        sets = [["DUT_NAME", lf_tools.dut_name]]
        print("sets", sets)
        #lf_tools.add_stations(band="2G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        #lf_tools.add_stations(band="5G", num_stations=max, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        influx_tags = "wifi-capacity-tcp-download-nat-wpa2-80Mhz-AX"
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1.5Gbps", batch_size="1",
                                        influx_tags=influx_tags, sets=sets,
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000", move_to_influx=True)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        lf_tools.attach_report_kpi(report_name=report_name)

        assert True


setup_params_general_160Mhz = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
            "5G": {
                "channel-width": 160,
             }
        },
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput across channel-width Tests : WPA2 Personal Security")
@allure.suite("NAT Mode")
@allure.sub_suite("160Mhz Channel Bandwidth")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_160Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputAcrossBw160MhzNAT(object):
    """Throughput Across Bw NAT Mode
       pytest -m "throughput_across_bw_test and NAT"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2559", name="WIFI-2559")
    @pytest.mark.bw160Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, 
                                     lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw NAT Mode
           pytest -m "throughput_across_bw_test and NAT and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_160Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, bw="160")
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

