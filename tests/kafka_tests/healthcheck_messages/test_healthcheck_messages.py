"""
    Test Case Module:  Testing Kafka messages for Health check Messages
"""
import allure
import pytest


@allure.feature("Test Kafka Messages")
@allure.title("Health check Messages")
@pytest.mark.healthcheck_messages
class TestHealthCheckMessages(object):
    # Pytest unit test for validating Kafka healthcheck messages
    @allure.title("Test HealthCheck Messages")
    @pytest.mark.health_check
    def test_kafka_healthcheck(self, kafka_consumer_healthcheck):
        is_valid = None
        # Consume messages and validate them
        for message in kafka_consumer_healthcheck:
            # Apply validation logic on message value
            print(message)
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
            if message.value is not None:
                is_valid = True
                allure.attach(name="Kafka Health Check Message Info", body=str(message.value))
                break

            # Assert that the message is valid
        assert is_valid is not None, f'Message validation failed: \n'
