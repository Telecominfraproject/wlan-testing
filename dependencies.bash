#!/bin/bash


if [ -d ../lanforge-scripts ]
then
    rm -fr wlan-testing/libs/controller/controller_3x/wifi_ctl_9800_3504.py

    cp -a ../lanforge-scripts/wifi_ctl_9800_3504.py ../wlan-testing/libs/controller/controller_3x/wifi_ctl_9800_3504.py
fi