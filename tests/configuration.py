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


Run the below command to open tunnel to all labs:

ssh -C -L 8700:lf1:4002 -L 8701:lf1:5901 -L 8702:lf1:8080 -L 8703:lab-ctlr:22 -L 8704:lf1:22 -L 3389:lf1:3389\
 -L 8710:lf2:4002 -L 8711:lf2:5901 -L 8712:lf2:8080 -L 8713:lab-ctlr:22 -L 8714:lf2:22 -L 3390:lf2:3389\
 -L 8720:lf3:4002 -L 8721:lf3:5901 -L 8722:lf3:8080 -L 8723:lab-ctlr:22 -L 8724:lf3:22 -L 3391:lf3:3389\
 -L 8730:lf4:4002 -L 8731:lf4:5901 -L 8732:lf4:8080 -L 8733:lab-ctlr:22 -L 8734:lf4:22 -L 3392:lf4:3389\
 -L 8740:lf12:4002 -L 8741:lf12:5901 -L 8742:lf12:8080 -L 8743:lab-ctlr4:22 -L 8744:lf12:22 -L 3393:lf12:3389\
 -L 8750:lf13:4002 -L 8751:lf13:5901 -L 8752:lf13:8080 -L 8753:lab-ctlr4:22 -L 8754:lf13:22 -L 3394:lf13:3389\
 -L 8760:lf14:4002 -L 8761:lf14:5901 -L 8762:lf14:8080 -L 8763:lab-ctlr4:22 -L 8764:lf14:22 -L 3395:lf14:3389\
 -L 8770:lf15:4002 -L 8771:lf15:5901 -L 8772:lf15:8080 -L 8773:lab-ctlr4:22 -L 8774:lf15:22 -L 3396:lf15:3389\
 ubuntu@3.130.51.163

"""

Customer = ""
server = ""
CONFIGURATION = {
    "basic-01": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'edgecore_ecw5410',
                'mode': 'wifi5',
                'serial': '3c2c99f44e77',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8703,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8702,
                "ssh_port": 8704,
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
    },  # checked   deployed    1.x
    "basic-02": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'hfcl_ion4',
                'mode': 'wifi6',
                'serial': '0006aee53b84',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8713,
                'jumphost_tty': '/dev/ttyAP2',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8712,
                "ssh_port": 8714,
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
    },  # checked   deployed    1.x
    "basic-03": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'tp-link_ec420-g1',
                'mode': 'wifi5',
                'serial': '001122090801',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8723,
                'jumphost_tty': '/dev/ttyAP3',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8722,
                "ssh_port": 8724,
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
    },  # checked   2.x
    "basic-03a": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'indio_um-305ac',
                'mode': 'wifi5',
                'serial': '706dec0a8a79',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8723,
                'jumphost_tty': '/dev/ttyAP6',
                'version': "release-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8722,
                "ssh_port": 8724,
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
      },  # checked   2.x

   "basic-04": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'edgecore_ecw5211',
                'mode': 'wifi5',
                'serial': '68215fda456d',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8733,
                'jumphost_tty': "/dev/ttyAP5",
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8732,
                "ssh_port": 8734,
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
    },  # checked   2.x
    "basic-05": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'cig_wf188n',
                'mode': 'wifi6',
                'serial': '0000c1018812',
                'jumphost': True,
                'ip': "localhost",
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8743,
                'jumphost_tty': '/dev/ttyAP1',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",
                "port": 8742,
                "ssh_port": 8744,
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
    },  # checked   2.x
    "basic-06": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'edgecore_eap102',
                'mode': 'wifi6',
                'serial': '903cb39d6918',
                'jumphost': True,
                'ip': "localhost",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8753,  # 22
                'jumphost_tty': '/dev/ttyAP2',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",  # 10.28.3.30
                "port": 8752,  # 8080
                "ssh_port": 8754,
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
    },  # checked   2.x
    "basic-07": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'edgecore_eap101',
                'mode': 'wifi6',
                'serial': '903cb36ae223',
                'jumphost': True,
                'ip': "localhost",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8763,  # 22
                'jumphost_tty': '/dev/ttyAP3',
                'version': "next-latest"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",  # 10.28.3.32
                "port": 8762,  # 8080
                "ssh_port": 8764,
                "2.4G-Radio": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream": "1.1.eth2",
                "upstream_subnet": "10.28.2.1/24",
                "uplink": "1.1.eth3",
                "2.4G-Station-Name": "sta10",
                "5G-Station-Name": "sta00",
                "AX-Station-Name": "ax"
            }
        }
    },  # checked   2.x
    "basic-08": {
        "controller": {
            'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
            'username': "tip@ucentral.com",
            'password': 'OpenWifi%123',
        },
        'access_point': [
            {
                'model': 'cig_wf194c',
                'mode': 'wifi6',
                'serial': '089b4bb2f10c',
                'jumphost': True,
                'ip': "localhost",  # 10.28.3.103
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8773,  # 22
                'jumphost_tty': '/dev/ttyAP5',
                'version': "next-650adaf"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "localhost",  # 10.28.3.34
                "port": 8772,  # 8080
                "ssh_port": 8774,
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
    },  # checked   2.x
    "mesh": {
        "controller": {
            'url': "http://wlan-portal-svc-digicert.cicd.lab.wlan.tip.build",  # API base url for the controller
            'username': 'support@example.com',
            'password': 'support',
            'version': '1.1.0-SNAPSHOT',
            'commit_date': "2021-06-01"
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
                'version': "next-650adaf"
            }
        ],
        "traffic_generator": {
            "name": "lanforge",
            "details": {
                "ip": "10.28.3.14",  # 10.28.3.34
                "port": 8080,  # 8080
                "ssh_port": 22,
                "2.4G-Radio": ["wiphy0", "wiphy2"],
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
                'version': "next-650adaf"
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
            'password': 'OpenWifi%123',
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
                'version': "next-650adaf"
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
            'password': 'OpenWifi%123',
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
                'version': "next-650adaf"
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
                'version': "next-650adaf"
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
    "ip": "10.10.1.221",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

RADIUS_ACCOUNTING_DATA = {
    "ip": "10.10.1.221",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

RATE_LIMITING_RADIUS_SERVER_DATA = {
    "ip": "18.189.85.200",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

RATE_LIMITING_RADIUS_ACCOUNTING_DATA = {
    "ip": "18.189.85.200",
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

open_flow = {}