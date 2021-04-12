import pytest


@pytest.mark.sanity
@pytest.mark.bridge
class TestSetupBridge:

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_rf_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_radius_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_open_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_open_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_equipment_ap_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_push_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_config(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_state(self):
        assert True


@pytest.mark.sanity
@pytest.mark.nat
class TestSetupNAT:

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_rf_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_radius_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_open_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_open_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_equipment_ap_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_push_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_config(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_state(self):
        assert True


@pytest.mark.sanity
@pytest.mark.vlan
class TestSetupVLAN:

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_rf_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_radius_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_open_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_open_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, cleanup_profile):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_equipment_ap_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_push_profile(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_config(self):
        assert True

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_verify_vif_state(self):
        assert True
