"""
Rate LImiting Bridge Mode Scenario
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("Bridge MODE Rate Limiting")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRateLimitingBridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upload
    @pytest.mark.batch_size_125
    @pytest.mark.ow_rate_limiting_tests_lf
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.download
    @pytest.mark.batch_size_125
    @pytest.mark.ow_rate_limiting_tests_lf
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and dw and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upload_download
    @pytest.mark.ow_sanity_lf
    @pytest.mark.batch_size_125
    @pytest.mark.ow_rate_limiting_tests_lf
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.disable_up_dw
    @pytest.mark.ow_rate_limiting_tests_lf
    def test_wpa2_personal_ssid_disable_up_dw_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and disable_up_dw"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        profile_data["rate-limit"][0] = 0
        profile_data["rate-limit"][1] = 0
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_di", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw_per_client
    @pytest.mark.ow_rate_limiting_tests_lf
    def test_wpa2_personal_ssid_up_dw_per_client_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_dw_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_bridge_up_dw_per_cl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_per_client
    @pytest.mark.ow_rate_limiting_tests_lf
    def test_wpa2_personal_ssid_up_per_client_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_per_cl", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw_per_client
    @pytest.mark.ow_rate_limiting_tests_lf
    def test_wpa2_personal_ssid_dw_per_client_batch_size_125_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and dw_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["dw_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_per_cl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_125", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and dw and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_125", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_125", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_1_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_1", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_1_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and dw and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl_dw_1", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_1_2g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl_up_dw_1", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_1_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_1_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and dw and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_1_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.disable_up_dw
    def test_wpa2_personal_ssid_disable_up_dw_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and disable_up_dw"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        profile_data["rate-limit"][0] = 0
        profile_data["rate-limit"][1] = 0
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_di_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw_per_client
    def test_wpa2_personal_ssid_up_dw_per_client_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_dw_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_per_cl_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_per_client
    def test_wpa2_personal_ssid_up_per_client_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_per_cl_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw_per_client
    def test_wpa2_personal_ssid_dw_per_client_batch_size_125_5g(self, lf_test, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and dw_per_client"
        """
        # run wifi capacity test here
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        raw_lines = [["dw_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_per_cl_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000", raw_lines=raw_lines)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
