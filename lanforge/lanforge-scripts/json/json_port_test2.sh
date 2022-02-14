#!/bin/bash
set -e
unset proxy
unset http_proxy
Q='"'
q="'"
S='*'
application_json="application/json"
accept_json="Accept: $application_json"
accept_html='Accept: text/html'
accept_text='Accept: text/plain'
#accept_any="'Accept: */*'" # just dont use
content_plain='Content-Type: text/plain'
content_json="Content-Type: $application_json"
switches='-sq'
#switches='-sq'

function Kurl() {
   echo "======================================================================================="
   echo "curl $switches $@"
   echo "======================================================================================="
   curl $switches "$@" | json_pp
   echo ""
   echo "======================================================================================="
}

function Jurl() {
   echo "=J====================================================================================="
   echo "curl $switches -H $accept_json -H $content_json $@"
   echo "=J====================================================================================="
   curl $switches -H "$accept_json" -H "$content_json" -X POST "$@"
   echo ""
   echo "=J====================================================================================="
}

url="http://jedtest.jbr:8080"
#url="http://127.0.0.1:8080"
data_file="/var/tmp/data.$$"
result_file="/var/tmp/result_file.$$"

function PortDown() {
   echo "{\"shelf\":1,\"resource\":3,\"port\":\"$1\",\"current_flags\":1, \"interest\":8388610}" > $data_file
   curl $switches -H "$accept_json" -H "$content_json" -X POST  -d"@$data_file" "$url/cli-json/set_port"
   sleep 0.3
   for f in `seq 1 10`; do
      echo "{\"shelf\":1,\"resource\":3,\"port\":\"$1\"}" > $data_file
      curl $switches -H "$accept_json" -H "$content_json" -X POST -d"@$data_file" "$url/cli-json/nc_show_ports"
      sleep 0.5
      curl $switches "$url/port/1/3/$1?fields=alias,ip,down" | json_reformat > $result_file
      egrep '"down" *: "?true"?' $result_file && break || :
   done
}

function PortUp() {
   #set_port 1 3 sta3101 NA NA NA NA 0 NA NA NA NA 8388610
   echo "{\"shelf\":1,\"resource\":3,\"port\":\"$1\",\"current_flags\":0, \"interest\":8388610}" > $data_file
   curl $switches -H "$accept_json" -H "$content_json" -X POST  -d"@$data_file" "$url/cli-json/set_port"
   sleep 1
   for f in `seq 1 100`; do
      echo "{\"shelf\":1,\"resource\":3,\"port\":\"$1\"}" > $data_file
      #Jurl -d"@$data_file" "$url/cli-json/nc_show_ports"
      curl $switches -H "$accept_json" -H "$content_json" -X POST -d"@$data_file" "$url/cli-json/nc_show_ports"
      sleep 0.5
      curl $switches "$url/port/1/3/$1?fields=alias,ip,down" | json_reformat > $result_file
      #cat $result_file
      egrep '"down" : "?false"?' $result_file && break || :
   done
}

function CxToggle() {
   echo "{\"test_mgr\":\"all\",\"cx_name\":\"$1\",\"cx_state\":\"$2\"}" > $data_file
   curl $switches -H "$accept_json" -H "$content_json" -X POST  -d"@$data_file" "$url/cli-json/set_cx_state"
}

while true; do
   for e in `seq 3000 3020` ; do
      ea="udp:r3r2:$e"
      eu="udp%3Ar3r2%3A${e}-A"
      CxToggle "$ea" "STOPPED"
      sleep 0.1
      curl $switches  -H "$accept_json" "$url/endp/$eu?fields=name,run" | json_reformat > $result_file
      sleep 0.1
   done
   for sta in `seq 100 121`; do
      stb=$(( $sta + 3000))
      PortDown "sta$stb"
   done
   for sta in `seq 100 121`; do
      stb=$(( $sta + 3000))
      PortUp "sta$stb"
   done
   sleep 4
   for e in `seq 3000 3020` ; do
      ea="udp:r3r2:$e"
      eu="udp%3Ar3r2%3A${e}-A"
      CxToggle "$ea" "RUNNING"
      sleep 0.1
      curl $switches  -H "$accept_json" "$url/endp/$eu?fields=name,run" | json_reformat > $result_file
      sleep 0.1
   done
   sleep 14
done

#
