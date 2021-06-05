# """
#     Performance : Wifi Capacity Test : VLAN Mode
#
# """
#
# import pytest
# import allure
#
# pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.vlan]
#
# setup_params_general = {
#     "mode": "VLAN",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
#              "security_key": "something"}]},
#     "rf": {},
#     "radius": False
# }
#
#
# @pytest.mark.basic
# @allure.feature("VLAN MODE CLIENT CONNECTIVITY")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# class TestWifiCapacityVLANMode(object):
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.twog
#     def test_client_wpa2_personal_2g(self, lf_test, station_names_twog, create_lanforge_chamberview_dut,
#                                      get_configuration):
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "twog"
#         vlan = 1
#         dut_name = create_lanforge_chamberview_dut
#         PASS = lf_test.wifi_capacity(ssid=profile_data["ssid_name"], paswd=profile_data["security_key"],
#                                      security="wpa2", mode="VLAN", band="twog",
#                                      instance_name="wct_instance", )
#         assert PASS
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     def test_client_wpa2_personal_2g(self, lf_test, station_names_twog, create_lanforge_chamberview_dut,
#                                      get_configuration):
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "fiveg"
#         vlan = 1
#         dut_name = create_lanforge_chamberview_dut
#         PASS = lf_test.wifi_capacity(ssid=profile_data["ssid_name"], paswd=profile_data["security_key"],
#                                      security=security, mode=mode, band=band,
#                                      instance_name="wct_instance", )
#         assert PASS
