#!/bin/bash

INFLUX_TOKEN=31N9QDhjJHBu4eMUlMBwbK3sOjXLRAhZuCzZGeO8WVCj-xvR8gZWWvRHOcuw-5RHeB7xBFnLs7ZV023k4koR1A==
INFLUX_HOST=c7-grafana.candelatech.com
INFLUX_BUCKET=stidmatt

GRAFANA_TOKEN=eyJrIjoiS1NGRU8xcTVBQW9lUmlTM2dNRFpqNjFqV05MZkM0dzciLCJuIjoibWF0dGhldyIsImlkIjoxfQ==

GHOST_TOKEN=60df4b0175953f400cd30650:d50e1fabf9a9b5d3d30fe97bc3bf04971d05496a89e92a169a0d72357c81f742

SSID=lanforge
PASSWORD=password
SECURITY=wpa2
TEST_RIG=ct523c-ccbc
DUT_NAME=linksys-8450
MGR=192.168.1.7
RADIO=wiphy1
UPSTREAM=1.1.eth1

NOW=$(date +"%Y-%m-%d-%H-%M")

mkdir ${NOW}
#./scenario.py --mgr ${MGR} --load BLANK
#./create_l3.py --mgr ${MGR} --radio ${RADIO} --ssid ${SSID} --password ${PASSWORD} --security ${SECURITY}
# Create/update new DUT.
#Replace my arguments with your setup.  Separate your ssid arguments with spaces and ensure the names are lowercase
echo "Make new DUT"
./create_chamberview_dut.py --lfmgr ${MGR} --dut_name DUT_TO_GRAFANA_DUT \
--ssid "ssid_idx=0 ssid=lanforge security=WPA2 password=password bssid=04:f0:21:2c:41:84"

# Create/update chamber view scenario and apply and build it.
echo "Build Chamber View Scenario"
#change the lfmgr to your system, set the radio to a working radio on your LANforge system, same with the ethernet port.
./create_chamberview.py --lfmgr ${MGR} --create_scenario DUT_TO_GRAFANA_SCENARIO \
--line "Resource=1.1 Profile=default Amount=4 Uses-1=wiphy1 DUT=DUT_TO_GRAFANA_DUT Traffic=wiphy1 Freq=-1" \
--line "Resource=1.1 Profile=upstream Amount=1 Uses-1=eth1 DUT=DUT_TO_GRAFANA_DUT Traffic=eth1 Freq=-1"

./lf_wifi_capacity_test.py --mgr 192.168.1.7 --lf_user lanforge --lf_password lanforge --instance_name ${DUT_NAME} \
--config_name wifi_config --upstream ${UPSTREAM} --radio wiphy0 --ssid ${SSID} --paswd ${PASSWORD} --security ${SECURITY} \
--influx_host ${INFLUX_HOST} --influx_org Candela --influx_token ${INFLUX_TOKEN} --influx_bucket ${INFLUX_BUCKET} \
--test_rig ${TEST_RIG} --influx_tag testbed ${TEST_RIG} --set DUT_NAME ${DUT_NAME} \
--local_lf_report_dir /home/matthew/Documents/candela/lanforge-scripts/py-scripts/${NOW}
./lf_dataplane_test.py --mgr 192.168.1.7 --lf_user lanforge --lf_password lanforge --instance_name wct_instance \
--config_name wifi_config --upstream ${UPSTREAM} --influx_host ${INFLUX_HOST} --influx_org Candela \
--influx_token ${INFLUX_TOKEN} --influx_bucket ${INFLUX_BUCKET} --test_rig ${TEST_RIG} --influx_tag testbed ${TEST_RIG} \
--station 1.1.sta00000 --raw_line 'traffic_types: UDP;TCP' --set DUT_NAME ${DUT_NAME} \
--local_lf_report_dir /home/matthew/Documents/candela/lanforge-scripts/py-scripts/${NOW} --pull_report
./ghost_profile.py --ghost_token ${GHOST_TOKEN} --ghost_host v-centos8s.candelatech.com --authors Matthew --customer candela  \
--user_push lanforge --password_push lanforge --kpi_to_ghost --grafana_token ${GRAFANA_TOKEN} \
--grafana_host c7-grafana.candelatech.com --grafana_bucket lanforge_qa_testing \
--parent_folder /home/matthew/Documents/candela/lanforge-scripts/py-scripts/${NOW}