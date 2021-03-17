# Pytest Framework
## Perform Unit Tests in TIP Community Testbeds

### Fixtures : 
#### conftest.py
### Unit Tests : 
#### Structured around multiple Directories
### Markers : 
#### Categorized the Test across different Markers


### Note: Run all the tests from "tests" directory

## Examples:
Following are the examples for Running Client Connectivity Test with different Combinations

    pytest -m nightly -s
    pytest -m nightly_bridge -s
    pytest -m nightly_nat -s
    pytest -m nightly_vlan -s
    pytest -m bridge_mode_single_client_connectivity -s
    pytest -m nat_mode_single_client_connectivity -s
    pytest -m vlan_mode_single_client_connectivity -s
    pytest -m bridge_mode_client_connectivity -s
    pytest -m nat_mode_client_connectivity -s
    pytest -m vlan_mode_client_connectivity -s

Following are the examples for cloudSDK standalone tests
    
    pytest -m test_login -s
    pytest -m test_bearer_token -s 
    pytest -m test_portal_ping -s
    
    more to be added ...

Following are the examples for apnos standalone tests
    
    To be added...

Following are the examples for apnos+cloudsdk mixed tests
    
    To be added...

