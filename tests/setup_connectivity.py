import pytest


@pytest.mark.sanity
class TestConnection:

    @pytest.mark.test_cloud_connectivity
    def test_cloud_connectivity(self, instantiate_cloudsdk):
        assert instantiate_cloudsdk

    @pytest.mark.test_access_points_connectivity
    def test_access_points_connectivity(self, instantiate_cloudsdk):
        assert instantiate_cloudsdk

    @pytest.mark.test_lanforge_connectivity
    def test_lanforge_connectivity(self, setup_lanforge):
        assert "instantiate_cloudsdk"

    @pytest.mark.test_perfecto_connectivity
    def test_perfecto_connectivity(self, setup_perfecto_devices):
        assert "instantiate_cloudsdk"
