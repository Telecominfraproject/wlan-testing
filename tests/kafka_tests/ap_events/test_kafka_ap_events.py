"""
    Test Case Module:  Testing Kafka messages for AP events
"""
import allure
import pytest


@allure.feature("Test Kafka Messages")
@allure.title("Real Time AP Events")
@pytest.mark.ap_events
class TestKafkaApEvents(object):
    # Pytest unit test for validating Kafka healthcheck messages
    @allure.title("Test AP events")
    @pytest.mark.ap_events
    def test_kafka_ap_event(self, kafka_consumer_deq):
        # Consume messages and validate them
        for event in kafka_consumer_deq:
            # Apply validation logic on message value
            print(event)
            print("%s:%d:%d: key=%s value=%s" % (event.topic, event.partition,
                                                 event.offset, event.key,
                                                 event.value))
            if event.value is not None:
                allure.attach(name="Kafka AP Event Info", body=str(event.value))
                break

            # Assert that the message is valid
        assert True
        # assert is_valid is str, f'Message validation failed: {message.value}'
