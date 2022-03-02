#!/usr/bin/python3.9
"""
    ap_tools : Tools for Access Point
                reboot, run_cmd, etc
    ./ap_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action reboot
    ./ap_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action run_cmd --cmd ls
"""
import time
import requests
import argparse
global default_perfectoURL
default_perfectoURL = "tip"


class PhoneTools:

    def __init__(self, startTime, endTime, deviceId, securityToken, perfectoURL):
        self.startTime = startTime
        self.deviceId = deviceId
        self.securityToken = securityToken
        self.perfectoURL = perfectoURL

    def reserve(self):
        pattern = '%d.%m.%Y %H:%M:%S'
        startTime = int(time.mktime(time.strptime(self.startTime, pattern))) * 1000
        endTime = int(time.mktime(time.strptime(self.endTime, pattern))) * 1000
        url = "https://{}.perfectomobile.com/services/reservations?Operation=create&securityToken={}&StartTime={}&EndTime={}&ResourceIds={}".format(self.perfectoURL,self.securityToken,str(self.startTime),str(self.endTime),self.deviceId)
        print("url" + url)
        resp = requests.get(url=url)
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




def main():
    parser = argparse.ArgumentParser(prog="phone_tools",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About phone_tools.py",
                                     description="Tools for Phones on Perfecto")
    parser.add_argument('--startTime', type=str, help=' --host : when to start perfecto phone reservation')
    parser.add_argument('--endTime', type=str, help=' --when to end perfecto phone reservation')
    parser.add_argument('--deviceId', type=str, help=' --serial number of the phone')
    parser.add_argument('--securityToken', type=str, help='--users security token to access perfecto ')
    parser.add_argument('--perfectoURL', type=str, help='--url for perfecto', default="tip")
    args = parser.parse_args()
    print(args.tty)
    ph_tools = PhoneTools(startTime=args.startTime, endTime=args.endTime, deviceId=args.deviceId,
                       securityToken=args.securityToken, perfectoURL=args.perfectoURL)
    ph_tools.reserve()


if __name__ == '__main__':
    main()