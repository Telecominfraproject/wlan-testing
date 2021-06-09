import allure
import pytest

pytestmark = [pytest.mark.eap_nat_passpoint, pytest.mark.sanity, pytest.mark.nat]

setup_params_eap = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "passpoint_profile_download", "appliedRadios": ["is2dot4GHz"]}
        ],
        "wpa2_eap": [
            {"ssid_name": "ssid_wpa2_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
        ],
        "wpa2_only_eap": [
            {"ssid_name": "ssid_wpa2_only_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_only_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
        ]
    }
}


@allure.feature("NAT MODE EAP PASSPOINT SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_eap],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEapAuth(object):

    def test_eap_passpoint_osu_id_provider_creation(self, setup_profiles):
        test_cases, instantiate_profile, profile_data = setup_profiles
        assert test_cases['passpoint_osu_id_provider']['sdk'], "Failed to create passpoint_osu_id_provider profile"

    def test_eap_passpoint_operator_creation(self, setup_profiles):
        test_cases, instantiate_profile, profile_data = setup_profiles
        assert test_cases['passpoint_operator_profile']['sdk'], "Failed to create passpoint_osu_id_provider profile"

    def test_eap_passpoint_venue_creation(self, setup_profiles):
        test_cases, instantiate_profile, profile_data = setup_profiles
        assert test_cases['passpoint_venue_profile']['sdk'], "Failed to create passpoint_osu_id_provider profile"

    def test_eap_passpoint_creation(self, setup_profiles):
        test_cases, instantiate_profile, profile_data = setup_profiles
        assert test_cases['passpoint']['sdk'], "Failed to create passpoint_osu_id_provider profile"

    @pytest.mark.wpa2_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_wpa2_eap_2g(self, passpoint_profile_info, setup_profiles, push_ap_profile):
        assert push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_config'], \
            "Failed to push config for ssid_wpa2_eap_passpoint_2g"
        assert push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_state'], \
            "Failed to apply config on AP for ssid_wpa2_eap_passpoint_2g"

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

    @pytest.mark.wpa2_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_wpa2_eap_5g(self, passpoint_profile_info, setup_profiles, push_ap_profile):
        assert push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_config'], \
            "Failed to push config for ssid_wpa2_eap_passpoint_5g"
        assert push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_state'], \
            "Failed to apply config on AP for ssid_wpa2_eap_passpoint_5g"

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

    @pytest.mark.wpa2_only_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_wpa2_only_eap_2g(self, passpoint_profile_info, setup_profiles, push_ap_profile):
        assert push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_config'], \
            "Failed to push config for ssid_wpa2_only_eap_passpoint_2g"
        assert push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_state'], \
            "Failed to apply config on AP for ssid_wpa2_only_eap_passpoint_2g"

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][0]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])

    @pytest.mark.wpa2_only_eap
    @pytest.mark.fiveg
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_only_eap_passpoint_5g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_wpa2_only_eap_5g(self, passpoint_profile_info, setup_profiles, push_ap_profile):
        assert push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_config'], \
            "Failed to push config for ssid_wpa2_only_eap_passpoint_5g"
        assert push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_state'], \
            "Failed to apply config on AP for ssid_wpa2_only_eap_passpoint_5g"

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])
