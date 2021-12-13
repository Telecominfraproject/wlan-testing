import os

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest

import argparse

from common import wait_for_provisioning_status, get_session

run_id = os.environ.get('GITHUB_RUN_NUMBER', 1)
marker_expression = os.environ.get('MARKER_EXPRESSION', 'sanity') 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openwifi-version', default='main')
    parser.add_argument('--openwifi-gw-version', default='master')
    parser.add_argument('--openwifi-sec-version', default='main')
    parser.add_argument('--openwifi-fms-version', default='main')
    parser.add_argument('--openwifi-ui-version', default='main')
    parser.add_argument('--ap-model', default='[Any]')
    parser.add_argument('--wifi-type', default='[Any]')
    parser.add_argument('--blueprint', default='Basic Lab')
    args = parser.parse_args()

    session = get_session()

    reservation = session.CreateImmediateTopologyReservation(
        reservationName=f'{marker_expression}-{run_id}',
        owner=session.username,
        if marker_expression == 'advance':
          durationInMinutes=1440,
        else:
          durationInMinutes=360,
        topologyFullPath=args.blueprint,
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Chart Version', args.openwifi_version),
            UpdateTopologyGlobalInputsRequest('owgw Version', args.openwifi_gw_version),
            UpdateTopologyGlobalInputsRequest('owsec Version', args.openwifi_sec_version),
            UpdateTopologyGlobalInputsRequest('owfms Version', args.openwifi_fms_version),
            UpdateTopologyGlobalInputsRequest('owgwui Version', args.openwifi_ui_version),
            UpdateTopologyGlobalInputsRequest('AP Model', args.ap_model),
            UpdateTopologyGlobalInputsRequest('Wifi type', args.wifi_type),
        ]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
