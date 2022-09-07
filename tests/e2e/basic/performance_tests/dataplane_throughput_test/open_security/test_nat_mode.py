"""

    Performance Test: Dataplane Throughput Test open secutrity: nat Mode.
    pytest -m "dataplane_throughput_test and nat and open"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_throughput_test,
              pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("NAT MODE Dataplane Throughput Test")
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestDataplaneThroughputNAT(object):
    """Dataplane THroughput nat Mode
       pytest -m "dataplane_throughput_test and nat"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673", name="WIFI-3673")
    @pytest.mark.open
    @pytest.mark.twog
    def test_tcp_upd_open_nat_2g_band(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "NAT"
        band = "twog"
        influx_tags = "dataplane-tcp-udp-nat-open-2.4G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_OPEN_2G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.open
    @pytest.mark.fiveg
    def test_tcp_upd_open_nat_5g_band(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and open and fiveg"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        influx_tags = "dataplane-tcp-udp-nat-open-5G"
        get_test_library.dataplane_throughput_test(ssid=ssid_name, security=security,
                                                   num_sta=1, mode=mode,
                                                   band=band,
                                                   instance_name="TIP_DPT_DPT_OPEN_5G_NAT",
                                                   influx_tags=influx_tags, move_to_influx=False,
                                                   )

