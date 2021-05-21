import os
import time

from cloudshell.api.cloudshell_api import CloudShellAPISession

TIMEOUT=1200

def get_session() -> CloudShellAPISession:
    url = os.environ['CLOUDSHELL_URL']
    user = os.environ['CLOUDSHELL_USER']
    password = os.environ['CLOUDSHELL_PASSWORD']

    return CloudShellAPISession(url, user, password, "Global")

def __wait_for_status(session, res_id, field, target_status):
    timer = 0
    sleep_time = 5
    while True:
        status = session.GetReservationStatus(res_id).ReservationSlimStatus.__dict__[field]

        if status == target_status:
            break

        if timer >= TIMEOUT:
            raise RuntimeError(f'waiting for reservation to reach status {target_status} timed out')

        time.sleep(sleep_time)
        timer += sleep_time

def wait_for_provisioning_status(session, res_id, target_status):
    __wait_for_status(session, res_id, 'ProvisioningStatus', target_status)

def wait_for_reservation_status(session, res_id, target_status):
    __wait_for_status(session, res_id, 'Status', target_status)
