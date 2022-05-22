import datetime
import os
import sys
import time

""" Environment Paths """
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)

from controller.controller_2x.controller import Controller
from controller.controller_2x.controller import UProfileUtility

controller = {
    'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
    'username': "tip@ucentral.com",
    'password': 'OpenWifi%123',
}
SERIAL_NUMBERS = [
                  "0006aee53b84",
                  "001122090801",
                  "706dec0a8a79",
                  "68215fda456d",
                  "0000c1018812",
                  "903cb39d6918",
                  "903cb36ae223",
                  "089b4bb2f10c",
                  "f40b9fe78e03"
                  ]
RADIUS_SERVER_DATA = {
    "ip": "10.10.1.221",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}
RADIUS_ACCOUNTING_DATA= {
    "ip": "10.10.1.221",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}
setup_params = [
    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_psk_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk"},
            {"ssid_name": "ssid_psk_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_psk2_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk2"},
            {"ssid_name": "ssid_psk2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_sae_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "sae"},
            {"ssid_name": "ssid_sae_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "sae"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "none"},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "none"}],
        "radius": False
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa2"},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "wpa2"}],
        "radius": True
    },

    {
        "mode": "BRIDGE",
        "ssids": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa3"},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "wpa3"}],
        "radius": True
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_psk_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk"},
            {"ssid_name": "ssid_psk_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_psk2_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "psk2"},
            {"ssid_name": "ssid_psk2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_sae_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "sae"},
            {"ssid_name": "ssid_sae_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "sae"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "none"},
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "none"}],
        "radius": False
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa2"},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa2"}],
        "radius": True
    },

    {
        "mode": "NAT",
        "ssids": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something", "security": "wpa3"},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something",
             "security": "wpa3"}],
        "radius": True
    },

]

if __name__ == '__main__':
    while True:
        for config in setup_params:
            obj = Controller(controller_data=controller)
            up = UProfileUtility(sdk_client=obj, controller_data=controller)
            up.set_mode(config["mode"])
            up.set_radio_config()
            radius = config["radius"]
            for ssid in config["ssids"]:
                if radius:
                    up.add_ssid(ssid_data=ssid, radius=radius, radius_auth_data=RADIUS_SERVER_DATA, radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                else:
                    up.add_ssid(ssid_data=ssid)
            for serial in SERIAL_NUMBERS:
                status = up.push_config(serial_number=serial)
                if status.status_code != 200:
                    sys.exit("Configure Command failed at " + str(datetime.datetime.utcnow()))
                if status.status_code == 200:
                    print("Configure command success: ", serial, " Time: " + str(datetime.datetime.utcnow()))
            print("Sleeping 20 Sec before Next Config")
            time.sleep(30)
            obj.logout()