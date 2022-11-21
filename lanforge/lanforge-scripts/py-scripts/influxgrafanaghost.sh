#! /bin/bash

MGR=192.168.100.213
LFUSER=lanforge
LOCALDIR=/home/matthew/Documents/lanforge-scripts/py-scripts/lftest
TESTRIG="Matthew-ct523c"

GHOSTTOKEN=60df4b0175953f400cd30650:d50e1fabf9a9b5d3d30fe97bc3bf04971d05496a89e92a169a0d72357c81f742

INFLUXTOKEN=31N9QDhjJHBu4eMUlMBwbK3sOjXLRAhZuCzZGeO8WVCj-xvR8gZWWvRHOcuw-5RHeB7xBFnLs7ZV023k4koR1A==
INFLUXHOST=c7-grafana.candelatech.com
INFLUXBUCKET=stidmatt

GRAFANATOKEN=eyJrIjoiS1NGRU8xcTVBQW9lUmlTM2dNRFpqNjFqV05MZkM0dzciLCJuIjoibWF0dGhldyIsImlkIjoxfQ==

rm -r ${LOCALDIR}

mkdir ${LOCALDIR}

./scenario.py --mgr ${MGR} --load BLANK

sleep 10s

./create_l3.py --mgr ${MGR} --num_stations 4 --ssid stidmatt2 --password stidmatt2 --security wpa2 --radio wiphy0

./lf_dataplane_test.py --mgr ${MGR} --lf_user ${LFUSER} --lf_password lanforge --instance_name wct_instance \
--config_name 64_stations --upstream 1.1.eth1 --influx_host c7-grafana.candelatech.com --influx_org Candela \
--influx_token ${INFLUXTOKEN} --influx_bucket ${INFLUXBUCKET} --test_rig ${TESTRIG} --influx_tag testbed ${TESTRIG} \
--station 1.1.sta0000 --set DUT_NAME linksys-8450 --local_lf_report_dir ${LOCALDIR} \
--pull_report \
--download_speed 85% --upload_speed 0 \
--raw_line 'cust_pkt_sz: 88 1200' \
--raw_line 'directions: DUT Transmit;DUT Receive' \
--raw_line 'traffic_types: UDP' --pull_report --test_tag influxgrafanaghost.sh
#--raw_line 'pkts: Custom;60;142;256;512;1024;MTU'

./lf_wifi_capacity_test.py --mgr ${MGR} --lf_user ${LFUSER} --lf_password lanforge --instance_name linksys-8450 \
--config_name wifi_config --upstream 1.1.eth1 --radio wiphy0 --ssid lanforge --paswd lanforge --security wpa2 \
--influx_host ${INFLUXHOST} --influx_org Candela --influx_bucket ${INFLUXBUCKET} --test_rig ${TESTRIG} \
--influx_token ${INFLUXTOKEN} --influx_tag testbed ${TESTRIG} --set DUT_NAME linksys-8450 --local_lf_report_dir \
${LOCALDIR} --enable FALSE --pull_report --test_tag influxgrafanaghost.sh

./lf_wifi_capacity_test.py --mgr ${MGR} --lf_user ${LFUSER} --lf_password lanforge --instance_name linksys-8450 \
--config_name wifi_config --upstream 1.1.eth1 --radio wiphy0 --ssid lanforge --paswd lanforge --security wpa2 \
--influx_host ${INFLUXHOST} --influx_org Candela --influx_bucket ${INFLUXBUCKET} --test_rig ${TESTRIG} \
--influx_token ${INFLUXTOKEN} --influx_tag testbed ${TESTRIG} --set DUT_NAME linksys-8450 --local_lf_report_dir \
${LOCALDIR} --enable FALSE --pull_report --test_tag Can_we_use_two_test_tags

./lf_ap_auto_test.py --mgr ${MGR} --instance_name ap-auto-instance --config_name test_con --upstream 1.1.eth1 \
--dut5_0 'matthew-router lanforge 04:f0:21:c0:65:7b (1)' --dut2_0 'matthew-router lanforge 04:f0:21:c0:65:7b (1)' \
--max_stations_2 32 --max_stations_5 32 --max_stations_dual 100 --radio2 1.1.wiphy0 --radio5 1.1.wiphy0 \
--set 'Basic Client Connectivity' 1 --set 'Multi Band Performance' 1 --set 'Stability' 0   --set 'Capacity' 0 \
--set 'Multi-Station Throughput vs Pkt Size' 0 --set 'Throughput vs Pkt Size' 0 --set 'Band-Steering' 1 \
--influx_host ${INFLUXHOST} --influx_org Candela --influx_bucket ${INFLUXBUCKET} --test_rig ${TESTRIG} \
--influx_token ${INFLUXTOKEN} --influx_tag testbed ${TESTRIG} --pull_report --test_tag influxgrafanaghost.sh \
--local_lf_report_dir ${LOCALDIR}

./ghost_profile.py --ghost_token ${GHOSTTOKEN} --ghost_host 192.168.100.153 --authors Matthew --customer candela \
--user_push lanforge --password_push lanforge --kpi_to_ghost --grafana_token ${GRAFANATOKEN} \
--grafana_host 192.168.100.201 --grafana_bucket ${INFLUXBUCKET} --influx_host ${INFLUXHOST} --influx_org Candela \
--influx_token ${INFLUXTOKEN} --influx_bucket ${INFLUXBUCKET} --parent_folder ${LOCALDIR}