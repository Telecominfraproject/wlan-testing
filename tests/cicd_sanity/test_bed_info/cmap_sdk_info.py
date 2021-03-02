#!/usr/bin/python3

##AP Models Under Test
ap_models = ["ecw5211", 'ecw5410', 'eap102', 'wf188n']

##Cloud Type(cloudSDK = v1)
cloud_type = "cmap"
cloudSDK_url = "https://cmap-portal-svc.rtl.lab.netexperience.com"
customer_id = "2"
cloud_user = "lucas.rahn@netexperience.com"
cloud_password = "Lucas0609"
#Testrail info
tr_url = 'https://connectus.testrail.com'
tr_prefix = 'RTL_Sanity_'
tr_user = 'syama.devi@connectus.ai'
tr_pass = 'Connect123$'
tr_project_id = 'CMAP'
milestone = '5'
#AP Upgrade
ap_user = 'root'
jfrog_user = 'tip-read'
jfrog_pass = 'tip-read'
#Directory Paths
sanity_log_dir = 'logs/'
sanity_report_dir = 'reports/'
report_template = 'reports/report_template.php'
deletion_file = 'templates/delete_profile_list.json'

##LANForge Info
lanforge_ip = "10.10.10.201"
lanforge_2dot4g = "wiphy2"
lanforge_5g = "wiphy1"
# For single client connectivity use cases, use full station name for prefix to only read traffic from client under test
lanforge_2dot4g_prefix = "test"
lanforge_5g_prefix = "test"
lanforge_2dot4g_station = "test1235"
lanforge_5g_station = "test1235"
lanforge_bridge_port = "eth2"
# VLAN interface on LANForge - must be configured to use alias of "vlan###" to accommodate sta_connect2 library
lanforge_vlan_port = "vlan100"
vlan = 100

# Equipment IDs for Lab APs under test - for test to loop through multiple APs put additional keys in the dictionary
equipment_id_dict = {
    "ecw5211": '5',
    'ecw5410': '6',
    'eap102': '11',
    'wf188n': '10'
}
# Equipment IPs for SSH or serial connection information
equipment_ip_dict = {
    "ecw5211": "10.10.10.181",
    'ecw5410': '10.10.10.180',
    'eap102': '10.10.10.186',
    'wf188n': '10.10.10.179'
}

equipment_credentials_dict = {
    "ecw5211": "openwifi",
    'ecw5410': 'openwifi',
    'wf188n': 'openwifi',
    'eap102': 'openwifi'
}

##RADIUS Info
radius_info = {
    "server_ip": "10.10.10.203",
    "secret": "testing123",
    "auth_port": 1812,
    "eap_identity": "testing",
    "eap_pwd": "admin123"
}

## Other profiles
radius_profile = 9  # used as backup
rf_profile_wifi5 = 10
rf_profile_wifi6 = 762

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
    "ap_upgrade": 866,
    "5g_wpa2_bridge": 869,
    "2g_wpa2_bridge": 870,
    "5g_wpa_bridge": 871,
    "2g_wpa_bridge": 872,
    "2g_wpa_nat": 880,
    "5g_wpa_nat": 881,
    "2g_wpa2_nat": 882,
    "5g_wpa2_nat": 883,
    "2g_eap_bridge": 888,
    "5g_eap_bridge": 889,
    "2g_eap_nat": 890,
    "5g_eap_nat": 891,
    "cloud_connection": 905,
    "cloud_fw": 904,
    "5g_wpa2_vlan": 892,
    "5g_wpa_vlan": 893,
    "5g_eap_vlan": 894,
    "2g_wpa2_vlan": 895,
    "2g_wpa_vlan": 896,
    "2g_eap_vlan": 897,
    "cloud_ver": 901,
    "bridge_vifc": 913,
    "nat_vifc": 921,
    "vlan_vifc": 929,
    "bridge_vifs": 898,
    "nat_vifs": 899,
    "vlan_vifs": 900,
    "upgrade_api": 903,
    "create_fw": 902,
    "ap_bridge": 912,
    "ap_nat": 920,
    "ap_vlan": 928,
    "ssid_2g_eap_bridge": 906,
    "ssid_2g_wpa2_bridge": 907,
    "ssid_2g_wpa_bridge": 908,
    "ssid_5g_eap_bridge": 909,
    "ssid_5g_wpa2_bridge": 910,
    "ssid_5g_wpa_bridge": 911,
    "ssid_2g_eap_nat": 914,
    "ssid_2g_wpa2_nat": 915,
    "ssid_2g_wpa_nat": 916,
    "ssid_5g_eap_nat": 917,
    "ssid_5g_wpa2_nat": 918,
    "ssid_5g_wpa_nat": 919,
    "ssid_2g_eap_vlan": 922,
    "ssid_2g_wpa2_vlan": 923,
    "ssid_2g_wpa_vlan": 924,
    "ssid_5g_eap_vlan": 925,
    "ssid_5g_wpa2_vlan": 926,
    "ssid_5g_wpa_vlan": 927,
    "radius_profile": 4679,
    "bridge_ssid_update": 9115,
    "nat_ssid_update": 9116,
    "vlan_ssid_update": 9117
}

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
    },
    "ecw5211": {
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
        "ssid_list": [
            "ECW5211_5G_WPA2",
            "ECW5211_5G_WPA",
            "ECW5211_5G_WPA2-EAP",
            "ECW5211_2dot4G_WPA2",
            "ECW5211_2dot4G_WPA",
            "ECW5211_2dot4G_WPA2-EAP"
        ]
    },

    "ecw5211_nat": {
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
        "ssid_list": [
            "ECW5211_5G_WPA2_NAT",
            "ECW5211_5G_WPA_NAT",
            "ECW5211_5G_WPA2-EAP_NAT",
            "ECW5211_2dot4G_WPA2_NAT",
            "ECW5211_2dot4G_WPA_NAT",
            "ECW5211_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "ecw5211_vlan": {
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
        "ssid_list": [
            "ECW5211_5G_WPA2_VLAN",
            "ECW5211_5G_WPA_VLAN",
            "ECW5211_5G_WPA2-EAP_VLAN",
            "ECW5211_2dot4G_WPA2_VLAN",
            "ECW5211_2dot4G_WPA_VLAN",
            "ECW5211_2dot4G_WPA2-EAP_VLAN"
        ]
    },
    "eap102": {
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
        "ssid_list": [
            "EAP102_5G_WPA2",
            "EAP102_5G_WPA",
            "EAP102_5G_WPA2-EAP",
            "EAP102_2dot4G_WPA2",
            "EAP102_2dot4G_WPA",
            "EAP102_2dot4G_WPA2-EAP"
        ]
    },

    "eap102_nat": {
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
        "ssid_list": [
            "EAP102_5G_WPA2_NAT",
            "EAP102_5G_WPA_NAT",
            "EAP102_5G_WPA2-EAP_NAT",
            "EAP102_2dot4G_WPA2_NAT",
            "EAP102_2dot4G_WPA_NAT",
            "EAP102_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "eap102_vlan": {
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
        "ssid_list": [
            "EAP102_5G_WPA2_VLAN",
            "EAP102_5G_WPA_VLAN",
            "EAP102_5G_WPA2-EAP_VLAN",
            "EAP102_2dot4G_WPA2_VLAN",
            "EAP102_2dot4G_WPA_VLAN",
            "EAP102_2dot4G_WPA2-EAP_VLAN"
        ]
    },
    "wf188n": {
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
        "ssid_list": [
            "WF188N_5G_WPA2",
            "WF188N_5G_WPA",
            "WF188N_5G_WPA2-EAP",
            "WF188N_2dot4G_WPA2",
            "WF188N_2dot4G_WPA",
            "WF188N_2dot4G_WPA2-EAP"
        ]
    },

    "wf188n_nat": {
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
        "ssid_list": [
            "WF188N_5G_WPA2_NAT",
            "WF188N_5G_WPA_NAT",
            "WF188N_5G_WPA2-EAP_NAT",
            "WF188N_2dot4G_WPA2_NAT",
            "WF188N_2dot4G_WPA_NAT",
            "WF188N_2dot4G_WPA2-EAP_NAT"
        ]
    },

    "wf188n_vlan": {
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
        "ssid_list": [
            "WF188N_5G_WPA2_VLAN",
            "WF188N_5G_WPA_VLAN",
            "WF188N_5G_WPA2-EAP_VLAN",
            "WF188N_2dot4G_WPA2_VLAN",
            "WF188N_2dot4G_WPA_VLAN",
            "WF188N_2dot4G_WPA2-EAP_VLAN"
        ]
    }
}
