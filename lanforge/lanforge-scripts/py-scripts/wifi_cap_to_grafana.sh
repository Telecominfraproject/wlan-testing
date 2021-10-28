#!/bin/bash

# This bash script creates/updates a DUT, creates/updates a chamberview scenario,
# loads and builds that scenario, runs wifi capacity test, and saves the kpi.csv info
# into influxdb.  As final step, it builds a grafana dashboard for the KPI information.

# Define some common variables.  This will need to be changed to match your own testbed.
MGR=192.168.93.51
INFLUX_MGR=192.168.100.201
#INFLUXTOKEN=Tdxwq5KRbj1oNbZ_ErPL5tw_HUH2wJ1VR4dwZNugJ-APz__mEFIwnqHZdoobmQpt2fa1VdWMlHQClR8XNotwbg==
INFLUXTOKEN=31N9QDhjJHBu4eMUlMBwbK3sOjXLRAhZuCzZGeO8WVCj-xvR8gZWWvRHOcuw-5RHeB7xBFnLs7ZV023k4koR1A==
TESTBED=Heather
INFLUXBUCKET=stidmatt
#GRAFANATOKEN=eyJrIjoiZTJwZkZlemhLQVNpY3hiemRjUkNBZ3k2RWc3bWpQWEkiLCJuIjoibWFzdGVyIiwiaWQiOjF9
GRAFANATOKEN=eyJrIjoiS1NGRU8xcTVBQW9lUmlTM2dNRFpqNjFqV05MZkM0dzciLCJuIjoibWF0dGhldyIsImlkIjoxfQ==
GROUPS=lf_cv_rpt_filelocation.txt

rm lf_cv_rpt_filelocation.txt
touch lf_cv_rpt_filelocation.txt

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

# Run capacity test on the stations created by the chamber view scenario.
# Submit the KPI data into the influxdb.
#config_name doesn't matter, change the influx_host to your LANforge device,
echo "run wifi capacity test"
./lf_wifi_capacity_test.py --config_name Custom --create_stations --radio wiphy1 --pull_report --influx_host ${INFLUX_MGR} \
--influx_port 8086 --influx_org Candela --influx_token  ${INFLUXTOKEN} --influx_bucket ${INFLUXBUCKET} --mgr ${MGR} \
--instance_name testing --upstream eth1 --test_rig ${TESTBED} --graph_groups lf_cv_rpt_filelocation.txt --duration 15s --local_lf_report_dir ${REPORT_PATH}



#config_name doesn't matter, change the influx_host to your LANforge device,
echo "run Dataplane test"
./lf_dataplane_test.py --mgr ${MGR} --instance_name dataplane-instance --config_name test_config --upstream 1.1.eth1 \
--station 1.1.06 --dut linksys-8450 --influx_host ${INFLUX_MGR} --influx_port 8086 --influx_org Candela --influx_token ${INFLUXTOKEN} \
--influx_bucket ${INFLUXBUCKET} --influx_tag testbed ${TESTBED} --graph_groups lf_cv_rpt_filelocation.txt --duration 15s --pull_report --local_lf_report_dir ${REPORT_PATH}


# Build grafana dashboard and graphs view for the KPI in the capacity test.
#./grafana_profile.py --create_custom --title ${TESTBED} --influx_bucket ${INFLUXBUCKET} --mgr ${MGR} --grafana_token \
#${GRAFANATOKEN} --grafana_host ${INFLUX_MGR} --testbed ${TESTBED} --graph_groups_file lf_cv_rpt_filelocation.txt \
#--scripts Dataplane --datasource 'InfluxDB stidmatt bucket'

./ghost_profile.py --ghost_token ${GHOST_TOKEN} --ghost_host ${GHOST_MGR} --authors ${AUTHOR} --customer ${CUSTOMER} \
--user_push ${USER_PUSH} --password_push ${PASSWORD_PUSH} --kpi_to_ghost --grafana_token ${GRAFANATOKEN} --grafana_host ${INFLUX_MGR} \
--grafana_bucket ${INFLUXBUCKET} --influx_host ${INFLUX_MGR} --influx_org Candela --influx_token ${INFLUXTOKEN} \
--influx_bucket ${INFLUXBUCKET} --parent_folder ${REPORT_PATH}

rm lf_cv_rpt_filelocation.txt
