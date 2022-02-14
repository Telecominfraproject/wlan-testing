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
switches='-sqv'
function Kurl() {
   echo =======================================================================================
   echo curl $switches $@
   echo =======================================================================================
   #set -x
   curl $switches "$@"
   #set +x
   echo ""
   echo =======================================================================================
}
function Jurl() {
   echo =J=====================================================================================
   echo curl $switches -H "$accept_json" -H "$content_json" "$@"
   echo =J=====================================================================================
   set -x
   curl $switches -H "$accept_json" -H "$content_json" "$@"
   set +x
   echo ""
   echo =J=====================================================================================
}

url="http://localhost:8080"

if true; then
   #echo 'shelf=1&resource=3&port=sta3000&mac=xx:xx:xx:xx:xx:*' > /tmp/curl_data
   echo '{"shelf":1,"resource":1,"port":"eth3","current_flags":1, "interest":2}' > /tmp/curl_data
   Jurl -X POST -d '@/tmp/curl_data' "http://localhost:8080/cli-json/set_port"
fi



exit





if false; then
   Kurl $acept_json $url/resource/1/list
   echo 'shelf=1&resource=3&port=sta3000&mac=xx:xx:xx:xx:xx:*' > /tmp/curl_data
   curl -sqv -H 'Accept: application/json' -X POST -d '@/tmp/curl_data' http://localhost:8080/cli-form/set_port

   url="http://localhost:8080/cli"
   echo 'cmd=scan_wifi+1+3+sta30000' > /tmp/curl_data
   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"

# this is not supported
#   url="http://localhost:8080/cli/scan_wifi"
#   echo '1+3+sta30000' > /tmp/curl_data
#   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"


   #Kurl -X GET "$url/help/set_wifi_radio?cli=1%203%20wiphy1%20NA%20-1%20NA%20NA%20NA%20NA%20NA%20NA%20NA%20NA%200x1%20NA"
   #CMD: set_wifi_radio 1 3 wiphy1 NA -1 NA NA NA NA NA NA NA NA 0x1 NA
   echo "shelf=1&resource=3&radio=wiphy1&channel=-1&antenna=3x3&flags=0x10" > /tmp/curl_data
   Kurl -H "$accept_json" -X POST -d "@/tmp/curl_data" "$url/cli-form/set_wifi_radio"

   #CMD: add_sta 1 3 wiphy1 sta3000 0 idtest-1000-open NA [BLANK] AUTO NA 00:0e:8e:98:64:45 8 NA NA NA NA NA 0
   echo "shelf=1&resource=3&radio=wiphy1&sta_name=sta3000&flags=0&ssid=idtest-1000-open&key=[BLANK]&ap=AUTO&mac=00:0e:8e:98:64:45&mode=8&flags_mask=0" > /tmp/curl_data
   Kurl -H "$accept_json" -X POST -d "@/tmp/curl_data" "$url/cli-form/add_sta"

   #CMD: set_port 1 3 sta3000 0.0.0.0 255.255.0.0 0.0.0.0 NA 2147483648 00:0e:8e:98:64:45 NA NA NA 8405038 1000 NA NA NA NA NA NA NA NA NA NA NA NA NA NA NA NA NONE
   echo 'shelf=&resource=1&port=3&ip_addr=sta3000&netmask=0.0.0.0&gateway=255.255.0.0&cmd_flags=0.0.0.0&mac=2147483648&mtu=00:0e:8e:98:64:45&report_timer=8405038&flags2=1000&ipv6_dflt_gw=N&bypass_wdt=A' > /tmp/curl_data
   Kurl -H "$accept_json" -X POST -d "@/tmp/curl_data" "$url/cli-form/set_port"
   echo -n "shelf=1&resource=3&radio=wiphy1&mode=NA&channel=-1&country=NA&frequency=NA&frag_thresh=NA" > /tmp/curl_data
   echo -n "&rate=NA&rts=NA&txpower=NA&mac=NA&antenna=NA&flags=1&flags_mask=1&const_tx=NA" >> /tmp/curl_data
   echo -n "&pulse_width=NA&pulse_interval=NA&vdev_count=NA&peer_count=NA&stations_count=NA" >> /tmp/curl_data
   echo -n "&rate_ctrl_count=NA&fwname=NA&fwver=NA&txdesc_count=NA&tids_count=NA&skid_limit=NA" >> /tmp/curl_data
   echo -n "&active_peer_count=NA&tx_pulses=NA&pulse2_interval_us=NA&max_amsdu=NA&pref_ap=NA" >> /tmp/curl_data
   Kurl -X GET -d "@/tmp/curl_data"  $url/help/set_wifi_radio

   echo -n "http://cholla:8080/help/set_wifi_radio?"
   echo -n "shelf=1&resource=3&radio=wiphy1&mac=02:04:05:06:07:11&flags=1&flags_mask=1"

# -1=auto or -1=ANY
#CMD: set_wifi_radio 1 3 wiphy1 NA -1 NA NA NA NA NA NA NA NA 0x1 NA
   echo -n "shelf=1&resource=3&radio=NA&mode=NA&channel=NA&country=NA&frequency=NA&frag_thresh=NA" > /tmp/curl_data
   echo -n "&rate=NA&rts=NA&txpower=NA&mac=NA&antenna=NA&flags=NA&flags_mask=NA&const_tx=NA" >> /tmp/curl_data
   echo -n "&pulse_width=NA&pulse_interval=NA&vdev_count=NA&peer_count=NA&stations_count=NA" >> /tmp/curl_data
   echo -n "&rate_ctrl_count=NA&fwname=NA&fwver=NA&txdesc_count=NA&tids_count=NA&skid_limit=NA" >> /tmp/curl_data
   echo -n "&active_peer_count=NA&tx_pulses=NA&pulse2_interval_us=NA&max_amsdu=NA&pref_ap=NA" >> /tmp/curl_data
   url="http://localhost:8080/cli-form/set_wifi_radio"
   Kurl -X POST -d "@/tmp/curl_data" $url
#CMD: add_sta 1 3 wiphy1 sta3000 0 idtest-1000-open NA [BLANK] AUTO NA 00:0e:8e:98:64:45 8 NA NA NA NA NA 0 
#CMD: set_port 1 3 sta3000 0.0.0.0 255.255.0.0 0.0.0.0 NA 2147483648 00:0e:8e:98:64:45 NA NA NA 8405038 1000 NA NA NA NA NA NA NA NA NA NA NA NA NA NA NA NA NONE 

   # help demo
   url="http://localhost:8080/cli-form/add_vsta"
   Kurl  -X POST -d 'help=1' -H "$accept_json"  "$url"
   Kurl  -X POST -d 'help=?' -H "$accept_json"  "$url"
   Kurl  -X POST -d 'help=%63' -H "$accept_json"  "$url"
   #$::resource, $::sta_wiphy, $sta_name, "$flags", "$::ssid", "$::passphrase", $mac_addr, "$flagsmask", $wifi_m, $::bssid);
   url="http://localhost:8080/cli-form/add_vsta"
   echo 'shelf=1&resource=3&sta_wiphy=&sta_name=&flags=&ssid=&passphrase=&flagsmask=&wifi_m=&bssid=' > /tmp/curl_data
   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"

   url="http://localhost:8080/cli-form/add_sta"
   echo 'shelf=1&resource=3&sta_wiphy=&sta_name=&flags=&ssid=&passphrase=&flagsmask=&wifi_m=&bssid=' > /tmp/curl_data
   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"

   #fmt_port_cmd($resource, $sta_name, $ip_addr, $mac_addr);
   url="http://localhost:8080/cli-form/set_port"
   echo 'shelf=1&resource=3&port=&ip_addr=&mac=' > /tmp/curl_data
   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"

   #if ($::admin_down_on_add) {
   #  my $cur_flags = 0x1; # port down
   #  my $ist_flags = 0x800000; # port down
   #  $sta1_cmd = fmt_cmd("set_port", 1, $resource, $sta_name, "NA",
   #                      "NA", "NA", "NA", "$cur_flags",
   #                      "NA", "NA", "NA", "NA", "$ist_flags");
   #  3doCmd($sta1_cmd);
   #}

   echo 'cmd=set_port_alias&shelf=1&resource=2&port=sta333&vport=NA&alias=bob33' > /tmp/curl_data
   Kurl -X POST --data "@/tmp/curl_data" -H "$accept_json"  -H "$content_plain" "$url"
   sleep 5
   echo 'cmd=set_port_alias&shelf=1&resource=2&port=sta333&vport=NA&alias=bob33' > /tmp/curl_data
   Kurl  -X POST --data "@/tmp/curl_data" -H "$accept_json"  -H "$content_json" "$url"

   echo 'shelf=1&resource=3&port=12&vport=NA&alias-64=Ym9iMzMK' > /tmp/curl_data
   Kurl  -X POST --data "@/tmp/curl_data" -H "$accept_json"  "$url"

   echo 'shelf=1&resource=3&port=12&vport=NA&alias=bob+33' > /tmp/curl_data
   Kurl  -X POST --data "@/tmp/curl_data" -H "$accept_json"  "$url"

   url="http://localhost:8080/cli-form/"
   Kurl  -X POST -d 'cmd=gossip&message=hi+there' -H "$accept_json"  "$url"

   url="http://localhost:8080/cli-form/scan_wifi"
   echo 'shelf=1&resource=3&port=sta30000' > /tmp/curl_data
   Kurl  -X POST -d '@/tmp/curl_data' -H "$accept_json"  "$url"

   # the protocol command can only send back errors
   # udp--2.b2000-03.sta30000
   #url="http://localhost:8080/cli-form/getMAC"
   #echo 'CX=udp--2.b2000-03.sta30000&AorB=A' > /tmp/curl_data
   #Kurl  -X POST --data "@/tmp/curl_data" -H "$accept_json"  "$url"

fi

echo ""
echo "END"

exit
echo =======================================================================================
url="http://localhost:8080/port/1/2/2"

Kurl -X GET $url
Kurl -X HEAD $url
Kurl -X PUT $url
Kurl -X DELETE $url



port_fields=(
         "Crypt"
         "Beacon"
         "MAC"
         "QLEN"
         "Misc"
         "Phantom"
         "TX Pkts"
         "Login-Fail"
         "IPv6 Gateway"
         "Logout-OK"
         "CX Time (us)"
         "Connections"
         "Mask"
         "No CX (us)"
         "Channel"
         "RX Bytes"
         "bps RX"
         "TX Errors"
         "RX-Rate"
         "ANQP Time (us)"
         "RX Miss"
         "Bytes TX LL"
         "SSID"
         "TX Fifo"
         "DHCP (ms)"
         "Retry"
         "Port"
         "Bytes RX LL"
         "RX Errors"
         "4Way Time (us)"
         "Logout-Fail"
         "Pps RX"
         "MTU"
         "AP"
         "RX Length"
         "Parent Dev"
         "bps RX LL"
         "RX Fifo"
         "RX Drop"
         "Pps TX"
         "Noise"
         "IP"
         "TX Wind"
         "RX Frame"
         "Key/Phrase"
         "Signal"
         "SEC"
         "IPv6 Address"
         "TX Abort"
         "Device"
         "Gateway IP"
         "TX-Rate"
         "CX Ago"
         "RX Pkts"
         "Reset"
         "TX Crr"
         "RX Over"
         "TX Bytes"
         "Activity"
         "Collisions"
         "Alias"
         "bps TX"
         "bps TX LL"
         "Status"
         "TX HB"
         "Down"
         "RX CRC"
         "Login-OK"
      )
for name in "${port_fields[@]}"; do
   #echo "field <$name>"
   name2="${name// /%20}"
   url="http://localhost:8080/port/1/2/2,3,4?fields=$name2,Port"
   echo -n "..."
   curl -si -H 'Accept: application/json' "$url" > /tmp/response
   echo "$url"
   grep 'HTTP/1.1' /tmp/response
   tail -1 /tmp/response
   echo ""
   sleep 0.05
done
