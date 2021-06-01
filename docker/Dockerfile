FROM python:3.8
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
RUN echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
RUN pip3 install pytest==6.2.2 bs4 paramiko xlsxwriter requests pandas influxdb influxdb-client scp allure-pytest tip-wlan-cloud selenium perfecto-py37 Appium-Python-Client
COPY lanforge /wlan-testing/lanforge
COPY tests /wlan-testing/tests
COPY libs /wlan-testing/libs
WORKDIR /wlan-testing
ENTRYPOINT ["bash"]