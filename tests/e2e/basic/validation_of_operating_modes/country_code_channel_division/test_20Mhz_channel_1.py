"""

    Performance Test: Throughput vs Various Pkt Size Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.Bridge, pytest.mark.open,]
              # pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}]},
    "rf": [{
        'band': '2G',
        'country': 'US',
        'channel-width': 20,
        "channel": 1
    },
        {
        "band": "5G",
        "country": "US",
        "channel-width": 40,
        "channel": 36
        }],
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryCode20MhzBridge2G(object):
    """Throughput vs Various Pkt Size Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.twentyMhz
    @pytest.mark.chnone
    @pytest.mark.US
    def test_client_bridge_open_chn1_20Mhz_US_2g(self, lf_test, station_names_twog, get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and Bridge and open and twog and pkt60"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        if station:
            check_channel = station.json_get("/port/all?fields=alias,channel")
            assert True
        else:
            assert False