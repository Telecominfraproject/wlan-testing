import os
import datetime
from datetime import date
# Used to create SSID and AP profiles for throughput tests

import lab_ap_info
from lab_ap_info import profile_info_dict
import cloudsdk
from cloudsdk import CloudSDK

def main(fw_model, cloudSDK_url, cloud_type, customer_id):
    radius_profile = lab_ap_info.radius_profile
    rfProfileId = lab_ap_info.rf_profile
    ssid_template = "templates/ssid_profile_template.json"

    today = str(date.today())

    bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type)

    # Profile Dictionary
    profile_list = []
    ap_profiles = {}

    print(fw_model)
    # Bridge Profiles
    print("Bridge Profile Create")
    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_EAP_tput_'+today, customer_id,
                                             profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"], None,
                                             radius_profile,
                                             "wpa2OnlyRadius", "BRIDGE", 1,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G EAP:", fiveG_eap)
    profile_list.append(fiveG_eap)

    fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                              fw_model + '_5G_WPA2_tput_'+today, customer_id,
                                              profile_info_dict[fw_model]["fiveG_WPA2_SSID"],
                                              profile_info_dict[fw_model]["fiveG_WPA2_PSK"],
                                              0, "wpa2OnlyPSK", "BRIDGE", 1,
                                              ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA2:",fiveG_wpa2)
    profile_list.append(fiveG_wpa2)

    fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_WPA_tput_'+today, customer_id,
                                             profile_info_dict[fw_model]["fiveG_WPA_SSID"],
                                             profile_info_dict[fw_model]["fiveG_WPA_PSK"],
                                             0, "wpaPSK", "BRIDGE", 1,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA:", fiveG_wpa)
    profile_list.append(fiveG_wpa)

    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_EAP_tput_'+today, customer_id,
                                                profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"],
                                                None,
                                                radius_profile, "wpa2OnlyRadius", "BRIDGE", 1,
                                                ["is2dot4GHz"])
    print("2G EAP:", twoFourG_eap)
    profile_list.append(twoFourG_eap)
    twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                 fw_model + '_2G_WPA2_tput_'+today, customer_id,
                                                 profile_info_dict[fw_model]["twoFourG_WPA2_SSID"],
                                                 profile_info_dict[fw_model]["twoFourG_WPA2_PSK"],
                                                 0, "wpa2OnlyPSK", "BRIDGE", 1,
                                                 ["is2dot4GHz"])
    print("2G WPA2:", twoFourG_wpa2)
    profile_list.append(twoFourG_wpa2)

    twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_WPA_tput_'+today, customer_id,
                                                profile_info_dict[fw_model]["twoFourG_WPA_SSID"],
                                                profile_info_dict[fw_model]["twoFourG_WPA_PSK"],
                                                0, "wpaPSK", "BRIDGE", 1,
                                                ["is2dot4GHz"])
    print("2G WPA:", twoFourG_wpa)
    profile_list.append(twoFourG_wpa)

    child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa,
                      rfProfileId]
    print(child_profiles)

    ap_template = "templates/ap_profile_template.json"
    name = fw_model + " Automation_tput_"+today
    create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
    profile_list.append(create_ap_profile)
    ap_profiles["bridge_profile"] = create_ap_profile

    # NAT Profiles
    print("NAT Profile Create")
    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_EAP_NAT_tput_'+today, customer_id,
                                             profile_info_dict[fw_model + '_nat']["fiveG_WPA2-EAP_SSID"], None,
                                             radius_profile,
                                             "wpa2OnlyRadius", "NAT", 1,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G EAP:", fiveG_eap)
    profile_list.append(fiveG_eap)

    fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                              fw_model + '_5G_WPA2_NAT_tput_'+today, customer_id,
                                              profile_info_dict[fw_model + '_nat']["fiveG_WPA2_SSID"],
                                              profile_info_dict[fw_model + '_nat']["fiveG_WPA2_PSK"],
                                              0, "wpa2OnlyPSK", "NAT", 1,
                                              ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA2:", fiveG_wpa2)
    profile_list.append(fiveG_wpa2)

    fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_WPA_NAT_tput_'+today, customer_id,
                                             profile_info_dict[fw_model + '_nat']["fiveG_WPA_SSID"],
                                             profile_info_dict[fw_model + '_nat']["fiveG_WPA_PSK"],
                                             0, "wpaPSK", "NAT", 1,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA:", fiveG_wpa)
    profile_list.append(fiveG_wpa)

    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_EAP_NAT_tput_'+today, customer_id,
                                                profile_info_dict[fw_model + '_nat']["twoFourG_WPA2-EAP_SSID"],
                                                None,
                                                radius_profile, "wpa2OnlyRadius", "NAT", 1,
                                                ["is2dot4GHz"])
    print("2G EAP:", twoFourG_eap)
    profile_list.append(twoFourG_eap)

    twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                 fw_model + '_2G_WPA2_NAT_tput_'+today, customer_id,
                                                 profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"],
                                                 profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_PSK"],
                                                 0, "wpa2OnlyPSK", "NAT", 1,
                                                 ["is2dot4GHz"])
    print("2G WPA2:", twoFourG_wpa2)
    profile_list.append(twoFourG_wpa2)

    twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_WPA_NAT_tput_'+today, customer_id,
                                                profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"],
                                                profile_info_dict[fw_model + '_nat']["twoFourG_WPA_PSK"],
                                                0, "wpaPSK", "NAT", 1,
                                                ["is2dot4GHz"])
    print("2G WPA:", twoFourG_wpa)
    profile_list.append(twoFourG_wpa)

    child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa,
                      rfProfileId]
    print(child_profiles)

    ap_template = "templates/ap_profile_template.json"
    name = fw_model + " Automation_NAT_tput"+today
    create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
    ap_profiles["nat_profile"] = create_ap_profile

    # VLAN Profiles
    print("VLAN Profile Create")
    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_EAP_VLAN_tput_'+today, customer_id,
                                             profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_SSID"], None,
                                             radius_profile,
                                             "wpa2OnlyRadius", "BRIDGE", 100,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G EAP:", fiveG_eap)
    profile_list.append(fiveG_eap)

    fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                              fw_model + '_5G_WPA2_VLAN_tput_'+today, customer_id,
                                              profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"],
                                              profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_PSK"],
                                              0, "wpa2OnlyPSK", "BRIDGE", 100,
                                              ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA2:", fiveG_wpa2)
    profile_list.append(fiveG_wpa2)

    fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                             fw_model + '_5G_WPA_VLAN_tput_'+today, customer_id,
                                             profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"],
                                             profile_info_dict[fw_model + '_vlan']["fiveG_WPA_PSK"],
                                             0, "wpaPSK", "BRIDGE", 100,
                                             ["is5GHzU", "is5GHz", "is5GHzL"])
    print("5G WPA:", fiveG_wpa)
    profile_list.append(fiveG_wpa)

    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_EAP_VLAN_tput_'+today, customer_id,
                                                profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"],
                                                None,
                                                radius_profile, "wpa2OnlyRadius", "BRIDGE", 100,
                                                ["is2dot4GHz"])
    print("2G EAP:", twoFourG_eap)
    profile_list.append(twoFourG_eap)
    twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                 fw_model + '_2G_WPA2_VLAN_tput_'+today, customer_id,
                                                 profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"],
                                                 profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"],
                                                 0, "wpa2OnlyPSK", "BRIDGE", 100,
                                                 ["is2dot4GHz"])
    print("2G WPA2:", twoFourG_wpa2)
    profile_list.append(twoFourG_wpa2)

    twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                fw_model + '_2G_WPA_VLAN_tput_'+today, customer_id,
                                                profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"],
                                                profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"],
                                                0, "wpaPSK", "BRIDGE", 100,
                                                ["is2dot4GHz"])
    print("2G WPA:", twoFourG_wpa)
    profile_list.append(twoFourG_wpa)

    child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa,
                      rfProfileId]
    print(child_profiles)

    ap_template = "templates/ap_profile_template.json"
    name = fw_model + " Automation_VLAN_tput"+today
    create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
    profile_list.append(create_ap_profile)
    ap_profiles["vlan_profile"] = create_ap_profile

    return profile_list, ap_profiles
