"""
Rate LImiting Bridge Mode Scenario
"""

import allure
import pytest

pytestmark = [pytest.mark.bridge, pytest.mark.rate_limiting_tests]

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


@allure.parent_suite("OpenWifi Rate Limiting Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA2 Personal Security")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestRateLimitingBridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upload
    @pytest.mark.batch_size_125
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Upload batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_up_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up", mode=mode,
                                       download_rate="0Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5})
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.download
    @pytest.mark.batch_size_125
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Download batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_dw_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5})
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upload_download
    @pytest.mark.ow_sanity_lf
    @pytest.mark.batch_size_125
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Upload and Download batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_up_dw_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                        get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.disable_up_dw
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for ssid disable Upload and Download batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_disable_up_dw_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and disable_up_dw"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        profile_data["rate-limit"][0] = 0
        profile_data["rate-limit"][1] = 0
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_di", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw_per_client
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Upload and Download per client batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_up_dw_per_client_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                                   get_test_device_logs, num_stations,
                                                                   setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up_dw_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_up_dw_per_cl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5}, raw_lines=raw_lines)
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_per_client
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Upload per client batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_up_per_client_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_per_cl", mode=mode,
                                       download_rate="0Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5}, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw_per_client
    @pytest.mark.rate_limiting_tests
    @allure.title("Test for Download per client batch size 1,2,5 2.4 GHz")
    def test_wpa2_personal_ssid_dw_per_client_batch_size_125_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and dw_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["dw_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_per_cl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 5}, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_125
    @allure.title("Test for Upload per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_up_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_125", mode=mode,
                                       download_rate="0Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_125
    @allure.title("Test for Download per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_dw_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_125", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    @allure.title("Test for Upload and Download per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_up_dw_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                        get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_125", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.title("Test for Upload batch size 1 2.4 GHz")
    def test_wpa2_personal_ssid_up_batch_size_1_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                   get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_1", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.title("Test for Download batch size 1 2.4 GHz")
    def test_wpa2_personal_ssid_dw_batch_size_1_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                   get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_1", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.title("Test for Upload and Download batch size 1 2.4 GHz")
    def test_wpa2_personal_ssid_up_dw_batch_size_1_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and twog and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl_up_dw_1", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.title("Test for Upload batch size 1 5 GHz")
    def test_wpa2_personal_ssid_up_batch_size_1_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                   get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_1_5g", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.title("Test for Download batch size 1 5 GHz")
    def test_wpa2_personal_ssid_dw_batch_size_1_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                   get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_1_5g", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.title("Test for Upload and Download batch size 1 5 GHz")
    def test_wpa2_personal_ssid_up_dw_batch_size_1_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs, num_stations, setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_1_5g", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.disable_up_dw
    @allure.title("Test for ssid disable Upload and Download batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_disable_up_dw_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and disable_up_dw"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        profile_data["rate-limit"][0] = 0
        profile_data["rate-limit"][1] = 0
        mode = "BRIDGE"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_dw_di_5g", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5})

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw_per_client
    @allure.title("Test for Upload and Download per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_up_dw_per_client_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                                   get_test_device_logs, num_stations,
                                                                   setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up_dw_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_per_cl_5g", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5}, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_per_client
    @allure.title("Test for Upload per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_up_per_client_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and up_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["ul_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_up_per_cl_5g", mode=mode,
                                       download_rate="0Gbps", batch_size="1,2,5",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5}, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw_per_client
    @allure.title("Test for Download per client batch size 1,2,5 5 GHz")
    def test_wpa2_personal_ssid_dw_per_client_batch_size_125_5g(self, get_test_library, get_dut_logs_per_test_case,
                                                                get_test_device_logs, num_stations,
                                                                setup_configuration):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting_tests and bridge and wpa2_personal and fiveg and dw_per_client"
        """
        # run wifi capacity test here
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 100,
                            "egress-rate": 100
                        }
                        }
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        raw_lines = [["dw_rate_sel: Per-Station Download Rate:"]]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_dw_per_cl_5g", mode=mode,
                                       download_rate="1Gbps", batch_size="1,2,5",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 5}, raw_lines=raw_lines)

        assert True
