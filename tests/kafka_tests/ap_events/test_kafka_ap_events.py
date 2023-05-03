"""
    Test Case Module:  Testing Kafka messages for AP events
"""
import json
import random
import time
import allure
import pytest
import requests
import logging
import datetime


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
        is_valid = None
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
            allure.attach(name="firmware upgrade: \n", body="Sending Command: POST " + str(command) + "\n" +
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
                if messages:
                    logging.info(f"Polled messages: {messages}")
                    for topic, records in messages.items():
                        logging.info(f"Kafka Topic {topic}")
                        logging.info(f"Messages in Record: {records}")
                        for record in records:
                            logging.info(f"Record : {record}")
                            message_value = json.loads(record.value.decode('utf-8'))
                            logging.info("Message value: %s \n" % str(message_value))
                            # Validate the message value here
                            if 'unit.firmware_change' in str(message_value):
                                logging.info(f"unit.firmware_change has found in the Message")
                                is_valid = True
                                allure.attach(
                                    name="Check Kafka Message for Firmware Upgrade from Version X to Version Y",
                                    body=str(message_value))
                                break
                else:
                    # No messages received, sleep for a bit
                    time.sleep(1)

        # Assert that the message is valid
        assert is_valid is not None, f'Message not found'
