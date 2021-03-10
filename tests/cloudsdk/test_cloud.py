import pytest
import sys
if 'cloudsdk' not in sys.path:
    sys.path.append(f'../../libs/cloudsdk')
from cloudsdk import CloudSDK

@pytest.mark.login
class TestLogin:

    def test_token_login(self):
        try:
            obj = CloudSDK(testbed="nola-ext-04", customer_id=2)
            bearer = obj.get_bearer_token()
            value = bearer._access_token is None
        except:
            value = True
        assert value == False

    def test_ping(self):
        try:
            obj = CloudSDK(testbed="nola-ext-04", customer_id=2)
            value = obj.portal_ping() is None
        except:
            value = True
        assert value == False

