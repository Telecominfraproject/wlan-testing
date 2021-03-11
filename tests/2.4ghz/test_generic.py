import pytest

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.UHF # example of a class mark
class Test24ghz(object):
    @pytest.mark.wpa2
    def test_single_client_wpa2(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 1

    @pytest.mark.open
    def test_single_client_open(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 1

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.SHF # example of a class mark
class Test50ghz(object):
    @pytest.mark.wpa2
    def test_single_client_wpa2(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 0

    @pytest.mark.open
    def test_single_client_open(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 0











