#!/bin/bash

# script creates a series of connections between stations and an upstream resource

set -x # turn debugging on

cx_prefix=tcp_apple
number_of_cx=10
endp_type=lf_tcp
manager=idtest

resource_a=3 # holds upstream eth3
upstream_port=eth3
tx_speed_a=1000000

resource_b=6 # holds wiphy0 with stations 0-24
tx_speed_b=15400
first_sta=0 # becomes "sta+$sta_num", up to number_of_cx-1


for sta_num in `seq $first_sta $(($number_of_cx + $first_sta - 1))`; do

    ./lf_firemod.pl --mgr $manager --resource $resource_a --action create_endp --report_timer 1000 \
        --port_name $upstream_port --endp_type $endp_type --endp_name "${cx_prefix}${sta_num}-A" \
        --speed $tx_speed_a

    ./lf_firemod.pl --mgr $manager --resource $resource_b --action create_endp --report_timer 1000 \
        --port_name "sta${sta_num}" --endp_type $endp_type --endp_name "${cx_prefix}${sta_num}-B" \
        --speed $tx_speed_b

    ./lf_firemod.pl --mgr $manager --action create_cx --report_timer 1000 \
        --cx_name "${cx_prefix}${sta_num}" --cx_endps ${cx_prefix}${sta_num}-A,${cx_prefix}${sta_num}-B

done
# flush information to LFclients
./lf_firemod.pl --mgr $manager --action do_cmd --cmd "nc_show_endpoints all" &>/dev/null
