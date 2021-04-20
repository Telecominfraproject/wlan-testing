import pytest


@pytest.mark.rf
class TestRFProfiles:

    def test_rf_profile(self):
        assert True


@pytest.mark.radius
class TestRadiusProfile:

    def test_radius_profile(self):
        assert True


@pytest.mark.ssid
class TestSSIDProfile:

    @pytest.mark.open
    @pytest.mark.twog
    def test_open_ssid_2g(self):
        assert True

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_open_ssid_5g(self):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_wpa_ssid_2g(self):
        assert True

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_wpa_ssid_5g(self):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_personal_ssid_2g(self):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_personal_ssid_5g(self):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_wpa2_enterprise_ssid_2g(self):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_wpa2_enterprise_ssid_5g(self):
        assert True


@pytest.mark.equipment_ap_profile
class TestEquipmentAPProfile:

    @pytest.mark.bridge
    def test_equipment_ap_profile_bridge(self):
        assert True

    @pytest.mark.nat
    def test_equipment_ap_profile_nat(self):
        assert True

    @pytest.mark.vlan
    def test_equipment_ap_profile_vlan(self):
        assert True
