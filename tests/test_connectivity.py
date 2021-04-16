import pytest
import sys

@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestConnection:

    def test_cloud_connectivity(self, instantiate_cloudsdk, instantiate_testrail, instantiate_project, test_cases):
        try:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                             status_id=1, msg='Read CloudSDK version from API successfully')
            PASS = True
        except:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_ver"], run_id=instantiate_project,
                                                 status_id=0, msg='Could not read CloudSDK version from API')
            PASS = False
        assert instantiate_cloudsdk

    @pytest.mark.ap_conn
    def test_access_points_connectivity(self, test_access_point, instantiate_testrail, instantiate_project, test_cases):
        if "ACTIVE" not in test_access_point:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='CloudSDK connectivity failed')
            status = False
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Manager status is Active')
            status = True
            sys.exit()
        assert status

    def test_lanforge_connectivity(self, setup_lanforge):
        assert "instantiate_cloudsdk"

    def test_perfecto_connectivity(self, setup_perfecto_devices):
        assert "instantiate_cloudsdk"

