'''This file will have perfecto reservation related functions'''
import time
import requests

# Creates a reservation based on the deviceID.
#E.g. perfecto_device_reservation.reservation_device(request,"09.02.2022 13:52:00","09.02.2022 14:19:00", "3747365744583398")
def reservation_device(request, startTime, endTime, deviceId):
    pattern = '%d.%m.%Y %H:%M:%S'
    startTime = int(time.mktime(time.strptime(startTime, pattern)))*1000
    endTime = int(time.mktime(time.strptime(endTime, pattern)))*1000
    securityToken = request.config.getini("securityToken")
    perfectoURL = request.config.getini("perfectoURL")
    url = f"https://{perfectoURL}.perfectomobile.com/services/reservations?Operation=create&securityToken={securityToken}&StartTime=" + str(startTime) + "&EndTime=" + str(endTime) + "&ResourceIds=" + deviceId
    print("url" + url)
    resp = requests.get(url=url)
    if resp.status_code == 200:
        print("Request was successful")
    else:
        print("Request was not successful")
        print(resp.content)