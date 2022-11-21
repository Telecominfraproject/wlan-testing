#!/bin/bash
atten_vals=(150 250 350 450 550 650)
len=${#atten_vals[@]}
pids=()
function runTest() {
    test_command="./test_l3_longevity.py --test_duration 60s --polling_interval 1s --upstream_port $1 --radio 'radio==$2,stations==1,ssid==wactest,ssid_pw==[BLANK],security==wpa2,wifi_mode==0,wifi_settings==wifi_settings,enable_flags==(wpa2_enable|80211u_enable|create_admin_down)' --radio 'radio==$3,stations==1,ssid==wactest,ssid_pw==[BLANK],security==wpa2,wifi_mode==0,wifi_settings==wifi_settings,enable_flags==(wpa2_enable|80211u_enable|create_admin_down)' --radio 'radio==$4,stations==1,ssid==wactest,ssid_pw==[BLANK],security==wpa2,wifi_mode==0,wifi_settings==wifi_settings,enable_flags==(wpa2_enable|80211u_enable|create_admin_down)' --endp_type lf_udp --side_a_min_bps=$5 --side_b_min_bps=$6 --side_a_min_pdu=300 --side_b_min_pdu=300 --attenuators 1.1.1036.0,1.1.1036.1,1.1.1036.2,1.1.1036.3,1.1.1037.0,1.1.1037.1,1.1.1037.2,1.1.1037.3 --atten_vals $7 --local_lf_report_dir /home/lanforge/ --no_pre_cleanup --no_stop_traffic --sta_start_offset $8" 
    mate-terminal --title="$1" -- $test_command
}
for (( i=0; i<$len; i++));
do
    curr_atten=${atten_vals[$i]}
    runTest eth2 wiphy0 wiphy4 wiphy5 0 800000000 $curr_atten 5
    runTest eth3 wiphy6 wiphy7 wiphy8 0 333000000 $curr_atten 6
    pids+=($(pgrep -u lanforge python3))
    processes_running=0
    while (( $processes_running == 0))
    do
        sleep 5
        pids=()
        pids+=($(pgrep -u lanforge python3))
        if ((${#pids[@]} == 0)) ; then
            processes_running=$((processes_running+1))
        fi
        
    done
    echo "done $i"
done



