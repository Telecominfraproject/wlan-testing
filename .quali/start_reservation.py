import requests
import json
import os

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

import argparse

from common import wait_for_provisioning_status, get_session

run_id = os.environ.get('GITHUB_RUN_NUMBER', 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openwifi-version', default='main')
    parser.add_argument('--openwifi-gw-version', default='master')
    parser.add_argument('--openwifi-sec-version', default='main')
    parser.add_argument('--openwifi-fms-version', default='main')
    parser.add_argument('--openwifi-ui-version', default='main')
    parser.add_argument('--ap-model', default='EC420')
    parser.add_argument('--wifi-type', default='Wifi5')
    args = parser.parse_args()


    # Login to Sandbox API and get back Authorization token to use for later calls, auth token should timeout within 10 minutes by default
    #TODO handle Quali Server host + gihtub user credentials
    url = 'http://localhost:82/api/login'
    headers = {'content-type': 'application/json'}
    data = {
        "username": "admin",
        "password": "admin",
        "domain": "Global"
    }
    response = requests.put(url, data=json.dumps(data), headers=headers)
    auth_token = response.text.replace('"', '')
    print('Basic {}'.format(auth_token))

    #TODO Handle basic lab blueprint id + quali server host + arguments for sandbox
    # Start Sandbox from Blueprint Basic Lab
    basic_lab_id = '12345678'
    url = 'http://localhost:82/api/v2/blueprints/{}/start'.format(basic_lab_id)
    headers = {'content-type': 'application/json', 'Authorization': 'Basic {}'.format(auth_token)}
    data = {
        "name": f'sanity-{run_id}',
        "duration": "PT6H5M",
        "params": [
            {
                "name": "Chart Version",
                "value": args.openwifi_version
            },
            {
                "name": "owgw Version",
                "value": args.openwifi_gw_version
            },
            {
                "name": "owsec Version",
                "value": args.openwifi_sec_version
            },
            {
                "name": "owfms Version",
                "value": args.openwifi_fms_version
            },
            {
                "name": "owgwui Version",
                "value": args.openwifi_gwui_version
            },
            {
                "name": "owprov Version",
                "value": "main"
            },
            {
                "name": "owprovui Version",
                "value": "main"
            },
            {
                "name": "Wifi type",
                "value": "[Any]"
            },
            {
                "name": "AP Model",
                "value": args.ap_model
            }
        ],
        "permitted_users": [
            "owfgithub",
            "admin"
        ]
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_dict = json.loads(response.text)
    reservation_id = response_dict['id']

    print(reservation_id)

    session = get_session()
    wait_for_provisioning_status(session, reservation_id, 'Ready')

if __name__ == '__main__':
    main()
