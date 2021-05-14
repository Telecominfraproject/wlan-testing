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
        topologyFullPath='Basic Lab',
        globalInputs=[
            UpdateTopologyGlobalInputsRequest('Cloud Controller Version', '1.1.0-RC1'),
        ],
        requirementsInputs=[
            UpdateTopologyRequirementsInputsRequest('Access Point', 'Ap.Wifi type', 'Wifi5', 'Attributes'),
            UpdateTopologyRequirementsInputsRequest('Access Point', 'Ap.AP Model', 'ECW5410', 'Attributes')
        ]
    ).Reservation

    print(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, 'Ready')

if __name__ == '__main__':
    main()
