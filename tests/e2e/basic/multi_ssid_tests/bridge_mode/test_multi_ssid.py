"""
    Multiple number of SSIDs Test: Bridge Mode
    pytest -m multi_ssid
"""
import allure
import pytest

pytestmark = [pytest.mark.multi_ssid, pytest.mark.bridge, pytest.mark.twog, pytest.mark.fiveg]


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath1(object):
    """
        Multiple number of SSIDs Test: Bridge Mode

        Unique Marker:
        multi_ssid and bridge and one_ssid
    """

    @allure.title("1-SSID")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12227")
    @pytest.mark.wpa2_personal
    @pytest.mark.one_ssid
    def test_one_ssid(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs, setup_configuration,
                      check_connectivity):
        """
            Multi-SSID Bridge Mode

            Unique Marker: multi_ssid and bridge and one_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general1, no_of_2g_and_5g_stations=2)


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath2(object):
    """
        Multiple number of SSIDs Test: Bridge Mode
        pytest -m multi_ssid and two_ssid
    """

    @allure.title("2-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12228")
    @pytest.mark.wpa2_personal
    @pytest.mark.two_ssid
    def test_two_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and two_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general2, no_of_2g_and_5g_stations=2)


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath3(object):

    @allure.title("3-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.three_ssid
    def test_three_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and three_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general3, no_of_2g_and_5g_stations=3)


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath4(object):

    @allure.title("4-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.four_ssid
    def test_four_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and four_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general4, no_of_2g_and_5g_stations=4)


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath5(object):

    @allure.title("5-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.five_ssid
    def test_five_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and five_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general5, no_of_2g_and_5g_stations=5)


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath6(object):

    @allure.title("6-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.six_ssid
    def test_six_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and six_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general6, no_of_2g_and_5g_stations=6)


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid7_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath7(object):

    @allure.title("7-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.seven_ssid
    def test_seven_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and seven_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general7, no_of_2g_and_5g_stations=7)


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid7_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid8_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for")
class TestMultiSsidDataPath8(object):

    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.eight_ssid
    def test_eight_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker: multi_ssid and bridge and eight_ssid
        """

        get_test_library.multi_ssid_test(setup_params_general=setup_params_general8, no_of_2g_and_5g_stations=8)
