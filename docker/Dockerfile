FROM python:3.8
WORKDIR /ci

RUN apt update && apt install vim -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install requests xlsxwriter pandas

COPY wlan-lanforge-scripts/py-json/LANforge /ci/LANforge
COPY wlan-lanforge-scripts/py-json/realm.py /ci
COPY wlan-lanforge-scripts/py-json/generic_cx.py /ci
COPY wlan-lanforge-scripts/py-scripts/sta_connect2.py /ci
COPY wlan-lanforge-scripts/py-scripts/__init__.py /ci
COPY wlan-testing/docker/nightly.py /ci
COPY wlan-testing/docker/nightly_test_config.json /ci

ENTRYPOINT [ "/ci/nightly.py" ]
