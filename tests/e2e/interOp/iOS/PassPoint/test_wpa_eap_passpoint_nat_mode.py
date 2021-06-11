"""
    EAP Passpoint Test: NAT Mode
    pytest -m "interop_iOS and eap_passpoint and nat"
"""

import allure
import pytest

pytestmark = [pytest.mark.interop_iOS, pytest.mark.eap_passpoint, pytest.mark.nat]

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
    """
        EAP Passpoint NAT Mode
        pytest -m "interop_iOS and eap_passpoint and nat"
    """
    def test_eap_passpoint_osu_id_provider_creation(self, setup_profiles):
        """
            EAP Passpoint NAT Mode : OSU ID provider profile creation
            pytest -m "interop_iOS and eap_passpoint and nat"
        """
        test_cases, instantiate_profile, profile_data = setup_profiles
        result = test_cases['passpoint_osu_id_provider']['sdk']
        if result:
            allure.attach(name="OSU ID provider profile creation successful ", body="")
        else:
            allure.attach(name="OSU ID provider profile creation failed ", body="")
        assert result

    def test_eap_passpoint_operator_creation(self, setup_profiles):
        """
            EAP Passpoint NAT Mode : Passpoint operator profile creation
            pytest -m "interop_iOS and eap_passpoint and nat"
        """
        test_cases, instantiate_profile, profile_data = setup_profiles
        result = test_cases['passpoint_operator_profile']['sdk']
        if result:
            allure.attach(name="Passpoint operator profile creation successful ", body="")
        else:
            allure.attach(name="Passpoint operator profile creation failed ", body="")
        assert result

    def test_eap_passpoint_venue_creation(self, setup_profiles):
        """
            EAP Passpoint NAT Mode : Passpoint venue provider profile creation
            pytest -m "interop_iOS and eap_passpoint and nat"
        """
        test_cases, instantiate_profile, profile_data = setup_profiles
        result = test_cases['passpoint_venue_profile']['sdk']
        if result:
            allure.attach(name="Passpoint venue provider profile creation successful ", body="")
        else:
            allure.attach(name="Passpoint venue provider profile creation failed ", body="")
        assert result

    def test_eap_passpoint_creation(self, setup_profiles):
        """
            EAP Passpoint NAT Mode : Passpoint profile creation
            pytest -m "interop_iOS and eap_passpoint and nat"
        """
        test_cases, instantiate_profile, profile_data = setup_profiles
        result = test_cases['passpoint']['sdk']
        if result:
            allure.attach(name="Passpoint profile creation successful ", body="")
        else:
            allure.attach(name="Passpoint profile creation failed ", body="")
        assert result

    @pytest.mark.wpa2_eap
    @pytest.mark.twog
    @pytest.mark.parametrize(
        'push_ap_profile',
        [{"ssid_names": ["ssid_wpa2_eap_passpoint_2g", "passpoint_profile_download"]}],
        indirect=True,
        scope="function"
    )
    @pytest.mark.usefixtures("push_ap_profile")
    def test_wpa2_eap_2g(self, passpoint_profile_info, push_ap_profile):
        """
            EAP Passpoint NAT Mode
            pytest -m "interop_iOS and eap_passpoint and nat and wpa2_eap and twog"
        """
        result = push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_2g failed", body="")
        assert result
        result = push_ap_profile['ssid_wpa2_eap_passpoint_2g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_2g failed", body="")
        assert result

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
    def test_wpa2_eap_5g(self, passpoint_profile_info, push_ap_profile):
        """
            EAP Passpoint NAT Mode
            pytest -m "interop_iOS and eap_passpoint and nat and wpa2_eap and fiveg"
        """
        result = push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_eap_passpoint_5g failed", body="")
        assert result
        result = push_ap_profile['ssid_wpa2_eap_passpoint_5g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_eap_passpoint_5g failed", body="")
        assert result

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
    def test_wpa2_only_eap_2g(self, passpoint_profile_info, push_ap_profile):
        """
             EAP Passpoint NAT Mode
             pytest -m "interop_iOS and eap_passpoint and nat and wpa2_only_eap and twog"
        """
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_2g failed", body="")
        assert result
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_2g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_2g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_2g failed", body="")
        assert result

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
    def test_wpa2_only_eap_5g(self, passpoint_profile_info, push_ap_profile):
        """
             EAP Passpoint NAT Mode
             pytest -m "interop_iOS and eap_passpoint and nat and wpa2_only_eap and fiveg"
        """
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_config']
        if result:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config push to AP for ssid_wpa2_only_eap_passpoint_5g failed", body="")
        assert result
        result = push_ap_profile['ssid_wpa2_only_eap_passpoint_5g']['vif_state']
        if result:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_5g successful ", body="")
        else:
            allure.attach(name="Config apply to AP for ssid_wpa2_only_eap_passpoint_5g failed", body="")
        assert result

        print("SSID to download profile :: ", setup_params_eap["ssid_modes"]["open"][0]["ssid_name"])
        print("SSID to validate connectivity :: ", setup_params_eap["ssid_modes"]["wpa2_only_eap"][1]["ssid_name"])
        print("Profile download URL :: ", passpoint_profile_info["profile_download_url_ios"])
        print("Profile name to remove :: ", passpoint_profile_info["profile_name_on_device"])
