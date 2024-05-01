"""
    Config AP with maximum no. of SSIDs Test: VLAN Mode
    pytest -m max_ssid
"""
import allure
import pytest

pytestmark = [pytest.mark.max_ssid, pytest.mark.vlan, pytest.mark.open, pytest.mark.wpa, pytest.mark.wpa2_personal,
              pytest.mark.wpa3_personal]


setup_params_general0 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"], "vlan": 100}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Only 2.4GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general0],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid2G(object):
    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.eight_ssid_2g
    def test_max_eight_ssid_2g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                               get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and eight_ssid_2g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general0, mode='VLAN', vlan_id=[100])


setup_params_general1 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"], "vlan": 100},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Only 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid5G(object):
    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.fiveg
    @pytest.mark.eight_ssid_5g
    def test_max_eight_ssid_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                               get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and eight_ssid_5g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general1, mode='VLAN', vlan_id=[100])


setup_params_general2 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"], "vlan": 100}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Only 2.4GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid2G(object):
    @allure.title("Trying more than 8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.more_than_eight_ssid_2g
    def test_more_than_eight_ssid_2g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and more_than_eight_ssid_2g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general2, mode='VLAN', vlan_id=[100])


setup_params_general3 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"], "vlan": 100},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Only 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid5G(object):
    @allure.title("Trying more than 8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.fiveg
    @pytest.mark.more_than_eight_ssid_5g
    def test_more_than_eight_ssid_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and more_than_eight_ssid_5g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general3, mode='VLAN', vlan_id=[100])


setup_params_general4 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"], "vlan": 100},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Both 2.4GHz and 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxSixteenSsid(object):
    @allure.title("16-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.sixteen_ssid_2g_5g
    def test_max_sixteen_2g_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                               get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and sixteen_ssid_2g_5g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general4, mode='VLAN', vlan_id=[100])


setup_params_general5 = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"], "vlan": 100},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("VLAN Mode")
@allure.sub_suite("Both 2.4GHz and 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanSixteenSsid(object):
    @allure.title("Trying more than 16-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.more_than_sixteen_ssid_2g_5g
    def test_more_than_sixteen_2g_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and vlan and more_than_sixteen_ssid_2g_5g
        """

        get_test_library.max_ssid(setup_params_general=setup_params_general5, mode='VLAN', vlan_id=[100])
