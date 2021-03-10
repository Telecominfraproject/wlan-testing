import pytest
import sys

if 'cloudsdk' not in sys.path:
    sys.path.append(f'../../libs/cloudsdk')
from cloudsdk import CloudSDK


@pytest.mark.userfixtures('get_customer_id')
@pytest.mark.userfixtures('get_testbed_name')
@pytest.mark.login
class TestLogin(object):

    def test_token_login(self, get_customer_id, get_testbed_name):
        try:
            obj = CloudSDK(testbed=get_testbed_name, customer_id=get_customer_id)
            bearer = obj.get_bearer_token()
            value = bearer._access_token is None
        except:
            value = True
        assert value == False

    def test_ping(self, get_customer_id, get_testbed_name):
        try:
            obj = CloudSDK(testbed=get_testbed_name, customer_id=get_customer_id)
            value = obj.portal_ping() is None
        except:
            value = True
        assert value == False
