#!/bin/bash
unset proxy
unset http_proxy
set -x
set -e
ajson_h="Accept: application/json"
cjson_h="Content-type: application/json"
dbg=""
#dbg="__debug=1&"
R=1
W=wiphy0
M="10200"
N="10202"
SSID="jedway-wpa2-x2048-4-1"
KEY="jedway-wpa2-x2048-4-1"

#
# works for ifdown:
# set_port 1 8 sta8000 NA NA NA NA 1 NA NA NA NA 8388610
# works for ifup:
# set_port 1 8 sta8000 NA NA NA NA 0 NA NA NA NA 8388611
#
echo -n "Removing: "
for n in `seq $M $N`; do
   n=${n:1}
   echo -n "sta$n "
   echo "shelf=1&resource=$R&port=sta$n" > /tmp/curl_data
   curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/rm_vlan ||:
done
echo "."

sleep 2
echo -n "Adding: "
for n in `seq $M $N`; do
   n=${n:1}
   echo -n "${dbg}shelf=1&resource=$R&radio=$W" > /tmp/curl_data
   echo -n "&sta_name=sta$n" >> /tmp/curl_data
   echo -n "&flags=68727874560&ssid=idtest-1100-wpa2&key=idtest-1100-wpa2" >> /tmp/curl_data
   echo -n "&mac=xx:xx:xx:xx:*:xx&mode=0&rate=DEFAULT" >> /tmp/curl_data
   curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/add_sta ||:
done

sleep 2
for n in `seq $M $N`; do
   n=${n:1}
   echo -n "${dbg}shelf=1&resource=$R&port=sta$n" > /tmp/curl_data
   echo -n '&current_flags=2147483648&interest=16384' >> /tmp/curl_data
   curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/set_port ||:
done
echo "."

sleep 1
echo -n "Bringing ports up "
for n in `seq $M $N`; do
   n=${n:1}
   echo -n "${dbg}shelf=1&resource=$R&port=sta$n" > /tmp/curl_data
   echo -n '&current_flags=0&interest=8388611' >> /tmp/curl_data
   curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/set_port ||:
done
echo "."

sleep 3
echo -n "Querying ports "
for n in `seq $M $N`; do
   curl -sq -H "$ajson_h" -X GET -o /tmp/response "http://localhost:8080/port/1/$R/sta$n"
   echo -n "."
   #if [ -s /tmp/response ]; then
   #   json_pp < /tmp/response
   #fi
done
echo "...done."
exit




echo 'shelf=1&resource=3&port=sta3100' > /tmp/curl_data
curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/rm_vlan

sleep 1
echo 'shelf=1&resource=3&radio=wiphy1&sta_name=sta3100&flags=1024&ssid=idtest-1100-wpa2&nickname=sta3100&key=idtest-1100-wpa2&mac=XX:XX:XX:XX:*:*&flags_mask=1024' > /tmp/curl_data
curl -sq -H "$ajson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/add_sta


sleep 1
rm -f /tmp/response
curl -sq -H "$ajson_h" -X GET -o /tmp/response http://localhost:8080/port/1/3/sta3100
if [ -s /tmp/response ]; then
   json_pp < /tmp/response
fi

sleep 2
echo '{"shelf":1,"resource":3,"port":"sta3100"}' > /tmp/curl_data
curl -sq -H "$ajson_h" -H "$cjson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-json/rm_vlan

sleep 2
echo '{"shelf":1,"resource":3,"radio":"wiphy1","sta_name":"sta3100","flags":1024,"ssid":idtest-1100-wpa2","nickname":"sta3100","key":"idtest-1100-wpa2","mac":"XX:XX:XX:XX:*:XX","flags_mask":1024}' > /tmp/curl_data
curl -sq -H "$ajson_h" -H "$cjson_h" -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-json/add_sta

sleep 1
rm -f /tmp/response
curl -sq -H "$ajson_h" -X GET -o /tmp/response http://localhost:8080/port/1/3/sta3100
if [ -s /tmp/response ]; then
   json_pp < /tmp/response
fi


#
