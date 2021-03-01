"""
cloud_connectivity.py :

ConnectCloud : <class> has methods to invoke the connections to the cloud constructor
                default constructor of ConnectCloud class (args: testbed-name)
get_bearer() :  It is called by default from the constructor itself. bearer gets expired in 3000 seconds
refresh_bearer() : It is used to refresh the Connectivity. It can be used for Long test runs

"""

import sys

if "cloudsdk" not in sys.path:
    sys.path.append("../cloudsdk")

from swagger_client.api.login_api import LoginApi

class EquipmentUtility:

    def __init__(self, sdk_base_url=None, bearer=None):
        self.sdk_base_url = sdk_base_url
        self.bearer = bearer
