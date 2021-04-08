FROM python:alpine3.12
WORKDIR /tests
COPY . /tests

RUN mkdir ~/.pip \
    && echo "[global]" > ~/.pip/pip.conf \
    && echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf \
    && echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/sh" ]
