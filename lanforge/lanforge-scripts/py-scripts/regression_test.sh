#!/bin/bash
##########################
# Help
##########################
Help()
{
  echo "This bash script aims to automate the test process of all Candela Technologies's test_* scripts in the lanforge-scripts directory. The script can be run 2 ways and may include (via user input) the \"start_num\" and \"stop_num\" variables to select which tests should be run."
  echo "OPTION ONE: ./regression_test.sh : this command runs all the scripts in the array \"testCommands\""
  echo "OPTION TWO: ./regression_test.sh 4 5 :  this command runs py-script commands (in testCommands array) that include the py-script options beginning with 4 and 5 (inclusive) in case function ret_case_num."
  echo "Optional Variables:"
  echo "SSID is the name of the network you are testing against"
  echo "PASSWD is the password of said network"
  echo "SECURITY is the security protocol of the network"
  echo "MGR is the IP address of the device which has LANforge installed, if different from the system you are using."
  echo "A is used to call to test a specific command based on"
  echo "F is used to pass in an RC file which can store the credentials for running regression multiple times on your system"
  echo "Example command: ./regression_test.sh -s SSID -p PASSWD -w SECURITY -m MGR"
}

while getopts ":h:s:p:w:m:A:r:F:B:U:" option; do
  case "${option}" in
    h) # display Help
      Help
      exit 1
      ;;
    s)
      SSID_USED=${OPTARG}
      ;;
    p)
      PASSWD_USED=${OPTARG}
      ;;
    w)
      SECURITY=${OPTARG}
      ;;
    m)
      MGR=${OPTARG}
      ;;
    A)
      A=${OPTARG}
      ;;
    r)
      RADIO_USED=${OPTARG}
      ;;
    F)
      RC_FILE=${OPTARG}
      ;;
    B)
      BSSID=${OPTARG}
      ;;
    U)
      UPSTREAM=$OPTARG
      ;;
    *)

      ;;
  esac
done

if [[ ${#SSID_USED} -eq 0 ]]; then #Network credentials
  SSID_USED="jedway-wpa2-x2048-5-3"
  PASSWD_USED="jedway-wpa2-x2048-5-3"
  SECURITY="wpa2"
fi

if [[ ${#RADIO_USED} -eq 0 ]]; then # Allow the user to change the radio they test against
  RADIO_USED="wiphy1"
fi

if [[ ${#UPSTREAM} -eq 0 ]]; then
  UPSTREAM="eth1"
fi

if [[ ${#BSSID} -eq 0 ]]; then
  BSSID="04:f0:21:2c:41:84"
fi

FILE="/tmp/gui-update.lock"
if test -f "$FILE"; then
  echo "Finish updating your GUI"
  exit 0
fi

HOMEPATH=$(realpath ~)

if [[ ${#RC_FILE} -gt 0 ]]; then
  source "$RC_FILE"
fi

if [[ ${#SSID_USED} -gt 0 ]]; then
  if [ -f ./regression_test.rc ]; then
    source ./regression_test.rc # this version is a better unix name
  elif [ -f ./regression_test.txt ]; then
    source ./regression_test.txt # this less unixy name was discussed earlier
  fi
fi
NUM_STA=${NUM_STA:-4}
TEST_HTTP_IP=${TEST_HTTP_IP:-10.40.0.1}
MGRLEN=${#MGR}
COL_NAMES="name,tx_bytes,rx_bytes,dropped"

#CURR_TEST_NUM=0
CURR_TEST_NAME="BLANK"

REPORT_DIR="${HOMEPATH}/html-reports"
if [ ! -d "$REPORT_DIR" ]; then
    echo "Report directory [$REPORT_DIR] not found, bye."
    exit 1
fi
REPORT_DATA="${HOMEPATH}/report-data"
if [ ! -d "${REPORT_DATA}" ]; then
    echo "Data directory [$REPORT_DATA] not found, bye."
    exit 1
fi
TEST_DIR="${REPORT_DATA}/${NOW}"

function run_l3_longevity() {
  ./test_l3_longevity.py --test_duration 15s --upstream_port eth1 --radio "radio==wiphy0 stations==4 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY" --radio "radio==wiphy1 stations==4 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY" --mgr "$MGR"
}
function testgroup_list_groups() {
  ./scenario.py --load test_l3_scenario_throughput
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003 --list_groups --debug --mgr "$MGR"
}
function testgroup_list_connections() {
  ./scenario.py --load test_l3_scenario_throughput
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003 --show_group --debug --mgr "$MGR"
}
function testgroup_delete_group() {
  ./scenario.py --load test_l3_scenario_throughput
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003
  ./testgroup.py --group_name group1--del_group --debug --mgr "$MGR"
}
if [[ $MGRLEN -gt 0 ]]; then
  testCommands=(
      #"./create_bond.py --network_dev_list eth0,eth1 --debug --mgr $MGR"
      #"./create_bridge.py --radio $RADIO_USED --upstream_port eth1 --target_device sta0000 --debug --mgr $MGR"
      "./create_chamberview.py -m $MGR -cs \"regression_test\" --line \"Resource=1.1 Profile=STA-AC Amount=1 Uses-1 $RADIO_USED Freq=-1 DUT=TEST DUT_RADIO=$RADIO_USED Traffic=http\" --line \"Resource=1.1 Profile=upstream Amount=1 Uses-1=eth1 Uses-2=AUTO Freq=-1 DUT=Test DUT_RADIO=$RADIO_USED Traffic=http\""
      "./create_chamberview_dut.py --lfmgr $MGR --dut_name regression_dut --ssid \"ssid_idx=0 ssid=$SSID_USED security=$SECURITY password=$PASSWD_USED bssid=04:f0:21:2c:41:84\""
      #"./create_l3.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      #"./create_l4.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      #"./create_macvlan.py --radio 1.$RADIO_USED --macvlan_parent eth1 --debug --mgr $MGR"
      #"./create_qvlan.py --first_qvlan_ip 192.168.1.50 --mgr $MGR"
      #"./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_vap.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_vr.py --vr_name 2.vr0 --ports 2.br0,2.vap2 --services 1.br0=dhcp,nat --services 1.vr0=radvd"
      #./create_wanlink
      #./csv_convert
      #./csv_processor
      #./csv_to_grafana
      #./csv_to_influx
      "./cv_manager.py --mgr $MGR --scenario FACTORY_DFLT"
      #"./cv_to_grafana --mgr $MGR "
      #"./docstrings.py --mgr $MGR"
      #"./event_breaker --mgr $MGR"
      #"./event_flood --mgr $MGR"
      "./example_security_connection.py --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --radio $RADIO_USED --security wpa2 --debug --mgr $MGR"
      #./ftp_html.py
      #./ghost_profile
      #./grafana_profile
      #./html_template
      #./influx
      #./layer3_test.py --mgr $MGR --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY
      #./layer4_test --mgr $MGR --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY
      "./lf_ap_auto_test.py --mgr $MGR --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name ap-auto-instance --config_name test_con --upstream 1.1.eth2 \
      --dut5_0 \"linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)\" \
      --dut2_0 \"linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)\" \
      --max_stations_2 100 --max_stations_5 100 --max_stations_dual 200 \
      --radio2 1.1.wiphy0 --radio2 1.1.wiphy1 \
      --set \"Basic Client Connectivity\" 1 --set \"Multi Band Performance\" 1 \
      --set \"Skip 2.4Ghz Tests\" 1 --set \"Skip 5Ghz Tests\" 1 \
      --set \"Throughput vs Pkt Size\" 0 --set 'Capacity' 0 --set 'Stability' 0 --set 'Band-Steering' 0 \
      --set \"Multi-Station Throughput vs Pkt Size\" 0 --set \"Long-Term\" 0 \
      --pull_report \
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
      --influx_bucket ben \
      --influx_tag testbed Ferndale-01"
      #./lf_atten_mod_test
      #./lf_csv
      #./lf_dataplane_config
      "./lf_dataplane_test.py --mgr $MGR --lf_user lanforge --lf_password lanforge \
          --instance_name dataplane-instance --config_name test_con --upstream 1.1.$UPSTREAM \
          --dut linksys-8450 --duration 15s --station 1.1.sta01500 \
          --download_speed 85% --upload_speed 0 \
          --raw_line \"pkts: Custom;60;142;256;512;1024;MTU\" \
          --raw_line \"cust_pkt_sz: 88 1200\" \
          --raw_line \"directions: DUT Transmit;DUT Receive\" \
          --raw_line \"traffic_types: UDP;TCP\" \
          --test_rig Testbed-01 --pull_report \
          --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
          --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
          --influx_bucket ben \
          --influx_tag testbed Ferndale-01"
      #./lf_dfs_test
      #./lf_dut_sta_vap_test
      #"./lf_ftp.py --mgr $MGR --mgr_port 8080 --upstream_port $UPSTREAM --ssid $SSID --security $SECURITY --passwd $PASSWD_USED \
      # --ap_name WAC505 --ap_ip 192.168.213.90 --bands Both --directions Download --twog_radio wiphy1 --fiveg_radio wiphy0 --file_size 2MB --num_stations 40 --Both_duration 1 --traffic_duration 2 --ssh_port 22_"
      "./lf_ftp_test.py --mgr $MGR --ssid $SSID --passwd $PASSWD_USED --security $SECURITY --bands 5G --direction Download \
           --file_size 2MB --num_stations 2"
      "./lf_graph.py --mgr $MGR"
      #"./lf_mesh_test.py --mgr $MGR --upstream $UPSTREAM --raw_line 'selected_dut2 RootAP wactest $BSSID'"
      #./lf_multipsk
      #./lf_report
      #./lf_report_test
      #./lf_rvr_test
      #./lf_rx_sensitivity_test.py
      #./lf_sniff_radio
      #./lf_snp_test
      "./lf_tr398_test.py --mgr $MGR"
      #./lf_webpage
      "./lf_wifi_capacity_test.py --mgr $MGR --port 8080 --lf_user lanforge --lf_password lanforge \
             --instance_name this_inst --config_name test_con --upstream 1.1.eth2 --batch_size 1,5,25,50,100 --loop_iter 1 \
             --protocol UDP-IPv4 --duration 6000 --pull_report \
             --test_rig Testbed-01"
             #--influx_host c7-graphana --influx_port 8086 --influx_org Candela \
             #--influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
             #--influx_bucket ben \
      #measure_station_time_up.py
      #modify_station.py
      #modify_vap.py
      #recordinflux.py
      #run_cv_scenario.py
      #rvr_scenario.py
      #scenario.py
      #sta_connect2.py
      #sta_connect_bssid_mac.py
      #sta_connect_example.py
      #sta_connect_multi_example.py
      #sta_connect.py
      #sta_scan_test.py
      #station_layer3.py
      #stations_connected.py
      #test_1k_clients_jedtest.py
      #test_client_admission.py
      "./test_fileio.py --macvlan_parent eth2 --num_ports 3 --use_macvlans --first_mvlan_ip 192.168.92.13 --netmask 255.255.255.0 --gateway 192.168.92.1 --test_duration 30s --mgr $MGR" # Better tested on Kelly, where VRF is turned off
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfping --dest $TEST_HTTP_IP --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type speedtest --speedtest_min_up 20 --speedtest_min_dl 20 --speedtest_max_ping 150 --security $SECURITY --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type iperf3 --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfcurl --dest $TEST_HTTP_IP --file_output ${HOMEPATH}/Documents/lfcurl_output.txt --debug --mgr $MGR"
      "./testgroup.py --group_name group1 --add_group --list_groups --debug --mgr $MGR"
      #testgroup_list_groups
      #testgroup_list_connections
      #testgroup_delete_group
      #"./testgroup2.py --num_stations 4 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --radio $RADIO_USED --group_name group0 --add_group --mgr $MGR"
      "./test_ip_connection.py --radio $RADIO_USED --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      #"./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format excel --layer3_cols $COL_NAMES --debug --mgr $MGR  --traffic_type lf_udp"
      #"./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format csv --layer3_cols $COL_NAMES --debug --mgr $MGR  --traffic_type lf_udp"
      "./test_ip_connection.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR --ipv6"
      #"./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --debug --mgr $MGR --ipv6 --traffic_type lf_udp"
      #./test_ipv4_ps
      #./test_ipv4_ttls
      "./test_l3_longevity.py --mgr $MGR --endp_type 'lf_udp lf_tcp' --upstream_port 1.1.$UPSTREAM \
          --radio \"radio==1.1.wiphy0 stations==10 ssid==ASUS_70 ssid_pw==[BLANK] security==open\" \
          --radio \"radio==1.1.wiphy1 stations==1 ssid==ASUS_70 ssid_pw==[BLANK] security==open\" \
          --test_duration 5s --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
          --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
          --influx_bucket ben --rates_are_totals --side_a_min_bps=20000 --side_b_min_bps=300000000 \
          --influx_tag testbed regression_test --influx_tag DUT ROG -o longevity.csv"
      "./test_l3_powersave_traffic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./test_l3_scenario_throughput.py -t 15s -sc test_l3_scenario_throughput -m $MGR"
      #./test_l3_unicast_traffic_gen
      #./test_l3_unicast_traffic_gen
      #./test_l3_WAN_LAN
      #./test_l4
      "./test_status_msg.py --debug --mgr $MGR" #this is all which is needed to run
      #"./test_wanlink.py --name my_wanlink4 --latency_A 20 --latency_B 69 --rate 1000 --jitter_A 53 --jitter_B 73 --jitter_freq 6 --drop_A 12 --drop_B 11 --debug --mgr $MGR"
      #./test_wpa_passphrases
      #./tip_station_powersave
      #./vap_stations_example
      #./video_rates
      "./wlan_capacity_calculator.py -sta 11abg -t Voice -p 48 -m 106 -e WEP -q Yes -b 1 2 5.5 11 -pre Long -s N/A -co G.711 -r Yes -c Yes -m $MGR"
      "./wlan_capacity_calculator.py -sta 11n -t Voice -d 17 -ch 40 -gu 800 -high 9 -e WEP -q Yes -ip 5 -mc 42 -b 6 9 12 24 -m 1538 -co G.729 -pl Greenfield -cw 15 -r Yes -c Yes -m $MGR"
      "./wlan_capacity_calculator.py -sta 11ac -t Voice -d 9 -spa 3 -ch 20 -gu 800 -high 1 -e TKIP -q Yes -ip 3 -mc 0 -b 6 12 24 54 -m 1518 -co Greenfield -cw 15 -rc Yes -m $MGR"
      #"./ws_generic_monitor_test.py --mgr $MGR"
  )
elif [[ $MGR == "short" ]]; then
  testCommands=(
      run_l3_longevity
      "./test_ipv4_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format excel --layer3_cols $COL_NAMES --debug --mgr $MGR"
  )
else
  testCommands=(
       #"../cpu_stats.py --duration 15"
      "./example_security_connection.py --num_stations $NUM_STA --ssid jedway-wpa-1 --passwd jedway-wpa-1 --radio $RADIO_USED --security wpa --debug"
      "./example_security_connection.py --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --radio $RADIO_USED --security wpa2 --debug"
      "./example_security_connection.py --num_stations $NUM_STA --ssid jedway-wep-48 --passwd 0123456789 --radio $RADIO_USED --security wep --debug"
      "./example_security_connection.py --num_stations $NUM_STA --ssid jedway-wpa3-1 --passwd jedway-wpa3-1 --radio $RADIO_USED --security wpa3 --debug"
      "./sta_connect2.py --dut_ssid $SSID_USED --dut_passwd $PASSWD_USED --dut_security $SECURITY"
      "./sta_connect_example.py"
      # want if [[ $DO_FILEIO = 1 ]]
      "./test_fileio.py --macvlan_parent eth2 --num_ports 3 --use_macvlans --first_mvlan_ip 192.168.92.13 --netmask 255.255.255.0 --test_duration 30s --gateway 192.168.92.1" # Better tested on Kelly, where VRF is turned off
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfping --dest $TEST_HTTP_IP --debug"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type speedtest --speedtest_min_up 20 --speedtest_min_dl 20 --speedtest_max_ping 150 --security $SECURITY --debug"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type iperf3 --debug"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfcurl --dest $TEST_HTTP_IP --file_output ${HOMEPATH}/Documents/lfcurl_output.txt --debug"
      "./testgroup.py --group_name group1 --add_group --list_groups --debug"
      testgroup_list_groups
      testgroup_list_connections
      testgroup_delete_group
      "./testgroup2.py --num_stations 4 --ssid lanforge --passwd password --security wpa2 --radio wiphy0 --group_name group0 --add_group"
      "./test_ipv4_connection.py --radio $RADIO_USED --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./test_ipv4_l4_urls_per_ten.py --radio $RADIO_USED --num_stations $NUM_STA --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED --num_tests 1 --requests_per_ten 600 --target_per_ten 600 --debug"
      "./test_ipv4_l4_wifi.py --radio $RADIO_USED --num_stations $NUM_STA --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED --test_duration 15s --debug"
      "./test_ipv4_l4.py --radio $RADIO_USED --num_stations 4 --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED --test_duration 15s --debug"
      "./test_ipv4_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format excel --layer3_cols $COL_NAMES --traffic_type lf_udp --debug"
      "./test_ipv4_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format csv --layer3_cols $COL_NAMES --traffic_type lf_udp --debug"
      "./test_ipv4_l4_ftp_upload.py --upstream_port eth1 --radio $RADIO_USED --num_stations $NUM_STA --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED --test_duration 15s --debug"
      "./test_ipv6_connection.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./test_ipv6_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --cx_type tcp6 --debug"
      run_l3_longevity
      "./test_l3_powersave_traffic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      #"./test_l3_scenario_throughput.py -t 15s -sc test_l3_scenario_throughput" #always hangs the regression
      "./test_status_msg.py --action run_test " #this is all which is needed to run
      "./test_wanlink.py --debug"
      #"./ws_generic_monitor_test.py"
      #"../py-json/ws-sta-monitor.py --debug"
      "./create_bridge.py --radio $RADIO_USED --upstream_port eth1 --target_device sta0000 --debug"
      "./create_l3.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./create_l4.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./create_macvlan.py --radio $RADIO_USED --macvlan_parent eth1 --debug"
      "./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./create_vap.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug"
      "./create_vr.py --vr_name 2.vr0 --ports 2.br0,2.vap2 --services"
      "./create_qvlan.py --radio $RADIO_USED --qvlan_parent eth1"
      "./wlan_capacity_calculator.py -sta 11abg -t Voice -p 48 -m 106 -e WEP -q Yes -b 1 2 5.5 11 -pre Long -s N/A -co G.711 -r Yes -c Yes"
      "./wlan_capacity_calculator.py -sta 11n -t Voice -d 17 -ch 40 -gu 800 -high 9 -e WEP -q Yes -ip 5 -mc 42 -b 6 9 12 24 -m 1538 -co G.729 -pl Greenfield -cw 15 -r Yes -c Yes"
      "./wlan_capacity_calculator.py -sta 11ac -t Voice -d 9 -spa 3 -ch 20 -gu 800 -high 1 -e TKIP -q Yes -ip 3 -mc 0 -b 6 12 24 54 -m 1518 -co Greenfield -cw 15 -rc Yes"
  )
fi
#declare -A name_to_num
#if you want to run just one test as part of regression_test, you can call one test by calling its name_to_num identifier.
name_to_num=(
    ["create_bond"]=1
    ["create_bridge"]=2
    ["create_l3"]=3
    ["create_l4"]=4
    ["create_macvlan"]=5
    ["create_qvlan"]=6
    ["create_station"]=7
    ["create_va"]=8
    ["create_vr"]=9
    ["create_wanlink"]=10
    ["csv_convert"]=11
    ["csv_processor"]=12
    ["csv_to_grafana"]=13
    ["csv_to_influx"]=14
    ["cv_manager"]=15
    ["cv_to_grafana"]=16
    ["docstrings"]=17
    ["event_breaker"]=18
    ["event_flood"]=19
    ["example_security_connection"]=20
    ["ftp_html"]=21
    ["ghost_profile"]=22
    ["grafana_profile"]=23
    ["html_template"]=24
    ["influx"]=25
    ["layer3_test"]=26
    ["layer4_test"]=27
    ["lf_ap_auto_test"]=28
    ["lf_atten_mod_test"]=29
    ["lf_csv"]=30
    ["lf_dataplane_config"]=31
    ["lf_dataplane_test"]=32
    ["lf_dfs_test"]=33
    ["lf_dut_sta_vap_test"]=34
    ["lf_ft"]=35
    ["lf_ftp_test"]=36
    ["lf_graph"]=37
    ["lf_influx_db"]=38
    ["lf_mesh_test"]=39
    ["lf_multipsk"]=40
    ["lf_report"]=41
    ["lf_report_test"]=42
    ["lf_rvr_test"]=43
    ["lf_rx_sensitivity_test"]=44
    ["lf_sniff_radio"]=45
    ["lf_snp_test"]=46
    ["lf_tr398_test"]=47
    ["lf_webpage"]=48
    ["lf_wifi_capacity_test"]=49
    ["measure_station_time_u"]=50
    ["modify_station"]=51
    ["modify_va"]=52
    ["run_cv_scenario"]=53
    ["rvr_scenario"]=54
    ["scenario"]=55
    ["sta_connect"]=56
    ["sta_connect2"]=57
    ["sta_connect_bssid_mac"]=58
    ["sta_connect_example"]=59
    ["sta_connect_multi_example"]=60
    ["sta_connect_bssid_mac"]=61
    ["sta_connect_example"]=62
    ["sta_connect_multi_example"]=63
    ["sta_scan_test"]=64
    ["station_layer3"]=65
    ["stations_connected"]=66
    ["sta_scan_test"]=67
    ["station_layer3"]=68
    ["stations_connected"]=69
    ["test_1k_clients_jedtest"]=70
    ["test_client_admission"]=71
    ["test_fileio"]=72
    ["test_generic"]=73
    ["test_generic"]=74
    ["test_generic"]=75
    ["test_generic"]=76
    ["testgrou"]=77
    ["testgroup_list_groups"]=78
    ["testgroup_list_connections"]=79
    ["testgroup_delete_grou"]=80
    ["testgroup2"]=81
    ["test_ip_connection"]=82
    ["test_ip_variable_time"]=83
    ["test_ip_variable_time"]=84
    ["test_ip_connection"]=85
    ["test_ip_variable_time"]=86
    ["test_ipv4_ps"]=87
    ["test_ipv4_ttls"]=88
    ["test_l3_longevit"]=89
    ["test_l3_powersave_traffic"]=90
    ["test_l3_scenario_throughput"]=91
    ["test_l3_unicast_traffic_gen"]=92
    ["test_l3_unicast_traffic_gen"]=93
    ["test_l3_WAN_LAN"]=94
    ["test_l4"]=95
    ["test_status_msg"]=96
    ["test_wanlink"]=97
    ["test_wpa_passphrases"]=98
    ["tip_station_powersave"]=99
    ["vap_stations_example"]=100
    ["video_rates"]=101
    ["wlan_capacity_calculator"]=102
    ["wlan_capacity_calculator"]=103
    ["wlan_capacity_calculator"]=104
    ["ws_generic_monitor_test"]=105
)

function blank_db() {
    echo "Loading blank scenario..." >>"${HOMEPATH}/regression_file.txt"
    ./scenario.py --load BLANK >>"${HOMEPATH}/regression_file.txt"
    #check_blank.py
}

function echo_print() {
    echo "Beginning $CURR_TEST_NAME test..." >>"${HOMEPATH}/regression_file.txt"
}

function test() {
  if [[ $MGRLEN -gt 0 ]]; then
    ./scenario.py --load FACTORY_DFLT --mgr "${MGR}"
  else
    ./scenario.py --load FACTORY_DFLT
  fi

  echo ""
  echo "Test $CURR_TEST_NAME"

  echo_print
  echo "$i"
  $i > "${TEST_DIR}/${NAME}.txt" 2> "${TEST_DIR}/${NAME}_stderr.txt"
  chmod 664 "${TEST_DIR}/${NAME}.txt"
  FILESIZE=$(stat -c%s "${TEST_DIR}/${NAME}_stderr.txt") || 0
  if (( FILESIZE > 0)); then
      results+=("<tr><td>${CURR_TEST_NAME}</td><td class='scriptdetails'>${i}</td>
                <td class='failure'>Failure</td>
                <td><a href=\"${URL2}/${NAME}.txt\" target=\"_blank\">STDOUT</a></td>
                <td><a href=\"${URL2}/${NAME}_stderr.txt\" target=\"_blank\">STDERR</a></td></tr>")
  else
      results+=("<tr><td>${CURR_TEST_NAME}</td><td class='scriptdetails'>${i}</td>
                <td class='success'>Success</td>
                <td><a href=\"${URL2}/${NAME}.txt\" target=\"_blank\">STDOUT</a></td>
                <td></td></tr>")
  fi
}

function run_test()  {
  if [[ ${#A} -gt 0 ]]; then
    for i in "${testCommands[@]}"; do
      NAME=$(cat < /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
      CURR_TEST_NAME=${i%%.py*}
      CURR_TEST_NAME=${CURR_TEST_NAME#./*}
      #CURR_TEST_NUM="${name_to_num[$CURR_TEST_NAME]}"
      if [[ $A == "$CURR_TEST_NAME" ]]; then
        test
      fi
    done
  else
    for i in "${testCommands[@]}"; do
      NAME=$(cat < /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
      CURR_TEST_NAME=${i%%.py*}
      CURR_TEST_NAME=${CURR_TEST_NAME#./*}
      #CURR_TEST_NUM="${name_to_num[$CURR_TEST_NAME]}"
      test
    done
  fi
}

function html_generator() {
    LAST_COMMIT=$(git log --pretty=oneline | tail -n 1)
    header="<html>
		<head>
		<title>Regression Test Results $NOW</title>
		<style>
		.success {
			background-color:green;
		}
		.failure {
			background-color:red;
		}
		table {
			border: 1px solid gray;
		}
		td {
			margin: 0;
			padding: 2px;
			font-family: 'Courier New',courier,sans-serif;
		}
		h1, h2, h3, h4 {
			font-family: 'Century Gothic',Arial,sans,sans-serif;
		}
		.scriptdetails {
			font-size: 10px;
		}
		</style>
		<script src=\"sortabletable.js\"></script>
		</head>
		<body>
		<h1>Regression Results</h1>
		<h4>$NOW</h4>
		<h4>$LAST_COMMIT</h4>
		<table border ='1' id='myTable2'>
		<tr>
        <th onclick=\"sortTable(0)\">Command Name</th>
        <th onclick=\"sortTable(1)\">Command</th>
        <th onclick=\"sortTable(2)\">Status</th>
        <th onclick=\"sortTable(3)\">STDOUT</th>
        <th onclick=\"sortTable(4)\">STDERR</th>
    </tr>"
    tail="</body>
		</html>"

    fname="${HOMEPATH}/html-reports/regression_file-${NOW}.html"
    echo "$header"  >> "$fname"
    echo "${results[@]}"  >> "$fname"
    echo "</table>" >> "$fname"
    echo "$tail" >> "$fname"
    if [ -f "${HOMEPATH}/html-reports/latest.html" ]; then
        rm -f "${HOMEPATH}/html-reports/latest.html"
    fi
    ln -s "${fname}" "${HOMEPATH}/html-reports/latest.html"
    HOSTNAME=$(ip -4 addr show enp3s0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    content="View the latest regression report at ${HOSTNAME}/html-reports/latest.html"
    echo "${content}"
    #mail -s "Regression Results" scripters@candelatech.com <<<$content
}

results=()
NOW=$(date +"%Y-%m-%d-%H-%M")
NOW="${NOW/:/-}"
TEST_DIR="${REPORT_DATA}/${NOW}"
URL2="${HOMEPATH}/report-data/${NOW}"
mkdir "${TEST_DIR}"
echo "Recording data to $TEST_DIR"

run_test
html_generator
