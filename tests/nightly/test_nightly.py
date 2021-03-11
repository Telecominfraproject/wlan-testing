import pytest


@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.nightly
class TestNightly(object):

    @pytest.mark.usefixtures('setup_cloudsdk')
    @pytest.mark.usefixtures('update_firmware')
    @pytest.mark.nightly_bridge
    def test_nightly_bridge(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 1

    @pytest.mark.usefixtures('setup_cloudsdk')
    @pytest.mark.usefixtures('update_firmware')
    @pytest.mark.nightly_nat
    def test_nightly_nat(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 1

    @pytest.mark.usefixtures('setup_cloudsdk')
    @pytest.mark.usefixtures('update_firmware')
    @pytest.mark.nightly_vlan
    def test_nightly_vlan(self, setup_cloudsdk, update_firmware):
        print(setup_cloudsdk)
        assert 1 == 1
