"""

    Performance Test: Throughput vs Various Pkt Size Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""
# TODO: remove 5g config
#  correct markers in comments

import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.Bridge, pytest.mark.wpa2, pytest.mark.US]
              # pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                         {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"2G":
        {
        'band': '2G',
        'country': 'US',
        'channel-width': 20,
        "channel": 1
    },
        "5G":
            {
        "band": "5G",
        "country": "US",
        "channel-width": 40,
        "channel": 36
        }},
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
class TestCountryUS20Mhz2GChannel1(object):
    """Throughput vs Various Pkt Size Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    # @pytest.mark.US
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channelone
    def test_client_bridge_open_chn1_20Mhz_US_2g(self, lf_test, station_names_twog, get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and Bridge and open and twog and pkt60"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf']['2G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel)
        if result:
            assert True
        else:
            assert False