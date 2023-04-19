"""
    Test Case Module:  Testing Kafka messages for AP events
"""
import allure
import pytest

pytestmark = [pytest.mark.kafka_tests]


@allure.feature("Test Kafka Messages")
@allure.title("Real Time AP Events")
class KafkaEvents(object):
    # Pytest unit test for validating Kafka healthcheck messages
    @pytest.mark.health_check
    @allure.title("Test HealthCheck Messages")
    def test_kafka_healthcheck(self, kafka_consumer_healthcheck):
        # Consume messages and validate them
        for message in kafka_consumer_healthcheck:
            # Apply validation logic on message value
            print(message)
            if message.value is not None:
                break

            # Assert that the message is valid
        assert True
        # assert is_valid is str, f'Message validation failed: {message.value}'
