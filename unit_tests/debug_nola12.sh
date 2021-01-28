#!/bin/bash

# Commands to grab debug info off of NOLA-12.  Everything is hard-coded assuming you use
# ssh tunnel in the suggested way.  Otherwise, you will need to edit things...

set -x

# cloud sdk profile dump
./query_sdk.py --testrail-user-id NONE --model ecw5410 --sdk-base-url https://wlan-portal-svc-ben-testbed.cicd.lab.wlan.tip.build --sdk-user-id support@example.com --sdk-user-password support --type profile --cmd get > /tmp/nola-12-profiles.txt

# ovsdb-client dump
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port 8823 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 -m ecw5410 --cmd "ovsdb-client dump" > /tmp/nola-12-ap.txt

# interface info
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port 8823 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 -m ecw5410 --cmd "iwinfo && brctl show" > /tmp/nola-12-ap-if.txt

# TODO:  Add more things here as we learn what better provides debug info to cloud.

echo "Grab:  /tmp/nola-12-profiles.txt /tmp/nola-12-ap.txt /tmp/nola-12-ap-if.txt"
