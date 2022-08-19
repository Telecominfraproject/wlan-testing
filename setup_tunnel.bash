#!/usr/bin/bash
# Setup python environment variable and pip environment variable like
# export PYTHON=/usr/bin/python3
# export PIP=/usr/bin/pip3
#sh setup_env.bash -t tip_2x -d all -n "Shivam Thakur" -o TIP -e shivam.thakur@candelatech.com -i "TIP OpenWIFI 2.X Library"
helpFunction()
{
   echo "Setup SSH Tunnel for TIP Labs"
   echo "Usage: $0 -l lab "
   echo -e "\t-l Target Lab basic-01 | basic-02 | basic-03 | basic-04 | basic-05 | basic-06 | basic-07 | basic-08 | advance-01 | advance-02"
   exit 1 # Exit script after printing help
}

basic1_8080=8800
basic1_22=8801
basic1_lab_ctlr=8802
basic1_vnc=8803

basic2_8080=8810
basic2_22=8811
basic2_lab_ctlr=8812
basic2_vnc=8813

basic3_8080=8820
basic3_22=8821
basic3_lab_ctlr=8822
basic3_vnc=8823

basic4_8080=8830
basic4_22=8831
basic4_lab_ctlr=8832
basic4_vnc=8833

basic5_8080=8840
basic5_22=8841
basic5_lab_ctlr=8842
basic5_vnc=8843

basic6_8080=8850
basic6_22=8851
basic6_lab_ctlr=8852
basic6_vnc=8853

basic7_8080=8860
basic7_22=8861
basic7_lab_ctlr=8862
basic7_vnc=8863


basic8_8080=8870
basic8_22=8871
basic8_lab_ctlr=8872
basic8_vnc=8873

advance1_8080=8880
advance1_22=8881
advance1_lab_ctlr=8882
advance1_vnc=8883

advance2_8080=8890
advance2_22=8891
advance2_lab_ctlr=8892
advance2_vnc=8893

advance3_8080=8900
advance3_22=8901
advance3_lab_ctlr=8902
advance3_vnc=8903
Create_lab_info_json()
{
  rm tests/lab_info.json
  touch lab_info.json
  # shellcheck disable=SC2016
  echo -e '
  {

"CONFIGURATION" : {
        "basic-04" : {
        "target": "tip_2x",
        "controller" : {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "edgecore_ecw5211",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth2",
            "lan_port": "1.1.eth1",
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi5",
            "identifier": "68215fda456d",
            "method": "serial",
            "host_ip": "localhost",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": ' $basic4_lab_ctlr ',
            "serial_tty": "/dev/ttyAP5",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "localhost",
                "http_port":' $basic4_8080',
                "ssh_port":' $basic4_22',
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                        }
                    }
                },
                "lan_ports": {
                    "1.1.eth1" : {
                        "addressing": "dynamic"
                    }
                },
                "uplink_nat_ports": {
                    "1.1.eth3": {
                        "addressing": "static",
                        "ip": "10.28.2.9",
                        "gateway_ip": "10.28.2.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    },
        "basic-05" : {
        "target": "tip_2x",
        "controller" : {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "cig_wf188n",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth2",
            "lan_port": null,
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "0000c1018812",
            "method": "serial",
            "host_ip": "localhost",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port":' $basic5_lab_ctlr',
            "serial_tty": "/dev/ttyAP1",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "localhost",
                "http_port":' $basic5_8080',
                "ssh_port":' $basic5_22',
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                        }
                    }
                },
                "lan_ports": {

                },
                "uplink_nat_ports": {
                    "1.1.eth1": {
                        "addressing": "static",
                        "ip": "10.28.2.16",
                        "gateway_ip": "10.28.2.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    },
    "basic-06" : {
        "target": "tip_2x",
        "controller" : {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "edgecore_eap102",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth2",
            "lan_port": null,
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "903cb39d6918",
            "method": "serial",
            "host_ip": "localhost",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port":' $basic6_lab_ctlr',
            "serial_tty": "/dev/ttyAP2",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "localhost",
                "http_port":' $basic6_8080',
                "ssh_port":' $basic6_22',
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                        }
                    }
                },
                "lan_ports": {

                },
                "uplink_nat_ports": {
                    "1.1.eth3": {
                        "addressing": "static",
                        "ip": "10.28.2.17",
                        "gateway_ip": "10.28.2.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    },
        "advance-03" : {
        "target": "tip_2x",
        "controller" : {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "cig_wf196",
            "supported_bands": ["2G", "5G", "6G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.3.eth2",
            "lan_port": null,
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6e",
            "identifier": "824f816011e4",
            "method": "serial",
            "host_ip": "localhost",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port":' $advance3_lab_ctlr',
            "serial_tty": "/dev/ttyAP0",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "10.28.3.117",
                "http_port": ' $advance3_8080',
                "ssh_port": ' $advance3_22',
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.3.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                        }
                    }
                },
                "lan_ports": {

                },
                "uplink_nat_ports": {
                    "1.3.eth3": {
                        "addressing": "static",
                        "ip": "10.28.2.39",
                        "gateway_ip": "10.28.2.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    }
},

"PERFECTO_DETAILS" : {
    "securityToken":"eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
    "projectName": "TIP-PyTest-Execution",
    "projectVersion": "1.0",
    "reportTags": "TestTag",
    "perfectoURL":"tip",
    "available_devices": [""],
    "iPhone-11": {
        "model-iOS": "iPhone-11",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-11",
        "jobNumber": 38
    },
    "iPhone-12": {
        "model-iOS": "iPhone-12",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-12",
        "jobNumber": 38
    },
    "iPhone-7": {
        "model-iOS": "iPhone-7",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-7",
        "jobNumber": 38
    },
    "iPhone-XR": {
        "model-iOS": "iPhone-XR",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-XR",
        "jobNumber": 38
    },
    "Galaxy S20": {
        "platformName-android": "Android",
        "model-android": "Galaxy S20",
        "appPackage-android": "com.android.settings",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "jobName": "Interop-Galaxy-S20",
        "jobNumber": 38
    },
    "Galaxy S10.*": {
        "platformName-android": "Android",
        "model-android": "Galaxy S10.*",
        "appPackage-android": "com.android.settings",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "jobName": "Interop-Galaxy-S10",
        "jobNumber": 38
    },
    "Galaxy S9": {
        "platformName-android": "Android",
        "model-android": "Galaxy S9",
        "appPackage-android": "com.android.settings",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "jobName": "Interop-Galaxy-S9",
        "jobNumber": 38
    },
    "Pixel 4": {
        "platformName-android": "Android",
        "model-android": "Pixel 4",
        "appPackage-android": "com.android.settings",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "jobName": "Interop-pixel-4",
        "jobNumber": 38
    }
},
"RADIUS_SERVER_DATA" : {
    "ip": "10.10.1.221",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"RADIUS_ACCOUNTING_DATA" : {
    "ip": "10.10.1.221",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"DYNAMIC_VLAN_RADIUS_SERVER_DATA" : {
    "ip": "3.20.165.131",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA" : {
    "ip": "3.20.165.131",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"RATE_LIMITING_RADIUS_SERVER_DATA" : {
    "ip": "18.189.85.200",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"RATE_LIMITING_RADIUS_ACCOUNTING_DATA" : {
    "ip": "18.189.85.200",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
},

"PASSPOINT_RADIUS_SERVER_DATA" : {
    "ip": "52.234.179.191",
    "port": 11812,
    "secret": "yeababy20!",
    "user": "nolaradius",
    "password": "nolastart",
    "pk_password": "whatever"
},

"PASSPOINT_RADIUS_ACCOUNTING_SERVER_DATA" : {
    "ip": "52.234.179.191",
    "port": 11813,
    "secret": "yeababy20!"
},

"PASSPOINT_PROVIDER_INFO" : {
    "mcc": null,
    "mnc": null,
    "network": null,
    "nai_realms": {
        "domain": "oss.ameriband.com",
        "encoding": 0,
        "eap_map": {"EAP-TTLS with username/password": ["Credential Type:username/password",
                                                        "Non-EAP Inner Authentication Type:MSCHAPV2"]}
    },
    "osu_nai_standalone": "anonymous@ameriband.com",
    "osu_nai_shared": "anonymous@ameriband.com",
    "roaming_oi": []
},

"PASSPOINT_OPERATOR_INFO" : {
    "osen": "Disabled",
    "domain_name_list": ["telecominfraproject.atlassian.net"],
    "operator_names": [
        {"locale": "eng", "name": "Default friendly passpoint_operator name"},
        {"locale": "fra", "name": "Nom de lopérateur convivial par défaut"}
    ]
},

"PASSPOINT_VENUE_INFO" : {
    "venue_type": {"group": "Business", "type": "Police Station"},
    "venue_names": [
        {"locale": "eng", "name": "Example passpoint_venue", "url": "http://www.example.com/info-eng"},
        {"locale": "fra", "name": "Exemple de lieu", "url": "http://www.example.com/info-fra"}
    ]
},

"PASSPOINT_PROFILE_INFO" : {
    "profile_download_url_ios": "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig",
    "profile_download_url_android": "https://onboard.almondlabs.net/ttls/androidconfig.cfg",
    "profile_name_on_device": "AmeriBand",
    "radius_configuration": {
        "user_defined_nas_id": "FB001AP001",
        "operator_id": "AmeribandTIP",
        "radius_acounting_service_interval": 60
    },
    "interworking_hs2dot0": "Enabled",
    "hessid": null,
    "access_network": {
        "Access Network Type": "Free Public Network",
        "Authentication Type": "Acceptance of Terms & Conditions",
        "Emergency Services Reachable": "Enabled",
        "Unauthenticated Emergency Service": "Disabled"
    },
    "ip_connectivity": {
        "Internet Connectivity": "Enabled",
        "IP Address Type": "Public IPv4 Address Available",
        "Connection Capability": [{"status": "open", "protocol": "TCP", "port": 8888}],
        "ANQP Domain ID": 1234,
        "GAS Address 3 Behaviour": "P2P Spec Workaround From Request",
        "Disable DGAF": false
    }
},
"open_flow":{},

"influx_params" : {}

}   ' >> tests/lab_info.json



}
while getopts "l:" opt
do
   case "$opt" in
      l ) lab="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$lab" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi
if [ "$lab" = "basic-01" ]; then
    echo "Initiating LAB Connection in basic-01"

    Create_lab_info_json
    ssh -C -L 8800:10.28.3.6:8080 -L 8801:10.28.3.6:22 -L 8802:10.28.3.100:22 -L 8803:10.28.3.6:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-02" ]; then
    echo "Initiating LAB Connection in basic-02"
    Create_lab_info_json
    ssh -C -L 8810:10.28.3.8:8080 -L 8811:10.28.3.8:22 -L 8812:10.28.3.100:22 -L 8813:10.28.3.8:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-03" ]; then
    echo "Initiating LAB Connection in basic-03"
    Create_lab_info_json
    ssh -C -L 8820:10.28.3.10:8080 -L 8821:10.28.3.10:22 -L 8822:10.28.3.100:22 -L 8823:10.28.3.10:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-04" ]; then
    echo "Initiating LAB Connection in basic-04"
    Create_lab_info_json
    ssh -C -L 8830:10.28.3.12:8080 -L 8831:10.28.3.12:22 -L 8832:10.28.3.100:22 -L 8833:10.28.3.12:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-05" ]; then
    echo "Initiating LAB Connection in basic-05"
    Create_lab_info_json
    ssh -C -L 8840:10.28.3.28:8080 -L 8841:10.28.3.28:22 -L 8842:10.28.3.103:22 -L 8843:10.28.3.28:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-06" ]; then
    echo "Initiating LAB Connection in basic-06"
    Create_lab_info_json
    ssh -C -L 8850:10.28.3.30:8080 -L 8851:10.28.3.30:22 -L 8852:10.28.3.103:22 -L 8853:10.28.3.30:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-07" ]; then
    echo "Initiating LAB Connection in basic-07"
    Create_lab_info_json
    ssh -C -L 8860:10.28.3.32:8080 -L 8861:10.28.3.32:22 -L 8862:10.28.3.103:22 -L 8863:10.28.3.32:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "basic-08" ]; then
    echo "Initiating LAB Connection in basic-08"
    Create_lab_info_json
    ssh -C -L 8870:10.28.3.34:8080 -L 8871:10.28.3.34:22 -L 8872:10.28.3.103:22 -L 8873:10.28.3.34:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "advance-01" ]; then
    echo "Initiating LAB Connection in advance-01"
    Create_lab_info_json
    ssh -C -L 8880:10.28.3.24:8080 -L 8881:10.28.3.24:22 -L 8882:10.28.3.102:22 -L 8883:10.28.3.24:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "advance-02" ]; then
    echo "Initiating LAB Connection in advance-02"
    Create_lab_info_json
    ssh -C -L 8890:10.28.3.26:8080 -L 8801:10.28.3.26:22 -L 8892:10.28.3.102:22 -L 8893:10.28.3.26:5901 ubuntu@3.130.51.163
fi
if [ "$lab" = "advance-03" ]; then
    echo "Initiating LAB Connection in advance-03"
    Create_lab_info_json
    ssh -C -L 8900:10.28.3.117:8080 -L 8901:10.28.3.117:22 -L 8902:10.28.3.115:22 -L 8903:10.28.3.117:5901 ubuntu@3.130.51.163
else
    echo "Testbed is Not Available"
fi


