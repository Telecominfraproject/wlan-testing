"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.bridge, pytest.mark.wpa2, pytest.mark.canada]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_1", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 1
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel1(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel1
    def test_client_bridge_wpa2_chn1_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel1"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general1['rf']['2G']['channel']
        channel_width = setup_params_general1['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_2", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 2
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel2(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel2
    def test_client_bridge_wpa2_chn2_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel2"
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general2['rf']['2G']['channel']
        channel_width = setup_params_general2['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_3", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 3
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel3(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel3
    def test_client_bridge_wpa2_chn3_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel3"
        """
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general3['rf']['2G']['channel']
        channel_width = setup_params_general3['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_4", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 4
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel4(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel4
    def test_client_bridge_wpa2_chn4_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel4"
        """
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general4['rf']['2G']['channel']
        channel_width = setup_params_general4['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_5", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 5
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel5(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel5
    def test_client_bridge_wpa2_chn5_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel5"
        """
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general5['rf']['2G']['channel']
        channel_width = setup_params_general5['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_6", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 6
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel6(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel6
    def test_client_bridge_wpa2_chn6_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel6"
        """
        profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general6['rf']['2G']['channel']
        channel_width = setup_params_general6['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_7", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 7
             }
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel7(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel7
    def test_client_bridge_wpa2_chn7_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel7"
        """
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general7['rf']['2G']['channel']
        channel_width = setup_params_general7['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_8", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 8}
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel8(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel8
    def test_client_bridge_wpa2_chn8_20Mhz_CA_2g(self, lf_test, station_names_twog, get_configuration):
        """Country code Bridge Mode
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel8"
        """
        profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][0]
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        channel = setup_params_general8['rf']['2G']['channel']
        channel_width = setup_params_general8['rf']['2G']['channel-width']

        result = lf_test.country_code_channel_division(ssid=ssid, security=security, passkey=security_key, mode=mode,
                                                       band=band, station_name=station_names_twog, vlan_id=vlan,
                                                       channel=channel, channel_width=channel_width, country_num=124,
                                                       country='Canada(CA)')
        if result:
            assert True
        else:
            assert False


setup_params_general9 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_9", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 9}
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel9(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True



setup_params_general10 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 10}
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general10],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz2GChannel10(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True



setup_params_general11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G":
            {'band': '2G',
             'channel-width': 20,
             "channel": 11}
    },
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test20Mhz2GChannel11PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True
