"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""


import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.bridge, pytest.mark.wpa2, pytest.mark.united_kingdom]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G":
            {'band': '5G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 36
             },
        "2G":
            {'band': '2G',
            'country': 'GB',
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
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-36)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel36(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    @allure.title("Test for bandwidth 20 and channel 36")
    def test_client_bridge_wpa2_chn36_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel36"
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
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
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
        'country': 'GB',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 40},
        "2G":
            {'band': '2G',
            'country': 'GB',
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
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-40)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel40(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel40
    @allure.title("Test for bandwidth 20 and channel 40")
    def test_client_bridge_wpa2_chn40_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel40"
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
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
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
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 44},
        "2G":
            {'band': '2G',
            'country': 'GB',
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
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-44)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel44(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel44
    @allure.title("Test for bandwidth 20 and channel 44")
    def test_client_bridge_wpa2_chn44_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel44"
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
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
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
        'country': 'GB',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 48},
        "2G":
            {'band': '2G',
            'country': 'GB',
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
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-48)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel48(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel48
    @allure.title("Test for bandwidth 20 and channel 48")
    def test_client_bridge_wpa2_chn48_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel48"
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
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 52},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-52)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel52(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel52
    @allure.title("Test for bandwidth 20 and channel 52")
    def test_client_bridge_wpa2_chn52_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel52"
        """
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general5['rf']['5G']['channel']
        channel_width = setup_params_general5['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 56},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-56)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel56(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel56
    @allure.title("Test for bandwidth 20 and channel 56")
    def test_client_bridge_wpa2_chn56_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel56"
        """
        profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general6['rf']['5G']['channel']
        channel_width = setup_params_general6['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 60},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-60)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel60(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel60
    @allure.title("Test for bandwidth 20 and channel 60")
    def test_client_bridge_wpa2_chn60_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel60"
        """
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general7['rf']['5G']['channel']
        channel_width = setup_params_general7['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        "channel-mode": "VHT",
        'channel-width': 20,
        "channel": 64},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-64)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel64(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel64
    @allure.title("Test for bandwidth 20 and channel 64")
    def test_client_bridge_wpa2_chn64_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel64"
        """
        profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general8['rf']['5G']['channel']
        channel_width = setup_params_general8['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general9 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 100},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-100)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel100(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel100
    @allure.title("Test for bandwidth 20 and channel 100")
    def test_client_bridge_wpa2_chn100_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel100"
        """
        profile_data = setup_params_general9["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general9['rf']['5G']['channel']
        channel_width = setup_params_general9['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general10 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 104},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general10],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-104)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel104(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel104
    @allure.title("Test for bandwidth 20 and channel 104")
    def test_client_bridge_wpa2_chn104_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel104"
        """
        profile_data = setup_params_general10["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general10['rf']['5G']['channel']
        channel_width = setup_params_general10['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 108},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-108)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel108(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel108
    @allure.title("Test for bandwidth 20 and channel 108")
    def test_client_bridge_wpa2_chn108_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel108"
        """
        profile_data = setup_params_general11["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general11['rf']['5G']['channel']
        channel_width = setup_params_general11['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general12 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 112},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general12],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-112)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel112(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel112
    @allure.title("Test for bandwidth 20 and channel 112")
    def test_client_bridge_wpa2_chn112_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel112"
        """
        profile_data = setup_params_general12["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general12['rf']['5G']['channel']
        channel_width = setup_params_general12['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general13 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 116},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general13],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-116)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel116(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel116
    @allure.title("Test for bandwidth 20 and channel 116")
    def test_client_bridge_wpa2_chn116_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel116"
        """
        profile_data = setup_params_general13["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general13['rf']['5G']['channel']
        channel_width = setup_params_general13['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False

setup_params_general14 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 120},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general14],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-120)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel120(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel120
    @allure.title("Test for bandwidth 20 and channel 120")
    def test_client_bridge_wpa2_chn120_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel120"
        """
        profile_data = setup_params_general14["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general14['rf']['5G']['channel']
        channel_width = setup_params_general14['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general15 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 124},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general15],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-124)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel124(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel124
    @allure.title("Test for bandwidth 20 and channel 124")
    def test_client_bridge_wpa2_chn124_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel124"
        """
        profile_data = setup_params_general15["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general15['rf']['5G']['channel']
        channel_width = setup_params_general15['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general16 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 128},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general16],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-128)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel128(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel128
    @allure.title("Test for bandwidth 20 and channel 128")
    def test_client_bridge_wpa2_chn128_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel128"
        """
        profile_data = setup_params_general16["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general16['rf']['5G']['channel']
        channel_width = setup_params_general16['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general17 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 132},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general17],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-132)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel132(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel132
    @allure.title("Test for bandwidth 20 and channel 132")
    def test_client_bridge_wpa2_chn132_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel132"
        """
        profile_data = setup_params_general17["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general17['rf']['5G']['channel']
        channel_width = setup_params_general17['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general18 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 136},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general18],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-136)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel136(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel136
    @allure.title("Test for bandwidth 20 and channel 136")
    def test_client_bridge_wpa2_chn136_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel136"
        """
        profile_data = setup_params_general18["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general18['rf']['5G']['channel']
        channel_width = setup_params_general18['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general19 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 140},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general19],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-140)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel140(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel140
    @allure.title("Test for bandwidth 20 and channel 140")
    def test_client_bridge_wpa2_chn140_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel140"
        """
        profile_data = setup_params_general19["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general19['rf']['5G']['channel']
        channel_width = setup_params_general19['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general20 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 144},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general20],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-144)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel144(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel144
    @allure.title("Test for bandwidth 20 and channel 144")
    def test_client_bridge_wpa2_chn144_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel144"
        """
        profile_data = setup_params_general20["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general20['rf']['5G']['channel']
        channel_width = setup_params_general20['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general21 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 149},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general21],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-149)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel149(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel149
    @allure.title("Test for bandwidth 20 and channel 149")
    def test_client_bridge_wpa2_chn149_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel149"
        """
        profile_data = setup_params_general21["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general21['rf']['5G']['channel']
        channel_width = setup_params_general21['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general22 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 153},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general22],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-153)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel153(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel153
    @allure.title("Test for bandwidth 20 and channel 153")
    def test_client_bridge_wpa2_chn153_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel153"
        """
        profile_data = setup_params_general22["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general22['rf']['5G']['channel']
        channel_width = setup_params_general22['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general23 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 157},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general23],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-157)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel157(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel157
    @allure.title("Test for bandwidth 20 and channel 157")
    def test_client_bridge_wpa2_chn157_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel157"
        """
        profile_data = setup_params_general23["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general23['rf']['5G']['channel']
        channel_width = setup_params_general23['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general24 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 161},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general24],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-161)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel161(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel161
    @allure.title("Test for bandwidth 20 and channel 161")
    def test_client_bridge_wpa2_chn161_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel161"
        """
        profile_data = setup_params_general24["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general24['rf']['5G']['channel']
        channel_width = setup_params_general24['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False


setup_params_general25 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {"5G":
        {'band': '5G',
        'country': 'GB',
        'channel-mode': 'VHT',
        'channel-width': 20,
        "channel": 165},
        "2G":
            {'band': '2G',
            'country': 'GB',
            "channel-mode": "VHT",
            'channel-width': 20,
            "channel": 1}
           },
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general25],
    indirect=True,
    scope="class"
)
@allure.feature("Channel vs Country Code")
@allure.parent_suite("Country Code Tests")
@allure.suite("BRIDGE Mode(20 MHz)")
@allure.sub_suite("GB country code (Channel-165)")
@pytest.mark.usefixtures("setup_configuration")
class TestCountryGB20Mhz5GChannel165(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel165
    @allure.title("Test for bandwidth 20 and channel 165")
    def test_client_bridge_wpa2_chn165_20Mhz_GB_5g(self, get_test_library, setup_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel165"
        """
        profile_data = setup_params_general25["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general25['rf']['5G']['channel']
        channel_width = setup_params_general25['rf']['5G']['channel-width']

        result = get_test_library.country_code_channel_division(ssid=ssid, security=security, passkey=security_key,
                                                       band=band,  vlan_id=vlan, channel=channel, mode=mode,
                                                       channel_width=channel_width,country_num=826,
                                                       country='United Kingdom(GB)', dut_data=setup_configuration)
        if result:
            assert True
        else:
            assert False