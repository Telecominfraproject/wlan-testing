"""
ec420	basic-03
ecw5410	basic-01
ecw5211		not available in basic
wf188n	basic-05
eap102	basic-06
eap101	basic-02
wf194c	baisc-08-02

ssh -C -L 8800:lf1:4002 -L 8801:lf1:5901 -L 8802:lf1:8080 -L 8803:lab-ctlr:22 \     # basic-01
-L 8720:lf2:4002 -L 8721:lf2:5901 -L 8722:lf2:8080 -L 8723:lab-ctlr:22 \			# basic-02
-L 8830:lf3:4002 -L 8831:lf3:5901 -L 8832:lf3:8080 -L 8833:lab-ctlr:22 \			# basic-03
-L 8810:lf4:4002 -L 8811:lf4:5901 -L 8812:lf4:8080 -L 8813:lab-ctlr:22 \			# basic-04
-L 8850:lf12:4002 -L 8851:lf12:5901 -L 8852:lf12:8080 -L 8853:lab-ctlr4:22 \		# basic-05
-L 8860:lf13:4002 -L 8861:lf13:5901 -L 8862:lf13:8080 -L 8863:lab-ctlr4:22 \		# basic-06
-L 8870:lf14:4002 -L 8871:lf14:5901 -L 8872:lf14:8080 -L 8873:lab-ctlr4:22 \		# basic-07
-L 8880:lf15:4002 -L 8881:lf15:5901 -L 8882:lf15:8080 -L 8883:lab-ctlr4:22 \		# basic-08
ubuntu@3.130.51.163



ssh -C -L 8800:lf1:4002 -L 8801:lf1:5901 -L 8802:lf1:8080 -L 8803:lab-ctlr:22 \
-L 8720:lf2:4002 -L 8721:lf2:5901 -L 8722:lf2:8080 -L 8723:lab-ctlr:22 \
-L 8830:lf3:4002 -L 8831:lf3:5901 -L 8832:lf3:8080 -L 8833:lab-ctlr:22 \
-L 8810:lf4:4002 -L 8811:lf4:5901 -L 8812:lf4:8080 -L 8813:lab-ctlr:22 \
-L 8850:lf12:4002 -L 8851:lf12:5901 -L 8852:lf12:8080 -L 8853:lab-ctlr4:22 \
-L 8860:lf13:4002 -L 8861:lf13:5901 -L 8862:lf13:8080 -L 8863:lab-ctlr4:22 \
-L 8870:lf14:4002 -L 8871:lf14:5901 -L 8872:lf14:8080 -L 8873:lab-ctlr4:22 \
-L 8880:lf15:4002 -L 8881:lf15:5901 -L 8882:lf15:8080 -L 8883:lab-ctlr4:22 \
ubuntu@3.130.51.163

"""

CONFIGURATION = {
    "basic-ext-04-01": {
        "controller": {
            'url': "https://wlan-portal-svc-digicert.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': "1.1.0-SNAPSHOT",
            'commit_date': "2021-04-27"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': "wifi5",
                'serial': '903cb3944857',
                'jumphost': True,
                'ip': "192.168.200.80",
                'username': "lanforge",
                'password': "lanforge",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "ecw5410-2021-04-23-30496b1"
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
                "upstream_subnet": "192.168.200.0/24",
                "uplink" : "1.1.eth2",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax",
            }
        }
    }
}

FIRMWARE = {
    # jFrog parameters
    "JFROG":
        {
            "jfrog-base-url": "https://tip.jFrog.io/artifactory/tip-wlan-ap-firmware",
            "build": "pending",
            "branch": "trunk"
        }

}

RADIUS_SERVER_DATA = {
    "ip": "192.168.200.75",
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
