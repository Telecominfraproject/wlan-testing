#!/bin/bash

# Commands to grab debug info off of NOLA-01.  Everything is hard-coded assuming you use
# ssh tunnel in the suggested way.  Otherwise, you will need to edit things...

set -x

NOLANUM=01
PORTAL=wlan-portal-svc.cicd.lab.wlan.tip.build
APPORT=8803
APTTY=/dev/ttyAP1
MODEL=ecw5410

# cloud sdk profile dump
./query_sdk.py --testrail-user-id NONE --model $MODEL --sdk-base-url https://$PORTAL --sdk-user-id support@example.com --sdk-user-password support --type profile --cmd get > /tmp/nola-$NOLANUM-profiles.txt

# ovsdb-client dump
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port $APPORT --ap-jumphost-password pumpkin77 --ap-jumphost-tty $APTTY -m $MODEL --cmd "ovsdb-client dump" > /tmp/nola-$NOLANUM-ap.txt

# interface info
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port $APPORT --ap-jumphost-password pumpkin77 --ap-jumphost-tty $APTTY -m $MODEL --cmd "iwinfo && brctl show" > /tmp/nola-$NOLANUM-ap-if.txt

# TODO:  Add more things here as we learn what better provides debug info to cloud.

echo "Grab:  /tmp/nola-$NOLANUM-profiles.txt /tmp/nola-$NOLANUM-ap.txt /tmp/nola-$NOLANUM-ap-if.txt"
