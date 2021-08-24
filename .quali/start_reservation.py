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
        durationInMinutes=60,
        topologyFullPath='PyTest Attributes Testing',
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Cloud Controller Version', '1.1.0-RC1'),
        ],
        #requirementsInputs=[
        #    UpdateTopologyRequirementsInputsRequest('Access Point', 'Ap.OS Version', 'latest', 'Attributes'),
        #]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
