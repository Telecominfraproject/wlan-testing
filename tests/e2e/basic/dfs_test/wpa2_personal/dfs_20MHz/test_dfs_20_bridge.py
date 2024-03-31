import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.dfs_tests,
              pytest.mark.bandwidth_20MHz]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 52
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-52")
@pytest.mark.usefixtures("setup_configuration")
class TestDFSChannel52Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6472", name="WIFI-6472")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_52_bw_20
    @allure.title("Test for Channel 52 and bandwidth 20")
    def test_dfs_channel_52_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  get_target_object,
                                  num_stations, check_connectivity, setup_configuration):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 52 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_52_bw_20
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 100
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-100")
class TestDFSChannel100Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6473", name="WIFI-6473")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_100_bw_20
    @allure.title("Test for Channel 100 and bandwidth 20")
    def test_dfs_channel_100_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 100 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_100_bw_20
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 104
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-104")
class TestDFSChannel104Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6474", name="WIFI-6474")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_104_bw_20
    @allure.title("Test for Channel 104 and bandwidth 20")
    def test_dfs_channel_104_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 104 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_104_bw_20
        """
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general3["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 56
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-56")
class TestDFSChannel56Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6475", name="WIFI-6475")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_56_bw_20
    @allure.title("Test for Channel 56 and bandwidth 20")
    def test_dfs_channel_56_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 56 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_56_bw_20
        """
        profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 60
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-60")
class TestDFSChannel60Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6476", name="WIFI-6476")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_60_bw_20
    @allure.title("Test for Channel 60 and bandwidth 20")
    def test_dfs_channel_60_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 60 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_60_bw_20
        """
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 64
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-64")
class TestDFSChannel64Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6477", name="WIFI-6477")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_64_bw_20
    @allure.title("Test for Channel 64 and bandwidth 20")
    def test_dfs_channel_64_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 64 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_64_bw_20
        """
        profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 108
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-108")
class TestDFSChannel108Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6478", name="WIFI-6478")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_108_bw_20
    @allure.title("Test for Channel 108 and bandwidth 20")
    def test_dfs_channel_108_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 108 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_108_bw_20
        """
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 112
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-112")
class TestDFSChannel112Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6479", name="WIFI-6479")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_112_bw_20
    @allure.title("Test for Channel 112 and bandwidth 20")
    def test_dfs_channel_112_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 112 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_112_bw_20
        """
        profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general10 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 132
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general10],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-132")
class TestDFSChannel132Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6481", name="WIFI-6481")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_132_bw_20
    @allure.title("Test for Channel 132 and bandwidth 20")
    def test_dfs_channel_132_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 132 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_132_bw_20
        """
        profile_data = setup_params_general10["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 136
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-136")
class TestDFSChannel136Bw20(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6482", name="WIFI-6482")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_136_bw_20
    @allure.title("Test for Channel 136 and bandwidth 20")
    def test_dfs_channel_136_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 136 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_136_bw_20
        """
        profile_data = setup_params_general11["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general12 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 140
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general12],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-140")
class TestDFSChannel140Bw20(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6483", name="WIFI-6483")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_140_bw_20
    @allure.title("Test for Channel 140 and bandwidth 20")
    def test_dfs_channel_140_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 140 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_140_bw_20
        """
        profile_data = setup_params_general12["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general13 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 20,
            "channel": 144
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general13],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("Bridge Mode(20 MHz)")
@allure.sub_suite("Channel-144")
class TestDFSChannel144Bw20(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6484", name="WIFI-6484")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_144_bw_20
    @allure.title("Test for Channel 144 and bandwidth 20")
    def test_dfs_channel_144_bw_20(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        DFS (Dynamic Frequency Selection) is a function in 5Ghz band. In 5Ghz band few channels are used by the
        RADAR systems. So, a mechanism called DFS was created to have the WIFI devices listen for radar events
        and either stop using the channels and automatically move to a non-DFS channel.
        So, verifying DFS with channel 144 at 20MHz bandwidth.

        Unique Marker:
        dfs_tests and bandwidth_20MHz and wpa2_personal and fiveg and dfs_channel_144_bw_20
        """
        profile_data = setup_params_general13["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)
