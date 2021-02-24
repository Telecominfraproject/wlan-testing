#!/usr/bin/python3

##AP Models Under Test
ap_models = ["ecw5410"]

##Cloud Type(cloudSDK = v1)
cloud_type = "v1"
cloudSDK_url = "https://wlan-portal-svc-nola-04.cicd.lab.wlan.tip.build"
customer_id = "2"
cloud_user = "support@example.com"
cloud_password = "support"

# LANForge Info
lanforge_ip = "10.28.3.12"
lanforge_2dot4g = "wiphy4"
lanforge_5g = "wiphy5"
# For single client connectivity use cases, use full station name for prefix to only read traffic from client under test
lanforge_2dot4g_prefix = "test"
lanforge_5g_prefix = "test"
lanforge_2dot4g_station = "test1234"
lanforge_5g_station = "test1234"
# Used for bridge and NAT
lanforge_bridge_port = "eth2"
# VLAN interface on LANForge - must be configured to use alias of "vlan###" to accommodate sta_connect2 library
lanforge_vlan_port = "vlan100"
vlan = 100

##Equipment IDs for Lab APs under test
equipment_id_dict = {
    "ecw5410": "1",
}
# Equipment IPs for SSH or serial connection information
equipment_ip_dict = {
    "ecw5410": "/dev/ttyAP4"
}

equipment_credentials_dict = {
    "ecw5410": "openwifi",
}

##RADIUS Info
radius_info = {
    "server_ip": "10.28.3.100",
    "secret": "testing123",
    "auth_port": 1812,
    "eap_identity": "nolaradius",
    "eap_pwd": "nolastart"
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
        "ssid_list": [
            "ECW5410_5G_WPA2",
            "ECW5410_5G_WPA",
            "ECW5410_5G_WPA2-EAP",
            "ECW5410_2dot4G_WPA2",
            "ECW5410_2dot4G_WPA",
            "ECW5410_2dot4G_WPA2-EAP"
        ]
    },

    "ecw5410_nat": {
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
        "ssid_list": [
            "ECW5410_5G_WPA2_NAT",
            "ECW5410_5G_WPA_NAT",
            "ECW5410_5G_WPA2-EAP_NAT",
            "ECW5410_2dot4G_WPA2_NAT",
            "ECW5410_2dot4G_WPA_NAT",
            "ECW5410_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ecw5410_vlan": {
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
        "ssid_list": [
            "ECW5410_5G_WPA2_VLAN",
            "ECW5410_5G_WPA_VLAN",
            "ECW5410_5G_WPA2-EAP_VLAN",
            "ECW5410_2dot4G_WPA2_VLAN",
            "ECW5410_2dot4G_WPA_VLAN",
            "ECW5410_2dot4G_WPA2-EAP_VLAN"
        ]
    }
}