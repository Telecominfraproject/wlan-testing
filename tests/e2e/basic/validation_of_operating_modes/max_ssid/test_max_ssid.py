"""
    Config AP with maximum no.of SSIDs Test: Bridge Mode
    pytest -m max_ssid
"""

import time
import allure
import pytest
from configuration import DYNAMIC_VLAN_RADIUS_SERVER_DATA
from configuration import DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.max_ssid, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMaxEightSsid2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.eight_ssid_2g
    @pytest.mark.twog
    def test_max_eight_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general["ssid_modes"]:
            for j in range(len(setup_params_general["ssid_modes"][i])):
                profile_data = setup_params_general["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_twog[0] + str(int(station_names_twog[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan, scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x : x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMaxEightSsid5G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.eight_ssid_5g
    @pytest.mark.fiveg
    def test_max_eight_ssid_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general1["ssid_modes"]:
            for j in range(len(setup_params_general1["ssid_modes"][i])):
                profile_data = setup_params_general1["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_fiveg[0] + str(int(station_names_fiveg[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan, scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x : x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMoreThanEightSsid2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_eight_ssid_2g
    @pytest.mark.twog
    def test_more_than_eight_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general2["ssid_modes"]:
            for j in range(len(setup_params_general2["ssid_modes"][i])):
                profile_data = setup_params_general2["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_twog[0] + str(int(station_names_twog[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan, scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x : x == False, pass_list))
        if len(fail_list) == len(pass_list):
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMoreThanEightSsid5G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_eight_ssid_5g
    @pytest.mark.fiveg
    def test_more_than_eight_ssid_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general["ssid_modes"]:
            for j in range(len(setup_params_general["ssid_modes"][i])):
                profile_data = setup_params_general["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_fiveg[0] + str(int(station_names_fiveg[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan, scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x : x == False, pass_list))
        if len(fail_list) == pass_list:
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMaxSixteenSsid(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.sixteen_ssid_2g_5g
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_max_sixteen_2g_5g(self, lf_test, station_names_twog, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band_name = (lambda bnd: '2G' if bnd == 'twog' else '5G')
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general4["ssid_modes"]:
            for j in range(len(setup_params_general4["ssid_modes"][i])):
                profile_data = setup_params_general4["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                if profile_data["appliedRadios"] == ['2G']:
                    band = 'twog'
                    sta_name = station_names_twog
                elif profile_data["appliedRadios"] == ['5G']:
                    band = 'fiveg'
                    sta_name = station_names_fiveg
                station_names = band_name(band) + sta_name[0] + str(int(sta_name[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz and 5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMoreThanSixteenSsid(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_sixteen_ssid_2g_5g
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_more_than_sixteen_2g_5g(self, lf_test, station_names_twog, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band_name = (lambda bnd: '2G' if bnd == 'twog' else '5G')
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general5["ssid_modes"]:
            for j in range(len(setup_params_general5["ssid_modes"][i])):
                profile_data = setup_params_general5["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                if profile_data["appliedRadios"] == ['2G']:
                    band = 'twog'
                    sta_name = station_names_twog
                elif profile_data["appliedRadios"] == ['5G']:
                    band = 'fiveg'
                    sta_name = station_names_fiveg
                station_names = band_name(band) + sta_name[0] + str(int(sta_name[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == len(pass_list):
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz and 5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False