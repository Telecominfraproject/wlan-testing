'''This file will have perfecto reservation related functions'''
import time
import requests

# Creates a reservation based on the deviceID.
# E.g. perfecto_device_reservation.reservation_device(request,"09.02.2022 13:52:00","09.02.2022 14:19:00", "3747365744583398")
# Returns reservationId if the reservation is successful.Returns an empty string if the request is not successful
def create(request, startTime, endTime, deviceId):
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
        data = resp.json()
        reservationId = data["reservationIds"][0]
        print(f"ReservationId: {reservationId}")
        return reservationId
    else:
        print("Request was not successful")
        print(resp.content)
        return ""

# Deletes an already created reservation
# E.g. perfecto_device_reservation.delete(request,"114").This reservationId is returned from 'create' function
# Returns True if the request is successfully deleted, False otherwise
def delete(request, reservationId):
    securityToken = request.config.getini("securityToken")
    perfectoURL = request.config.getini("perfectoURL")
    url = f"https://{perfectoURL}.perfectomobile.com/services/reservations/{reservationId}?operation=delete&securityToken={securityToken}"
    resp = requests.get(url=url)
    if resp.status_code == 200:
        print(f"Request was successful. Successfully deleted reservation {reservationId}")
        return True
    else:
        print(f"Request was not successful.Not able to delete reservation {reservationId}")
        print(resp.content)
        return ""

# Updates an already created reservation
# E.g. perfecto_device_reservation.update(request,"15.02.2022 14:52:00","15.02.2022 15:19:00", "117").This reservationId is returned from 'create' function
# Returns True if the request is successfully updated, False otherwise
def update(request, startTime, endTime, reservationId):
    pattern = '%d.%m.%Y %H:%M:%S'
    startTime = int(time.mktime(time.strptime(startTime, pattern)))*1000
    endTime = int(time.mktime(time.strptime(endTime, pattern)))*1000
    securityToken = request.config.getini("securityToken")
    perfectoURL = request.config.getini("perfectoURL")
    url = f"https://{perfectoURL}.perfectomobile.com/services/reservations/{reservationId}?Operation=update&securityToken={securityToken}&StartTime=" + str(startTime) + "&EndTime=" + str(endTime)
    print("url" + url)
    resp = requests.get(url=url)
    if resp.status_code == 200:
        print(f"Request was successful. Successfully updated the reservation {reservationId}")
        data = resp.json()
        return True
    else:
        print(f"Request was not successful.Not able to delete reservation {reservationId}")
        print(resp.content)
        return False
