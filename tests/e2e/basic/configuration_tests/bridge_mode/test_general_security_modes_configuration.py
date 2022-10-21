"""

    Profile Configuration : Non-Enterprise SSID's Bridge Mode
    pytest -m "setup and bridge and general"

"""
import time

import allure
import pytest

pytestmark = [pytest.mark.setup, pytest.mark.bridge, pytest.mark.sanity, pytest.mark.general,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.suiteA
@allure.feature("BRIDGE MODE SETUP")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestSetupBridgeSuiteA(object):
    """ General Security Modes: SuiteA
        pytest -m "setup and bridge and general and suiteA"
    """

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_open_2g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation open 2.4G
            pytest -m "setup and bridge and general and suiteA and open and twog"
        """
        assert setup_configuration['open_2g']

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_open_5g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation open 5G
            pytest -m "setup and bridge and general and suiteA and open and fiveg"
         """
        assert setup_configuration['open_5g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa 2.4G
            pytest -m "setup and bridge and general and suiteA and wpa and twog"
        """
        assert setup_configuration['wpa_2g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa 5G
            pytest -m "setup and bridge and general and suiteA and wpa and fiveg"
        """
        assert setup_configuration['wpa_5g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, setup_configuration, update_report,
                                                 test_cases):
        """ SSID Profile Creation wpa2_personal 2.4G
            pytest -m "setup and bridge and general and suiteA and wpa2_personal and twog"
        """
        assert setup_configuration['wpa2_personal_2g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, setup_configuration, update_report,
                                                 test_cases):
        """ SSID Profile Creation wpa2_personal 5G
            pytest -m "setup and bridge and general and suiteA and wpa2_personal and fiveg"
         """
        assert setup_configuration['wpa2_personal_5g']

    @pytest.mark.sanity_light
    def test_setup_equipment_ap_profile(self, setup_configuration, update_report,
                                        test_cases):
        """ Equipment AP Profile SuiteA General """
        assert setup_configuration['equipment_ap']

    @pytest.mark.sanity_light
    def test_verify_vif_config(self, setup_configuration, update_report,
                               test_cases):
        """ vifc SuiteA General """
        assert setup_configuration['vifc']

    @pytest.mark.sanity_light
    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_configuration, update_report,
                              test_cases):
        """ vifs SuiteA General """
        time.sleep(200)
        assert setup_configuration['vifs']


setup_params_general_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.suiteB
@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectivitySuiteB(object):
    """ General Security Modes: SuiteB """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    def test_setup_wpa3_personal_2g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa3_personal 2.4G
            pytest -m "setup and bridge and general and suiteB and wpa3_personal and twog"
         """
        assert setup_configuration['wpa3_personal_2g']

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    def test_setup_wpa3_personal_5g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa3_personal 5G
            pytest -m "setup and bridge and general and suiteB and wpa3_personal and fiveg"
        """

        assert setup_configuration['wpa3_personal_5g']

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    def test_setup_wpa3_personal_mixed_2g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa3_personal_mixed 2.4G
            pytest -m "setup and bridge and general and suiteB and wpa3_personal_mixed and twog"
         """
        assert setup_configuration['wpa3_personal_mixed_2g']

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    def test_setup_wpa3_personal_mixed_5g_ssid_profile(self, setup_configuration, update_report, test_cases):
        """ SSID Profile Creation wpa3_personal_mixed 5G
            pytest -m "setup and bridge and general and suiteB and wpa3_personal_mixed and fiveg"

         """
        assert setup_configuration['wpa3_personal_mixed_5g']

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    def test_setup_wpa_wpa2_personal_mixed_2g_ssid_profile(self, setup_configuration, update_report,
                                                           test_cases):
        """ SSID Profile Creation wpa_wpa2_personal_mixed 2.4G
            pytest -m "setup and bridge and general and suiteB and wpa_wpa2_personal_mixed and twog"

        """
        assert setup_configuration['wpa_wpa2_personal_mixed_2g']

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    def test_setup_wpa_wpa2_personal_mixed_5g_ssid_profile(self, setup_configuration, update_report,
                                                           test_cases):
        """ SSID Profile Creation wpa_wpa2_personal_mixed 5G
            pytest -m "setup and bridge and general and suiteB and wpa_wpa2_personal_mixed and fiveg"

         """
        assert setup_configuration['wpa_wpa2_personal_mixed_5g']

    def test_setup_equipment_ap_profile(self, setup_configuration, update_report,
                                        test_cases):
        """ Equipment AP Suite B """
        assert setup_configuration['equipment_ap']

    def test_verify_vif_config(self, setup_configuration, update_report,
                               test_cases):
        """ vif config Suite B """
        assert setup_configuration['vifc']

    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_configuration, update_report,
                              test_cases):
        """ vif state Suite B """
        time.sleep(200)
        assert setup_configuration['vifs']