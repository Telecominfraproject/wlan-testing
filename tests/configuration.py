"""
ec420	basic-03
ecw5410	basic-04
ecw5211		not available in basic
wf188n	config
eap102	basic-06
eap101	basic-02
wf194c	baisc-08-02

ssh -C -L 8800:lf1:4002 -L 8801:lf1:5901 -L 8802:lf1:8080 -L 8803:lab-ctlr:22 \	    # basic-01
-L 8720:lf2:4002 -L 8721:lf2:5901 -L 8722:lf2:8080 -L 8723:lab-ctlr:22 \			# basic-02
-L 8830:lf3:4002 -L 8831:lf3:5901 -L 8832:lf3:8080 -L 8833:lab-ctlr:22 \			# basic-03
-L 8810:lf4:4002 -L 8811:lf4:5901 -L 8812:lf4:8080 -L 8813:lab-ctlr:22 \			# basic-04
-L 8850:lf12:4002 -L 8851:lf12:5901 -L 8852:lf12:8080 -L 8853:lab-ctlr4:22 \		# config
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

Customer = ""
server = ""
CONFIGURATION = {
    "basic-01": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",  # API base url for the controller
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
                'ip': "10.28.3.100",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.2.0-rc2.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.6",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy4"],
                "5G-Radio": ["1.1.wiphy5"],
                "AX-Radio": ["1.1.wiphy0", "1.1.wiphy1", "1.1.wiphy2", "1.1.wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan1",
                "AX-Station-Name": "ax"
            }
        }
    },  # checked   deployed
    "basic-02": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': "1.1.0-SNAPSHOT",
            'commit_date': "2021-06-01"
        },
        'access_point': [
            {
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af48db',
                'jumphost': True,
                'ip': "10.28.3.100",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP2',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/eap101/trunk/eap101-1.2.0-rc2.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.8",
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
    },  # checked   deployed
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
                'version': "latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.10",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy4"],
                "5G-Radio": ["1.1.wiphy5"],
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
                'jumphost_tty': "/dev/ttyAP5",
                'version': "latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.12",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy4"],
                "5G-Radio": [ "1.1.wiphy5"],
                "AX-Radio": ["1.1.wiphy0", "1.1.wiphy1", "1.1.wiphy2", "1.1.wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
        }
    },  # checked   uci
    "basic-05": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'cig_wf188',
                'mode': 'wifi6',
                'serial': '0000c1018812',
                'jumphost': True,
                'ip': "10.28.3.103",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "trunk-d6c5e1f"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.28",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth1",
                "2.4G-Station-Name": "sta00",
                "5G-Station-Name": "sta10",
                "AX-Station-Name": "ax"
            }
        }
    },  # checked   uci
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
                'version': "latest"
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
    "basic-07": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '903cb36ae223',
                'jumphost': True,
                'ip': "10.28.3.103",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP3',
                'version': "latest-next",
                'version_branch': "trunk-d6c5e1f"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.32",  # 10.28.3.32
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["wiphy4"],
                "5G-Radio": ["wiphy5"],
                "AX-Radio": ["wiphy0", "wiphy1", "wiphy2", "wiphy3"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "sta10",
                "5G-Station-Name": "sta00",
                "AX-Station-Name": "ax"
            }
        }
    },  # checked   uci
    "basic-08": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'wf194c',
                'mode': 'wifi6',
                'serial': '089b4bb2f10c',
                'jumphost': True,
                'ip': "10.28.3.103",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP5',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/cig_wf194c/20210729-cig_wf194c-v2.0.0-rc2-02244b8-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.34",  # 10.28.3.34
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
    },  # checked

    "mesh": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af4a7a',
                'jumphost': True,
                'ip': "10.28.3.101",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP2',
                'version': "latest"
            },
{
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af4903',
                'jumphost': True,
                'ip': "10.28.3.101",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP3',
                'version': "latest"
            },
{
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af4a7a',
                'jumphost': True,
                'ip': "10.28.3.101",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,  # 22
                'jumphost_tty': '/dev/ttyAP4',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/eap101/trunk/eap101-1.1.0.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details-mobile-sta": {
                "ip": "10.28.3.14",  # 10.28.3.34
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
            },
            "details-root": {
                "ip": "10.28.3.14",  # 10.28.3.34
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["wiphy1", "wiphy3"],
                "AX-Radio": ["wiphy4", "wiphy5", "wiphy6", "wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            },
            "details-node-1": {
                "ip": "10.28.3.14",  # 10.28.3.34
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["wiphy1", "wiphy3"],
                "AX-Radio": ["wiphy4", "wiphy5", "wiphy6", "wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            },
            "details-node-2": {
                "ip": "10.28.3.14",  # 10.28.3.34
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["wiphy1", "wiphy3"],
                "AX-Radio": ["wiphy4", "wiphy5", "wiphy6", "wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }

        }
    },  # checked
    "interop-01": {
        "controller": {
            'url': "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': '19.07-SNAPSHOT',
            'commit_date': '2021-06-01'
        },
        'access_point': [
            {
                'model': 'ecw5410',
                'mode': 'wifi5',
                'serial': '68215fd2f78c',
                'jumphost': True,
                'ip': "10.28.3.102",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "https://tip-tip-wlan-cloud-docker-repo.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/dev/ecw5410-2021-07-28-pending-0ec23e8.tar.gz"
            }
        ],
        "traffic_generator": {
                "name": "lanforge",
                "details": {
                    "ip": "10.28.3.22",
                    "port": 8080,  # 8080
                    "ssh_port": 22,
                    "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                    "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                    "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                    "upstream": "1.1.eth1",
                    "upstream_subnet": "10.28.2.1/24",
                    "uplink": "1.1.eth3",
                    "2.4G-Station-Name": "wlan0",
                    "5G-Station-Name": "wlan1",
                    "AX-Station-Name": "ax",
                    "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
                    "perfectoURL": "tip"
                }
        }
    },

    "interop-02": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'eap101',
                'mode': 'wifi5',
                'serial': '903cb36ae4a3',
                'jumphost': True,
                'ip': "10.28.3.102",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP4',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/edgecore_eap101/20210729-edgecore_eap101-v2.0.0-rc2-02244b8-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.22",
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream": "1.1.eth1",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan1",
                "AX-Station-Name": "ax",
                "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
                "perfectoURL": "tip"
            }
        }
    },

    "interop-03": {
        "controller": {
            'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'openwifi',
        },
        'access_point': [
            {
                'model': 'eap101',
                'mode': 'wifi5',
                'serial': '903cb36ae255',
                'jumphost': True,
                'ip': "10.28.3.102",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 22,
                'jumphost_tty': '/dev/ttyAP5',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/edgecore_eap101/20210729-edgecore_eap101-v2.0.0-rc2-02244b8-upgrade.bin"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.22",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream": "1.1.eth1",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan1",
                "AX-Station-Name": "ax",
                "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
                "perfectoURL": "tip"
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
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/ecw5410/trunk/ecw5410-1.1.0.tar.gz"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "192.168.200.80",
                "port": 8080,
                "ssh_port": 22,
                "2.4G-Radio": ["wiphy0"],
                "5G-Radio": ["wiphy1"],
                "AX-Radio": ["wiphy2"],
                "upstream": "1.1.eth1",
                "upstream_subnet": "192.168.200.1/24",
                "uplink": "1.1.eth2",
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

RADIUS_ACCOUNTING_DATA = {
    "ip": "10.10.10.72",
    "port": 1812,
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
    "2g_wpa3_eap_ttls_bridge": 9754,
    "5g_wpa3_eap_ttls_bridge": 9755,
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
    "2g_wpa3_mixed_eap_ttls_wpa3_bridge": 9766,
    "2g_wpa3_mixed_wpa3_bridge": 9767,
    "5g_wpa3_mixed_eap_ttls_wpa3_bridge": 9768,
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
