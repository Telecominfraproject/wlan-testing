#!/bin/bash
unset proxy
unset http_proxy
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----#
##  tests to exercise perl-json api                           #
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----#


# ares-f30m64.jbr.candelatech.com
HOST=${1:-localhost}
BASEURL="http://${HOST}:8080"
HELPURL="${BASEURL}/help"
FORMURL="${BASEURL}/cli-form"
JSONURL="${BASEURL}/cli-json"

function Get() {
   [ -f /tmp/$$.result ] && rm -f /tmp/$$.result
   curl -sq -H 'Accept: application/json' "${BASEURL}${@}" &> /tmp/$$.result
   wc -l /tmp/$$.result
   if [[ $? = 0 ]]; then
      json_reformat < /tmp/$$.result
   fi
}

# test that we have a connection to lfclient
echo "Testing $HOST $BASEURL"
Get /port/1/1/eth1 || exit 1

cd json
./port_test.pl --host $HOST --ssid kedtest-wpa2 --pass kedtest-wpa2
sleep 1
./test_sta_mode.pl --host $HOST
sleep 1
./json_port_test3.sh $HOST


## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----#

# create a pair of redirect ports
RDD=('rd0a' 'rd0b' 'rd1a' 'rd1b')



# create a wanlink between two of them
WL='wl1'
WLEP=("${WL}-A" "${WL}-B")

# create a layer 3 connection between the a-side rdds
CX='tcp1'
EPS=("${CX}-A" "${CX}-B")

# start the wanlink

# start the layer3

# print port stats after 30 seconds




###
###
###
