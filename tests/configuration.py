Controller = {
    'url': "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",  # API base url for the controller
    'username': 'support@example.com',
    'password': 'support',
    'version': '1.0.0-SNAPSHOT',
    'commit_date': '2021-03-01'
}

LabController = [
    {
        'ip': "ip address of the controller",
        'Username': "<username>",
        'Password': "<password>"
    },
    {
        'ip': "ip address of the controller",
        'Username': "<username>",
        'Password': "<password>"
    }
]

AccessPoints = [
    {
      'model': 'ecw5410',
      'serial number': 'serial-number',
      'jumphost': True,
      'ip': "192.168.200.81",
      'username': "lanforge",
      'password': "lanforge",
      'port': 22,
      'jumphost_tty': '/dev/ttyAP1',
      'version': "version"
    },
    {
      'model': 'ecw5410',
      'serial number' : 'serial-number',
      'jumphost': True,
      'ip': "192.168.200.81",
      'username': "lanforge",
      'password': "lanforge",
      'port': 22,
      'jumphost_tty': '/dev/ttyAP1',
      'version': "version"
    }
]

CLOUDSDK_VERSION = {}
TrafficGenerator = {
    "lanforge": {
        "ip": "192.168.200.81",
        "port": 8080,
        "2.4G-Radio": "wihpy0",
        "5G-Radio": "wiphy1",
        "AX-Radio": "wiphy2",
        "upstream": "eth1",
        "2.4G-Station-Name": "two",
        "5G-Station-Name": "five",
        "AX-Station-Name": "ax",
    },
    "perfecto": {

    }
}

RADIUS_SERVER_DATA = {
    "ip": "192.168.200.75",
    "port": 1812,
    "secret": "testing123"
}


LAB_INFO = {
    "ap_model": "ecw5410",
    "cloudsdk_url": "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",
    "equipment_details": {
        "serial_number_1": {
            "ip": "",
            "firmware_ver": ""

        },
        "serial_number_2": {
            "ip": "",
            "firmware_ver": ""
        },
        "serial_number_3": {
            "ip": "",
            "firmware_ver": ""
        }
    }
}


APNOS_CREDENTIAL_DATA = {
    'ip': "192.168.200.81",
    'username': "lanforge",
    'password': "lanforge",
    'port': 22,
    'mode': 1,
    'jumphost_tty': '/dev/ttyAP1',

}

"""
AP --- ssh

ssh tunnel --- localhost:8800

"""

NOLA = {
    # It is in NOLA-01 equipment 4 lab-ctlr minicom ap1
    "ecw5410": {
        "cloudsdk_url": "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",
        "customer_id": 2,
        "equipment_id": 21
    },
    "ecw5211": {
        "cloudsdk_url": "",
        "customer_id": 2,
        "equipment_id": ""
    },
    # WORKS     # NOLA -03 lab-ctlr minicom ap3, lf4
    "ec420": {
        "cloudsdk_url": "http://wlan-ui.nola-qa.lab.wlan.tip.build",
        "customer_id": 2,
        "equipment_id": 7
    },
    "wf194c": {
        "cloudsdk_url": "",
        "customer_id": 2,
        "equipment_id": ""
    },
    # NOLA -01 lab-ctlr3 minicom ap3
    "eap102": {
        "cloudsdk_url": "http://wlan-ui.nola-qa.lab.wlan.tip.build",
        "customer_id": 2,
        "equipment_id": ""
    },
    # WORKS    # NOLA -02 lab-ctlr minicom ap2, lf2
    "eap101": {
        "cloudsdk_url": "http://wlan-ui.nola-qa.lab.wlan.tip.build",
        "customer_id": 2,
        "equipment_id": 8
    },
    "wf188n": {
        "cloudsdk_url": "",
        "customer_id": 2,
        "equipment_id": ""
    }
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


"""
orch
    lab-ctlr
    lab-ctlr2
    lab-ctlr3
    lab-ctlr4
"""
