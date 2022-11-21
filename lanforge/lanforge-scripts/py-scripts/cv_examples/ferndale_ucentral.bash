#!/bin/bash

# This bash script creates/updates a DUT, creates/updates a chamberview scenario,
# loads and builds that scenario, runs wifi capacity test, and saves the kpi.csv info
# into influxdb.  As final step, it builds a grafana dashboard for the KPI information.

set -x

# Define some common variables.  This will need to be changed to match your own testbed.
# MGR is LANforge GUI machine
#MGR=192.168.100.209
MGR=localhost

# Candela internal influx
INFLUXTOKEN=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ==
INFLUX_HOST=192.168.100.201
INFLUX_BUCKET=ben
INFLUX_ORG=Candela

GRAFANATOKEN=eyJrIjoiVXVyZ0dQSXlNdGlQNGQ1R282S2p6SE1PZXJVOVpvM1UiLCJuIjoiYmVuLWdyYWZhbmEiLCJpZCI6MX0=
GRAFANA_HOST=192.168.100.201
GROUP_FILE=/tmp/lf_cv_rpt_filelocation.txt
TESTBED=Ferndale-01
DUT=linksys-8450
UPSTREAM=eth2
LF_WAN_PORT=eth3
MGR_PORT=8080

if [ -f $HOME/influx_vars.sh ]
then
    # Put private keys and other variable overrides in here.
    . $HOME/influx_vars.sh
fi


# Create/update new DUT.
#Replace my arguments with your setup.  Separate your ssid arguments with spaces and ensure the names are lowercase
echo "Make new DUT"
./create_chamberview_dut.py --lfmgr ${MGR} --port ${MGR_PORT} --dut_name ${DUT} \
  --ssid "ssid_idx=0 ssid=Default-SSID-2g security=WPA2 password=12345678 bssid=c4:41:1e:f5:3f:24" \
  --ssid "ssid_idx=1 ssid=Default-SSID-5gl security=WPA2 password=12345678 bssid=c4:41:1e:f5:3f:25" \
  --sw_version "ucentral-01" --hw_version ea8450 --serial_num 1001 --model_num 8450

# Create/update chamber view scenario and apply and build it.
# Easiest way to get these lines is to build it in the GUI and then
# copy/tweak what it shows in the 'Text Output' tab after saving and re-opening
# the scenario.
echo "Build Chamber View Scenario"
#change the lfmgr to your system, set the radio to a working radio on your LANforge system, same with the ethernet port.

./create_chamberview.py --lfmgr ${MGR} --port ${MGR_PORT} --delete_scenario \
  --create_scenario ucentral-scenario \
  --raw_line "profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-1' NA wiphy0,AUTO -1 NA" \
  --raw_line "profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-1' NA wiphy2,AUTO -1 NA" \
  --raw_line "profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-2' NA wiphy1,AUTO -1 NA" \
  --raw_line "profile_link 1.1 STA-AC 46 'DUT: $DUT Radio-2' NA wiphy3,AUTO -1 NA" \
  --raw_line "profile_link 1.1 upstream-dhcp 1 NA NA $UPSTREAM,AUTO -1 NA" \
  --raw_line "profile_link 1.1 uplink-nat 1 'DUT: upstream LAN 192.168.100.1/24' NA $LF_WAN_PORT,$UPSTREAM -1 NA" \
  --raw_line "profile_link 1.1 STA-AC 1 'DUT: $DUT Radio-2' NA ALL-AX,AUTO -1 NA"

# Run capacity test on the stations created by the chamber view scenario.
# Submit the KPI data into the influxdb.
#config_name doesn't matter, change the influx_host to your LANforge device,
# NOTE:  My influx token is unlucky and starts with a '-', but using the syntax below
# with '=' right after the argument keyword works as hoped.
echo "run wifi capacity test"
./lf_wifi_capacity_test.py --config_name Custom --pull_report --influx_host ${INFLUX_HOST} \
  --influx_port 8086 --influx_org ${INFLUX_ORG} --influx_token=${INFLUXTOKEN} --influx_bucket ${INFLUX_BUCKET} --mgr ${MGR} \
  --port ${MGR_PORT} \
  --instance_name testing --upstream 1.1.$UPSTREAM --test_rig ${TESTBED} --graph_groups ${GROUP_FILE} \
  --batch_size "100" --protocol "TCP-IPv4" --duration 20000

# Build grafana dashboard and graphs view for the KPI in the capacity test.
#echo "Adding grafana dashboard"
#./grafana_profile.py --create_custom --title ${TESTBED} --influx_bucket ${INFLUX_BUCKET} --grafana_token ${GRAFANATOKEN} \
#  --grafana_host ${GRAFANA_HOST} --testbed ${TESTBED} --graph-groups ${GROUPS} --scripts Dataplane --scripts 'WiFi Capacity'

rm ${GROUP_FILE}
