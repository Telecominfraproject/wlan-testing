CONFIGURATION = {
    "basic-lab": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',  # cloud controller Login
            'password': 'support',          # Cloud Controller Login Password
            'version': '1.1.0-SNAPSHOT',    # Controller version
            'commit_date': "2021-04-27"     # Controller version sdk, commit date
        },
        'access_point': [
            {
                'model': 'ecw5410',     # AP Model, can be found in ap console using "node" command
                'mode': 'wifi5',        # wifi5/wifi6   can be found on AP Hardware page on Confluence
                'serial': '3c2c99f44e77',   # "node" command has serial_number information
                'jumphost': True,           # True, if you have AP On serial console and not ssh access, False, if you have AP ssh access from the machine
                'ip': "localhost",          # IP Address of System, which has AP Connected to serial cable (if jumphost is True), else -  AP IP Address
                'username': "lanforge",     # ssh username of system (lab-ctlr/ap)
                'password': "pumpkin77",    # ssh password for system (lab-ctlr/ap)
                'port': 8803,  # 22,        # ssh port for system (lab-ctlr/ap)
                'jumphost_tty': '/dev/ttyAP1',  # if jumphost is True, enter the serial console device name
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.0.0-rc2.tar.gz"   # Enter the Target AP Version URL for Testing
            }
        ],
        # Traffic generator
        "traffic_generator": {
            "name": "lanforge", #( lanforge/ perfecto)
            # Details for LANforge system
            "details": {
                "ip": "localhost",  # localhost,
                "port": 8802,  # 8802,
                "2.4G-Radio": ["wiphy4"],
                "5G-Radio": ["wiphy5"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink" : "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }
    }
}


RADIUS_SERVER_DATA = {
    "ip": "10.10.10.72",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

TEST_CASES = {
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
