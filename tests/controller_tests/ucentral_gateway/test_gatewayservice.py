"""

    UCentral Gateway Services Rest API Tests

"""
import pytest
import json
import allure


@pytest.mark.uc_sanity
@allure.feature("SDK REST API")
class TestUcentralGatewayService(object):
    """
    """

    @pytest.mark.sdk_restapi
    def test_gwservice_listdevices(self, setup_controller):
        """
            Test the list devices endpoint
            WIFI-3452
        """
        resp = setup_controller.request("gw", "devices", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw list devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

    @pytest.mark.sdk_restapi
    def test_gwservice_createdevice(self, setup_controller):
        """
            Test the create device endpoint
            WIFI-3453
        """
        configuration = {'uuid': '1'}
        payload = {'serialNumber': 'DEADBEEF0011',
                   'UUID': '123456',
                   'configuration': configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': 'DE:AD:BE:EF:00:11',
                   'manufacturer': 'Testing',
                   'owner': ''}
        print(json.dumps(payload))
        resp = setup_controller.request("gw", "device/DEADBEEF0011", "POST", None, json.dumps(payload))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_controller.request("gw", "device/DEADBEEF0011", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.request("gw", "device/DEADBEEF0011", "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device delete", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.sdk_restapi
    def test_gwservice_updatedevice(self, setup_controller):
        """
            Test the update device endpoint
            WIFI-3454
        """
        configuration = {'uuid': '1'}
        payload = {'serialNumber': 'DEADBEEF0011',
                   'UUID': '123456',
                   'configuration': configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': 'DE:AD:BE:EF:00:11',
                   'manufacturer': 'Testing',
                   'owner': ''}
        resp = setup_controller.request("gw", "device/DEADBEEF0011", "POST", None, json.dumps(payload))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        payload = {'serialNumber': 'DEADBEEF0011',
                   'owner': 'pytest'}
        resp = setup_controller.request("gw", "device/DEADBEEF0011", "PUT", None, json.dumps(payload))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw get device", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.request("gw", "device/DEADBEEF0011", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device verify", body=body)
        if resp.status_code != 200:
            assert False

        device = json.loads(resp.text)
        print(device)

        resp = setup_controller.request("gw", "device/DEADBEEF0011", "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw get device", body=body)
        if resp.status_code != 200:
            assert False

        @pytest.mark.sdk_restapi
        def test_gwservice_deletedevice(self, setup_controller):
            """
                Test the delete device endpoint
                WIFI-3455
            """
            configuration = {'uuid': '1'}
            payload = {'serialNumber': 'DEADBEEF0011',
                       'UUID': '123456',
                       'configuration': configuration,
                       'deviceType': 'AP',
                       'location': '',
                       'macAddress': 'DE:AD:BE:EF:00:11',
                       'manufacturer': 'Testing',
                       'owner': ''}
            resp = setup_controller.request("gw", "device/DEADBEEF0011", "POST", None, json.dumps(payload))
            body = resp.url + "," + str(resp.status_code) + ',' + resp.text
            allure.attach(name="gw create devices", body=body)
            if resp.status_code != 200:
                assert False
            devices = json.loads(resp.text)
            print(devices)

            resp = setup_controller.request("gw", "device/DEADBEEF0011", "DELETE", None, None)
            body = resp.url + "," + str(resp.status_code) + ',' + resp.text
            allure.attach(name="gw get device", body=body)
            if resp.status_code != 200:
                assert False
