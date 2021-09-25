import json
import sys

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

from common import get_session

def main():
    session = get_session()
    res_id = sys.argv[1]

    reservation_details = session.GetReservationDetails(res_id).ReservationDescription
    resources_in_reservation = reservation_details.Resources
    services_in_reservation = reservation_details.Services

    config = {
        'controller': {},
        'access_point':[],
        'traffic_generator': {}
    }

    for service in services_in_reservation:
        if service.ServiceName != 'Helm Service V2':
            continue

        config['controller']['url'] = f'https://sec-ucentral-{res_id.split("-")[0]}.cicd.lab.wlan.tip.build:16001'
        config['controller']['username'] = next(attr.Value for attr in service.Attributes if attr.Name == f'{service.ServiceName}.User')
        #config['controller']['password'] = next(attr.Value for attr in service.Attributes if attr.Name == f'{service.ServiceName}.Password')
        config['controller']['password'] = 'openwifi'

    for resource in resources_in_reservation:
        if resource.ResourceModelName == 'Ap':
            details = session.GetResourceDetails(resource.Name)
            ap_config = {}

            for attribute in details.ResourceAttributes:
                key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')
                key = 'username' if key == 'uname' else key
                key = 'password' if key == 'passkey' else key

                if attribute.Type == 'Boolean':
                    value = True if attribute.Value == 'True' else False
                elif attribute.Type == 'Numeric':
                    value = int(attribute.Value)
                else:
                    value = attribute.Value
    
                ap_config[key] = value

            config['access_point'].append(ap_config)

        elif resource.ResourceModelName == 'Trafficgenerator':
            details = session.GetResourceDetails(resource.Name)
            tf_config = {}
            for attribute in details.ResourceAttributes:
                key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')

                if attribute.Type == 'Boolean':
                    value = True if attribute.Value == 'True' else False
                elif attribute.Type == 'Numeric':
                    value = int(attribute.Value)
                else:
                    value = attribute.Value
    
                tf_config[key] = value

            config['traffic_generator'] = {
                'name': 'lanforge',
                'details': {
                    'ip': tf_config['ip'],
                    'port': tf_config['port'],
                    'ssh_port': tf_config['ssh_port'],
                    '2.4G-Radio': [tf_config['lf_2dot4G_Radio']],
                    '5G-Radio': [tf_config['lf_5G_Radio']],
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

    print(repr(config))

if __name__ == '__main__':
    main()
