# wlan-testing framework Information

### e2e/basic

#### Basic test environment has 1 Access Point, 1 Cloud Controller, and 1 Candela LANforge Unit.

### Setup

There are 3 different Configuration Modes in an Access Point
1. Bridge   
2. NAT
3. VLAN

####Any one mode of setup can be done in an Access Point at a time.
#### Within each mode, n number of SSID's can be provisioned from the controller to the cloud


setup will take the inputs from the Test cases

Test cases can be bunched on a
1. class level (have a module/ test_xx.py , have one or more classes, do setup once for each class)
2. function level   (have a module/ test_xx.py , have one or more functions, do setup once for each function)

### SAMPLE Test Case Example:

test_featureA_bridge.py
    
```python
import pytest
pytestmark = [pytest.mark.test_featureA, pytest.mark.bridge]


@pytest.mark.wifi_capacity_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["BRIDGE"], ["BRIDGE"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestFeatureABridge(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_wpa_2g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"] 
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2g"]
        # Write Your test case Here
        PASS = True
        assert PASS

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_client_wpa_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"] 
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]
        # Write Your test case Here
        PASS = True
        assert PASS


    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA2_P"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"] 
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2g"]
        # Write Your test case Here
        PASS = True
        assert PASS

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA2_P"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"] 
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]
        # Write Your test case Here
        PASS = True
        assert PASS



```


### Follow the e2e/basic/client_connectivity_test, for more understanding

## NOTE: 
1. Marking the test case is important, setup will take the markers associated with it, and decide the configuration
2. PARAMETRIZATION: 
```python
import pytest

@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["BRIDGE"], ["BRIDGE"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestSomething(object):
    ...
```
### Passing the parameters to the "setup_profiles" and "create_profiles" will setup in each of the asked modes
### For setup to be done in BRIDGE mode, see the above example
### setup can be done on different scope levels, mentioned below 
####[scope="class", scope="function"]