"""
    Test Case Module:  Testing Kafka messages for AP events
"""
import json
import os
import random
import time
import allure
import pytest
import requests
import logging
import datetime

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
            params = "limit=500" + \
                     "&deviceType=" + ap_model + \
                     "&offset=0"
            response = requests.get(url, params=params, verify=False, timeout=120,
                                    headers=get_target_object.firmware_library_object.sdk_client.make_headers())

            firmwares = response.json()
            if response.status_code == 200:
                firmware_list[f"{ap_model}"] = firmwares['firmwares']
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
                                    logging.info(f"wifi.start has found in the Message")
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
            if 'wifi.start' in config_data["metrics"]["realtime"]["types"]:
                idx = config_data["metrics"]["realtime"]["types"].index('wifi.start')
                config_data["metrics"]["realtime"]["types"][idx] = 'wifi.stop'
            elif 'wifi.stop' not in config_data["metrics"]["realtime"]["types"]:
                config_data["metrics"]["realtime"]["types"].append('wifi.stop')
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

            timeout = 180  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # create a client to identify wifi stop event from kafka log
                if not client_created:
                    sta_data = get_test_library.client_connect(ssid=ssid, passkey=passwd, security="wpa2", sta_mode=0,
                                                               mode="BRIDGE", band="twog", num_sta=1, scan_ssid=False,
                                                               allure_name="station data", dut_data=get_target_object.device_under_tests_info)
                    if type(sta_data) == dict:
                        allure.attach(body=str(sta_data), name="client data")
                        client_created = True
                if client_created:
                    get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
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
                                    logging.info(f"wifi.stop has found in the Message")
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

            timeout = 180  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # create a client to identify client join event from kafka log
                if not client_created:
                    sta_data = get_test_library.client_connect(ssid=ssid, passkey=passwd, security="wpa2", sta_mode=0,
                                                               mode="BRIDGE", band="twog", num_sta=1, scan_ssid=False,
                                                               allure_name="station data", dut_data=get_target_object.device_under_tests_info)
                    if type(sta_data) == dict:
                        allure.attach(body=str(sta_data), name="client data")
                        client_created = True
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

            timeout = 180  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # create a client to identify client join event from kafka log
                if not client_created:
                    sta_data = get_test_library.client_connect(ssid=ssid, passkey=passwd, security="wpa2",
                                                               sta_mode=0,
                                                               mode="BRIDGE", band="twog", num_sta=1,
                                                               scan_ssid=False,
                                                               allure_name="station data",
                                                               dut_data=get_target_object.device_under_tests_info)
                    if type(sta_data) == dict:
                        allure.attach(body=str(sta_data), name="client data")
                        client_created = True
                if client_created:
                    get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
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

            timeout = 180  # Timeout in seconds
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Poll for new messages
                messages = kafka_consumer_deq.poll(timeout_ms=120000)
                # create a client to identify client join event from kafka log
                if not client_created:
                    sta_data = get_test_library.client_connect(ssid=ssid, passkey=passwd, security="wpa2", sta_mode=0,
                                                               mode="BRIDGE", band="twog", num_sta=1, scan_ssid=False,
                                                               allure_name="station data",
                                                               dut_data=get_target_object.device_under_tests_info)
                    if type(sta_data) == dict:
                        allure.attach(body=str(sta_data), name="client data")
                        client_created = True
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
