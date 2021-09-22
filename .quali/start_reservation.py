import json
import os

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

import argparse

from common import wait_for_provisioning_status, get_session

run_id = os.environ.get('GITHUB_RUN_NUMBER', 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ucentral-version', default='main')
    parser.add_argument('--ucentral-gw-version', default='master')
    parser.add_argument('--ucentral-sec-version', default='main')
    parser.add_argument('--ucentral-fms-version', default='main')
    parser.add_argument('--ucentral-ui-version', default='main')
    parser.add_argument('--ap-model', default='EC420')
    parser.add_argument('--wifi-type', default='Wifi5')
    args = parser.parse_args()

    session = get_session()

    reservation = session.CreateImmediateTopologyReservation(
        reservationName=f'sanity-{run_id}',
        owner=session.username,
        durationInMinutes=360,
        topologyFullPath='Basic Lab',
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Chart Version', args.ucentral_version),
            UpdateTopologyGlobalInputsRequest('ucentralgw Version', args.ucentral_gw_version),
            UpdateTopologyGlobalInputsRequest('ucentralsec Version', args.ucentral_sec_version),
            UpdateTopologyGlobalInputsRequest('ucentralfms Version', args.ucentral_fms_version),
            UpdateTopologyGlobalInputsRequest('ucentralgwui Version', args.ucentral_ui_version),
            UpdateTopologyGlobalInputsRequest('AP Model', args.ap_model),
            UpdateTopologyGlobalInputsRequest('Wifi type', args.wifi_type),
        ]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
