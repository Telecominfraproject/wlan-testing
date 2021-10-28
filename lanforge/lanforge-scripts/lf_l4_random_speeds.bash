#!/bin/bash

mgr="jedtest"
url="http://10.26.0.1/random.txt"
endp_list=("tg1" "tg2")
resource=2
pause_sec=15
max_speed=1000000000
port=b2000

proxyport=NA
con_timeout=1000
url_rate=6000
url="dl $url /dev/null"
proxy_svr=NA
proxy_creds=NA
ssl_cert_fname=NA
user_agent=NA
# set proxy_auth_type=64 to enable gzip
proxy_auth_type=0
http_auth_type=0
dns_cache_timeout=0
tftp_block_sz=NA
smtpfm=NA
sec_ip=NA

function create_l4_endp() {
    echo -n " $endp"
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "set_cx_state default_tm CX_$endp STOPPED" >/dev/null
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "add_l4_endp $endp 1 $resource $port l4_generic $proxyport $con_timeout $url_rate '$url' $proxy_svr $proxy_creds $ssl_cert_fname $user_agent $proxy_auth_type $http_auth_type $dns_cache_timeout $new_speed $tftp_block_sz $smtpfm $sec_ip" >/dev/null
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "add_cx CX_$endp default_tm $endp NA" >/dev/null
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "set_endp_report_timer $endp 1000" >/dev/null
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "set_cx_report_timer default_tm CX_$endp 1000" >/dev/null
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
       "set_cx_state default_tm CX_$endp RUNNING" >/dev/null
}

# the nc_show_endpoints flushes cached endpoint settings
function ncshow() {
    ./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd --cmd \
        "nc_show_endpoints $endp" > /dev/null
}


##
##  M A I N
##

# method uses random modulus of list of speeds
set_speeds=(72800 128300 435000)
echo "Using set of speeds: ${set_speeds[@]}... "
for i in `seq 1 10`; do
    j=`expr $RANDOM % ${#set_speeds[@]}`
    new_speed=${set_speeds[$j]}
    echo -n " $new_speed bps:"
    for endp in ${endp_list[@]}; do
        create_l4_endp
        ncshow
    done
    sleep $pause_sec
done
echo ""
echo "Now using random speeds lower than $max_speed... "
# use a random fraction of maximum speed
for i in `seq 1 5`; do
    new_speed=`echo "scale=0; $max_speed / $RANDOM" | bc -l`
    new_speed=`echo "$RANDOM + $new_speed" | bc -l`
    echo -n " $new_speed bps:"
    for endp in ${endp_list[@]}; do
        create_l4_endp       
        ncshow
    done
    sleep $pause_sec
done

sleep $pause_sec

echo ""

