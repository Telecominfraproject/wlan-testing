import json
import os

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

from common import wait_for_provisioning_status, get_session

run_id = os.environ.get('GITHUB_RUN_NUMBER', 1)

def main():
    session = get_session()

    reservation = session.CreateImmediateTopologyReservation(
        reservationName=f'sanity-{run_id}',
        owner=session.username,
        durationInMinutes=180,
        topologyFullPath='Basic Lab',
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Chart Version', 'main'),
            UpdateTopologyGlobalInputsRequest('ucentralgw Version', 'main'),
            UpdateTopologyGlobalInputsRequest('ucentralsec Version', 'main'),
            UpdateTopologyGlobalInputsRequest('ucentralfms Version', 'main'),
            UpdateTopologyGlobalInputsRequest('ucentralgwui Version', 'main'),
            UpdateTopologyGlobalInputsRequest('AP Model', 'EC420'),
            UpdateTopologyGlobalInputsRequest('Wifi type', 'Wifi5'),
        ]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
