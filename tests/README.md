# Pytest Framework
## Perform Unit Tests in TIP Community Testbeds

### Fixtures : 
#### conftest.py
### Unit Tests : 
#### Structured around multiple Directories
### Markers : 
#### Categorized the Test across different Markers


### Note: Run all the tests from "tests" directory

Modify pytest.ini based on the config for your setup
You can modify the ini options by using switch -o 

## Examples:
Following are the examples for Running Client Connectivity Test with different Combinations:

    # Run the sanity test in all modes across wpa, wpa2 and eap)
    pytest -m sanity -s

    # Run the sanity test in all modes except wpa2_enterprise)
    pytest -m "sanity and not wpa2_enterprise" -s

    # Run the bridge test in all modes across wpa, wpa2 and eap)
    pytest -m bridge -s

    # Run the bridge test in all modes except wpa2_enterprise)
    pytest -m "bridge and not wpa2_enterprise" -s

    # Run the nat test in all modes across wpa, wpa2 and eap)
    pytest -m nat -s

    # Run the nat test in all modes except wpa2_enterprise)
    pytest -m "nat and not wpa2_enterprise" -s

    # Run the vlan test in all modes across wpa, wpa2 and eap)
    pytest -m vlan -s

    # Run the vlan test in all modes except wpa2_enterprise)
    pytest -m "vlan and not wpa2_enterprise" -s


Following are the examples for cloudSDK standalone tests
    
    # Run cloud connection test, it executes the two tests, bearer and ping
    pytest -m cloud -s
    
    # Run cloud connection test, gets the bearer
    pytest -m bearer -s 
    
    # Run cloud connection test, pings the portal
    pytest -m ping -s
    
    more to be added ...

Following are the examples for apnos standalone tests
    
    To be added...

Following are the examples for apnos+cloudsdk mixed tests
    
    To be added...

