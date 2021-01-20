FROM python:3.8
WORKDIR /ci

RUN apt update && apt install vim -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install requests xlsxwriter pandas pytest

COPY wlan-lanforge-scripts/py-json/LANforge /ci/LANforge
COPY wlan-lanforge-scripts/py-json/realm.py /ci
COPY wlan-lanforge-scripts/py-json/generic_cx.py /ci
COPY wlan-lanforge-scripts/py-scripts/sta_connect2.py /ci
COPY wlan-testing/pytest/conftest.py /ci
COPY wlan-testing/pytest/test* /ci
COPY wlan-testing/pytest/pytest.ini /ci
COPY wlan-testing/pytest/helpers /ci/helpers

ENTRYPOINT [ "pytest" ]
