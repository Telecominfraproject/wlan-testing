#!/bin/bash
# this is a test of the JSON add/show chamber api
echo 'name=cha&flags=OPEN' > /tmp/curl_data
curl -sqv -H 'Accept: application/json' -X POST -d '@/tmp/curl_data' http://cholla5:8080/cli-form/add_chamber

echo 'name=cha' > /tmp/curl_data
curl -sqv -H 'Accept: application/json' -X POST -d '@/tmp/curl_data' http://cholla5:8080/cli-form/show_chamber

#chamber [id] [angle] [flags] [table-speed-rpm]
#echo "cmd=chamber&arg1=cha&arg2=0&arg3=OPEN&arg5=3" > /tmp/curl_data
echo 'cmd=chamber&arg1=cha&arg2=0&arg3=open&arg5=3'
curl -sqv -H 'Accept: application/json' -X POST -d '@/tmp/curl_data' http://cholla5:8080/cli-form/admin

