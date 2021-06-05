CONFIGURATION = {
    "basic-01": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': '1.1.0-SNAPSHOT',
            'commit_date': "2021-06-01"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': 'wifi5',
                'serial': '3c2c99f44e77',
                'jumphost': True,
                'ip': "localhost",  # localhost
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8803,  # 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.1.0.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",  # localhost,
                "port": 8802,  # 8802,
                "ssh_port": 8804,
                "2.4G-Radio": ["wiphy4"],
                "5G-Radio": ["wiphy5"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }
    },
    # This is sample Config of a Testbed
    "basic-ext-01": {
        "controller": {
            'url': "http://wlan-portal-svc-digicert.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',  # cloud controller Login
            'password': 'support',  # Cloud Controller Login Password
            'version': '1.1.0-SNAPSHOT',  # Controller version
            'commit_date': "2021-04-27"  # Controller version sdk, commit date
        },
        'access_point': [
            {
                'model': 'ecw5410',  # AP Model, can be found in ap console using "node" command
                'mode': 'wifi5',  # wifi5/wifi6   can be found on AP Hardware page on Confluence
                'serial': '903cb3944873',  # "node" command has serial_number information
                'jumphost': True,
                # True, if you have AP On serial console and not ssh access, False, if you have AP ssh access from the machine
                'ip': "192.168.80.99",
                # IP Address of System, which has AP Connected to serial cable (if jumphost is True), else -  AP IP Address
                'username': "lanforge",  # ssh username of system (lab-ctlr/ap)
                'password': "lanforge",  # ssh password for system (lab-ctlr/ap)
                'port': 22,  # 22,        # ssh port for system (lab-ctlr/ap)
                'jumphost_tty': '/dev/ttyAP1',  # if jumphost is True, enter the serial console device name
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.1.0.tar.gz"
                # Enter the Target AP Version URL for Testing
            }
        ],
        # Traffic generator
        "traffic_generator": {
            "name": "lanforge",  # ( lanforge/ perfecto)
            # Details for LANforge system
            "details": {
                "ip": "192.168.80.99",  # localhost,
                "port": 8080,  # 8802,
                "2.4G-Radio": ["wiphy4"],
                "5G-Radio": ["wiphy5"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }

    },
    "basic-lab": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',  # cloud controller Login
            'password': 'support',  # Cloud Controller Login Password
            'version': '1.1.0-SNAPSHOT',  # Controller version
            'commit_date': "2021-04-27"  # Controller version sdk, commit date
        },
        'access_point': [
            {
                'model': 'ecw5410',  # AP Model, can be found in ap console using "node" command
                'mode': 'wifi5',  # wifi5/wifi6   can be found on AP Hardware page on Confluence
                'serial': '903cb3944873',  # "node" command has serial_number information
                'jumphost': True,
                # True, if you have AP On serial console and not ssh access, False, if you have AP ssh access from the machine
                'ip': "localhost",
                # IP Address of System, which has AP Connected to serial cable (if jumphost is True), else -  AP IP Address
                'username': "lanforge",  # ssh username of system (lab-ctlr/ap)
                'password': "pumpkin77",  # ssh password for system (lab-ctlr/ap)
                'port': 8803,  # 22,        # ssh port for system (lab-ctlr/ap)
                'jumphost_tty': '/dev/ttyAP1',  # if jumphost is True, enter the serial console device name
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.1.0.tar.gz"
                # Enter the Target AP Version URL for Testing
            }
        ],
        # Traffic generator
        "traffic_generator": {
            "name": "lanforge",  # ( lanforge/ perfecto)
            # Details for LANforge system
            "details": {
                "ip": "localhost",  # localhost,
                "port": 8802,  # 8802,
                "2.4G-Radio": ["wiphy4"],
                "5G-Radio": ["wiphy5"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }

    },
    "interop":  {
            "controller": {
                'url': "https://wlan-portal-svc-nola-01.cicd.lab.wlan.tip.build",  # API base url for the controller
                'username': 'support@example.com',
                'password': 'support',
                'version': '1.0.0-SNAPSHOT',
                'commit_date': '2021-03-01'
            },
            'access_point': [
                {
                    'model': 'ecw5410',
                    'mode': 'wifi5',
                    'serial': '68215fd2f78c',
                    'jumphost': True,
                    'ip': "localhost",
                    'username': "lanforge",
                    'password': "pumpkin77",
                    'port': 8803,
                    'jumphost_tty': '/dev/ttyAP1',
                    'version': "ecw5410-2021-04-26-pending-3fc41fa"
                }
            ],
            "traffic_generator":  {
                "name": "Perfecto",
                "details": {
                    "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
                    "perfectoURL": "tip"
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
    "2g_wpa2_eap_ttls_bridge": 5214,
    "5g_wpa2_eap_ttls_bridge": 5215,
    "2g_wpa2_eap_ttls_nat": 5216,
    "5g_wpa2_eap_ttls_nat": 5217,
    "cloud_connection": 5222,
    "cloud_fw": 5247,
    "5g_wpa2_vlan": 5248,
    "5g_wpa_vlan": 5249,
    "5g_wpa2_eap_ttls_vlan": 5250,
    "2g_wpa2_vlan": 5251,
    "2g_wpa_vlan": 5252,
    "2g_wpa2_eap_ttls_vlan": 5253,
    "cloud_ver": 5540,
    "bridge_vifc": 5541,
    "nat_vifc": 5542,
    "vlan_vifc": 5543,
    "bridge_vifs": 5544,
    "nat_vifs": 5545,
    "vlan_vifs": 5546,
    "upgrade_api": 5547,
    "create_fw": 5548,
    "ap_profile_bridge": 5641,
    "ap_profile_nat": 5642,
    "ap_profile_vlan": 5643,
    "ssid_2g_wpa2_eap_bridge": 5644,
    "ssid_2g_wpa2_bridge": 5645,
    "ssid_2g_wpa_bridge": 5646,
    "ssid_5g_wpa2_eap_bridge": 5647,
    "ssid_5g_wpa2_bridge": 5648,
    "ssid_5g_wpa_bridge": 5649,
    "ssid_2g_wpa2_eap_nat": 5650,
    "ssid_2g_wpa2_nat": 5651,
    "ssid_2g_wpa_nat": 5652,
    "ssid_5g_wpa2_eap_nat": 5653,
    "ssid_5g_wpa2_nat": 5654,
    "ssid_5g_wpa_nat": 5655,
    "ssid_2g_wpa2_eap_vlan": 5656,
    "ssid_2g_wpa2_vlan": 5657,
    "ssid_2g_wpa_vlan": 5658,
    "ssid_5g_wpa2_eap_vlan": 5659,
    "ssid_5g_wpa2_vlan": 5660,
    "ssid_5g_wpa_vlan": 5661,
    "radius_profile": 5808,
    "bridge_ssid_update": 8742,
    "nat_ssid_update": 8743,
    "vlan_ssid_update": 8744,
    "2g_wpa3_bridge": 9740,
    "5g_wpa3_bridge": 9741,
    "ssid_2g_wpa3_bridge": 9742,
    "ssid_5g_wpa3_bridge": 9743,
    "ssid_2g_wpa3_nat": 9744,
    "ssid_5g_wpa3_nat": 9745,
    "ssid_2g_wpa3_vlan": 9746,
    "ssid_5g_wpa3_vlan": 9747,
    "2g_wpa3_nat": 9748,
    "5g_wpa3_nat": 9749,
    "2g_wpa3_vlan": 9750,
    "5g_wpa3_vlan": 9751,
    "ssid_2g_wpa3_eap_bridge": 9752,
    "ssid_5g_wpa3_eap_bridge": 9753,
    "2g_wpa3_eap_bridge": 9754,
    "5g_wpa3_eap_bridge": 9755,
    "ssid_2g_wpa3_eap_nat": 9756,
    "ssid_5g_wpa3_eap_nat": 9757,
    "ssid_2g_wpa3_eap_vlan": 9758,
    "ssid_5g_wpa3_eap_vlan": 9759,
    "2g_wpa3_eap_ttls_nat": 9760,
    "5g_wpa3_eap_ttls_nat": 9761,
    "2g_wpa3_eap_ttls_vlan": 9762,
    "5g_wpa3_eap_ttls_vlan": 9763,
    "ssid_2g_wpa3_mixed_bridge": 9764,
    "ssid_5g_wpa3_mixed_bridge": 9765,
    # "2g_wpa3_mixed_wpa2_bridge": 9766,
    "2g_wpa3_mixed_wpa3_bridge": 9767,
    # "5g_wpa3_mixed_wpa2_bridge": 9768,
    "5g_wpa3_mixed_wpa3_bridge": 9769,
    "ssid_2g_wpa3_mixed_nat": 9770,
    "ssid_5g_wpa3_mixed_nat": 9771,
    "ssid_2g_wpa3_mixed_vlan": 9772,
    "ssid_5g_wpa3_mixed_vlan": 9773,
    # "2g_wpa3_mixed_wpa2_nat": 9774,
    "2g_wpa3_mixed_wpa3_nat": 9775,
    # "5g_wpa3_mixed_wpa2_nat": 9776,
    "5g_wpa3_mixed_wpa3_nat": 9777,
    # "2g_wpa3_mixed_wpa2_vlan": 9778,
    "2g_wpa3_mixed_wpa3_vlan": 9779,
    # "5g_wpa3_mixed_wpa2_vlan": 9780,
    "5g_wpa3_mixed_wpa3_vlan": 9781,
    "ssid_2g_wpa3_enterprise_mixed_bridge": 9782,
    "ssid_5g_wpa3_enterprise_mixed_bridge": 9783,
    "2g_wpa2_mixed_eap_wpa2_bridge": 9784,
    "2g_wpa3_mixed_eap_wpa3_bridge": 9785,
    "5g_wpa3_mixed_eap_wpa2_bridge": 9786,
    "5g_wpa3_mixed_eap_wpa3_bridge": 9787,
    "ssid_2g_wpa3_enterprise_mixed_nat": 9788,
    "ssid_5g_wpa3_enterprise_mixed_nat": 9789,
    "2g_wpa3_mixed_eap_wpa2_nat": 9790,
    "2g_wpa3_mixed_eap_ttls_wpa3_nat": 9791,
    "5g_wpa3_mixed_eap_wpa2_nat": 9792,
    "5g_wpa3_mixed_eap_ttls_wpa3_nat": 9793,
    "ssid_2g_wpa3_enterprise_mixed_vlan": 9794,
    "ssid_5g_wpa3_enterprise_mixed_vlan": 9795,
    "2g_wpa3_mixed_eap_wpa2_vlan": 9796,
    "2g_wpa3_mixed_eap_ttls_wpa3_vlan": 9797,
    "5g_wpa3_mixed_eap_wpa2_vlan": 9798,
    "5g_wpa3_mixed_eap_ttls_wpa3_vlan": 9799,
    "ssid_2g_open_bridge": 9805,
    "ssid_5g_open_bridge": 9806,
    "ssid_2g_open_nat": 9807,
    "ssid_5g_open_nat": 9808,
    "ssid_2g_open_vlan": 9809,
    "ssid_5g_open_vlan": 9810,
    "ssid_2g_wpa2_mixed_bridge": 9811,
    "ssid_5g_wpa2_mixed_bridge": 9812,
    "ssid_2g_wpa2_mixed_nat": 9813,
    "ssid_5g_wpa2_mixed_nat": 9814,
    "ssid_2g_wpa2_mixed_vlan": 9815,
    "ssid_5g_wpa2_mixed_vlan": 9817,
    "ssid_2g_wpa_wpa2_enterprise_mixed_bridge": 9818,
    "ssid_5g_wpa_wpa2_enterprise_mixed_bridge": 9819,
    "ssid_2g_wpa_wpa2_enterprise_mixed_nat": 9820,
    "ssid_5g_wpa_wpa2_enterprise_mixed_nat": 9821,
    "ssid_2g_wpa_wpa2_enterprise_mixed_vlan": 9822,
    "ssid_5g_wpa_wpa2_enterprise_mixed_vlan": 9823,
    "ssid_2g_wpa_eap_bridge": 9824,
    "ssid_5g_wpa_eap_bridge": 9825,
    # "ssid_2g_wpa2_eap_bridge": 9824,
    # "ssid_5g_wpa2_eap_bridge": 9825,
    "ssid_2g_wpa_eap_nat": 9826,
    "ssid_5g_wpa_eap_nat": 9827,
    "ssid_2g_wpa_eap_vlan": 9828,
    "ssid_5g_wpa_eap_vlan": 9829,
    # "ap_update_bridge": 9856,
    # "ap_update_nat": 9857,
    # "ap_update_vlan": 9858,
    # "bridge_vifc_update": 9859,
    # "nat_vifc_update": 9860,
    # "vlan_vifc_update": 9861,
    # "bridge_vifs_update": 9862,
    # "nat_vifs_update": 9863,
    # "vlan_vifs_update": 9864,
    "2g_wpa_eap_ttls_bridge": 9867,
    "5g_wpa_eap_ttls_bridge": 9768,
    "2g_wpa_eap_ttls_nat": 9869,
    "5g_wpa_eap_ttls_nat": 9770,
    "2g_wpa_eap_ttls_vlan": 9871,
    "5g_wpa_eap_ttls_vlan": 9872,
    # "2g_wpa2_mixed_eap_wpa_bridge": 9873,
    "2g_wpa2_mixed_eap_ttls_wpa2_bridge": 9874,
    # "5g_wpa2_mixed_eap_wpa_bridge": 9875,
    "5g_wpa2_mixed_eap_ttls_wpa2_bridge": 9876,
    # "2g_wpa2_mixed_eap_wpa_nat": 9877,
    "2g_wpa2_mixed_eap_ttls_wpa2_nat": 9878,
    # "5g_wpa2_mixed_eap_wpa_nat": 9879,
    "5g_wpa2_mixed_eap_ttls_wpa2_nat": 9880,
    # "2g_wpa2_mixed_eap_wpa_vlan": 9881,
    "2g_wpa2_mixed_eap_ttls_wpa2_vlan": 9882,
    # "5g_wpa2_mixed_eap_wpa_vlan": 9883,
    "5g_wpa2_mixed_eap_ttls_wpa2_vlan": 9884,
    # "2g_wpa2_mixed_wpa_bridge": 9885,
    "2g_wpa2_mixed_wpa2_bridge": 9886,
    # "5g_wpa2_mixed_wpa_bridge": 9887,
    "5g_wpa2_mixed_wpa2_bridge": 9888,
    # "2g_wpa2_mixed_wpa_nat": 9889,
    "2g_wpa2_mixed_wpa2_nat": 9890,
    # "5g_wpa2_mixed_wpa_nat": 9891,
    "5g_wpa2_mixed_wpa2_nat": 9892,
    # "2g_wpa2_mixed_wpa_vlan": 9893,
    "2g_wpa2_mixed_wpa2_vlan": 9894,
    # "5g_wpa2_mixed_wpa_vlan": 9895,
    "5g_wpa2_mixed_wpa2_vlan": 9896,
    "2g_open_bridge": 2234,
    "5g_open_bridge": 2235,
    "2g_open_nat": 4321,
    "5g_open_nat": 4322,
    "2g_open_vlan": 9897,
    "5g_open_vlan": 9898
}

