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
        'controller': {},
        'access_point': [],
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
                key = 'username' if key == 'uname' else key
                key = 'password' if key == 'passkey' else key

                if get_attribute_value(session, attribute) != "":
                    ap_config[key] = get_attribute_value(session, attribute)
                #ap_config[key] = get_attribute_value(session, attribute)

            config['access_point'].append(ap_config)

        elif resource.ResourceModelName == 'Trafficgenerator':
            details = session.GetResourceDetails(resource.Name)
            tf_config = {}
            for attribute in details.ResourceAttributes:
                key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')

                tf_config[key] = get_attribute_value(session, attribute)

            config['traffic_generator'] = {
                'name': 'lanforge',
                'details': {
                    'ip': tf_config['ip'],
                    'port': tf_config['port'],
                    'ssh_port': tf_config['ssh_port'],
                    '2.4G-Radio': tf_config['lf_2dot4G_Radio'].replace(' ', '').split(','),
                    '5G-Radio': tf_config['lf_5G_Radio'].replace(' ', '').split(','),
                    'AX-Radio': tf_config['AX_Radio'].replace(' ', '').split(','),
                    'upstream': tf_config['Upstream'],
                    'upstream_subnet': tf_config['upstream_subnet'],
                    'uplink': tf_config['uplink'],
                    '2.4G-Station-Name': tf_config['lf_2dot4G_Station_Name'],
                    '5G-Station-Name': tf_config['lf_5G_Station_Name'],
                    'AX-Station-Name': tf_config['AX_Station_Name']
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