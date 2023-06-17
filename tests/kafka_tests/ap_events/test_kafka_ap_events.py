"""
    Test Case Module:  Testing Kafka messages for AP events
"""
import json
import os
import random
import re
import time
import allure
import pytest
import requests
import logging
import datetime
import paramiko

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'test-config.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data = json.loads(json_string)


@allure.feature("Test Real TIme AP Events using Kafka")
@allure.title("Real Time AP Events")
@pytest.mark.ap_events
class TestKafkaApEvents(object):
    # Pytest unit test for validating Kafka healthcheck messages
    @allure.title("Test Firmware Upgrade from Version x to Version y")
    @pytest.mark.fw_upgrade_xy
    def test_kafka_fw_upgrade_xy(self, get_target_object, kafka_consumer_deq):
        # Consume messages and validate them
        url = get_target_object.firmware_library_object.sdk_client.build_url_fms(path="firmwares")
        firmware_list = {}
        devices = []
        is_valid = False
        msg_found = False
        payload_msg = ""
        record_messages = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            ap_model = get_target_object.firmware_library_object.ap_model_lookup(
                model=get_target_object.device_under_tests_info[ap]['model'])
            devices.append(ap_model)
            # check the current AP Revision before upgrade
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).replace("\n", "")
            params = "limit=500" + \
                     "&deviceType=" + ap_model + \
                     "&offset=0"
            response = requests.get(url, params=params, verify=False, timeout=120,
                                    headers=get_target_object.firmware_library_object.sdk_client.make_headers())

            firmwares = response.json()
            if response.status_code == 200:
                # Remove the current AP Revision from the firmwares list
                if len(firmwares['firmwares']) > 0:
                    firmware_list[f"{ap_model}"] = [f for f in firmwares['firmwares'] if
                                                    f["revision"] != current_version]
                else:
                    pytest.fail("No firmware found to upgrade")
            else:
                pytest.fail("Test failed - Error Code: " + response.status_code + f" - {response.reason}")
            firmware_uri = firmware_list[ap_model][random.randint(0, len(firmware_list[ap_model]))]['uri']
            payload = "{ \"serialNumber\" : " + "\"" + \
                      get_target_object.device_under_tests_info[ap]["identifier"] + "\"" + " , \"uri\" : " \
                      + "\"" + firmware_uri \
                      + "\"" + ", \"when\" : 0" \
                      + " }"
            command = "device/" + get_target_object.device_under_tests_info[ap]["identifier"] + "/upgrade"
            url = get_target_object.firmware_library_object.sdk_client.build_uri(path=command)
            upgrade_response = requests.post(url, data=payload,
                                             headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                             verify=False, timeout=120)
            if upgrade_response.status_code == 200:
                logging.info("Firmware Upgrade request Applied")
            logging.info("wait for 300 sec to finish Firmware Upgrade")
            logging.info("Request : POST {}".format(url) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "URI: " + str(url) + "\n" +
                         "Data: " + str(payload) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="firmware upgrade: \n", body="Sending Command: POST " + str(url) + "\n" +
                                                            "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                            "Data: " + str(payload) + "\n" +
                                                            "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))

            timeout = 300  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'payload' in record.value['payload']:
                                payload_msg = record.value['payload']['payload']
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == 'unit.firmware_change':
                                    logging.info(f"unit.firmware_change has found in the Message")
                                    old_firmware = payload_msg['oldFirmware']
                                    new_firmware = payload_msg['newFirmware']
                                    is_valid = True
                                    allure.attach(
                                        name="Check Kafka Message for Firmware Upgrade from Version X to Version Y",
                                        body=str(record))
                                    allure.attach(name='old firmware', body=str(old_firmware))
                                    allure.attach(name='new firmware', body=str(new_firmware))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'Message not found'

    @allure.title("Test Wifi Start Event")
    @pytest.mark.wifi_start
    def test_kafka_wifi_start_event(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "wifi.start"
        record_messages = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'wifi.start' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"].append('wifi.start')
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Wifi Start Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test Wifi Stop Event")
    @pytest.mark.wifi_stop
    def test_kafka_wifi_stop_event(self, get_target_object, kafka_consumer_deq, get_test_library):
        is_valid = False
        msg_found = False
        payload_msg = "wifi.stop"
        record_messages = []
        client_created = False
        ssid, passwd = config_data["interfaces"][0]["ssids"][0]["name"], \
            config_data["interfaces"][0]["ssids"][0]["encryption"]["key"]
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'wifi.stop' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"] = ['wifi.start', 'wifi.stop']
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
            timeout = 120  # Timeout in seconds
            start_time = time.time()
            run_once = False
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # create a client to identify wifi stop event from kafka log
                if not client_created:
                    sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd,
                                                                              security="wpa2",
                                                                              mode="BRIDGE", radio="wiphy0",
                                                                              station_name=["sta100"],
                                                                              create_vlan=False)
                    if not sta_created:
                        logging.info("Failed to create station")
                        pytest.fail("Station creation failed")
                    else:
                        client_created = True
                if client_created:
                    get_test_library.client_disconnect(station_name=["sta100"])
                # Apply config to check whether wifi-stop event has occurred or not
                if not run_once:
                    resp = requests.post(uri, data=json.dumps(payload),
                                         headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                         verify=False, timeout=120)
                    logging.info(resp.json())
                    if resp.status_code == 200:
                        run_once = True
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Wifi Stop Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test Device configuration change")
    @pytest.mark.dev_config_change
    def test_kafka_dev_config_change(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "unit.configuration_change"
        record_messages = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'wifi.start' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"].append('wifi.start')
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info("unit.configuration_change has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Device Configuration change Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test UE/Client join event")
    @pytest.mark.client_join
    def test_kafka_client_join(self, get_target_object, kafka_consumer_deq, get_test_library):
        is_valid = False
        msg_found = False
        payload_msg = "client.join"
        record_messages = []
        client_created = False
        ssid, passwd = config_data["interfaces"][0]["ssids"][0]["name"], \
            config_data["interfaces"][0]["ssids"][0]["encryption"]["key"]
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["client.join", "client.leave", "client.key-mismatch"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 300  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=300000)
                # create a client to identify wifi stop event from kafka log
                if not client_created:
                    sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd,
                                                                              security="wpa2",
                                                                              mode="BRIDGE", radio="wiphy0",
                                                                              station_name=["sta100"],
                                                                              create_vlan=False)
                    if not sta_created:
                        logging.info("Failed to create station")
                        pytest.fail("Station creation failed")
                    else:
                        client_created = True
                if client_created:
                    get_test_library.client_disconnect(station_name=["sta100"])
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info("client.join has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Device Configuration change Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test UE/Client leave event")
    @pytest.mark.client_leave
    def test_kafka_client_leave(self, get_target_object, kafka_consumer_deq, get_test_library):
        is_valid = False
        msg_found = False
        payload_msg = "client.leave"
        record_messages = []
        client_created = False
        ssid, passwd = config_data["interfaces"][0]["ssids"][0]["name"], \
            config_data["interfaces"][0]["ssids"][0]["encryption"]["key"]
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["client.join", "client.leave", "client.key-mismatch"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 300  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=300000)
                # create a client to identify wifi stop event from kafka log
                if not client_created:
                    sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd,
                                                                              security="wpa2",
                                                                              mode="BRIDGE", radio="wiphy0",
                                                                              station_name=["sta100"],
                                                                              create_vlan=False)
                    if not sta_created:
                        logging.info("Failed to create station")
                        pytest.fail("Station creation Failed")
                    else:
                        client_created = True
                if client_created:
                    get_test_library.client_disconnect(station_name=["sta100"])
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info("client.join has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Device Configuration change Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test UE/Client Pass Key Mismatch event")
    @pytest.mark.client_key_mismatch
    def test_kafka_client_key_mismatch(self, get_target_object, kafka_consumer_deq, get_test_library):
        is_valid = False
        msg_found = False
        payload_msg = "client.key-mismatch"
        record_messages = []
        client_created = False
        ssid, passwd = config_data["interfaces"][0]["ssids"][0]["name"], "something"
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["client.join", "client.leave", "client.key-mismatch"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 300  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=300000)
                # create a client to identify wifi stop event from kafka log
                if not client_created:
                    sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey="something",
                                                                              security="wpa2",
                                                                              mode="BRIDGE", radio="wiphy0",
                                                                              station_name=["sta100"],
                                                                              create_vlan=False)
                    if not sta_created:
                        client_created = False
                if client_created:
                    get_test_library.client_disconnect(station_name=["sta100"])
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info("client.join has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Device Configuration change Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test Health Radius event")
    @pytest.mark.health_radius
    def test_kafka_check_health_radius(self, get_target_object, kafka_consumer_deq, get_test_library):
        is_valid = False
        msg_found = False
        payload_msg = "health.radius"
        record_messages = []
        ssid = config_data["interfaces"][0]["ssids"][0]["name"]
        radius = {
            "authentication": {
                "host": "18.189.85.2",
                "port": 1812,
                "secret": "testing123"
            },
            "accounting": {
                "host": "18.189.85.2",
                "port": 1813,
                "secret": "testing123"
            },
            "health": {
                "username": "user",
                "password": "password"
            }
        }
        for i in range(len(config_data["interfaces"][0]["ssids"])):
            if "radius" not in config_data["interfaces"][0]["ssids"][i]:
                config_data["interfaces"][0]["ssids"][i].update({"radius": radius})
            if "proto" in config_data[0]["ssids"][i]["encryption"]:
                config_data["interfaces"][0]["ssids"][i]["encryption"]["proto"] = "wpa2"
            if "key" in config_data["interfaces"][0]["ssids"][i]["encryption"]:
                config_data["interfaces"][0]["ssids"][i]["encryption"].pop("key")
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["health"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 300  # Timeout in seconds
            start_time = time.time()
            run_once = False
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=300000)
                # create a client to check whether radius health event can be captured
                if not run_once:
                    result, description = get_test_library.enterprise_client_connectivity_test(ssid=ssid,
                                                                                               security="wpa2",
                                                                                               key_mgmt="WPA-EAP",
                                                                                               ttls_passwd="password",
                                                                                               eap="TTLS",
                                                                                               allure_attach=False,
                                                                                               identity="user")
                    run_once = True
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Health radius Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))
        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test Warm Restart event - System Restart/Reboot")
    @pytest.mark.uboot_up
    def test_kafka_uboot_up(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "unit.boot-up"
        record_messages = []
        run_once = False
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'unit.boot-up' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"] = ["unit.boot-up"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())

            timeout = 180  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # Trigger reboot to capture uboot up event message
                if not run_once:
                    payload = {"serialNumber": serial_number, "when": 0}
                    uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                        "device/" + serial_number + "/reboot")
                    logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                                 "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                 "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                                 "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
                    allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                                "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                                "Data: " + str(payload) + "\n" +
                                                                "Headers: " + str(
                        get_target_object.firmware_library_object.sdk_client.make_headers()))
                    resp1 = requests.post(uri, data=json.dumps(payload),
                                          headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                          verify=False, timeout=120)
                    logging.info(resp1.json())
                    allure.attach(name=f"Response - {resp1.status_code}{resp1.reason}", body=str(resp1.json()))
                    if resp1.status_code == 200:
                        run_once = True
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Boot up Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test Wired Interface Up/Down")
    @pytest.mark.wired_interface_up_or_down
    def test_kafka_wired_interface_up_or_down(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "wired.carrier-up"
        payload_msg1 = "wired.carrier-down"
        record_messages = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["wired.carrier-up", "wired.carrier-down"]
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg or event_type == payload_msg1:
                                    if event_type == payload_msg and event_type != payload_msg1:
                                        logging.info(f"{payload_msg} has found in the Message")
                                    if event_type != payload_msg and event_type == payload_msg1:
                                        logging.info(f"{payload_msg1} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Wired Interface up/down Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg}/{payload_msg1} Message not found'

    @allure.title("Test to check black listed device")
    @pytest.mark.check_blacklisted_device
    def test_kafka_check_blacklisted_device(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "blacklisted_device"
        record_messages = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            logging.info(config_data)
            payload = {"serialNumber": serial_number, "reason": "Automation Test to check blacklisted device"}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "blacklist/" + serial_number)
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check Blacklisted Device Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
            # If Device becomes black listed, remove it from black list to connect it back to controller
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "blacklist/" + serial_number)
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp1 = requests.get(uri, headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            if resp1.status_code == 200:
                resp2 = requests.delete(uri,
                                        headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                        verify=False, timeout=120)
                if resp2.status_code != 200:
                    assert False, "Failed to remove device from blacklisted Devices"
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test to check ssh event")
    @pytest.mark.ssh_event
    def test_kafka_ssh(self, get_target_object, get_testbed_details, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "ssh"
        record_messages = []
        run_once = False
        for ap in range(len(get_target_object.device_under_tests_info)):
            for i in range(len(config_data["interfaces"])):
                if "services" in config_data["interfaces"][i]:
                    if "ssh" not in config_data["interfaces"][i]["services"]:
                        config_data["interfaces"][i]["services"].append("ssh")
            if 'types' in config_data["metrics"]["realtime"]:
                config_data["metrics"]["realtime"]["types"] = ["ssh"]
            logging.info(config_data)
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
            cmd_output = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig up0v0")
            if "inet addr:" in cmd_output:
                pattern = re.search(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', cmd_output)
                ip_address = pattern.group(1)
                logging.info(f"The IP address of up0v0 is: {ip_address}")
            else:
                logging.info(f"No IP address found for up0v0")
                pytest.fail("up0v0 Interface doesn't have an IP address")
            host_ip, host_username, host_password = get_target_object.device_under_tests_info[ap]['host_ip'], \
                get_target_object.device_under_tests_info[ap]['host_username'], \
            get_target_object.device_under_tests_info[ap][
                'host_password']
            upstream = get_target_object.device_under_tests_info[ap]['wan_port'].split(".")[2]
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                if not run_once:
                    try:
                        ssh_client.connect(hostname=host_ip, username=host_username, password=host_password)
                        # Create the lanforge SSH client from the jump host SSH session
                        lf_client = ssh_client.invoke_shell()
                        cmd = f'./vrf_exec.bash {upstream} ssh root@{ip_address}'
                        # Execute the SSH command on the traffic generator
                        lf_client.send(
                            f'ssh root@{get_testbed_details["traffic_generator"]["details"]["manager_ip"]}\n')
                        lf_client.send('lanforge\n')
                        lf_client.send(f'{cmd}\n')
                        lf_client.send(f'openwifi\n')
                        output = lf_client.recv(4096).decode()
                        logging.info(f"Output: {output}")
                    finally:
                        ssh_client.close()
                        run_once = True
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check ssh event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test to check Health DNS event")
    @pytest.mark.health_dns
    def test_kafka_health_dns(self, get_target_object, get_testbed_details, get_test_library, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "health.dns"
        record_messages = []
        run_once = False
        client_created = False
        for ap in range(len(get_target_object.device_under_tests_info)):
            for i in range(len(config_data["interfaces"])):
                if config_data["interfaces"][i]["name"] == "WAN":
                    if "ssids" in config_data["interfaces"][i]:
                        config_data["interfaces"][i].pop("ssids")
                if config_data["interfaces"][i]["name"] == "LAN" and "ssids" not in config_data["interfaces"][i]:
                    config_data["interfaces"][i]["ssids"] = [
                        {
                            "name": "OpenWifi",
                            "wifi-bands": [
                                "2G", "5G"
                            ],
                            "bss-mode": "ap",
                            "encryption": {
                                "proto": "psk2",
                                "key": "OpenWifi@123",
                                "ieee80211w": "optional"
                            }
                        }
                    ]
            if 'health' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"] = ["health"]
            logging.info(config_data)
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # change the interface ip from configured gateway to some other ip to capture dns event
                if not run_once:
                    if not client_created:
                        ssid, passwd = config_data["interfaces"][1]["ssids"][0]["name"], \
                            config_data["interfaces"][1]["ssids"][0]["encryption"]["key"]
                        sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd,
                                                                                  security="wpa2",
                                                                                  mode="BRIDGE", radio="wiphy0",
                                                                                  station_name=["sta0001"],
                                                                                  create_vlan=False)
                        if not sta_created:
                            logging.info("Failed to create station")
                            pytest.fail("Station creation failed")
                        else:
                            client_created = True
                    if client_created:
                        get_test_library.client_disconnect(station_name=["sta0001"])
                    cmd_output = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0")
                    allure.attach(name="down1v0 interface info before ip change", body=str(cmd_output))
                    if "inet addr:" in cmd_output:
                        pattern = re.search(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', cmd_output)
                        ip_address = pattern.group(1)
                        logging.info(f"The IP address of down1v0 is: {ip_address}")
                        cmd_set_ip = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0 "
                                                                                                  "192.146.5.6")
                        cmd_output2 = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0")
                        allure.attach(name="down1v0 interface info after ip change", body=str(cmd_output2))
                        pattern1 = re.search(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', cmd_output2)
                        ip_address1 = pattern1.group(1)
                        if ip_address1 == '192.146.5.6':
                            run_once = True
                    else:
                        logging.info(f"No IP address found for down1v0")
                        pytest.fail("down1v0 Interface does not have an IP address")
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check health DNS event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test to check Health DHCP Event")
    @pytest.mark.health_dhcp
    def test_kafka_health_dhcp(self, get_test_library, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "health.dhcp"
        record_messages = []
        run_once = False
        client_created = False
        logging.info(config_data)
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            for i in range(len(config_data["interfaces"])):
                if config_data["interfaces"][i]["name"] == "WAN":
                    if "ssids" in config_data["interfaces"][i]:
                        config_data["interfaces"][i].pop("ssids")
                if config_data["interfaces"][i]["name"] == "LAN" and "ssids" not in config_data["interfaces"][i]:
                    config_data["interfaces"][i]["ssids"] = [
                        {
                            "name": "OpenWifi",
                            "wifi-bands": [
                                "2G", "5G"
                            ],
                            "bss-mode": "ap",
                            "encryption": {
                                "proto": "psk2",
                                "key": "OpenWifi@123",
                                "ieee80211w": "optional"
                            }
                        }
                    ]
            if 'health' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"] = ["health"]
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # change the interface ip from configured gateway to some other ip to capture dhcp event
                if not run_once:
                    if not client_created:
                        ssid, passwd = config_data["interfaces"][1]["ssids"][0]["name"], \
                            config_data["interfaces"][1]["ssids"][0]["encryption"]["key"]
                        sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd,
                                                                                  security="wpa2",
                                                                                  mode="BRIDGE", radio="wiphy0",
                                                                                  station_name=["sta0001"],
                                                                                  create_vlan=False)
                        if not sta_created:
                            logging.info("Failed to create station")
                            pytest.fail("Station creation failed")
                        else:
                            client_created = True
                    if client_created:
                        get_test_library.client_disconnect(station_name=["sta0001"])
                    cmd_output = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0")
                    allure.attach(name="down1v0 interface info before ip change", body=str(cmd_output))
                    if "inet addr:" in cmd_output:
                        pattern = re.search(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', cmd_output)
                        ip_address = pattern.group(1)
                        logging.info(f"The IP address of down1v0 is: {ip_address}")
                        cmd_set_ip = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0 "
                                                                                                  "192.146.5.6")
                        cmd_output2 = get_target_object.dut_library_object.run_generic_command(cmd="ifconfig down1v0")
                        allure.attach(name="down1v0 interface info after ip change", body=str(cmd_output2))
                        pattern1 = re.search(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', cmd_output2)
                        ip_address1 = pattern1.group(1)
                        if ip_address1 == '192.146.5.6':
                            run_once = True
                    else:
                        logging.info(f"No IP address found for down1v0")
                        pytest.fail("down1v0 Interface does not have an IP address")
                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check health DHCP Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'

    @allure.title("Test health Memory Event")
    @pytest.mark.health_memory
    def test_kafka_health_memory(self, get_target_object, kafka_consumer_deq):
        is_valid = False
        msg_found = False
        payload_msg = "health.memory"
        record_messages = []
        run_once = False
        for ap in range(len(get_target_object.device_under_tests_info)):
            if 'health' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"] = ["health"]
            logging.info(config_data)
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))

            timeout = 120  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)

                # increase the memory on ap to capture memory increase event
                if not run_once:
                    cmd_output = get_target_object.dut_library_object.run_generic_command(cmd="cd /tmp && mount -t "
                                                                                              "tmpfs -o size=300M "
                                                                                              "tmpfs ap-event-test && "
                                                                                              "dd if=/dev/urandom "
                                                                                              "of=sample.txt bs=64M "
                                                                                              "count=16")
                    allure.attach(name="command output", body=str(cmd_output))
                    if "Error: " not in cmd_output:
                        run_once = True

                # Check if any messages were returned
                if messages and not msg_found:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            record_messages.append(record)
                            if 'type' in record.value['payload']:
                                event_type = record.value['payload']['type']
                                # Validate the message value here
                                if event_type == payload_msg:
                                    logging.info(f"{payload_msg} has found in the Message")
                                    is_valid = True
                                    allure.attach(
                                        name="Check health Memory Event Message",
                                        body=str(record))
                                    msg_found = True
                                    break
                                else:
                                    continue
                elif msg_found:
                    break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)
            payload = {"serialNumber": serial_number, "when": 0}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/reboot")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp1 = requests.post(uri, data=json.dumps(payload),
                                  headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                  verify=False, timeout=120)
            logging.info(resp1.json())
            allure.attach(name=f"Response - {resp1.status_code}{resp1.reason}", body=str(resp1.json()))

        allure.attach(name="Messages Recorded in Test Execution", body=str(record_messages))

        # Assert that the message is valid
        assert is_valid, f'{payload_msg} Message not found'
