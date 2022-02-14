#!/bin/bash
##########################
# Help
##########################
Help()
{
  echo "This bash script aims to automate the test process of all Candela Technologies test_* scripts in the lanforge-scripts directory to detect software regressions. The script can be run 2 ways and may include (via user input) the \"start_num\" and \"stop_num\" variables to select which tests should be run."
  echo "OPTION ONE: ./regression_test.sh : this command runs all the scripts in the array \"testCommands\""
  echo "OPTION TWO: ./regression_test.sh 4 5 :  this command runs py-script commands (in testCommands array) that include the py-script options beginning with 4 and 5 (inclusive) in case function ret_case_num."
  echo "Optional Variables:"
  echo "s is the SSID of the 5g network you are testing against.  This is treated as the main ssid for tests that take one SSID"
  echo "u is the SSID of the 2g network you are testing against"
  echo "PASSWD is the password of said network"
  echo "SECURITY is the security protocol of the network"
  echo "MGR is the IP address of the device which has LANforge installed, if different from the system you are using."
  echo "A is used to call to test a specific command based on"
  echo "b is 2g BSSID"
  echo "B is 5g BSSID"
  echo "F is used to pass in an RC file which can store the credentials for running regression multiple times on your system"
  echo "H is used to test the help feature of each script, to make sure it renders properly."
  echo "L is used to give the IP address of the LANforge device which is under test"
  echo "D is DUT5 name."
  echo "2 is DUT2 name."
  echo "r is 5Ghz radio, default is 1.1.wiphy1"
  echo "M is 2.4Ghz radio, default is 1.1.wiphy0"
  echo "Example command: ./regression_test.sh -s SSID -p PASSWD -w SECURITY -m MGR"
  echo "Example command: ./regression_test.sh -s j-wpa2-153 -p j-wpa2-153 -w wpa2 -r 1.1.wiphy0 \\\\"
  echo "   -M 1.1.wiphy1 -B 04:F0:21:CB:01:8B -V heather_ssid_2022 -m heather -R /tmp/ 1"
  echo "If using the help flag, put the H flag at the end of the command after other flags."
}

HOMEPATH=$(realpath ~)
REPORT_DIR="${HOMEPATH}/html-reports"
TESTBED=UNKNOWN
NOW=$(date +"%Y-%m-%d-%H-%M")
NOW="${NOW/:/-}"
DUT2_NAME=regression_dut
DUT5_NAME=regression_dut
RADIO_USED="1.1.wiphy1"
RADIO5=$RADIO_USED
RADIO2="1.1.wiphy0"
SSID_USED=
SSID_USED2=
BSSID=
BSSID2=

# Load config file
if [ -f ./regression_test.rc ]; then
    source ./regression_test.rc # this version is a better unix name
elif [ -f ./regression_test.txt ]; then
    source ./regression_test.txt # this less unixy name was discussed earlier
fi

# cmd line arguments take precedence over config file, so they are processed here.
while getopts ":h:s:S:p:w:m:r:R:F:b:B:u:U:D:2:H:M:C:e:u:V:E:T:" option; do
  case "${option}" in
    h) # display Help
      Help
      exit 1
      ;;
    s)
      SSID_USED=${OPTARG}
      ;;
    u)
      SSID_USED2=${OPTARG}
      ;;
    S)
      SHORT="yes"
      ;;
    T)
      TESTBED=${OPTARG}
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
    r)
      RADIO_USED=${OPTARG}
      RADIO5=${OPTARG}
      ;;
    M)
      RADIO2=${OPTARG}
      ;;
    R)
      REPORT_DIR=${OPTARG}
      ;;
    F)
      REGRESSION_COMMANDS=${OPTARG}
      ;;
    B)
      BSSID=${OPTARG}
      ;;
    b)
      BSSID2=${OPTARG}
      ;;
    u)
      # like eth0
      UPSTREAM_BARE=${OPTARG}
      ;;
    U)
      # like 1.1.eth0
      UPSTREAM=${OPTARG}
      ;;
    D)
      DUT5_NAME=${OPTARG}
      ;;
    2)
      DUT2_NAME=${OPTARG}
      ;;
    H)
      ./lf_help_check.bash
      ;;
    C)
      RESOURCE=${OPTARG}
      ;;
    e)
      END_TEXT=${OPTARG}
      ;;
    V)
      VAP_SSID=${OPTARG}
      ;;
    E)
      EXIT_ON_ERROR=${OPTARG}
      ;;
    *)

      ;;
  esac
done

if [ "_$BSSID2" != "_" ]
then
    DUT2="$DUT2_NAME $SSID_USED2 $BSSID2 (1)"
fi

if [ "_$BSSID" != "_" ]
then
    DUT5="$DUT5_NAME $SSID_USED5 $BSSID (1)"
fi

if [[ ${#MGR} -eq 0 ]]; then # Allow the user to change the radio they test against
  MGR="localhost"
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version)')

which jq > /dev/null 2>&1 || (echo "jq not found, please install" && exit 1)
if [[ $? != "0" ]]
    then
    exit 1
fi

BuildVersion=$(wget $MGR:8080 -q -O - | jq '.VersionInfo.BuildVersion')
BuildDate=$(wget $MGR:8080 -q -O - | jq '.VersionInfo.BuildDate')
OS_Version=$(grep 'VERSION=' /etc/os-release)
HOSTNAME=$(cat /etc/hostname)
IP_ADDRESS=$(ip a sho eth0 | grep 'inet ' | cut -d "/" -f1 | cut -d "t" -f2)
PYTHON_ENVIRONMENT=$(which python3)

#SCENARIO_CHECK="$(python3 -c "import requests; print(requests.get('http://${MGR}:8080/events/').status_code)")"
#if [[ ${SCENARIO_CHECK} -eq 200 ]]; then
#  :
#else
#  echo "${SCENARIO_CHECK}"
#  echo "Your LANforge Manager is out of date. Regression test requires LANforge version 5.4.4 or higher in order to run"
#  echo "Please upgrade your LANforge using instructions found at https://www.candelatech.com/downloads.php#releases"
#  exit 1
#fi
git pull --rebase

python3 -m pip install --upgrade pip
if [ -d "/home/lanforge/lanforge_env" ]; then
  source /home/lanforge/lanforge_env/bin/activate
  pip3 install --upgrade lanforge-scripts
elif  [ -d "/home/lanforge/anaconda3" ]; then
  pip3 install --upgrade lanforge-scripts
else
  pip3 install --user lanforge_scripts --upgrade
fi

if [[ ${#SSID_USED} -eq 0 ]]; then #Network credentials
  SSID_USED="jedway-wpa2-x2048-5-3"
  PASSWD_USED="jedway-wpa2-x2048-5-3"
  SECURITY="wpa2"
fi

if [[ ${#VAP_SSID} -eq 0 ]]; then
  VAP_SSID=SSID_USED
fi

if [[ ${#UPSTREAM_BARE} -eq 0 ]]; then
  UPSTREAM_BARE="eth1"
fi

if [[ ${#UPSTREAM} -eq 0 ]]; then
  UPSTREAM=$UPSTREAM_BARE
fi

if [[ ${#BSSID} -eq 0 ]]; then
  BSSID="04:f0:21:2c:41:84"
fi

if [[ $RESOURCE -eq 0 ]]; then
  RESOURCE="1.1"
fi

FILE="/tmp/gui-update.lock"
if test -f "$FILE"; then
  echo "Finish updating your GUI"
  exit 0
fi

NUM_STA=${NUM_STA:-4}
TEST_HTTP_IP=${TEST_HTTP_IP:-10.40.0.1}
COL_NAMES="name,tx_bytes,rx_bytes,dropped"

#CURR_TEST_NUM=0
CURR_TEST_NAME="BLANK"

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
  ./test_l3_longevity.py --test_duration 15s --upstream_port $UPSTREAM --radio "radio==wiphy0 stations==4 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY" --radio "radio==wiphy1 stations==4 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY" --lfmgr "$MGR"
}
function testgroup_list_groups() {
  ./scenario.py --load test_l3_scenario_throughput --mgr "${MGR}"
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003 --list_groups --debug --mgr "$MGR"
}
function testgroup_list_connections() {
  ./scenario.py --load test_l3_scenario_throughput --mgr "${MGR}"
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003 --show_group --debug --mgr "$MGR"
}
function testgroup_delete_group() {
  ./scenario.py --load test_l3_scenario_throughput --mgr "${MGR}"
  ./testgroup.py --group_name group1 --add_group --add_cx cx0000,cx0001,cx0002 --remove_cx cx0003
  ./testgroup.py --group_name group1--del_group --debug --mgr "$MGR"
}

function create_station_and_dataplane() {
      set -x
      ./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR --noclean
      ./lf_dataplane_test.py --mgr $MGR --lf_user lanforge --lf_password lanforge \
          --instance_name dataplane-instance --config_name test_con --upstream $UPSTREAM \
          --dut regression_dut --duration 15s --station $RESOURCE.sta0001 \
          --download_speed 85% --upload_speed 0 \
          --test_rig $TESTBED --pull_report \
          --local_lf_report_dir ~/html-reports/dataplane_${NOW}
      set +x
}

function create_station_and_sensitivity {
  set -x
  # TODO:  This uses wrong dut name for generic testbed, probably it fails in other ways too.
  # I guess we can at least use it as a negative test hoping to see failure.
  # until we can make it work better.
  ./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR
  ./lf_rx_sensitivity_test.py --mgr $MGR --port 8080 --lf_user lanforge --lf_password lanforge \
                      --instance_name rx-sensitivity-instance --config_name test_con --upstream $UPSTREAM \
                      --dut linksys-8450 --duration 15s --station $RESOURCE.sta0001 \
                      --download_speed 85% --upload_speed 0 \
                      --raw_line 'txo_preamble\: VHT' \
                      --raw_line 'txo_mcs\: 4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT' \
                      --raw_line 'spatial_streams\: 3' \
                      --raw_line 'bandw_options\: 80' \
                      --raw_line 'txo_sgi\: ON' \
                      --raw_line 'txo_retries\: No Retry' \
                      --raw_line 'txo_txpower\: 17' \
                      --test_rig Testbed-01 --pull_report \
                      --report_dir ~/html-reports/rx_sens_"$NOW"
                      #--influx_host 192.168.100.153 --influx_port 8086 --influx_org Candela \
                      #--influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
                      #--influx_bucket ben \
                      #--influx_tag testbed Ferndale-01
  set +x
}
if [[ ${#SHORT} -gt 0 ]]; then
  testCommands=(
      "./create_bond.py --network_dev_list $RESOURCE.eth0,$UPSTREAM --debug --mgr $MGR"
      "./create_l3.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR --endp_a wiphy0 --endp_b wiphy1"
      "./create_l3_stations.py --mgr $MGR --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug"
      "./create_l4.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_macvlan.py --macvlan_parent $UPSTREAM --debug --mgr $MGR"
      "./create_qvlan.py --first_qvlan_ip 192.168.1.50 --mgr $MGR --qvlan_parent $UPSTREAM"
      "./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_vap.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format excel --layer3_cols $COL_NAMES --debug --mgr $MGR  --traffic_type lf_udp"


  )
elif [[ ${#REGRESSION_COMMANDS} -gt 0 ]]; then
  testCommands=(cat "$REGRESSION_COMMANDS")
else
  testCommands=(
      "./create_bond.py --network_dev_list $RESOURCE.eth2,$UPSTREAM --bond_name $RESOURCE.bond5 --debug --mgr $MGR"
      "./create_bridge.py --target_device $RESOURCE.eth2,$UPSTREAM --bridge_name $RESOURCE.br5 --debug --mgr $MGR"
      "./create_chamberview_dut.py --lfmgr $MGR --dut_name regression_dut --ssid \"ssid_idx=0 ssid='$SSID_USED' security='$SECURITY' password='$PASSWD_USED' bssid=$BSSID\" && ./create_chamberview.py -m $MGR -cs 'regression_test' --delete_scenario --line \"Resource=1.$RESOURCE Profile=STA-AC Amount=1 Uses-1=$RADIO_USED Freq=-1 DUT=regression_dut DUT_Radio=$RADIO_USED Traffic=http\" --line \"Resource=1.$RESOURCE Profile=upstream Amount=1 Uses-1=$UPSTREAM_BARE Uses-2=AUTO Freq=-1 DUT=regression_dut DUT_Radio=LAN Traffic=http\""
      "./create_l3.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR --endp_a wiphy0 --endp_b wiphy1"
      "./create_l3_stations.py --mgr $MGR --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug"
      "./create_l4.py --radio $RADIO_USED --ssid $SSID_USED --password $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_macvlan.py --macvlan_parent $UPSTREAM --debug --mgr $MGR"
      "./create_qvlan.py --first_qvlan_ip 192.168.1.50 --mgr $MGR --qvlan_parent $UPSTREAM"
      "./create_station.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./create_vap.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      #"./create_vr.py --mgr $MGR --vr_name 2.vr0 --ports 2.br0,2.vap2 --services 1.br0=dhcp,nat --services 1.vr0=radvd --debug"
      #./csv_convert
      #./csv_processor
      #./csv_to_grafana
      #./csv_to_influx
      #"./cv_manager.py --mgr $MGR --scenario FACTORY_DFLT"
      #"./cv_to_grafana --mgr $MGR "
      #"./docstrings.py --mgr $MGR"
      #"./scripts_deprecated/event_break_flood.py --mgr $MGR"
      "./example_security_connection.py --num_stations $NUM_STA --ssid $SSID_USED \
      --passwd $PASSWD_USED --radio $RADIO_USED --security wpa2 --debug --mgr $MGR"
      #./ftp_html.py
      #./grafana_profile
      "./lf_ap_auto_test.py \
        --mgr $MGR --port 8080 --lf_user lanforge --lf_password lanforge \
        --instance_name ap-auto-instance --config_name test_con --upstream $UPSTREAM \
        --dut5_0 '$DUT5' \
        --dut2_0 '$DUT2' \
        --max_stations_2 64 \
        --max_stations_5 64 \
        --max_stations_dual 64 \
        --radio5 $RADIO5 \
        --radio2 $RADIO2 \
        --set 'Basic Client Connectivity' 1 \
        --set 'Multi Band Performance' 0 \
        --set 'Skip 2.4Ghz Tests' 1 \
        --set 'Skip 5Ghz Tests' 1 \
        --set 'Skip Dual-Band Tests' 1 \
        --set 'Throughput vs Pkt Size' 0 \
        --set 'Capacity' 0 \
        --set 'Stability' 0 \
        --set 'Band-Steering' 0 \
        --set 'Multi-Station Throughput vs Pkt Size' 0 \
        --set 'Long-Term' 0 \
        --pull_report \
        --local_lf_report_dir ~/html-reports/ap_auto_$NOW"
      #"./lf_atten_mod_test.py --host $MGR --debug"
      #./lf_csv
      #./lf_dataplane_config
      create_station_and_dataplane
      #"./lf_dut_sta_vap_test.py --manager $MGR --radio $RADIO_USED \
      #    --num_sta 1 --sta_id 1 --ssid $SSID_USED --security $SECURITY --upstream $UPSTREAM \
      #    --protocol lf_udp --min_mbps 1000 --max_mbps 10000 --duration 1"
      "./lf_graph.py --mgr $MGR"
      "./lf_mesh_test.py --mgr $MGR --upstream $UPSTREAM --raw_line 'selected_dut2 RootAP wactest $BSSID'"
      "./lf_multipsk.py --mgr $MGR --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --radio $RADIO_USED --debug"
      "./lf_report.py"
      "./lf_report_test.py"
      # "./lf_rvr_test.py"
      create_station_and_sensitivity
      "./lf_sniff_radio.py \
                               --mgr $MGR \
                               --mgr_port 8080 \
                               --outfile /home/lanforge/test_sniff.pcap \
                               --duration 20 \
                               --channel 52 \
                               --radio_mode AUTO"
      "./lf_snp_test.py --help"
      "./lf_tr398_test.py --mgr $MGR --upstream $UPSTREAM"
      #./lf_webpage
      "./lf_wifi_capacity_test.py --mgr $MGR --port 8080 --lf_user lanforge --lf_password lanforge \
             --instance_name this_inst --config_name test_con --upstream $UPSTREAM --batch_size 1,5,25,50,100 --loop_iter 1 \
             --protocol UDP-IPv4 --duration 6000 --pull_report --ssid $SSID_USED --paswd $PASSWD_USED --security $SECURITY\
             --test_rig Testbed-01 --create_stations --stations $RESOURCE.sta0000,$RESOURCE.sta0001 --local_lf_report_dir ~/report-data/wifi_capacity_$NOW"
      "./measure_station_time_up.py --radio $RADIO_USED --num_stations 3 --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED \
      --debug --report_file measure_station_time_up.pkl --radio2 wiphy1 --mgr $MGR"
      "./create_station.py --mgr $MGR --radio $RADIO_USED --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED && ./modify_station.py \
                   --mgr $MGR \
                   --radio $RADIO_USED \
                   --station $RESOURCE.sta0000 \
                   --security $SECURITY \
                   --ssid $SSID_USED \
                   --passwd $PASSWD_USED \
                   --enable_flag osen_enable \
                   --disable_flag ht160_enable \
                   --debug"
      #recordinflux.py
      #"./run_cv_scenario.py --lfmgr $MGR --lanforge_db 'handsets' --cv_test 'WiFi Capacity' --test_profile 'test-20' --cv_scenario ct-us-001"
      #"./rvr_scenario.py --lfmgr $MGR --lanforge_db 'handsets' --cv_test Dataplane --test_profile http --cv_scenario ct-us-001"
      #./sta_connect_bssid_mac.py
      "./sta_connect_example.py --mgr $MGR --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --radio $RADIO_USED --upstream_port $UPSTREAM --test_duration 15s --debug"
      "./sta_connect.py --mgr $MGR --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --radio $RADIO_USED --upstream_port $UPSTREAM --test_duration 15s --dut_bssid $BSSID --debug"
      "./sta_connect2.py --dest $MGR --dut_ssid $SSID_USED --dut_passwd $PASSWD_USED --dut_security $SECURITY --radio $RADIO_USED --upstream_port $UPSTREAM"
      "./sta_scan_test.py --mgr $MGR --ssid $SSID_USED --security $SECURITY --passwd $PASSWD_USED --radio $RADIO_USED --debug"
      #station_layer3.py
      #stations_connected.py
      #"./test_1k_clients_jedtest.py
      # --mgr $MGR
      # --mgr_port 8080
      # --sta_per_radio 300
      # --test_duration 3m
      # --a_min 1000
      # --b_min 1000
      # --a_max 0
      # --b_max 0
      # --debug"
      #test_client_admission.py
      "./test_fileio.py --macvlan_parent $UPSTREAM --num_ports 3 --use_macvlans --first_mvlan_ip 10.40.92.13 --netmask 255.255.255.0 --gateway 192.168.92.1 --test_duration 30s --mgr $MGR --debug" # Better tested on Kelly, where VRF is turned off
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfping --dest $TEST_HTTP_IP --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type speedtest --speedtest_min_up 20 --speedtest_min_dl 20 --speedtest_max_ping 150 --security $SECURITY --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type iperf3 --debug --mgr $MGR"
      "./test_generic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED  --security $SECURITY --num_stations $NUM_STA --type lfcurl --dest $TEST_HTTP_IP --file_output ${HOMEPATH}/Documents/lfcurl_output.txt --debug --mgr $MGR"
      "./testgroup.py --group_name group1 --add_group --list_groups --debug --mgr $MGR"
      "./testgroup2.py --num_stations 4 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --radio $RADIO_USED --group_name group0 --add_group --mgr $MGR --debug"
      "./test_ip_connection.py --radio $RADIO_USED --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format excel --layer3_cols $COL_NAMES --debug --mgr $MGR  --traffic_type lf_udp"
      "./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --output_format csv --layer3_cols $COL_NAMES --debug --mgr $MGR  --traffic_type lf_udp"
      #"./test_ip_connection.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR --ipv6"
      #"./test_ip_variable_time.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --test_duration 15s --debug --mgr $MGR --ipv6 --traffic_type lf_udp"
      "./test_ipv4_ps.py --radio $RADIO_USED --ssid $VAP_SSID --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR --radio2 $RADIO2"
      #"./test_ipv4_ttls.py --radio $RADIO_USED --ssid $VAP_SSID --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      "./test_l3.py --mgr $MGR --radio 'radio==$RADIO_USED stations==4 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY'"
      "./test_l3_longevity.py --mgr $MGR --endp_type 'lf_tcp' --upstream_port $UPSTREAM --radio \
      'radio==$RADIO_USED stations==10 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY' --radio \
      'radio==$RADIO2 stations==1 ssid==$SSID_USED ssid_pw==$PASSWD_USED security==$SECURITY' --test_duration 5s --rates_are_totals \
      --side_a_min_bps=20000 --side_b_min_bps=300000000  -o longevity.csv --debug"
      "./test_l3_powersave_traffic.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR"
      #"./test_l3_scenario_throughput.py -t 15s -sc test_l3_scenario_throughput -m $MGR"
      "./test_l3_unicast_traffic_gen.py --mgr $MGR --radio_list $RADIO_USED 4 $SSID_USED $PASSWD_USED --debug"
      #./test_l3_WAN_LAN
      "./test_l4.py --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --mgr $MGR --test_duration 15s"
      "./test_status_msg.py --debug --mgr $MGR" #this is all which is needed to run
      #"./test_wanlink.py --name my_wanlink4 --latency_A 20 --latency_B 69 --rate 1000 --jitter_A 53 --jitter_B 73 --jitter_freq 6 --drop_A 12 --drop_B 11 --debug --mgr $MGR"
      #./test_wpa_passphrases
      #./tip_station_powersave
      #./video_rates
      "./wlan_capacity_calculator.py -sta 11abg -t Voice -p 48 -m 106 -e WEP -q Yes -b 1 2 5.5 11 -pre Long -s N/A -co G.711 -r Yes -c Yes"
      "./wlan_capacity_calculator.py -sta 11n -t Voice -d 17 -ch 40 -gu 800 -high 9 -e WEP -q Yes -ip 5 -mc 42 -b 6 9 12 24 -m 1538 -co G.729 -pl Greenfield -cw 15 -r Yes -c Yes"
      "./wlan_capacity_calculator.py -sta 11ac -t Voice -d 9 -spa 3 -ch 20 -gu 800 -high 1 -e TKIP -q Yes -ip 3 -mc 0 -b 6 12 24 54 -m 1518 -co Greenfield -cw 15 -rc Yes"
      #"./ws_generic_monitor_test.py --mgr $MGR"
      "python3 -c 'import lanforge_scripts'"
  )
fi

function blank_db() {
    echo "Loading blank scenario..." >>"${HOMEPATH}/regression_file.txt"
    ./scenario.py --mgr "${MGR}" --load BLANK >>"${HOMEPATH}/regression_file.txt"
    #check_blank.py
}

function echo_print() {
    echo "Beginning $CURR_TEST_NAME test..." >>"${HOMEPATH}/regression_file.txt"
}

function test() {
  FILENAME="${TEST_DIR}/${NAME}"
  START_JC=$(date '+%Y-%m-%d %H:%M:%S') # Start of journalctl logging.

  if [[ ${#PORTS} -gt 0 ]]; then
    ./scenario.py --load BLANK --mgr ${MGR} --check_phantom "${PORTS}" --debug > "${FILENAME}.txt"
  else
    ./scenario.py --load BLANK --mgr ${MGR} --debug > "${FILENAME}.txt"
  fi

  echo ""
  echo "Test $CURR_TEST_NAME"

  echo_print
  echo "$testcommand"
  start=$(date +%s)
  # this command saves stdout and stderr to the stdout file
  FILENAME="${TEST_DIR}/${NAME}"
  eval "$($testcommand >> "${FILENAME}.txt" 2>&1)"
  TESTRV=$?
  #echo "TESTRV: $TESTRV"

  chmod 664 "${FILENAME}.txt"
  # Check to see if the error is due to LANforge
  ERROR_DATA=$(cat "${FILENAME}.txt")
  if [[ $ERROR_DATA =~ "LANforge Error Messages" ]]; then
    LANforgeError="Lanforge Error"
    echo "LANforge Error"
  else
    LANforgeError=""
  fi
  end=$(date +%s)
  execution="$((end-start))"
  TEXT=$(cat "${FILENAME}".txt)

  if [[ $TESTRV != "0" ]]; then
    echo "Test failed with non-zero return code"
    TEXTCLASS="failure"
    TDTEXT="Failure"
    LOGGING="<a href=\"${URL2}/logs/${NAME}\" target=\"_blank\">Logging directory</a>"
  elif [[ $TEXT =~ "tests failed" ]]; then
    TEXTCLASS="partial_failure"
    TDTEXT="Partial Failure"
    echo "Partial Failure"
    LOGGING="<a href=\"${URL2}/logs/${NAME}\" target=\"_blank\">Logging directory</a>"
  elif [[ $TEXT =~ "FAILED" ]]; then
    TEXTCLASS="partial_failure"
    TDTEXT="ERROR"
    echo "ERROR"
    LOGGING="<a href=\"${URL2}/logs/${NAME}\" target=\"_blank\">Logging directory</a>"
  else
    TEXTCLASS="success"
    TDTEXT="Success"
    echo "No errors detected"
    LOGGING=""
  fi

  if [[ ${#LOGGING} -gt 0 ]]; then
    mkdir "${LOG_DIR}/${NAME}"
    if [[ $MGR == "localhost" ]]; then
      cp "${HOMEPATH}"/lanforge_log* "${LOG_DIR}/${NAME}"
      cp "${HOMEPATH}"/run_client* "${LOG_DIR}/${NAME}"
      cp "${HOMEPATH}"/run_mgr* "${LOG_DIR}/${NAME}"
      journalctl --since "$START_JC" > "${LOG_DIR}/${NAME}/journalctl_log.txt"
    else
      # TODO:  Need to parameterize the password some day.
      sshpass -p "lanforge" scp lanforge@"${MGR}":~/lanforge_log* "${LOG_DIR}/${NAME}"
      sshpass -p "lanforge" scp lanforge@"${MGR}":~/run_client* "${LOG_DIR}/${NAME}"
      sshpass -p "lanforge" scp lanforge@"${MGR}":~/run_mgr* "${LOG_DIR}/${NAME}"
      # TODO:  Add ability to get logs from secondary resource(s) as well.
      sshpass -p "lanforge" scp root@"${MGR}":/home/lanforge/wifi/*supplicant*log*.txt "${LOG_DIR}/${NAME}"
      sshpass -p "lanforge" ssh root@"${MGR}" "journalctl --since '$START_JC'" > "${LOG_DIR}/${NAME}/journalctl_log.txt"
    fi
    #for file in "${LOG_DIR}/${NAME}"/lanforge_log*; do
    #  ./log_filter.py --input_file "$file" --timestamp "$START_TIME" --output_file "$file"
    #done
  fi

  results+=("<tr><td>${CURR_TEST_NAME}</td>
                       <td class='scriptdetails'>${testcommand}</td>
                       <td class='${TEXTCLASS}'>$TDTEXT</td>
                       <td>${execution}</td>
                       <td><a href=\"${URL2}/${NAME}.txt\" target=\"_blank\">STDOUT</a></td>
                       <td>${LANforgeError}</td>
                       <td>${LOGGING}</td>
                       </tr>")
  # Propagate test script exit code
  return $TESTRV
}

function start_tests()  {
  for testcommand in "${testCommands[@]}"; do
    NAME=$(cat < /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    CURR_TEST_NAME=${testcommand%%.py*}
    CURR_TEST_NAME=${CURR_TEST_NAME#./*}
    CHECK_PORTS=()
    if [[ ${testcommand} =~ ${RADIO_USED} ]]; then
      CHECK_PORTS+=("$RADIO_USED")
    fi
    if [[ ${testcommand} =~ ${RADIO2} ]]; then
      CHECK_PORTS+=("$RADIO2")
    fi
    if [[ ${testcommand} =~ ${UPSTREAM} ]]; then
      CHECK_PORTS+=("$UPSTREAM")
    fi
    PORTS=$( IFS=$','; echo "${CHECK_PORTS[*]}" )
    if [[ ${#EXIT_ON_ERROR} -gt 0 ]]; then
      test || return $?
    else
      test
    fi
  done
}

function html_generator() {
    LAST_COMMIT=$(git log --pretty=oneline | head -n 1)
    header="<!DOCTYPE html>
<html>
<head>
<meta http-equiv='Cache-Control' content='no-store' />
<title>${HOSTNAME} Regression Test Results $NOW</title>
<link rel='stylesheet' href='report.css' />
<style>
body {
    font-family: 'Century Gothic';
}
.success {
    background-color:green;
}
.failure {
    background-color:red;
}
.partial_failure {
  background-color:yellow;
}
table {
    border: 0 none;
    border-collapse: collapse;
}
td {
    margin: 0;
    padding: 2px;
    font-family: 'Century Gothic',Arial,Verdana,Tahoma,'Trebuchet MS',Impact,sans-serif;
    border: 1px solid gray;
}
h1, h2, h3, h4 {
    font-family: 'Century Gothic',Arial,Verdana,Tahoma,'Trebuchet MS',Impact,sans-serif;
}
.scriptdetails {
    font-size: 10px;
    font-family:'Lucida Typewriter','Andale Mono','Courier New',Courier,FreeMono,monospace;
}
td.testname {
    font-size:14px;
    font-weight: bold;
}
</style>
<script src=\"sortabletable.js\"></script>
</head>
<body>
    <h1>Regression Results</h1>
    <h4 id=\"timestamp\">$NOW</h4>
    <h4 id=\"Git Commit\">$LAST_COMMIT</h4>
    <h4>Test results</h4>
    <table border ='1' id='myTable2' id='SuiteResults'>
    <thead>
        <tr>
            <th onclick=\"sortTable('myTable2', 0)\">Command Name</th>
            <th onclick=\"sortTable('myTable2', 1)\">Command</th>
            <th onclick=\"sortTable('myTable2', 2)\">Status</th>
            <th onclick=\"sortTable('myTable2', 3)\">Execution time</th>
            <th onclick=\"sortTable('myTable2', 4)\">STDOUT</th>
            <th onclick=\"sortTable('myTable2', 6)\">LANforge Error</th>
            <th onclick=\"sortTable('myTable2', 7\">LANforge logging</th>
        </tr>
    </thead>
    <tbody>"
    tail="</body></html>"

    fname="${HOMEPATH}/html-reports/regression_file-${NOW}.html"
    echo "$header" >> "$fname"
    echo "${results[@]}"  >> "$fname"
    echo "</tbody>
    </table>
    <br />
    <h3>System information</h3>
    <table id=\"SystemInformation\" border ='1'>
    <thead>
      <tr>
        <th>Python version</th>
        <th>LANforge version</th>
        <th>LANforge build date</th>
        <th>OS Version</th>
        <th>Hostname</th>
        <th>IP Address</th>
        <th>Python Environment</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td id='PythonVersion'>${PYTHON_VERSION}</td>
        <td id='LANforgeVersion'>${BuildVersion}</td>
        <td id='LANforgeBuildDate'>${BuildDate}</td>
        <td id='OS_Version'>${OS_Version}</td>
        <td id='Hostname'>${HOSTNAME}</td>
        <td id='ip_address'>${IP_ADDRESS}</td>
        <td id='python_environment'>${PYTHON_ENVIRONMENT}</td>
      </tr>
    </tbody>
    </table>
    <script> sortTable('myTable2', 2); </script>
" >> "$fname"
    if [[ ${#END_TEXT} -gt 0 ]]; then
      end_text=$(cat "$END_TEXT")
      "<p>${end_text}</p>" >> "$fname"
    fi
    echo "$tail" >> "$fname"
    if [ -f "${HOMEPATH}/html-reports/latest.html" ]; then
        rm -f "${HOMEPATH}/html-reports/latest.html"
    fi
    ln -s "${fname}" "${HOMEPATH}/html-reports/latest.html"
    echo "Saving HTML file to disk"
    #HOSTNAME=$(ip -4 addr show enp3s0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    #content="View the latest regression report at /html-reports/latest.html"
    #echo "${content}"
    #mail -s "Regression Results" scripters@candelatech.com <<<$content
}

results=()
NOW=$(date +"%Y-%m-%d-%H-%M")
NOW="${NOW/:/-}"
TEST_DIR="${REPORT_DATA}/${NOW}"
URL2="/report-data/${NOW}"
LOG_DIR="${TEST_DIR}/logs"
mkdir "${TEST_DIR}"
mkdir "${LOG_DIR}"
echo "Recording data to $TEST_DIR"

start_tests
html_generator
