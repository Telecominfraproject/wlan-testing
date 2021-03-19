# """
# About: It contains some Functional Unit Tests for CloudSDK+APNOS and to run and test them on per unit level
# """
# import pytest
#
#
# # Note: Use Reusable Fixtures, Create SSID Profile, Equipment_AP Profile, Use RF Profile, Radius Profile,
# # Push and Verify
# @pytest.mark.test_apnos_profiles
# class TestProfiles(object):
#
#     @pytest.mark.test_apnos_open_ssid
#     def test_open_ssid(self):
#         # Write a Test case that creates Open ssid and pushes it to AP, and verifies that profile is applied properly
#         yield True
#
#     @pytest.mark.test_apnos_wpa_ssid
#     def test_wpa_ssid(self):
#         # Write a Test case that creates WPA ssid and pushes it to AP, and verifies that profile is applied properly
#         yield True
#
#     @pytest.mark.test_apnos_wpa2_personal_ssid
#     def test_wpa2_personal_ssid(self):
#         # Write a Test case that creates WPA2-PERSONAL ssid and pushes it to AP, and verifies that profile is applied
#         # properly
#         yield True
#
#     @pytest.mark.test_apnos_wpa2_enterprise_ssid
#     def test_wpa2_enterprise_ssid(self):
#         # Write a Test case that creates WPA2-ENTERPRISE ssid and pushes it to AP, and verifies that profile is
#         # applied properly
#         yield True
#
#     @pytest.mark.test_apnos_wpa3_personal_ssid
#     def test_wpa3_personal_ssid(self):
#         # Write a Test case that creates WPA3-PERSONAL ssid and pushes it to AP, and verifies that profile is applied
#         # properly
#         yield True
#
#     @pytest.mark.test_apnos_wpa3_enterprise_ssid
#     def test_wpa3_enterprise_ssid(self):
#         # Write a Test case that creates WPA3-ENTERPRISE ssid and pushes it to AP, and verifies that profile is
#         # applied properly
#         yield True
