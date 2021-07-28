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
                'jumphost_tty': '/dev/ttyAP2',
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
                "2.4G-Station-Name": "twog0",
                "5G-Station-Name": "fiveg0",
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
    "interop": {
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
        "traffic_generator": {
            "name": "Perfecto",
            "details": {
                "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
                "perfectoURL": "tip"
            }
        }
    },
    "ubasic-01": {
        "controller": {
            'url': 'https://sdk-ucentral-2.cicd.lab.wlan.tip.build:16001/api/v1/oauth2',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
            # 'version': "1.1.0-SNAPSHOT",
            # 'commit_date': "2021-04-27"
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': 'wifi5',
                'serial': '903cb3944873',
                'jumphost': True,
                'ip': "192.168.52.100",  # localhost
                'username': "lanforge",
                'password': "lanforge",
                'port': 22,  # 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.1.0.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "192.168.52.100",  # localhost,
                "port": 8080,  # 8802,
                "ssh_port": 22,
                "2.4G-Radio": ["wiphy0"],
                "5G-Radio": ["wiphy0"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth1",
                "upstream_subnet": "192.168.52.1/24",
                "uplink": "1.1.eth2",
                "2.4G-Station-Name": "sta00",
                "5G-Station-Name": "sta10",
                "AX-Station-Name": "ax"
            }
        }
    },
    "basic-06": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'eap102',
                'mode': 'wifi6',
                'serial': '903cb39d6918',
                'jumphost': True,
                'ip': "10.28.3.103",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP2',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/edgecore_eap102/20210625-edgecore_eap102-uCentral-trunk-4225122-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.30",  # 10.28.3.30
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }
    },
    "basic-03": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'ec420',
                'mode': 'wifi5',
                'serial': '001122090801',
                'jumphost': True,
                'ip': "10.28.3.100",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP3',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/tplink_ec420/20210728-tplink_ec420-uCentral-trunk-12ad0d5-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.10",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy4"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy5"],
                "AX-Radio": ["1.1.wiphy0", "1.1.wiphy1", "1.1.wiphy2", "1.1.wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "sta00",
                "5G-Station-Name": "sta10",
                "AX-Station-Name": "ax"
            }
        }
    },
    "basic-04": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'ecw5211',
                'mode': 'wifi5',
                'serial': '68215fda456d',
                'jumphost': True,
                'ip': "10.28.3.100",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP5',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/edgecore_eap102/20210625-edgecore_eap102-uCentral-trunk-4225122-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.12",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy4"],
                "5G-Radio": ["1.1.wiphy5"],
                "AX-Radio": ["1.1.wiphy0", "1.1.wiphy1", "1.1.wiphy2", "1.1.wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }
    }  # checked   uci

}

RADIUS_SERVER_DATA = {
    "ip": "10.10.10.72",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

RADIUS_ACCOUNTING_DATA = {
    "ip": "10.10.10.72",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

PASSPOINT_RADIUS_SERVER_DATA = {
    "ip": "52.234.179.191",
    "port": 11812,
    "secret": "yeababy20!",
    "user": "nolaradius",
    "password": "nolastart",
    "pk_password": "whatever"
}

PASSPOINT_RADIUS_ACCOUNTING_SERVER_DATA = {
    "ip": "52.234.179.191",
    "port": 11813,
    "secret": "yeababy20!"
}

PASSPOINT_PROVIDER_INFO = {
    "mcc": None,
    "mnc": None,
    "network": None,
    "nai_realms": {
        "domain": "oss.ameriband.com",
        "encoding": 0,
        "eap_map": {"EAP-TTLS with username/password": ["Credential Type:username/password",
                                                        "Non-EAP Inner Authentication Type:MSCHAPV2"]}
    },
    "osu_nai_standalone": "anonymous@ameriband.com",
    "osu_nai_shared": "anonymous@ameriband.com",
    "roaming_oi": []
}

PASSPOINT_OPERATOR_INFO = {
    "osen": "Disabled",
    "domain_name_list": ["telecominfraproject.atlassian.net"],
    "operator_names": [
        {"locale": "eng", "name": "Default friendly passpoint_operator name"},
        {"locale": "fra", "name": "Nom de l'opérateur convivial par défaut"}
    ]
}

PASSPOINT_VENUE_INFO = {
    "venue_type": {"group": "Business", "type": "Police Station"},
    "venue_names": [
        {"locale": "eng", "name": "Example passpoint_venue", "url": "http://www.example.com/info-eng"},
        {"locale": "fra", "name": "Exemple de lieu", "url": "http://www.example.com/info-fra"}
    ]
}

PASSPOINT_PROFILE_INFO = {
    "profile_download_url_ios": "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig",
    "profile_download_url_android": "https://onboard.almondlabs.net/ttls/androidconfig.cfg",
    "profile_name_on_device": "AmeriBand",
    "radius_configuration": {
        "user_defined_nas_id": "FB001AP001",
        "operator_id": "AmeribandTIP",
        "radius_acounting_service_interval": 60
    },
    "interworking_hs2dot0": "Enabled",
    "hessid": None,
    "access_network": {
        "Access Network Type": "Free Public Network",
        "Authentication Type": "Acceptance of Terms & Conditions",
        "Emergency Services Reachable": "Enabled",
        "Unauthenticated Emergency Service": "Disabled",
    },
    "ip_connectivity": {
        "Internet Connectivity": "Enabled",
        "IP Address Type": "Public IPv4 Address Available",
        "Connection Capability": [{"status": "open", "protocol": "TCP", "port": 8888}],
        "ANQP Domain ID": 1234,
        "GAS Address 3 Behaviour": "P2P Spec Workaround From Request",
        "Disable DGAF": False
    }
}

TEST_CASES = {}