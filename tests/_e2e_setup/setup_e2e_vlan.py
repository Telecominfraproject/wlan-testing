import pytest


@pytest.mark.sanity
@pytest.mark.vlan
class TestSetupRF:

    @pytest.mark.wifi5
    def test_setup_rf_profile_wifi5(self, get_markers):
        assert True

    @pytest.mark.wifi6
    def test_setup_rf_profile_wifi6(self):
        assert True


@pytest.mark.sanity
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestSetupRadius:

    @pytest.mark.radius
    def test_setup_radius_profile(self):
        assert True


@pytest.mark.sanity
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestSetupSSIDProfiles:

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_open_2g_ssid_profile(self):
        assert True

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_open_5g_ssid_profile(self):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self):
        assert True

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self):
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_2g_ssid_profile(self):
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self):
        assert True


@pytest.mark.equipment_ap
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestEquipmentAPProfilevlan:

    @pytest.mark.fiveg
    @pytest.mark.radius
    @pytest.mark.twog
    @pytest.mark.wpa2_enterprise
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa
    @pytest.mark.open
    def test_setup_equipment_ap_profile(self):
        assert True


@pytest.mark.sanity
@pytest.mark.vlan
@pytest.mark.wifi5
@pytest.mark.wifi6
class TestProfilePush:

    def test_push_profile(self):
        assert True

    def test_verify_vif_config(self):
        assert True

    def test_verify_vif_state(self):
        assert True
