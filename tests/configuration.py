CONFIGURATION = {
    "basic-ext-03-01": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-03.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': "1.1.0-SNAPSHOT",
            'commit_date': "2021-04-27"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': "wifi5",
                'serial': '903cb3944807',
                'jumphost': True,
                'ip': "192.168.200.230",
                'username': "lanforge",
                'password': "lanforge",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "ecw5410-2021-03-30-pending-9cb289b"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8080,
                "2.4G-Radio": ["wiphy0"],
                "5G-Radio": ["wiphy1"],
                "AX-Radio": ["wiphy2"],
                "upstream": "eth1",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan1",
                "AX-Station-Name": "ax",
            }
        }
    },
    "basic-ext-03-02": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-03.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': "1.1.0-SNAPSHOT",
            'commit_date': "2021-04-27"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': 'wifi5',
                'serial': '903cb394486f',
                'jumphost': True,
                'ip': "192.168.200.233",
                'username': "lanforge",
                'password': "lanforge",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "ecw5410-2021-04-26-pending-3fc41fa"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "192.168.200.233",
                "port": 8080,
                "2.4G-Radio": ["wiphy0"],
                "5G-Radio": ["wiphy1"],
                "AX-Radio": ["wiphy2"],
                "upstream": "eth1",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan1",
                "AX-Station-Name": "ax",
            }
        }
    },
    "basic-ext-03-03": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-03.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': "1.1.0-SNAPSHOT",
            'commit_date': "2021-04-27"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': 'wifi5',
                'serial': '903cb3944857',
                'jumphost': True,
                'ip': "192.168.200.80",
                'username': "lanforge",
                'password': "lanforge",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "ecw5410-2021-04-26-pending-3fc41fa"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "192.168.200.80",
                "port": 8080,
                "2.4G-Radio": ["wiphy0"],
                "5G-Radio": ["wiphy1"],
                "AX-Radio": ["wiphy2"],
                "upstream": "1.1.eth1",
                "uplink": "1.1.eth2",
                "upstream_subnet": "192.168.200.1/24",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax",
            }
        }
    },
}

FIRMWARE = {
    # jFrog parameters
    "JFROG":
        {
            "jfrog-base-url": "https://tip.jFrog.io/artifactory/tip-wlan-ap-firmware",
            "username": "tip-read",
            "password": "tip-read",
            "build": "pending",
            "branch": "dev"
        }

}

RADIUS_SERVER_DATA = {
    "ip": "10.28.3.100",
    "port": 1812,
    "secret": "testing123",
    "user": "nolaradius",
    "password": "nolastart",
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
# cmd = /bin/wlan_ap_redirector.sh ssl:opensync-redirector-nola-01.cicd.lab.wlan.tip.build:6643
# radius server
# radsec
