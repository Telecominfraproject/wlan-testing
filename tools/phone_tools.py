#!/usr/bin/python3.9
"""
    phone_tools : Tools for Phones: Reserve / Unreserve using Perfecto
    ./phone_tools --startTime 09.02.2022 13:52:00 --endTime 09.02.2022 14:19:00 --deviceId 3747365744583398
     --securityToken eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ --perfectoURL tip --action reserve --reservationNumber
"""

import time
import requests
import argparse

global default_perfectoURL
default_perfectoURL = "tip"


class PhoneTools:

    def __init__(self, startTime, endTime, deviceId, securityToken, perfectoURL):
        self.startTime = startTime
        self.endTime = endTime
        self.deviceId = deviceId
        self.securityToken = securityToken
        self.perfectoURL = perfectoURL

    # Creates a reservation based on the deviceID.
    # Returns reservationId if the reservation is successful.Returns an empty string if the request is not successful
    def reserve(self):
        pattern = '%d.%m.%Y %H:%M:%S'
        startTime = int(time.mktime(time.strptime(self.startTime, pattern))) * 1000
        endTime = int(time.mktime(time.strptime(self.endTime, pattern))) * 1000
        perfecto_mobile_url = "https://{}.perfectomobile.com/services/reservations?Operation=create&securityToken={}&StartTime={}&EndTime={}&ResourceIds={}".format(
            self.perfectoURL, self.securityToken, str(startTime), str(endTime), self.deviceId)
        print("url" + perfecto_mobile_url)
        resp = requests.get(url=perfecto_mobile_url)
        if resp.status_code == 200:
            print("Request was successful")
            data = resp.json()
            reservationId = data["reservationIds"][0]
            print("ReservationId: {}".format(reservationId))
            return reservationId
        else:
            print("Request was not successful")
            print(resp.content)
            return ""

    # Deletes an already created reservation
    # E.g. perfecto_device_reservation.delete(request,"114").This reservationId is returned from 'reserve' function
    # Returns True if the request is successfully deleted, False otherwise
    def unreserve(self, reservationId):
        url = "https://{}.perfectomobile.com/services/reservations/{}?operation=delete&securityToken={}".format(
            self.perfectoURL, reservationId, self.securityToken)
        resp = requests.get(url=url)
        if resp.status_code == 200:
            print("Request was successful. Successfully deleted reservation {}".format(reservationId))
            return True
        else:
            print("Request was not successful.Not able to delete reservation {}".format(reservationId))
            print(resp.content)
            return ""


def main():
    parser = argparse.ArgumentParser(prog="phone_tools",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About phone_tools.py",
                                     description="Tools for Phones on Perfecto")
    parser.add_argument('--startTime', type=str,
                        help=' --host : when to start perfecto phone reservation Format: 09.02.2022 13:52:00')
    parser.add_argument('--endTime', type=str,
                        help=' --when to end perfecto phone reservation Format: 09.02.2022 13:52:00')
    parser.add_argument('--deviceId', type=str, help=' --serial number of the phone')
    parser.add_argument('--securityToken', type=str,
                        help='--users security token to access perfecto. Obtain this from your perfecto login.')
    parser.add_argument('--perfectoURL', type=str,
                        help='-- identifier token for perfecto URL Ex: tip for Telecom Infrastructure Project',
                        default="tip")
    parser.add_argument('--action', type=str, help='--either reserve / unreserve (decides action on phone)',
                        default="reserve")
    parser.add_argument('--reservationNumber', type=str, help='--for reserve it is "" / for unreserve it is the perfecto reservationID of the reserved phone',
                        default="reserve")

    args = parser.parse_args()
    ph_tools = PhoneTools(startTime=args.startTime, endTime=args.endTime, deviceId=args.deviceId,
                          securityToken=args.securityToken, perfectoURL=args.perfectoURL)
    if args.action == "reserve":
        reservationNumber = ph_tools.reserve()
        print(reservationNumber)
    elif args.action == "unreserve":
        ph_tools.unreserve(args.reservationNumber)
    else:
        print("Invalid action input")


if __name__ == '__main__':
    main()
