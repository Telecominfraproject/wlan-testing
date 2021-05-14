FROM python:3.8
WORKDIR /wlan-testing
RUN apt update && apt install vim -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install pytest==6.2.2 bs4 paramiko xlsxwriter requests pandas influxdb scp allure-pytest
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
RUN echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
RUN echo "tip-wlan-cloud" > ~/.pip/requirements.txt
RUN pip3 install -r ~/.pip/requirements.txt
COPY lanforge /wlan-testing/lanforge
COPY tests /wlan-testing/tests
COPY libs /wlan-testing/libs
