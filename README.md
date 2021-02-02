## TIP Open WiFi Testing
This repository contains the test automation framework and scripts for  TIP Open WiFi.

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

## Proposed Directory Structure
```bash
├── tests
├── libs
│   ├── cloudsdk
│   ├── apnos
│   ├── lanforge
│   ├── perfecto
│   ├── <future>
├── tools
├── docker
├── pytest          - /* to be migrated */
├── CICD_AP_CLOUSDK - /* to be migrated */
├── cicd            - /* to be migrated */
├── lanforge        - /* under cleanup consideration */
├── testbeds        - /* under cleanup consideration */
├── unit_tests      - /* to be migrated */
```

## TO DO
- [x] Pytest proof of concept
- [ ] Pytest documentation
- [x] Dockerized test framework PoC
- [x] Github nightly trigger - PoC
- [ ] Deprecate uni_tests script and move methods into pytest Directory
- [ ] Move Java Selenium to python/Selenium
- [ ] Deprecate cicd scripts and move to Pytest
- [ ] lanforge needs to be ingested as python module
- [ ] testbeds cleanup based on Lab Orchestration
