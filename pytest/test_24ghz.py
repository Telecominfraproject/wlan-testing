# https://docs.pytest.org/en/latest/example/markers.html
# https://docs.pytest.org/en/latest/usage.html
# http://pythontesting.net/framework/pytest/pytest-introduction/

import pytest
from time import sleep, gmtime, strftime
from sta_connect2 import StaConnect2

@pytest.mark.usefixtures('setup_testrails')
@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.usefixtures('instantiate_testrail')
class Test24ghz(object):
    @pytest.mark.featureA
    def test_single_client_wpa2(self, setup_testrails, setup_cloudsdk, update_firmware, instantiate_testrail):
        lf_config = setup_cloudsdk["LANforge"]
        radio_config = setup_cloudsdk["24ghz"]

        staConnect = StaConnect2(lf_config["host"], lf_config["port"], debug_ = False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = lf_config["eth_port"]
        staConnect.radio = lf_config["radio"]
        staConnect.runtime_secs = lf_config["runtime_duration"]
        staConnect.resource = 1
        staConnect.dut_ssid = radio_config["ssid"]
        staConnect.dut_passwd = radio_config["password"]
        staConnect.dut_security = "wpa2"
        staConnect.station_names = radio_config["station_names"]
        staConnect.bringup_time_sec = 60
        staConnect.cleanup_on_exit = True
        staConnect.setup()
        staConnect.start()
        sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()

        assert staConnect.passes()
        if setup_testrails > 0:
            instantiate_testrail.update_testrail(case_id=2835, run_id=setup_testrails, status_id=1, msg="testing")

    @pytest.mark.featureB
    def test_feature_b(self):
        pass

    @pytest.mark.featureC
    def test_feature_c(self):
        assert 1 == 0

    @pytest.mark.featureD
    def test_feature_d(self):
        pytest.skip("speedup")

    @pytest.mark.xfail
    @pytest.mark.featureE
    def test_feature_e(self):
        assert 1 == 0
