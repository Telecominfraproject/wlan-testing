## TIP Open WiFi Testing
This repository contains the test automation framework and scripts for  TIP Open WiFi.

## Cloud Controller build
You can provision additional cloud controllers for your tests using [update cloud controllers](https://github.com/Telecominfraproject/wlan-testing/actions?query=workflow%3A%22update+cloud+controllers+build%22) build. To add additional cloud controller add another json object to the `testbeds` variable at line 19, where

1. number == NOLA testbed number this cloud controller is assigned to
2. version == docker images version to use with this particular deployment. supports 3 options:
  1. "latest" - will use `0.0.1-SNAPSHOT` images
  2. "" - will use `0.0.1-SNAPSHOT-yyyy-mm-dd` images from yesterdays date
  3. "yyyy-mm-dd" - will use `0.0.1-SNAPHOST-yyyy-mm-dd` with the date provided (if they are available, if not build will fail).
 
## Motivation
Automate Automate and Automate!

## Build status
*WIP*  
[![Build Status](https://github.com/Telecominfraproject/wlan-testing/workflows/nightly%20build/badge.svg)]

## Best Practice
This project is built using python 3 and strongly recommends using virtualenv to ensure that your dev environment sandbox is created.

## Code style
All code must be written in python 3 and conform to PEP 8 style guide. The test framework is built using pytest.  

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)   
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)  

## Pytest Directory Structure
```bash
├── lanforge      - /* to be migrated */
├── libs
│   ├── controller  -/* Library Support for controller part  */
    │   ├── apnos   -/* Library Support for Access Points (uses AP SSH)  */
│   ├── lanforge    
│   ├── perfecto    -/* Library Support for Perfecto Traffic Generator*/
│   ├── testrails   -/* Result Visualization (will be depreciated )*/
├── tests            - /* Pytest cases Directory */
│   ├── _basic_test_setup
│   ├── access_point
│   ├── controller
│   ├── e2e
      ├── advanced
      ├── basic
      ├── interOp
      ├── mdu
      |── mesh
      |── scale
    |── README.md  - /* Pytest framework and setup instructions */
```

## BASIC SETUP

wlan-testing requires a sync with wlan-lanforge-scripts
So we have sync_repos.bash, that can do that

```bash

git clone https://github.com/Telecominfraproject/wlan-lanforge-scripts
Make sure this structure exists
├── wlan-lanforge-scripts
├── wlan-testing

./sync_repos.bash
```

## TO DO
- [x] Pytest documentation
- [ ] Dockerized test framework PoC
- [ ] Github nightly trigger - PoC
- [x] lanforge needs to be ingested as python module
- [x] testbeds cleanup based on Lab Orchestration
