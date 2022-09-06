FROM python:3.8
# Version of cloudsdk to be tested
ARG CLOUDSDK_LIBRARY=tip_2x
ARG TEST_DEVICE_NAME=all

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tshark \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
RUN echo "extra-index-url = https://tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple/" >> ~/.pip/pip.conf
COPY requirements.txt /wlan-testing/requirements.txt
RUN pip3 install -r /wlan-testing/requirements.txt
COPY tests /wlan-testing/tests
COPY libs /wlan-testing/libs
COPY setup_env.bash /wlan-testing/setup_env.bash
ENV PYTHON=/usr/local/bin/python3
ENV PIP=/usr/local/bin/pip3
RUN /wlan-testing/setup_env.bash -t $CLOUDSDK_LIBRARY -d $TEST_DEVICE_NAME -n "TIP Automation" -o TIP -e tip-automation@telecominfraproject.com -i "TIP OpenWIFI Library" && pip3 freeze
WORKDIR /wlan-testing
ENTRYPOINT ["/bin/bash"]
