FROM python:3.8
WORKDIR /ci

RUN pip3 install requests

COPY wlan-LANforge-scripts/py-json/LANforge /ci/LANforge
COPY wlan-LANforge-scripts/py-json/realm.py /ci
COPY wlan-LANforge-scripts/py-json/generic_cx.py /ci
COPY wlan-LANforge-scripts/py-scripts/sta_connect2.py /ci
COPY wlan-LANforge-scripts/py-scripts/__init__.py /ci
COPY wlan-testing/docker/nightly.py /ci

ENTRYPOINT [ "/ci/nightly.py" ]
