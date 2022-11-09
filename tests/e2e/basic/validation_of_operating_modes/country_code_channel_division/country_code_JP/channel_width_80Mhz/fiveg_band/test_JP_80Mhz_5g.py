"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""


import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.bridge, pytest.mark.wpa2, pytest.mark.japan]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'JP',
        "channel-mode": "VHT",
        'channel-width': 80,
        "channel": 36},
        "2G":
        {'band': '2G',
        'country': 'JP',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("JP country code (Channel-36)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryJP80Mhz5GChannel36(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    @allure.title("Test for bandwidth 80 and channel 36")
    def test_client_bridge_wpa2_chn36_80Mhz_JP_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel36"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general1['rf']['5G']['channel']
        channel_width = setup_params_general1['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=392,
                                                       country='Japan(JP)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'JP',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 52},
        "2G":
        {'band': '2G',
        'country': 'JP',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("JP country code (Channel-52)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryJP80Mhz5GChannel52(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel52
    @allure.title("Test for bandwidth 80 and channel 52")
    def test_client_bridge_wpa2_chn52_80Mhz_JP_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel52"
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general2['rf']['5G']['channel']
        channel_width = setup_params_general2['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=392,
                                                       country='Japan(JP)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'JP',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 100},
        "2G":
        {'band': '2G',
        'country': 'JP',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("JP country code (Channel-100)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryJP80Mhz5GChannel100(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel100
    @allure.title("Test for bandwidth 80 and channel 100")
    def test_client_bridge_wpa2_chn100_80Mhz_JP_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel100"
        """
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general3['rf']['5G']['channel']
        channel_width = setup_params_general3['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=392,
                                                       country='Japan(JP)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'JP',
        'channel-mode': 'VHT',
        'channel-width': 80,
        "channel": 116},
        "2G":
        {'band': '2G',
        'country': 'JP',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("JP country code (Channel-116)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryJP80Mhz5GChannel116(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel116
    @allure.title("Test for bandwidth 80 and channel 116")
    def test_client_bridge_wpa2_chn116_80Mhz_JP_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and eightyMhz and wpa2 and fiveg and channel116"
        """
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general4['rf']['5G']['channel']
        channel_width = setup_params_general4['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=392,
                                                       country='Japan(JP)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False

