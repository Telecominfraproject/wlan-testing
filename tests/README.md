##Pytest Framework

wlan-testing Supports the following Tests integrated in a pytest framework

## Framework Overview

1. pytest framework is designed in such a way that there is a categorization of test cases based on the Test case Requirements
We have different environment suite available 
2. Based on the test case requirements, Test case writer will select, that which environment is suitable for test case.
3. test cases are structures in different directories in tests/e2e
we have each directory representing the environments, and test cases written in each of the environment will setup the environment.
4.   Refer README.md in each environment directories for details











## Setting up the Development Environment

Setup the python packages for pytests

```shell    
pip install pytest
```

Setup the python packages for libraries


```shell
mkdir ~/.pip
echo "[global]" > ~/.pip/pip.conf
echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
echo "tip-wlan-cloud" > ~/.pip/requirements.txt
```




