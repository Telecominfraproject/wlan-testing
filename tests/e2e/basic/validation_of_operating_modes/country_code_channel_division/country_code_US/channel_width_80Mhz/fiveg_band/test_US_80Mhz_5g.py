"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""


import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.bridge, pytest.mark.wpa2, pytest.mark.united_states]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'US',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 36},
           "2G":
        {'band': '2G',
        'country': 'US',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS80Mhz5GChannel36(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    def test_client_bridge_wpa2_chn36_80Mhz_US_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel36"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general1['rf']['5G']['channel']
        channel_width = setup_params_general1['rf']['5G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,channel_width=channel_width,country_num=840,
                                                       country='United States(US)')
        if result:
            assert True
        else:
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'US',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 52},
           "2G":
        {'band': '2G',
        'country': 'US',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS80Mhz5GChannel52(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel52
    def test_client_bridge_wpa2_chn52_80Mhz_US_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel52"
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general2['rf']['5G']['channel']
        channel_width = setup_params_general2['rf']['5G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,channel_width=channel_width,country_num=840,
                                                       country='United States(US)')
        if result:
            assert True
        else:
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'US',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 100},
           "2G":
        {'band': '2G',
        'country': 'US',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS80Mhz5GChannel100(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel100
    def test_client_bridge_wpa2_chn100_80Mhz_US_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel100"
        """
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general3['rf']['5G']['channel']
        channel_width = setup_params_general3['rf']['5G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,channel_width=channel_width,country_num=840,
                                                       country='United States(US)')
        if result:
            assert True
        else:
            assert False


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'US',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 132},
           "2G":
        {'band': '2G',
        'country': 'US',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS80Mhz5GChannel132(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel132
    def test_client_bridge_wpa2_chn132_80Mhz_US_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel132"
        """
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general4['rf']['5G']['channel']
        channel_width = setup_params_general4['rf']['5G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,channel_width=channel_width,country_num=840,
                                                       country='United States(US)')
        if result:
            assert True
        else:
            assert False

