"""

    UCI Rest API Tests: Test Devices API

"""
import pytest


class TestUCIAUTHDEAUTH(object):
    """
        pytest -m "uci_login or uci_logout" --ucentral
    """

    @pytest.mark.uci_login
    def test_get_all_devices(self, setup_controller):
        """
            pytest -m "uci_login" --ucentral
        """
        print(setup_controller.login_resp)
        assert setup_controller.login_resp.status_code == 200

    @pytest.mark.uci_logout
    def test_get_device_by_serial(self, setup_controller):
        """
            pytest -m "uci_logout" --ucentral
        """
        resp = setup_controller.logout()
        print(resp)
        assert resp.status_code == 200
