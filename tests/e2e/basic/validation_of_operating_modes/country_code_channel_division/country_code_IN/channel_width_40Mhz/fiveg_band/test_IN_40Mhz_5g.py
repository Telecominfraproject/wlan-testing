"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""


import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.bridge, pytest.mark.wpa2, pytest.mark.india]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
        "channel": 36},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
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
class TestCountryIN40Mhz5GChannel36(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    def test_client_bridge_wpa2_chn36_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel36"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general1['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
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
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 44},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
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
class TestCountryIN40Mhz5GChannel44(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel44
    def test_client_bridge_wpa2_chn44_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel44"
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general2['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
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
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 52},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
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
class TestCountryIN40Mhz5GChannel52(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel52
    def test_client_bridge_wpa2_chn52_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel52"
        """
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general3['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
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
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 60},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
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
class TestCountryIN40Mhz5GChannel60(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel60
    def test_client_bridge_wpa2_chn60_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel60"
        """
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general4['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
        if result:
            assert True
        else:
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 100},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryIN40Mhz5GChannel100(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel100
    def test_client_bridge_wpa2_chn100_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel100"
        """
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general5['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
        if result:
            assert True
        else:
            assert False


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 108},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryIN40Mhz5GChannel108(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel108
    def test_client_bridge_wpa2_chn108_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel108"
        """
        profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general6['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
        if result:
            assert True
        else:
            assert False


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 132},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryIN40Mhz5GChannel132(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel132
    def test_client_bridge_wpa2_chn132_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel132"
        """
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general7['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
        if result:
            assert True
        else:
            assert False


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'IN',
        'channel-mode': 'VHT',
        'channel-width': 40,
        "channel": 140},
           "2G":
        {'band': '2G',
        'country': 'IN',
        "channel-mode": "VHT",
        'channel-width': 40,
        "channel": 1}
           },
    "radius": False
}

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryIN40Mhz5GChannel140(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel140
    def test_client_bridge_wpa2_chn140_40Mhz_IN_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel140"
        """
        profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][1]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general8['rf']['5G']['channel']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                                       channel=channel,country=356)
        if result:
            assert True
        else:
            assert False


