import os
import time

from cloudshell.api.cloudshell_api import CloudShellAPISession

TIMEOUT=600

def get_session():
    url = os.environ['CLOUDSHELL_URL']
    user = os.environ['CLOUDSHELL_USER']
    password = os.environ['CLOUDSHELL_PASSWORD']

    return CloudShellAPISession(url, user, password, "Global")


def wait_for_reservation_status(session, res_id, target_status):
    timer = 0
    sleep_time = 5
    while True:
        status = session.GetReservationStatus(res_id).ReservationSlimStatus.ProvisioningStatus

        if status == target_status:
            break

        if timer >= TIMEOUT:
            raise RuntimeError(f'waiting for reservation to reach status {target_status} timed out')

        time.sleep(sleep_time)
        timer += sleep_time
