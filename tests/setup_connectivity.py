import pytest


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestConnection:

    def test_cloud_connectivity(self, instantiate_cloudsdk):
        assert instantiate_cloudsdk

    def test_access_points_connectivity(self, instantiate_cloudsdk):
        assert instantiate_cloudsdk

    def test_lanforge_connectivity(self, setup_lanforge):
        assert "instantiate_cloudsdk"

    def test_perfecto_connectivity(self, setup_perfecto_devices):
        assert "instantiate_cloudsdk"
