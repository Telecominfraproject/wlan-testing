FROM python:3.8
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tshark \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
RUN echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY lanforge /wlan-testing/lanforge
COPY tests /wlan-testing/tests
COPY libs /wlan-testing/libs
WORKDIR /wlan-testing
ENTRYPOINT ["bash"]
