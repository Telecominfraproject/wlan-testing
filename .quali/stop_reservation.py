import sys

from common import wait_for_reservation_status, get_session

def main():
    session = get_session()
    res_id = sys.argv[1]
    session.EndReservation(res_id)
    wait_for_reservation_status(session, res_id, ['Completed'])

if __name__ == '__main__':
    main()
