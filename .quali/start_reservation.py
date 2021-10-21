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
    parser.add_argument('--openwifi-prov-version', default='main')
    parser.add_argument('--openwifi-provui-version', default='main')
    parser.add_argument('--ap-model', default='EC420')
    #parser.add_argument('--wifi-type', default='Wifi5')
    args = parser.parse_args()

    session = get_session()

    reservation = session.CreateImmediateTopologyReservation(
        reservationName=f'sanity-{run_id}',
        owner=session.username,
        durationInMinutes=360,
        topologyFullPath='Basic Lab',
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Chart Version', args.openwifi_version),
            UpdateTopologyGlobalInputsRequest('owgw Version', args.openwifi_gw_version),
            UpdateTopologyGlobalInputsRequest('owsec Version', args.openwifi_sec_version),
            UpdateTopologyGlobalInputsRequest('owfms Version', args.openwifi_fms_version),
            UpdateTopologyGlobalInputsRequest('owgwui Version', args.openwifi_ui_version),
            UpdateTopologyGlobalInputsRequest('owprov Version', args.openwifi_prov_version),
            UpdateTopologyGlobalInputsRequest('owprovui Version', args.openwifi_provui_version),
            UpdateTopologyGlobalInputsRequest('AP Model', args.ap_model),
            #UpdateTopologyGlobalInputsRequest('Wifi type', args.wifi_type),
        ]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
