# wlan-testing framework Information

### e2e/basic

#### Basic test environment has 1 Access Point, 1 Cloud Controller, and 1 Candela LANforge Unit.

### Setup

There are 3 different Configuration Modes in an Access Point
1. Bridge   
2. NAT
3. VLAN

####Any one mode of setup can be done in an Access Point at a time.
#### Within each mode, n number of SSID's can be provisioned from the controller to the AP


setup will take the inputs from the Test cases

Test cases can be bunched on a
1. class level (have a module/ test_xx.py , have one or more classes, do setup once for each class)
2. function level   (have a module/ test_xx.py , have one or more functions, do setup once for each function)


# Use the below sample template for starting to write test cases in basic
### SAMPLE Test Case Example:

test_featureA_bridge.py
    
```python
import pytest
import allure

# Module level Marking
pytestmark = [pytest.mark.usefixtures("setup_test_run"), pytest.mark.featureA]

# It is compulsory to put pytest.mark.usefixtures("setup_test_run")   in module level marking

profile_config = {
    "mode": "NAT",      # Mode of config ("BRIDGE"/"NAT"/"VLAN")
    
    # SSID modes and its Config: Enter the json data structure in the below format for test cases
    "ssid_modes": {
        # Enter the ssid modes:
        # (open/wpa/wpa2_personal/wpa3_personal/wpa3_personal_mixed/wpa_wpa2_personal_mixed/
        #  wpa_enterprise/wpa2_enterprise/wpa3_enterprise/wpa_wpa2_enterprise_mixed/wpa3_enterprise_mixed
        #  /wep)
        # Each security type can have multiple ssid config placed in a list and is customizable
        "wpa": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 1 },
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]
    },
    # rf config data that is need to be pushed, 
    # Leave Blank for default (default config is taken from configuration.py for the selected testbed and AP Model)
    "rf": {},
    # True if you want to create a Radius Profile(Radius config by default is taken from configuration.py)
    "radius": True
}


# Class level Marking
@pytest.mark.suite_a
@pytest.mark.parametrize(
    'setup_profiles',   # Name of the fixture
    [profile_config],   # Passing the above static profile_config data for setup for tests in this class
    indirect=True,
    scope="class"       # Scope of the fixture (Its experimental for current framework (keep it "class" for default scenario))
)
@pytest.mark.usefixtures("setup_profiles")
class TestFeatureABridge(object):

    @pytest.mark.wpa        # Marker for the wifi encryption needed - Compulsory
    @pytest.mark.twog       # Marker for band (twog/fiveg) - Compulsory
    def test_client_wpa_2g(self):
        profile_data = profile_config["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"  # refer to appliedRadios in ssid_modes config   (twog/fiveg)
        #        vlan = 1        # 1 for "BRIDGE"/"NAT"  # Can be customised in the ssid config json
        
        # Write Your test case Here
        # Some Recommendations: 
        #        If your test case has components that are to be used by other test case,
        #        then make it library and call its instance from fixture.
        #        If your test case has some reports, then attach it as an allure report
        
        allure.attach(name="Test case report", body="Test case result description") # Check its usages for more detail
        
        PASS_FAIL_CONDITION = True
        assert PASS_FAIL_CONDITION

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_client_wpa_5g(self):
        profile_data = profile_config["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "fiveg"  # refer to appliedRadios in ssid_modes config   (twog/fiveg)
        vlan = 1        # 1 for "BRIDGE"/"NAT"  # Can be customised in the ssid config json
        
        # Write Your test case Here
        # Some Recommendations: 
        #        If your test case has components that are to be used by other test case,
        #        then make it library and call its instance from fixture.
        #        If your test case has some reports, then attach it as an allure report
        
        allure.attach(name="Test case report", body="Test case result description") # Check its usages for more detail
        
        PASS_FAIL_CONDITION = True
        assert PASS_FAIL_CONDITION
    
    @pytest.mark.wpa2_personal        # Marker for the wifi encryption needed - Compulsory
    @pytest.mark.twog       # Marker for band (twog/fiveg) - Compulsory
    def test_client_wpa2_personal_2g(self):
        profile_data = profile_config["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"  # refer to appliedRadios in ssid_modes config   (twog/fiveg)
        #        vlan = 1        # 1 for "BRIDGE"/"NAT"  # Can be customised in the ssid config json
        
        # Write Your test case Here
        # Some Recommendations: 
        #        If your test case has components that are to be used by other test case,
        #        then make it library and call its instance from fixture.
        #        If your test case has some reports, then attach it as an allure report
        
        allure.attach(name="Test case report", body="Test case result description") # Check its usages for more detail
        
        PASS_FAIL_CONDITION = True
        assert PASS_FAIL_CONDITION

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self):
        profile_data = profile_config["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"  # refer to appliedRadios in ssid_modes config   (twog/fiveg)
        vlan = 1        # 1 for "BRIDGE"/"NAT"  # Can be customised in the ssid config json
        
        # Write Your test case Here
        # Some Recommendations: 
        #        If your test case has components that are to be used by other test case,
        #        then make it library and call its instance from fixture.
        #        If your test case has some reports, then attach it as an allure report
        
        allure.attach(name="Test case report", body="Test case result description") # Check its usages for more detail
        
        PASS_FAIL_CONDITION = True
        assert PASS_FAIL_CONDITION

    



```
##General Guardrails: 
```
setup_profile is a Fixture that collects markers 
from the test case to decide which security modes and band is need to be applied on the Access Point

Test cases can be selected based upon the markers 

# This selection will push all the config for the above scenario, considering that you have specified all required markers
pytest -m featureA

# This selection will select only wpa test cases and will push the config for wpa mode only because wpa2_personal marker is not selected
pytest -m "featureA and wpa"

Conclusion: Security modes for SSID has some specific markers which are specified as follows

open/wpa/wpa2_personal/wpa3_personal/wpa3_personal_mixed/wpa_wpa2_personal_mixed
wpa_enterprise/wpa2_enterprise/wpa3_enterprise/wpa_wpa2_enterprise_mixed/wpa3_enterprise_mixed/wep

and for band, its (twog/fiveg)

if you don't specifi the marker, then no matter what profile_config you are passing to setup_profile fixture,
it will not be pushed

Refer other test cases for more reference



```

## If you have special Config requirements for test case, then reach out to Shivam Thakur on Slack, or email (shivam.thakur@candelatech.com)