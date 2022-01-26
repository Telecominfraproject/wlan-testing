import json
import os

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest

import argparse

from common import wait_for_provisioning_status, get_session

run_number = os.environ.get('GITHUB_RUN_NUMBER', 1)
run_id = os.environ.get('GITHUB_JOB', 'job')
workflow = os.environ.get('GITHUB_WORKFLOW', "workflow")
marker_expression = os.environ.get('MARKER_EXPRESSION', 'sanity') 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--global-inputs', help="JSON dictionary that contains global inputs that will be passed to Quali", default="{}")
    parser.add_argument('--reservation-duration', help='duration of reservation', default=360)
    parser.add_argument('--reservation-id-file', help='file that the reservation ID will be written to', default='./reservation_id.txt')
    parser.add_argument('blueprint', help='name of blueprint to create reservation from')
    args = parser.parse_args()

    session = get_session()

    global_inputs = {}
    try:
        global_inputs = json.loads(args.global_inputs)
    except json.JSONDecodeError as e:
        print(f'failed to decode global inputs: {e}')
        exit(1)

    reservation = session.CreateImmediateTopologyReservation(
        reservationName=f'{workflow}/{run_number}/{run_id}',
        owner=session.username,
        durationInMinutes=args.reservation_duration,
        topologyFullPath=args.blueprint,
        globalInputs=[UpdateTopologyGlobalInputsRequest(key, value) for key, value in global_inputs.items()]
    ).Reservation

    with open(args.reservation_id_file, 'w') as f:
        f.write(reservation.Id)

    wait_for_provisioning_status(session, reservation.Id, ['Ready'], ['Teardown'])

if __name__ == '__main__':
    main()
