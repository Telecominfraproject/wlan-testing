import time

import allure
import pytest


@pytest.mark.uc_sanity
@allure.feature("SDK REST API")
@pytest.mark.gateway_ap_api
class TestAP(object):

    def test_ap_reboot(self, setup_controller, get_configuration, get_apnos):
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw)
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("Connected:")
            print(connected)
            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
        allure.attach(name="Status before reboot(Uci show ucentral):", body=str(gw))
        allure.attach(name="Status before reboot(ubus call ucentral status):", body=str(connected))
        allure.attach(name="Status before reboot(iwinfo):", body=str(iwinfo))
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "when": 0
                }
        resp = setup_controller.ap_reboot(device_name, payload)
        time.sleep(150)
        print(resp.json())
        allure.attach(name="Reboot", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw1 = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw1)
            connected1, latest1, active1 = ap_ssh.get_ucentral_status()
            print("Connected1:")
            print(connected1)
            iwinfo1 = ap_ssh.get_iwinfo()
            print("iwinfo1:")
            print(iwinfo1)
        allure.attach(name="Status after reboot(Uci show ucentral):", body=str(gw1))
        allure.attach(name="Status after reboot(ubus call ucentral status):", body=str(connected1))
        allure.attach(name="Status after reboot(iwinfo):", body=str(iwinfo1))
        assert (resp.status_code == 200) & (gw == gw1) & (connected == connected1) & (iwinfo == iwinfo1)

    def test_ap_factory_reset(self, setup_controller, get_configuration, get_apnos):
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw)
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("Connected:")
            print(connected)
            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
        allure.attach(name="Status before factory reset(Uci show ucentral):", body=str(gw))
        allure.attach(name="Status before factory reset(ubus call ucentral status):", body=str(connected))
        allure.attach(name="Status before factory reset(iwinfo):", body=str(iwinfo))
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "when": 0,
                  "keepRedirector": True
                }
        resp = setup_controller.ap_factory_reset(device_name, payload)
        time.sleep(200)
        print(resp.json())
        allure.attach(name="Factory Reset", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw1 = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw1)
            connected1, latest1, active1 = ap_ssh.get_ucentral_status()
            print("Connected1:")
            print(connected1)
            iwinfo1 = ap_ssh.get_iwinfo()
            print("iwinfo1:")
            print(iwinfo1)
        allure.attach(name="Status after factory reset(Uci show ucentral):", body=str(gw1))
        allure.attach(name="Status after factory reset(ubus call ucentral status):", body=str(connected1))
        allure.attach(name="Status after factory reset(iwinfo):", body=str(iwinfo1))
        assert (resp.status_code == 200) & (gw == gw1) & (connected == connected1) & (iwinfo == iwinfo1)