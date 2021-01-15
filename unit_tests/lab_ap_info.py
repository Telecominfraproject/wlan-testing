#!/usr/bin/python3

##AP Models Under Test
ap_models = ["ec420","ea8300","ecw5211","ecw5410"]

##Cloud Type(cloudSDK = v1, CMAP = cmap)
cloud_type = "v1"

##LANForge Info
lanforge_ip = "10.10.10.201"
lanforge_2dot4g = "wiphy0"
lanforge_5g = "wiphy3"
lanforge_prefix = "sdk"

##RADIUS Info
radius_info = {

    "name": "Lab-RADIUS",
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
    "ecw5410": "ECW5410"
}

mimo_5g = {
    "ec420": "4x4",
    "ea8300": "2x2",
    "ecw5211": "2x2",
    "ecw5410": "4x4"
}

mimo_2dot4g = {
    "ec420": "2x2",
    "ea8300": "2x2",
    "ecw5211": "2x2",
    "ecw5410": "4x4"
}

sanity_status = {
    "ea8300": "failed",
    "ecw5211": 'passed',
    "ecw5410": 'failed',
    "ec420": 'failed'
}

##Customer ID for testing
customer_id = "2"

##Equipment IDs for Lab APs under test
equipment_id_dict = {
    "ea8300": "19",
    "ecw5410": "20",
    "ecw5211": "21",
    "ec420": "27"
}

equipment_ip_dict = {
    "ea8300": "10.10.10.103",
    "ecw5410": "10.10.10.105",
    "ec420": "10.10.10.104",
    "ecw5211": "10.10.10.102"
}

eqiupment_credentials_dict = {
    "ea8300": "openwifi",
    "ecw5410": "openwifi",
    "ec420": "openwifi",
    "ecw5211": "admin123"
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
    "radius_profile": 5808
}

## Other profiles
radius_profile = 129
rf_profile = 10

###Testing AP Profile Information
profile_info_dict = {
    "ecw5410": {
        "profile_id": "2",
        "childProfileIds": [
            129,
            3,
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
        "fiveG_WPA2_profile": 3,
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
        "profile_id": "153",
        "childProfileIds": [
            17,
            129,
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
        "profile_id": "20",
        "childProfileIds": [
            129,
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
        "profile_id": "27",
        "childProfileIds": [
            32,
            129,
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

    "ecw5410_nat": {
        "profile_id": "68",
        "childProfileIds": [
            192,
            129,
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
            129,
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
            129,
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
            129,
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

    "ecw5410_vlan": {
        "profile_id": "338",
        "childProfileIds": [
            336,
            320,
            129,
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
            129,
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
            129,
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
            129,
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
    }
}
