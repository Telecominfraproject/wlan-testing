"""

    Save crashlog to pstore
    pytest -m "save_crashlog_to_pstore"

"""
import json
import logging
import time

import allure
import pytest

pytestmark = [pytest.mark.save_crashlog_to_pstore, pytest.mark.bridge, pytest.mark.wap2_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "OpenWifi_2G", "appliedRadios": ["2G"], "security_key": "OpenWifi"}]},
    "rf":{},
    "radius": False
}

@allure.feature("Save_crashlog_to_pstore")
@allure.parent_suite("Save crashlog to pstore")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestSaveCrashlogToPstore(object):
    """
        Save crashlog to pstore
        pytest -m "save_crashlog_to_pstore"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("Test save crashlog to pstore")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14627", name="WIFI-14627")
    def test_save_crashlog_to_pstore(self, get_test_library,
                                              get_testbed_details,
                                              get_target_object,
                                              setup_configuration,
                                              ):
        """
            Test Description: To verify whether the APs are saving crash logs to pstore or uploading them to the cloud.
            We manually trigger a crash using the command echo c > /proc/sysrq-trigger. After executing the crash command,
            wait for the AP to crash and reconnect to the Gateway (GW).
            Once the AP is back online, check the crashlogs under the Reboot Logs section in the
            GW to verify if the crash logs have been saved. If the logs are present, the test is considered PASS.
            Marker: "save_crashlog_to_pstore"
        """
        get_test_library.save_crashlogs_to_pstore(get_target_object=get_target_object, get_testbed_details=get_testbed_details)

        assert True
