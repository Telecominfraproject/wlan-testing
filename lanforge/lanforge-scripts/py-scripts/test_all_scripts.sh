#!/bin/bash
#This bash script aims to automate the test process of all Candela Technologies's test_* scripts in the lanforge-scripts directory. The script can be run 2 ways and may include (via user input) the "start_num" and "stop_num" variables to select which tests should be run.
# OPTION ONE: ./test_all_scripts.sh : this command runs all the scripts in the array "testCommands"
# OPTION TWO: ./test_all_scripts.sh 4 5 :  this command runs py-script commands (in testCommands array) that include the py-script options beginning with 4 and 5 (inclusive) in case function ret_case_num.
#Variables
NUM_STA=4
SSID_USED="jedway-wpa2-x2048-5-3"
PASSWD_USED="jedway-wpa2-x2048-5-3"
RADIO_USED="wiphy1"
SECURITY="wpa2"

START_NUM=0
CURR_TEST_NUM=0
CURR_TEST_NAME="BLANK"
STOP_NUM=9

#Test array
testCommands=("./example_security_connection.py --num_stations $NUM_STA --ssid jedway-r8000-36 --passwd jedway-r8000-36 --radio $RADIO_USED --security wpa "
    "./example_security_connection.py --num_stations $NUM_STA --ssid $SSID_USED --passwd $SSID_USED --radio $RADIO_USED --security wpa2"
    "./example_security_connection.py --num_stations $NUM_STA --ssid jedway-wep-48 --passwd jedway-wep-48 --radio $RADIO_USED --security wep"
    "./example_security_connection.py --num_stations $NUM_STA --ssid jedway-wpa3-1 --passwd jedway-wpa3-1 --radio $RADIO_USED --security wpa3"
    "./test_ipv4_connection.py --radio wiphy2 --num_stations $NUM_STA --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY --debug --upstream_port eth1"
    "./test_generic.py --mgr localhost --mgr_port 4122 --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --num_stations $NUM_STA --type lfping --dest 10.40.0.1 --security $SECURITY"
    "./test_generic.py --mgr localhost --mgr_port 4122 --radio $RADIO_USED --ssid $SSID_USED --passwd $PASSWD_USED --num_stations $NUM_STA --type speedtest --speedtest_min_up 20 --speedtest_min_dl 20 --speedtest_max_ping 150 --security $SECURITY"
    "./test_ipv4_l4_urls_per_ten.py --upstream_port eth1 --radio $RADIO_USED --num_stations $NUM_STA --security $SECURITY --ssid $SSID_USED --passwd $PASSWD_USED  --num_tests 1 --requests_per_ten 600 --target_per_ten 600"
    "./test_ipv4_l4_wifi.py --upstream_port eth1 --radio wiphy0 --num_stations $NUM_STA --security $SECURITY --ssid jedway-wpa2-x2048-4-4 --passwd jedway-wpa2-x2048-4-4  --test_duration 3m"
    "./test_ipv4_l4.py --radio wiphy3 --num_stations 4 --security wpa2 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1  --url \"dl http://10.40.0.1 /dev/null\"  --test_duration 2m --debug"
    "./test_ipv4_variable_time.py --radio wiphy1 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --mode 4 --ap 00:0e:8e:ff:86:e6 --test_duration 30s --output_format excel"
    "./test_ipv4_variable_time.py --radio wiphy1 --ssid jedway-wpa2-x2048-4-1 --passwd jedway-wpa2-x2048-4-1 --security wpa2 --mode 4 --ap 00:0e:8e:ff:86:e6 --test_duration 30s --output_format csv"
    "./create_bridge.py --radio wiphy1 --upstream_port eth1"
    "./create_l3.py --radio wiphy1 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY"
    "./create_l4.py --radio wiphy1 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY"
    "./create_macvlan.py --radio wiphy1"
    "./create_station.py --radio wiphy1 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY"
    "./create_vap.py --radio wiphy1 --ssid $SSID_USED --passwd $PASSWD_USED --security $SECURITY"
)
declare -A name_to_num
name_to_num=(
    ["example_security_connection"]=1
    ["test_ipv4_connection"]=2
    ["test_generic"]=3
    ["test_ipv4_l4_urls_per_ten"]=4
    ["test_ipv4_l4_wifi"]=5
    ["test_ipv4_l4"]=6
    ["test_ipv4_variable_time"]=7
    ["create_bridge"]=8
    ["create_l3"]=9
    ["create_l4"]=10
    ["create_macvlan"]=10
    ["create_station"]=11
    ["create_vap"]=12
)

function blank_db() {
    echo "Loading blank scenario..." >>~/test_all_output_file.txt
    ./scenario.py --load BLANK >>~/test_all_output_file.txt
    #check_blank.py
}
function echo_print() {
    echo "Beginning $CURR_TEST_NAME test..." >>~/test_all_output_file.txt
}
function run_test() {
    for i in "${testCommands[@]}"; do
        CURR_TEST_NAME=${i%%.py*}
        CURR_TEST_NAME=${CURR_TEST_NAME#./*}
        CURR_TEST_NUM="${name_to_num[$CURR_TEST_NAME]}"
        echo "$CURR_TEST_NAME $CURR_TEST_NUM"

        if (( $CURR_TEST_NUM > $STOP_NUM )) || (( $STOP_NUM == $CURR_TEST_NUM )) && (( $STOP_NUM != 0 )); then
            exit 1
        fi
        if (( $CURR_TEST_NUM > $START_NUM )) || (( $CURR_TEST_NUM == $START_NUM )); then
            echo_print
            echo "$i"
            [[ x$DEBUG != x ]] && sleep 2
            eval $i >>~/test_all_output_file.txt
            if [ $? -ne 0 ]; then
                echo $CURR_TEST_NAME failure
                [[ x$DEBUG != x ]] && exit 1
            else
                echo $CURR_TEST_NAME success
            fi
            if [[ "${CURR_TEST_NAME}" = @(example_wpa_connection|example_wpa2_connection|example_wpa3_connection|example_wep_connection) ]]; then
                blank_db
            fi
        fi
    done
}
function check_args() {
    if [ ! -z $1 ]; then
        START_NUM=$1
    fi
    if [ ! -z $2 ]; then
        STOP_NUM=$2
    fi
}
true >~/test_all_output_file.txt
check_args $1 $2
run_test
#test generic and fileio are for macvlans
