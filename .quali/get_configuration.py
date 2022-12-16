import argparse
import json
import sys

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

from common import get_session


def get_attribute_value(cloudshell_session, attribute):
    if attribute.Type == 'Boolean':
        return True if attribute.Value == 'True' else False
    elif attribute.Type == 'Numeric':
        return int(attribute.Value)
    elif attribute.Type == 'Password':
        return cloudshell_session.DecryptPassword(attribute.Value).Value
    else:
        return attribute.Value


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--json', default=False, help="render configuration as JSON instead of Python dict", action='store_true')
    argparser.add_argument('reservation_id')
    args = argparser.parse_args()

    session = get_session()
    res_id = args.reservation_id

    reservation_details = session.GetReservationDetails(res_id).ReservationDescription
    resources_in_reservation = reservation_details.Resources
    services_in_reservation = reservation_details.Services

    config = {
        'target': 'tip_2x',
        'controller': {},
        'device_under_tests': [],
        'traffic_generator': {}
    }

    for service in services_in_reservation:
        if service.ServiceName != 'Helm Service V2':
            continue

        config['controller']['url'] = f'https://sec-{res_id.split("-")[0]}.cicd.lab.wlan.tip.build:16001'
        config['controller']['username'] = next(
            attr.Value for attr in service.Attributes if attr.Name == f'{service.ServiceName}.User')
        # config['controller']['password'] = next(attr.Value for attr in service.Attributes if attr.Name == f'{service.ServiceName}.Password')
        config['controller']['password'] = 'OpenWifi%123'

    for resource in resources_in_reservation:
        if resource.ResourceModelName == 'ApV2':
            details = session.GetResourceDetails(resource.Name)
            ap_config = {}

            for attribute in details.ResourceAttributes:
                key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')
                key = 'host_username' if key == 'uname' else key
                key = 'host_password' if key == 'passkey' else key
                key = 'host_ip' if key == 'ip' else key
                key = 'identifier' if key == 'serial' else key
                key = 'serial_tty' if key == 'jumphost_tty' else key
                key = 'host_ssh_port' if key == 'port' else key
                key = 'firmware_version' if key == 'version' else key


                if get_attribute_value(session, attribute) != "":
                    ap_config[key] = get_attribute_value(session, attribute)
                #ap_config[key] = get_attribute_value(session, attribute)

            #Hard coded values
            if ap_config["lan_port"]=="N/A":
                ap_config["lan_port"]= None
            if ap_config['mode']=="Wifi5":
                ap_config["supported_bands"] = ["2G","5G"]
            elif ap_config['mode'] in ["Wifi6","Wifi6E"]:
                ap_config["supported_bands"] = ["2G","5G","6G"]
            ap_config["supported_modes"] = ["BRIDGE","NAT","VLAN"]
            ap_config["ssid"] = {}
            ap_config["method"]="serial"
            config['device_under_tests'].append(ap_config)

        elif resource.ResourceModelName == 'Trafficgenerator':
            details = session.GetResourceDetails(resource.Name)
            tf_config = {}
            for attribute in details.ResourceAttributes:
                key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')

                tf_config[key] = get_attribute_value(session, attribute)

            config['traffic_generator'] = {
                'name': 'lanforge',
                'testbed': tf_config["Lab Type"].lower(),
                'scenario': "dhcp-bridge",
                'details': {
                    'manager_ip': tf_config['ip'],
                    'http_port': tf_config['port'],
                    'ssh_port': tf_config['ssh_port'],
                    'setup': {"method":"build","DB": "Test_Scenario_Automation"},
                    'wan_ports': {
                        tf_config["Upstream"]: {"addressing": "dhcp-server",
                                                "subnet": "172.16.0.1/16",
                                                "dhcp": {
                                                    "lease-first": 10,
                                                    "lease-count": 10000,
                                                    "lease-time": "6h"
                                                        }
                                                }
                    },
                    'lan_ports':{},
                    "uplink_nat_ports":{
                        tf_config["uplink"]:{
                            "addressing":"static",
                            "ip":tf_config["eth3_ip"],
                            "gateway_ip":tf_config['upstream_subnet'],
                            "ip_mask": "255.255.255.0",
                            "dns_servers": "BLANK"
                        }
                    }
                }

            }
        else:
            continue

    if args.json:
        print(json.dumps(config))
    else:
        print(repr(config))


if __name__ == '__main__':
    main()