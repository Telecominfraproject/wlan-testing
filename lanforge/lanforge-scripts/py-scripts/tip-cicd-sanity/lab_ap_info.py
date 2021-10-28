#!/usr/bin/python3

##AP Models Under Test
ap_models = ["ec420","ea8300","ecw5211","ecw5410", "wf188n", "wf194c", "ex227", "ex447", "eap101", "eap102"]

##Cloud Type(cloudSDK = v1, CMAP = cmap)
cloud_type = "v1"

##LANForge Info
lanforge_ip = "10.10.10.201"
lanforge_2dot4g = "wiphy6"
lanforge_5g = "wiphy6"
# For single client connectivity use cases, use full station name for prefix to only read traffic from client under test
lanforge_2dot4g_prefix = "wlan6"
lanforge_5g_prefix = "wlan6"
lanforge_2dot4g_station = "wlan6"
lanforge_5g_station = "wlan6"

##RADIUS Info
radius_info = {

    "name": "Automation_RADIUS",
    "subnet_name": "Lab",
    "subnet": "10.10.0.0",
    "subnet_mask": 16,
    "region": "Toronto",
    "server_name": "Lab-RADIUS",
    "server_ip": "10.10.10.203",
    "secret": "testing123",
    "auth_port": 1812
}
##AP Models for firmware upload
cloud_sdk_models = {
    "ec420": "EC420-G1",
    "ea8300": "EA8300-CA",
    "ecw5211": "ECW5211",
    "ecw5410": "ECW5410",
    "wf188n": "WF188N",
    "wf194c": "WF194C",
    "ex227": "EX227",
    "ex447": "EX447",
    "eap101": "EAP101",
    "eap102": "EAP102"
}

ap_spec = {
    "ec420": "wifi5",
    "ea8300": "wifi5",
    "ecw5211": "wifi5",
    "ecw5410": "wifi5",
    "wf188n": "wifi6",
    "wf194c": "wifi6",
    "ex227": "wifi6",
    "ex447": "wifi6",
    "eap101": "wifi6",
    "eap102": "wifi6"
}

mimo_5g = {
    "ec420": "4x4",
    "ea8300": "2x2",
    "ecw5211": "2x2",
    "ecw5410": "4x4",
    "wf188n": "2x2",
    "wf194c": "8x8",
    "ex227": "",
    "ex447": "",
    "eap101": "2x2",
    "eap102": "4x4"
}

mimo_2dot4g = {
    "ec420": "2x2",
    "ea8300": "2x2",
    "ecw5211": "2x2",
    "ecw5410": "4x4",
    "wf188n": "2x2",
    "wf194c": "4x4",
    "ex227": "",
    "ex447": "",
    "eap101": "2x2",
    "eap102": "4x4"
}

sanity_status = {
    "ea8300": "failed",
    "ecw5211": 'passed',
    "ecw5410": 'failed',
    "ec420": 'failed',
    "wf188n": "failed",
    "wf194c": "failed",
    "ex227": "failed",
    "ex447": "failed",
    "eap101": "failed",
    "eap102": "failed"
}

##Customer ID for testing
customer_id = "2"

##Equipment IDs for Lab APs under test
equipment_id_dict = {
    #"ea8300": "3",
    #"ecw5410": "5",
    "ecw5211": "22",
    #"ec420": "11",
    "wf188n": "14",
    "ex227": "18",
    "eap102": "7",
    "wf194c": "15"
}

equipment_ip_dict = {
    "ea8300": "10.10.10.103",
    "ecw5410": "10.10.10.105",
    "ec420": "10.10.10.104",
    "ecw5211": "10.10.10.187",
    "wf188n": "10.10.10.179",
    "wf194c": "10.10.10.184",
    "ex227": "10.10.10.185",
    "eap102": "10.10.10.186"
}

eqiupment_credentials_dict = {
    "ea8300": "openwifi",
    "ecw5410": "openwifi",
    "ec420": "openwifi",
    "ecw5211": "openwifi",
    "wf188n": "openwifi",
    "wf194c": "openwifi",
    "ex227": "openwifi",
    "ex447": "openwifi",
    "eap101": "openwifi",
    "eap102": "openwifi"
}

##Test Case information - Maps a generic TC name to TestRail TC numbers
test_cases = {
    "ap_upgrade": 2233,
    "5g_wpa2_bridge": 2236,
    "2g_wpa2_bridge": 2237,
    "5g_wpa_bridge": 2419,
    "2g_wpa_bridge": 2420,
    "2g_wpa_nat": 4323,
    "5g_wpa_nat": 4324,
    "2g_wpa2_nat": 4325,
    "5g_wpa2_nat": 4326,
    "2g_eap_bridge": 5214,
    "5g_eap_bridge": 5215,
    "2g_eap_nat": 5216,
    "5g_eap_nat": 5217,
    "cloud_connection": 5222,
    "cloud_fw": 5247,
    "5g_wpa2_vlan": 5248,
    "5g_wpa_vlan": 5249,
    "5g_eap_vlan": 5250,
    "2g_wpa2_vlan": 5251,
    "2g_wpa_vlan": 5252,
    "2g_eap_vlan": 5253,
    "cloud_ver": 5540,
    "bridge_vifc": 5541,
    "nat_vifc": 5542,
    "vlan_vifc": 5543,
    "bridge_vifs": 5544,
    "nat_vifs": 5545,
    "vlan_vifs": 5546,
    "upgrade_api": 5547,
    "create_fw": 5548,
    "ap_bridge": 5641,
    "ap_nat": 5642,
    "ap_vlan": 5643,
    "ssid_2g_eap_bridge": 5644,
    "ssid_2g_wpa2_bridge": 5645,
    "ssid_2g_wpa_bridge": 5646,
    "ssid_5g_eap_bridge": 5647,
    "ssid_5g_wpa2_bridge": 5648,
    "ssid_5g_wpa_bridge": 5649,
    "ssid_2g_eap_nat": 5650,
    "ssid_2g_wpa2_nat": 5651,
    "ssid_2g_wpa_nat": 5652,
    "ssid_5g_eap_nat": 5653,
    "ssid_5g_wpa2_nat": 5654,
    "ssid_5g_wpa_nat": 5655,
    "ssid_2g_eap_vlan": 5656,
    "ssid_2g_wpa2_vlan": 5657,
    "ssid_2g_wpa_vlan": 5658,
    "ssid_5g_eap_vlan": 5659,
    "ssid_5g_wpa2_vlan": 5660,
    "ssid_5g_wpa_vlan": 5661,
    "radius_profile": 5808,
    "bridge_ssid_update": 8742,
    "nat_ssid_update": 8743,
    "vlan_ssid_update": 8744
}

## Other profiles
radius_profile = 9
rf_profile_wifi5 = 10
rf_profile_wifi6 = 762

###Testing AP Profile Information
profile_info_dict = {
    "ecw5410": {
        "profile_id": "6",
        "childProfileIds": [
            3647,
            10,
            11,
            12,
            13,
            190,
            191
        ],
        "fiveG_WPA2_SSID": "ECW5410_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5410_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5410_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "ECW5410_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "ECW5410_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "ECW5410_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5410_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5410_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 3647,
        "fiveG_WPA_profile": 13,
        "fiveG_WPA2-EAP_profile": 191,
        "twoFourG_WPA2_profile": 11,
        "twoFourG_WPA_profile": 12,
        "twoFourG_WPA2-EAP_profile": 190,
        "ssid_list": [
            "ECW5410_5G_WPA2",
            "ECW5410_5G_WPA",
            "ECW5410_5G_WPA2-EAP",
            "ECW5410_2dot4G_WPA2",
            "ECW5410_2dot4G_WPA",
            "ECW5410_2dot4G_WPA2-EAP"
        ]
    },

    "ea8300": {
        "profile_id": "6",
        "childProfileIds": [
            17,
            18,
            201,
            202,
            10,
            14,
            15
        ],
        "fiveG_WPA2_SSID": "EA8300_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EA8300_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EA8300_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EA8300_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EA8300_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EA8300_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EA8300_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EA8300_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 14,
        "fiveG_WPA_profile": 15,
        "fiveG_WPA2-EAP_profile": 202,
        "twoFourG_WPA2_profile": 17,
        "twoFourG_WPA_profile": 18,
        "twoFourG_WPA2-EAP_profile": 201,
        # EA8300 has 2x 5GHz SSIDs because it is a tri-radio AP!
        "ssid_list": [
            "EA8300_5G_WPA2",
            "EA8300_5G_WPA2",
            "EA8300_5G_WPA",
            "EA8300_5G_WPA",
            "EA8300_5G_WPA2-EAP",
            "EA8300_5G_WPA2-EAP",
            "EA8300_2dot4G_WPA2",
            "EA8300_2dot4G_WPA",
            "EA8300_2dot4G_WPA2-EAP"
        ]
    },

    "ec420": {
        "profile_id": "6",
        "childProfileIds": [
            209,
            210,
            21,
            22,
            24,
            25,
            10
        ],
        "fiveG_WPA2_SSID": "EC420_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EC420_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EC420_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EC420_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EC420_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EC420_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EC420_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EC420_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 21,
        "fiveG_WPA_profile": 22,
        "fiveG_WPA2-EAP_profile": 210,
        "twoFourG_WPA2_profile": 24,
        "twoFourG_WPA_profile": 25,
        "twoFourG_WPA2-EAP_profile": 209,
        "ssid_list": [
            "EC420_5G_WPA2",
            "EC420_5G_WPA",
            "EC420_5G_WPA2-EAP",
            "EC420_2dot4G_WPA2",
            "EC420_2dot4G_WPA",
            "EC420_2dot4G_WPA2-EAP"
        ]
    },

    "ecw5211": {
        "profile_id": "6",
        "childProfileIds": [
            32,
            10,
            28,
            29,
            205,
            206,
            31
        ],
        "fiveG_WPA2_SSID": "ECW5211_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5211_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5211_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "ECW5211_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "ECW5211_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "ECW5211_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5211_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5211_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 28,
        "fiveG_WPA_profile": 29,
        "fiveG_WPA2-EAP_profile": 206,
        "twoFourG_WPA2_profile": 31,
        "twoFourG_WPA_profile": 32,
        "twoFourG_WPA2-EAP_profile": 205,
        "ssid_list": [
            "ECW5211_5G_WPA2",
            "ECW5211_5G_WPA",
            "ECW5211_5G_WPA2-EAP",
            "ECW5211_2dot4G_WPA2",
            "ECW5211_2dot4G_WPA",
            "ECW5211_2dot4G_WPA2-EAP"
        ]
    },

    "wf188n": {
        "profile_id": "6",
        "childProfileIds": [
            3718,
            3719,
            3720,
            3721,
            3722,
            3723,
            10
        ],
        "fiveG_WPA2_SSID": "WF188N_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF188N_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF188N_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "WF188N_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "WF188N_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "WF188N_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF188N_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF188N_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 3719,
        "fiveG_WPA_profile": 3720,
        "fiveG_WPA2-EAP_profile": 3718,
        "twoFourG_WPA2_profile": 3722,
        "twoFourG_WPA_profile": 3723,
        "twoFourG_WPA2-EAP_profile": 3721,
        "ssid_list": [
            "WF188N_5G_WPA2",
            "WF188N_5G_WPA",
            "WF188N_5G_WPA2-EAP",
            "WF188N_2dot4G_WPA2",
            "WF188N_2dot4G_WPA",
            "WF188N_2dot4G_WPA2-EAP"
        ]
    },

    "wf194c": {
        "profile_id": "6",
        "childProfileIds": [
            4307,
            4308,
            4309,
            4310,
            4311,
            4312,
            10
        ],
        "fiveG_WPA2_SSID": "WF194C_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF194C_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF194C_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "WF194C_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "WF194C_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "WF194C_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF194C_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF194C_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 4308,
        "fiveG_WPA_profile": 4307,
        "fiveG_WPA2-EAP_profile": 4309,
        "twoFourG_WPA2_profile": 4311,
        "twoFourG_WPA_profile": 4310,
        "twoFourG_WPA2-EAP_profile": 4312,
        "ssid_list": [
            "WF194C_5G_WPA2",
            "WF194C_5G_WPA",
            "WF194C_5G_WPA2-EAP",
            "WF194C_2dot4G_WPA2",
            "WF194C_2dot4G_WPA",
            "WF194C_2dot4G_WPA2-EAP"
        ]
    },

    "ex227": {
        "profile_id": "6",
        "childProfileIds": [
            4958,
            4959,
            4960,
            4961,
            4962,
            4963,
            10
        ],
        "fiveG_WPA2_SSID": "EX227_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX227_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX227_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EX227_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EX227_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EX227_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX227_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX227_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 4959,
        "fiveG_WPA_profile": 4960,
        "fiveG_WPA2-EAP_profile": 4958,
        "twoFourG_WPA2_profile": 4962,
        "twoFourG_WPA_profile": 4963,
        "twoFourG_WPA2-EAP_profile": 4961,
        "ssid_list": [
            "EX227_5G_WPA2",
            "EX227_5G_WPA",
            "EX227_5G_WPA2-EAP",
            "EX227_2dot4G_WPA2",
            "EX227_2dot4G_WPA",
            "EX227_2dot4G_WPA2-EAP"
        ]
    },

    "ex447": {
        "profile_id": "6",
        "childProfileIds": [
            5002,
            5003,
            5004,
            5005,
            5006,
            5007,
            10
        ],
        "fiveG_WPA2_SSID": "EX447_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX447_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX447_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EX447_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EX447_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EX447_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX447_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX447_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 5003,
        "fiveG_WPA_profile": 5004,
        "fiveG_WPA2-EAP_profile": 5002,
        "twoFourG_WPA2_profile": 5006,
        "twoFourG_WPA_profile": 5007,
        "twoFourG_WPA2-EAP_profile": 5005,
        "ssid_list": [
            "EX447_5G_WPA2",
            "EX447_5G_WPA",
            "EX447_5G_WPA2-EAP",
            "EX447_2dot4G_WPA2",
            "EX447_2dot4G_WPA",
            "EX447_2dot4G_WPA2-EAP"
        ]
    },

    "eap101": {
        "profile_id": "6",
        "childProfileIds": [
            5023,
            5024,
            5025,
            5026,
            5027,
            5028,
            10
        ],
        "fiveG_WPA2_SSID": "EAP101_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP101_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP101_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EAP101_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EAP101_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EAP101_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP101_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP101_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 5024,
        "fiveG_WPA_profile": 5025,
        "fiveG_WPA2-EAP_profile": 5023,
        "twoFourG_WPA2_profile": 5027,
        "twoFourG_WPA_profile": 5028,
        "twoFourG_WPA2-EAP_profile": 5026,
        "ssid_list": [
            "EAP101_5G_WPA2",
            "EAP101_5G_WPA",
            "EAP101_5G_WPA2-EAP",
            "EAP101_2dot4G_WPA2",
            "EAP101_2dot4G_WPA",
            "EAP101_2dot4G_WPA2-EAP"
        ]
    },

    "eap102": {
        "profile_id": "6",
        "childProfileIds": [
            5044,
            5045,
            5046,
            5057,
            5048,
            5049,
            10
        ],
        "fiveG_WPA2_SSID": "EAP102_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP102_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP102_5G_OPEN",
        "fiveG_WPA2-EAP_SSID": "EAP102_5G_WPA2-EAP",
        "twoFourG_OPEN_SSID": "EAP102_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EAP102_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP102_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP102_2dot4G_WPA2-EAP",
        "fiveG_WPA2_profile": 5045,
        "fiveG_WPA_profile": 5046,
        "fiveG_WPA2-EAP_profile": 5044,
        "twoFourG_WPA2_profile": 5048,
        "twoFourG_WPA_profile": 5049,
        "twoFourG_WPA2-EAP_profile": 5047,
        "ssid_list": [
            "EAP102_5G_WPA2",
            "EAP102_5G_WPA",
            "EAP102_5G_WPA2-EAP",
            "EAP102_2dot4G_WPA2",
            "EAP102_2dot4G_WPA",
            "EAP102_2dot4G_WPA2-EAP"
        ]
    },

    "ecw5410_nat": {
        "profile_id": "68",
        "childProfileIds": [
            192,
            81,
            193,
            82,
            10,
            78,
            79
        ],
        "fiveG_WPA2_SSID": "ECW5410_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5410_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5410_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "ECW5410_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "ECW5410_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "ECW5410_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5410_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5410_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 78,
        "fiveG_WPA_profile": 79,
        "fiveG_WPA2-EAP_profile": 192,
        "twoFourG_WPA2_profile": 81,
        "twoFourG_WPA_profile": 82,
        "twoFourG_WPA2-EAP_profile": 193,
        "ssid_list": [
            "ECW5410_5G_WPA2_NAT",
            "ECW5410_5G_WPA_NAT",
            "ECW5410_5G_WPA2-EAP_NAT",
            "ECW5410_2dot4G_WPA2_NAT",
            "ECW5410_2dot4G_WPA_NAT",
            "ECW5410_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ea8300_nat": {
        "profile_id": "67",
        "childProfileIds": [
            72,
            73,
            10,
            75,
            203,
            76,
            204
        ],
        "fiveG_WPA2_SSID": "EA8300_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EA8300_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EA8300_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EA8300_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EA8300_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EA8300_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EA8300_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EA8300_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 72,
        "fiveG_WPA_profile": 73,
        "fiveG_WPA2-EAP_profile": 203,
        "twoFourG_WPA2_profile": 75,
        "twoFourG_WPA_profile": 76,
        "twoFourG_WPA2-EAP_profile": 204,
        # EA8300 has 2x 5GHz SSIDs because it is a tri-radio AP!
        "ssid_list": [
            "EA8300_5G_WPA2_NAT",
            "EA8300_5G_WPA2_NAT",
            "EA8300_5G_WPA_NAT",
            "EA8300_5G_WPA_NAT",
            "EA8300_5G_WPA2-EAP_NAT",
            "EA8300_5G_WPA2-EAP_NAT",
            "EA8300_2dot4G_WPA2_NAT",
            "EA8300_2dot4G_WPA_NAT",
            "EA8300_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ec420_nat": {
        "profile_id": "70",
        "childProfileIds": [
            211,
            212,
            90,
            10,
            91,
            93,
            94
        ],
        "fiveG_WPA2_SSID": "EC420_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EC420_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EC420_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EC420_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EC420_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EC420_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EC420_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EC420_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 90,
        "fiveG_WPA_profile": 91,
        "fiveG_WPA2-EAP_profile": 211,
        "twoFourG_WPA2_profile": 93,
        "twoFourG_WPA_profile": 94,
        "twoFourG_WPA2-EAP_profile": 212,
        "ssid_list": [
            "EC420_5G_WPA2_NAT",
            "EC420_5G_WPA_NAT",
            "EC420_5G_WPA2-EAP_NAT",
            "EC420_2dot4G_WPA2_NAT",
            "EC420_2dot4G_WPA_NAT",
            "EC420_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ecw5211_nat": {
        "profile_id": "69",
        "childProfileIds": [
            208,
            84,
            85,
            87,
            88,
            10,
            207
        ],
        "fiveG_WPA2_SSID": "ECW5211_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5211_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5211_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "ECW5211_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "ECW5211_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "ECW5211_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5211_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5211_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 84,
        "fiveG_WPA_profile": 85,
        "fiveG_WPA2-EAP_profile": 207,
        "twoFourG_WPA2_profile": 87,
        "twoFourG_WPA_profile": 88,
        "twoFourG_WPA2-EAP_profile": 208,
        "ssid_list": [
            "ECW5211_5G_WPA2_NAT",
            "ECW5211_5G_WPA_NAT",
            "ECW5211_5G_WPA2-EAP_NAT",
            "ECW5211_2dot4G_WPA2_NAT",
            "ECW5211_2dot4G_WPA_NAT",
            "ECW5211_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "wf188n_nat": {
        "profile_id": "3732",
        "childProfileIds": [
            3728,
            3729,
            3730,
            3731,
            10,
            3726,
            3727
        ],
        "fiveG_WPA2_SSID": "WF188N_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF188N_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF188N_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "WF188N_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "WF188N_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "WF188N_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF188N_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF188N_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 3727,
        "fiveG_WPA_profile": 3728,
        "fiveG_WPA2-EAP_profile": 3726,
        "twoFourG_WPA2_profile": 3730,
        "twoFourG_WPA_profile": 3731,
        "twoFourG_WPA2-EAP_profile": 3729,
        "ssid_list": [
            "WF188N_5G_WPA2_NAT",
            "WF188N_5G_WPA_NAT",
            "WF188N_5G_WPA2-EAP_NAT",
            "WF188N_2dot4G_WPA2_NAT",
            "WF188N_2dot4G_WPA_NAT",
            "WF188N_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "wf194c_nat": {
        "profile_id": "4416",
        "childProfileIds": [
            4410,
            4411,
            4412,
            4413,
            10,
            4414,
            4415
        ],
        "fiveG_WPA2_SSID": "WF194C_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF194C_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF194C_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "WF194C_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "WF194C_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "WF194C_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF194C_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF194C_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 4411,
        "fiveG_WPA_profile": 4412,
        "fiveG_WPA2-EAP_profile": 4410,
        "twoFourG_WPA2_profile": 4414,
        "twoFourG_WPA_profile": 4415,
        "twoFourG_WPA2-EAP_profile": 4413,
        "ssid_list": [
            "WF194C_5G_WPA2_NAT",
            "WF194C_5G_WPA_NAT",
            "WF194C_5G_WPA2-EAP_NAT",
            "WF194C_2dot4G_WPA2_NAT",
            "WF194C_2dot4G_WPA_NAT",
            "WF194C_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ex227_nat": {
        "profile_id": "4971",
        "childProfileIds": [
            4965,
            4966,
            4967,
            4968,
            10,
            4969,
            4970
        ],
        "fiveG_WPA2_SSID": "EX227_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX227_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX227_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EX227_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EX227_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EX227_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX227_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX227_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 4966,
        "fiveG_WPA_profile": 4967,
        "fiveG_WPA2-EAP_profile": 4965,
        "twoFourG_WPA2_profile": 4969,
        "twoFourG_WPA_profile": 4970,
        "twoFourG_WPA2-EAP_profile": 4968,
        "ssid_list": [
            "EX227_5G_WPA2_NAT",
            "EX227_5G_WPA_NAT",
            "EX227_5G_WPA2-EAP_NAT",
            "EX227_2dot4G_WPA2_NAT",
            "EX227_2dot4G_WPA_NAT",
            "EX227_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ex447_nat": {
        "profile_id": "5015",
        "childProfileIds": [
            5009,
            5010,
            5011,
            5012,
            10,
            5013,
            5014
        ],
        "fiveG_WPA2_SSID": "EX447_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX447_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX447_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EX447_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EX447_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EX447_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX447_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX447_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 5010,
        "fiveG_WPA_profile": 5011,
        "fiveG_WPA2-EAP_profile": 5009,
        "twoFourG_WPA2_profile": 5013,
        "twoFourG_WPA_profile": 5014,
        "twoFourG_WPA2-EAP_profile": 5012,
        "ssid_list": [
            "EX447_5G_WPA2_NAT",
            "EX447_5G_WPA_NAT",
            "EX447_5G_WPA2-EAP_NAT",
            "EX447_2dot4G_WPA2_NAT",
            "EX447_2dot4G_WPA_NAT",
            "EX447_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "eap102_nat": {
        "profile_id": "5057",
        "childProfileIds": [
            5051,
            5052,
            5053,
            5054,
            10,
            5055,
            5056
        ],
        "fiveG_WPA2_SSID": "EAP102_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP102_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP102_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EAP102_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EAP102_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EAP102_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP102_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP102_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 5052,
        "fiveG_WPA_profile": 5053,
        "fiveG_WPA2-EAP_profile": 5051,
        "twoFourG_WPA2_profile": 5055,
        "twoFourG_WPA_profile": 5056,
        "twoFourG_WPA2-EAP_profile": 5054,
        "ssid_list": [
            "EAP102_5G_WPA2_NAT",
            "EAP102_5G_WPA_NAT",
            "EAP102_5G_WPA2-EAP_NAT",
            "EAP102_2dot4G_WPA2_NAT",
            "EAP102_2dot4G_WPA_NAT",
            "EAP102_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "eap101_nat": {
        "profile_id": "5036",
        "childProfileIds": [
            5030,
            5031,
            5032,
            5033,
            10,
            5034,
            5035
        ],
        "fiveG_WPA2_SSID": "EAP101_5G_WPA2_NAT",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP101_5G_WPA_NAT",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP101_5G_OPEN_NAT",
        "fiveG_WPA2-EAP_SSID": "EAP101_5G_WPA2-EAP_NAT",
        "twoFourG_OPEN_SSID": "EAP101_2dot4G_OPEN_NAT",
        "twoFourG_WPA2_SSID": "EAP101_2dot4G_WPA2_NAT",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP101_2dot4G_WPA_NAT",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP101_2dot4G_WPA2-EAP_NAT",
        "fiveG_WPA2_profile": 5031,
        "fiveG_WPA_profile": 5032,
        "fiveG_WPA2-EAP_profile": 5030,
        "twoFourG_WPA2_profile": 5034,
        "twoFourG_WPA_profile": 5035,
        "twoFourG_WPA2-EAP_profile": 5033,
        "ssid_list": [
            "EAP101_5G_WPA2_NAT",
            "EAP101_5G_WPA_NAT",
            "EAP101_5G_WPA2-EAP_NAT",
            "EAP101_2dot4G_WPA2_NAT",
            "EAP101_2dot4G_WPA_NAT",
            "EAP101_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ecw5410_vlan": {
        "profile_id": "338",
        "childProfileIds": [
            336,
            320,
            337,
            10,
            333,
            334,
            335
        ],
        "fiveG_WPA2_SSID": "ECW5410_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5410_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5410_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "ECW5410_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "ECW5410_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "ECW5410_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5410_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5410_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 320,
        "fiveG_WPA_profile": 333,
        "fiveG_WPA2-EAP_profile": 337,
        "twoFourG_WPA2_profile": 334,
        "twoFourG_WPA_profile": 335,
        "twoFourG_WPA2-EAP_profile": 336,
        "ssid_list": [
            "ECW5410_5G_WPA2_VLAN",
            "ECW5410_5G_WPA_VLAN",
            "ECW5410_5G_WPA2-EAP_VLAN",
            "ECW5410_2dot4G_WPA2_VLAN",
            "ECW5410_2dot4G_WPA_VLAN",
            "ECW5410_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "ea8300_vlan": {
        "profile_id": "319",
        "childProfileIds": [
            313,
            10,
            314,
            315,
            316,
            317,
            318
        ],
        "fiveG_WPA2_SSID": "EA8300_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EA8300_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EA8300_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EA8300_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EA8300_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EA8300_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EA8300_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EA8300_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 313,
        "fiveG_WPA_profile": 314,
        "fiveG_WPA2-EAP_profile": 318,
        "twoFourG_WPA2_profile": 315,
        "twoFourG_WPA_profile": 316,
        "twoFourG_WPA2-EAP_profile": 317,
        # EA8300 has 2x 5GHz SSIDs because it is a tri-radio AP!
        "ssid_list": [
            "EA8300_5G_WPA2_VLAN",
            "EA8300_5G_WPA2_VLAN",
            "EA8300_5G_WPA_VLAN",
            "EA8300_5G_WPA_VLAN",
            "EA8300_5G_WPA2-EAP_VLAN",
            "EA8300_5G_WPA2-EAP_VLAN",
            "EA8300_2dot4G_WPA2_VLAN",
            "EA8300_2dot4G_WPA_VLAN",
            "EA8300_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "ec420_vlan": {
        "profile_id": "357",
        "childProfileIds": [
            352,
            353,
            354,
            355,
            356,
            10,
            351
        ],
        "fiveG_WPA2_SSID": "EC420_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EC420_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EC420_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EC420_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EC420_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EC420_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EC420_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EC420_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 351,
        "fiveG_WPA_profile": 352,
        "fiveG_WPA2-EAP_profile": 356,
        "twoFourG_WPA2_profile": 353,
        "twoFourG_WPA_profile": 354,
        "twoFourG_WPA2-EAP_profile": 355,
        "ssid_list": [
            "EC420_5G_WPA2_VLAN",
            "EC420_5G_WPA_VLAN",
            "EC420_5G_WPA2-EAP_VLAN",
            "EC420_2dot4G_WPA2_VLAN",
            "EC420_2dot4G_WPA_VLAN",
            "EC420_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "ecw5211_vlan": {
        "profile_id": "364",
        "childProfileIds": [
            358,
            359,
            360,
            361,
            10,
            362,
            363
        ],
        "fiveG_WPA2_SSID": "ECW5211_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5211_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5211_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "ECW5211_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "ECW5211_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "ECW5211_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "ECW5211_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "ECW5211_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 358,
        "fiveG_WPA_profile": 359,
        "fiveG_WPA2-EAP_profile": 363,
        "twoFourG_WPA2_profile": 360,
        "twoFourG_WPA_profile": 361,
        "twoFourG_WPA2-EAP_profile": 362,
        "ssid_list": [
            "ECW5211_5G_WPA2_VLAN",
            "ECW5211_5G_WPA_VLAN",
            "ECW5211_5G_WPA2-EAP_VLAN",
            "ECW5211_2dot4G_WPA2_VLAN",
            "ECW5211_2dot4G_WPA_VLAN",
            "ECW5211_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "wf188n_vlan": {
        "profile_id": "3740",
        "childProfileIds": [
            3734,
            3735,
            3736,
            3737,
            3738,
            10,
            3739
        ],
        "fiveG_WPA2_SSID": "WF188N_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF188N_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF188N_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "WF188N_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "WF188N_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "WF188N_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF188N_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF188N_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 3738,
        "fiveG_WPA_profile": 3739,
        "fiveG_WPA2-EAP_profile": 3737,
        "twoFourG_WPA2_profile": 3722,
        "twoFourG_WPA_profile": 3723,
        "twoFourG_WPA2-EAP_profile": 3721,
        "ssid_list": [
            "WF188N_5G_WPA2_VLAN",
            "WF188N_5G_WPA_VLAN",
            "WF188N_5G_WPA2-EAP_VLAN",
            "WF188N_2dot4G_WPA2_VLAN",
            "WF188N_2dot4G_WPA_VLAN",
            "WF188N_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "wf194c_vlan": {
        "profile_id": "4429",
        "childProfileIds": [
            4423,
            4424,
            4425,
            4426,
            4427,
            10,
            4428
        ],
        "fiveG_WPA2_SSID": "WF194C_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "WF194C_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "WF194C_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "WF194C_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "WF194C_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "WF194C_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "WF194C_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "WF194C_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 4424,
        "fiveG_WPA_profile": 4425,
        "fiveG_WPA2-EAP_profile": 4423,
        "twoFourG_WPA2_profile": 4427,
        "twoFourG_WPA_profile": 4428,
        "twoFourG_WPA2-EAP_profile": 4426,
        "ssid_list": [
            "WF194C_5G_WPA2_VLAN",
            "WF194C_5G_WPA_VLAN",
            "WF194C_5G_WPA2-EAP_VLAN",
            "WF194C_2dot4G_WPA2_VLAN",
            "WF194C_2dot4G_WPA_VLAN",
            "WF194C_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "ex227_vlan": {
        "profile_id": "4978",
        "childProfileIds": [
            4972,
            4973,
            4974,
            4975,
            4976,
            10,
            4977
        ],
        "fiveG_WPA2_SSID": "EX227_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX227_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX227_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EX227_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EX227_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EX227_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX227_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX227_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 4973,
        "fiveG_WPA_profile": 4974,
        "fiveG_WPA2-EAP_profile": 4972,
        "twoFourG_WPA2_profile": 4976,
        "twoFourG_WPA_profile": 4977,
        "twoFourG_WPA2-EAP_profile": 4975,
        "ssid_list": [
            "EX227_5G_WPA2_VLAN",
            "EX227_5G_WPA_VLAN",
            "EX227_5G_WPA2-EAP_VLAN",
            "EX227_2dot4G_WPA2_VLAN",
            "EX227_2dot4G_WPA_VLAN",
            "EX227_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "ex447_vlan": {
        "profile_id": "5022",
        "childProfileIds": [
            5016,
            5017,
            5018,
            5019,
            5020,
            10,
            5021
        ],
        "fiveG_WPA2_SSID": "EX447_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EX447_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EX447_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EX447_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EX447_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EX447_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EX447_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EX447_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 4973,
        "fiveG_WPA_profile": 4974,
        "fiveG_WPA2-EAP_profile": 4972,
        "twoFourG_WPA2_profile": 4976,
        "twoFourG_WPA_profile": 4977,
        "twoFourG_WPA2-EAP_profile": 4975,
        "ssid_list": [
            "EX447_5G_WPA2_VLAN",
            "EX447_5G_WPA_VLAN",
            "EX447_5G_WPA2-EAP_VLAN",
            "EX447_2dot4G_WPA2_VLAN",
            "EX447_2dot4G_WPA_VLAN",
            "EX447_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "eap101_vlan": {
        "profile_id": "5043",
        "childProfileIds": [
            5037,
            5038,
            5039,
            5040,
            5041,
            10,
            5042
        ],
        "fiveG_WPA2_SSID": "EAP101_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP101_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP101_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EAP101_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EAP101_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EAP101_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP101_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP101_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 5038,
        "fiveG_WPA_profile": 5039,
        "fiveG_WPA2-EAP_profile": 5037,
        "twoFourG_WPA2_profile": 5041,
        "twoFourG_WPA_profile": 5042,
        "twoFourG_WPA2-EAP_profile": 5040,
        "ssid_list": [
            "EAP101_5G_WPA2_VLAN",
            "EAP101_5G_WPA_VLAN",
            "EAP101_5G_WPA2-EAP_VLAN",
            "EAP101_2dot4G_WPA2_VLAN",
            "EAP101_2dot4G_WPA_VLAN",
            "EAP101_2dot4G_WPA2-EAP_VLAN"
        ]
    },

    "eap102_vlan": {
        "profile_id": "5064",
        "childProfileIds": [
            5058,
            5059,
            5060,
            5061,
            5062,
            10,
            5063
        ],
        "fiveG_WPA2_SSID": "EAP102_5G_WPA2_VLAN",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EAP102_5G_WPA_VLAN",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EAP102_5G_OPEN_VLAN",
        "fiveG_WPA2-EAP_SSID": "EAP102_5G_WPA2-EAP_VLAN",
        "twoFourG_OPEN_SSID": "EAP102_2dot4G_OPEN_VLAN",
        "twoFourG_WPA2_SSID": "EAP102_2dot4G_WPA2_VLAN",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID": "EAP102_2dot4G_WPA_VLAN",
        "twoFourG_WPA_PSK": "Connectus123$",
        "twoFourG_WPA2-EAP_SSID": "EAP102_2dot4G_WPA2-EAP_VLAN",
        "fiveG_WPA2_profile": 5059,
        "fiveG_WPA_profile": 5060,
        "fiveG_WPA2-EAP_profile": 5058,
        "twoFourG_WPA2_profile": 5060,
        "twoFourG_WPA_profile": 5061,
        "twoFourG_WPA2-EAP_profile": 5059,
        "ssid_list": [
            "EAP102_5G_WPA2_VLAN",
            "EAP102_5G_WPA_VLAN",
            "EAP102_5G_WPA2-EAP_VLAN",
            "EAP102_2dot4G_WPA2_VLAN",
            "EAP102_2dot4G_WPA_VLAN",
            "EAP102_2dot4G_WPA2-EAP_VLAN"
        ]
    },
}
