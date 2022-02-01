import os
import time

from cloudshell.api.cloudshell_api import CloudShellAPISession

TIMEOUT=3600

def get_session() -> CloudShellAPISession:
    url = os.environ['CLOUDSHELL_URL']
    user = os.environ['CLOUDSHELL_USER']
    password = os.environ['CLOUDSHELL_PASSWORD']

    return CloudShellAPISession(url, user, password, "Global")

def __wait_for_status(session, res_id, field, target_statuses=[], exit_statuses=[]):
    timer = 0
    sleep_time = 5
    while True:
        status = session.GetReservationStatus(res_id).ReservationSlimStatus.__dict__[field]

        if status in target_statuses:
            print(f'reached target status: {status}')
            break

        if status in exit_statuses:
            print(f'reached exit status: {status}')
            exit(1)

        print(f'current reservation status: {status}')

        if timer >= TIMEOUT:
            raise RuntimeError(f'waiting for reservation to reach one of {target_statuses} or {exit_statuses} statuses timed out')

        time.sleep(sleep_time)
        timer += sleep_time

def wait_for_provisioning_status(session, res_id, target_statuses, exit_statuses=[]):
    __wait_for_status(session, res_id, 'ProvisioningStatus', target_statuses, exit_statuses)

def wait_for_reservation_status(session, res_id, target_statuses, exit_statuses=[]):
    __wait_for_status(session, res_id, 'Status', target_statuses, exit_statuses)
