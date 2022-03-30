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


def refine(s):
    parts = s.split(" ")
    part1 = parts[0]
    part2 = parts[-1]
    part2_clean = ''.join(e for e in part2 if e.isalnum())
    return part1 + "-" + part2_clean


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

    pf_details = {}


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

                ap_config[key] = get_attribute_value(session, attribute)

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

        # Perfecto Details

        input_map = {}
        inputs = session.GetReservationInputs(reservationId=res_id).GlobalInputs
        for given_input in inputs:
            input_map[given_input.ParamName] = given_input.Value

        pf_details['securityToken'] = input_map['securityToken']
        pf_details["projectName"]: "TIP-PyTest-Execution"
        pf_details["projectVersion"] = "1.0"
        pf_details["reportTags"] = "TestTag"
        pf_details["perfectoURL"] = input_map["perfectoURL"]
        for resource in session.GetReservationDetails(reservationId=res_id).ReservationDescription.Resources:
            if resource.ResourceModelName == 'Phone':
                details = session.GetResourceDetails(resource.Name)
                phone_config = {}
                for attribute in details.ResourceAttributes:
                    key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')
                    phone_config[key] = get_attribute_value(session, attribute)
                if phone_config["OS"] == "iOS":
                    pf_details[phone_config['model']] = \
                        {
                            "model-iOS": phone_config['model'],
                            "bundleId-iOS": "com.apple.Preferences",
                            "platformName-iOS": phone_config['OS'],
                            "bundleId-iOS-Settings": "com.apple.Preferences",
                            "bundleId-iOS-Ping": "com.deftapps.ping",
                            "browserType-iOS": "Safari",
                            "bundleId-iOS-Safari": "com.apple.mobilesafari",
                            "platformName-android": "Android",
                            "appPackage-android": "com.android.settings",
                            "jobName": "Interop-" + phone_config['model'],
                            "jobNumber": 38
                        }
                elif phone_config["OS"] == "Android":
                    pf_details[phone_config['model']] = \
                        {
                            "platformName-android": phone_config["OS"],
                            "model-android": phone_config["model"],
                            "appPackage-android": "com.android.settings",
                            "bundleId-iOS-Settings": "com.apple.Preferences",
                            "bundleId-iOS-Safari": "com.apple.mobilesafari",
                            "jobName": "Interop-" + refine(phone_config['model']),
                            "jobNumber": 38
                        }
            else:
                continue

        entire_config = {"interop": config, "PERFECTO_DETAILS": pf_details}
        if args.json:
            print(json.dumps(entire_config))
        else:
            print(repr(config))


if __name__ == '__main__':
    main()
