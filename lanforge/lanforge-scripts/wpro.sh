#!/bin/bash

ssid=""
security="open"
passphrase=""

read -p "Name of SSID: " SSID
read -p "open or wpa2: " SECURITY
if [[ "$SECURITY" = "wpa2" ]]; then
   read -p "Passphrase: " PASSPHRASE
fi
if [ -z "$SSID" ]; then 
   echo "Blank SSID, bye."
   exit 1
fi
ssid="--ssid \"$SSID\""

if [ -z "$SECURITY" ]; then
   echo "Blank SECURITY, bye."
   exit 1
fi
security="--security $SECURITY"

if [[ "$SECURITY" = "wpa2" ]]; then
   passphrase="--passphrase \"$PASSPHRASE\""
fi

cd /home/lanforge/scripts
cmd="./wlanpro_test.pl --manager lanforge-74bb \
   --gui_host localhost --gui_port 7777 \
   --ip 5.5.5.2 --netmask 255.255.255.0 \
   --upstream_resource 1 --upstream_port eth4 --interferer_cx inter_r3_w0 \
   --ssid "$SSID" $security $passphrase \
   --testcase -1"
echo "$cmd"
read -p "Look good?"
$cmd
