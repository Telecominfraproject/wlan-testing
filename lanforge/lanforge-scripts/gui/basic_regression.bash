#!/bin/bash

# Run some automated GUI tests, save the results
# Example of how to run this and override LFMANAGER default settings.  Other values can
# be over-ridden as well.
#
#  LFMANAGER=192.168.100.156 ./basic_regression.bash
#
# Run subset of tests
#  LFMANAGER=192.168.100.156 DEFAULT_ENABLE=0 DO_SHORT_AP_STABILITY_RESET=1 ./basic_regression.bash
#
#

# Disable stdout buffering in python so that we get serial console log
# output promptly.

#set -x

PYTHONUNBUFFERED=1
export PYTHONUNBUFFERED

AP_SERIAL=${AP_SERIAL:-NONE}
LF_SERIAL=${LF_SERIAL:-NONE}
APGW=${APGW:-172.16.0.1}
LFPASSWD=${LFPASSWD:-lanforge}  # Root password on LANforge machine
AP_AUTO_CFG_FILE=${AP_AUTO_CFG_FILE:-test_configs/AP-Auto-ap-auto-32-64-dual.txt}
WCT_CFG_FILE=${WCT_CFG_FILE:-test_configs/WCT-64sta.txt}
DPT_CFG_FILE=${DPT_CFG_FILE:-test_configs/dpt-pkt-sz.txt}
SCENARIO_CFG_FILE=${SCENARIO_CFG_FILE:-test_configs/64_sta_scenario.txt}
WCT_DURATION=${WCT_DURATION:-60s}

# LANforge target machine
LFMANAGER=${LFMANAGER:-localhost}

# LANforge GUI machine (may often be same as target)
GMANAGER=${GMANAGER:-localhost}
GMPORT=${GMPORT:-3990}
MY_TMPDIR=${MY_TMPDIR:-/tmp}

# Test configuration (10 minutes by default, in interest of time)
STABILITY_DURATION=${STABILITY_DURATION:-600}
TEST_RIG_ID=${TEST_RIG_ID:-Unspecified}

# DUT configuration
DUT_FLAGS=${DUT_FLAGS:-NA}
DUT_FLAGS_MASK=${DUT_FLAGS_MASK:-NA}
DUT_SW_VER=${DUT_SW_VER:-NA}
DUT_HW_VER=${DUT_HW_VER:-NA}
DUT_MODEL=${DUT_MODEL:-NA}
DUT_SERIAL=${DUT_SERIAL:-NA}
DUT_SSID1=${DUT_SSID1:-NA}
DUT_SSID2=${DUT_SSID2:-NA}
DUT_SSID3=${DUT_SSID3:-NA}
DUT_PASSWD1=${DUT_PASSWD1:-NA}
DUT_PASSWD2=${DUT_PASSWD2:-NA}
DUT_PASSWD3=${DUT_PASSWD3:-NA}
DUT_BSSID1=${DUT_BSSID1:-NA}
DUT_BSSID2=${DUT_BSSID2:-NA}
DUT_BSSID3=${DUT_BSSID3:-NA}


# Tests to run
DEFAULT_ENABLE=${DEFAULT_ENABLE:-1}
DO_DPT_PKT_SZ=${DO_DPT_PKT_SZ:-$DEFAULT_ENABLE}
DO_WCT_DL=${DO_WCT_DL:-$DEFAULT_ENABLE}
DO_WCT_UL=${DO_WCT_UL:-$DEFAULT_ENABLE}
DO_WCT_BI=${DO_WCT_BI:-$DEFAULT_ENABLE}
DO_SHORT_AP_BASIC_CX=${DO_SHORT_AP_BASIC_CX:-$DEFAULT_ENABLE}
DO_SHORT_AP_TPUT=${DO_SHORT_AP_TPUT:-$DEFAULT_ENABLE}
DO_SHORT_AP_STABILITY_RESET=${DO_SHORT_AP_STABILITY_RESET:-$DEFAULT_ENABLE}
DO_SHORT_AP_STABILITY_RADIO_RESET=${DO_SHORT_AP_STABILITY_RADIO_RESET:-$DEFAULT_ENABLE}
DO_SHORT_AP_STABILITY_NO_RESET=${DO_SHORT_AP_STABILITY_NO_RESET:-$DEFAULT_ENABLE}

DATESTR=$(date +%F-%T)
RSLTS_DIR=${RSLTS_DIR:-basic_regression_results_$DATESTR}


# Probably no config below here
AP_AUTO_CFG=ben
WCT_CFG=ben
DPT_CFG=ben
# Change testbed_poll.pl if scenario changes below.
SCENARIO=tip-auto
RPT_TMPDIR=${MY_TMPDIR}/lf_reports
LF_SER_DEV=$(basename $LF_SERIAL)
DUT_SER_DEV=$(basename $AP_SERIAL)
LF_SER_LOG=$MY_TMPDIR/lanforge_console_log_$LF_SER_DEV.txt
DUT_SER_LOG=$MY_TMPDIR/dut_console_log_$DUT_SER_DEV.txt
REGLOG=$MY_TMPDIR/basic_regression_log_$$.txt

# Query DUT from the scenario
DUT=`grep DUT: $SCENARIO_CFG_FILE |head -1|grep -o "DUT: .*"|cut -f2 -d ' '`

echo "Found DUT: $DUT from scenario $SCENARIO_CFG_FILE"

function pre_test {
    # Remove existing data connections.
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli rm_cx all all"
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli rm_endp YES_ALL"

    # Clear port counters.
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli clear_port_counters ALL ALL ALL"

    # Clean logs, this bounces radios and such too as side effect
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli admin clean_logs"

    if [ "_${LF_SERIAL}" != "_NONE" ]
    then
        # Kill any existing processes on this serial port
        pkill -f ".*openwrt_ctl.*$LF_SERIAL.*"
        ../openwrt_ctl.py --action lurk $OWRTCTL_ARGS --tty $LF_SERIAL --scheme serial --user root --passwd $LFPASSWD --prompt "\[root@" >  $LF_SER_LOG 2>&1 &
    fi

    if [ "_${AP_SERIAL}" != "_NONE" ]
    then
        # Kill any existing processes on this serial port
        pkill -f ".*openwrt_ctl.*$AP_SERIAL.*"
        ../openwrt_ctl.py --action logread $OWRTCTL_ARGS --tty $AP_SERIAL --scheme serial >  $DUT_SER_LOG 2>&1 &
    fi
}

function reboot_dut {
     ../openwrt_ctl.py --action reboot $OWRTCTL_ARGS --tty $AP_SERIAL --scheme serial
     # TODO:  Support hard-power cycle with power-ctl switch as well?
}

function post_test {
    DEST=$1
    mkdir -p $DEST/logs

    if [ "_${LF_SERIAL}" != "_NONE" ]
        then
        # Kill any existing processes on this serial port
        pkill -f ".*openwrt_ctl.*$LF_SERIAL.*"
        mv $LF_SER_LOG $DEST/logs/lanforge_console_log.txt
    fi

    if [ "_${AP_SERIAL}" != "_NONE" ]
        then
        # Kill any existing processes on this serial port
        pkill -f ".*openwrt_ctl.*$AP_SERIAL.*"
        mv $DUT_SER_LOG $DEST/logs/dut_console_log.txt

        # Look for firmware crash files
        PIDD=$$
        ../openwrt_ctl.py $OWRTCTL_ARGS --tty $AP_SERIAL --scheme serial --action cmd --value "tar -cvzf /tmp/bugcheck.tgz /tmp/bugcheck"
        ../openwrt_ctl.py $OWRTCTL_ARGS --tty $AP_SERIAL --scheme serial --action upload --value "/tmp/bugcheck.tgz" --value2 "lanforge@$APGW:bugcheck-$PIDD.tgz"

        # Grab the file from LANforge
        scp lanforge@$LFMANAGER:bugcheck-$PIDD.tgz $DEST/logs/bugcheck.tgz

        # Clean log file
        ssh lanforge@$LFMANAGER "rm bugcheck-$PIDD.tgz"

        # detect a few fatal flaws and reqest AP restart if found.
        grep "Hardware became unavailable" $DEST/logs/dut_console_log.txt && reboot_dut
    fi

    mv $REGLOG $DEST/logs/test_automation_log.txt
    if [ -f /home/lanforge/lanforge_log_0.txt ]
    then
        # Must be running on LF itself
        cp /home/lanforge/lanforge_log_*.txt* $DEST/logs/
        cp /home/lanforge/wifi/*log* $DEST/logs/
    else
        # Try via scp.  Root perms needed to read wifi logs, thus root@
        scp root@$LFMANAGER:/home/lanforge/lanforge_log_*.txt* $DEST/logs/
        scp root@$LFMANAGER:/home/lanforge/wifi/*log* $DEST/logs/
    fi
}


set -x

mkdir -p $RSLTS_DIR

# Load scenario file
../lf_testmod.pl --mgr $LFMANAGER --action set --test_type Network-Connectivity --test_name $SCENARIO --file $SCENARIO_CFG_FILE

# Load AP-Auto config file
../lf_testmod.pl --mgr $LFMANAGER --action set --test_name AP-Auto-$AP_AUTO_CFG --file $AP_AUTO_CFG_FILE

# Load Wifi Capacity config file
../lf_testmod.pl --mgr $LFMANAGER --action set --test_name Wifi-Capacity-$WCT_CFG --file $WCT_CFG_FILE

# Load Dataplane config file
../lf_testmod.pl --mgr $LFMANAGER --action set --test_name dataplane-test-latest-$DPT_CFG --file $DPT_CFG_FILE

# Set DUT info if configured.
if [ "_$DUT" != "_" ]
then
    ../lf_portmod.pl --manager $LFMANAGER \
        --cli_cmd "add_dut $DUT $DUT_FLAGS NA '$DUT_SW_VER' '$DUT_HW_VER' '$DUT_MODEL' '$DUT_SERIAL' NA NA NA '$DUT_SSID1' '$DUT_PASSWD1' '$DUT_SSID2' '$DUT_PASSWD2' '$DUT_SSID3' '$DUT_PASSWD3' NA NA $DUT_FLAGS_MASK NA NA NA $DUT_BSSID1 $DUT_BSSID2 $DUT_BSSID3"
fi

# Make sure GUI is synced up with the server
../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli show_text_blob"
../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --cmd "cli show_dut"

# Pause to let GUI finish getting data from the server
sleep 20

# Tell GUI to load and build the scenario
../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --scenario $SCENARIO

# Clean out temp report directory on local system and remote
if [ -d $RPT_TMPDIR ]
then
    rm -fr $RPT_TMPDIR/*
fi
ssh lanforge\@$GMANAGER "test -d $RPT_TMPDIR && rm -fr $RPT_TMPDIR";

# Do dataplane pkt size test
echo "Checking if we should run Dataplane packet size test."
if [ "_$DO_DPT_PKT_SZ" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "Dataplane" --tname dpt-ben  --tconfig $DPT_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "Dataplane Pkt-Size" \
        --modifier_key "Show Low-Level Graphs" --modifier_val true \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/dataplane_pkt_sz
    post_test $RSLTS_DIR/dataplane_pkt_sz
fi

# Do capacity test
echo "Checking if we should run WCT Download test."
if [ "_$DO_WCT_DL" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "WiFi Capacity" --tname wct-ben  --tconfig $WCT_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "Capacity-Download" \
        --modifier_key "RATE_DL" --modifier_val "1Gbps" \
        --modifier_key "RATE_UL" --modifier_val "0" \
        --modifier_key "VERBOSITY" --modifier_val "9" \
        --modifier_key "Duration:" --modifier_val "$WCT_DURATION" \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/wifi_capacity_dl
    post_test $RSLTS_DIR/wifi_capacity_dl
fi

echo "Checking if we should run WCT Upload test."
if [ "_$DO_WCT_UL" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "WiFi Capacity" --tname wct-ben  --tconfig $WCT_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "Capacity-Upload" \
        --modifier_key "RATE_UL" --modifier_val "1Gbps" \
        --modifier_key "RATE_DL" --modifier_val "0" \
        --modifier_key "VERBOSITY" --modifier_val "9" \
        --modifier_key "Duration:" --modifier_val "$WCT_DURATION" \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/wifi_capacity_ul
    post_test $RSLTS_DIR/wifi_capacity_ul
fi

echo "Checking if we should run WCT Bi-Direction test."
if [ "_$DO_WCT_BI" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "WiFi Capacity" --tname wct-ben  --tconfig $WCT_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "Capacity-TCP-UL+DL" \
        --modifier_key "RATE_UL" --modifier_val "1Gbps" \
        --modifier_key "RATE_DL" --modifier_val "1Gbps" \
        --modifier_key "Protocol:" --modifier_val "TCP-IPv4" \
        --modifier_key "VERBOSITY" --modifier_val "9" \
        --modifier_key "Duration:" --modifier_val "$WCT_DURATION" \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/wifi_capacity_bi
    post_test $RSLTS_DIR/wifi_capacity_bi
fi


# Run basic-cx test
echo "Checking if we should run Short-AP Basic CX test."
if [ "_$DO_SHORT_AP_BASIC_CX" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "AP-Auto" --tname ap-auto-ben --tconfig $AP_AUTO_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "Band-Steering" --modifier_val false \
        --modifier_key "Multi-Station Throughput vs Pkt Size" --modifier_val false \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/ap_auto_basic_cx
    post_test $RSLTS_DIR/ap_auto_basic_cx
fi

# Run Throughput, Dual-Band, Capacity test in a row, the Capacity will use results from earlier
# tests.
echo "Checking if we should run Short-AP Throughput test."
if [ "_$DO_SHORT_AP_TPUT" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "AP-Auto" --tname ap-auto-ben --tconfig $AP_AUTO_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "Basic Client Connectivity" --modifier_val false \
        --modifier_key "Throughput vs Pkt Size" --modifier_val true \
        --modifier_key "Dual Band Performance" --modifier_val true \
        --modifier_key "Band-Steering" --modifier_val false \
        --modifier_key "Multi-Station Throughput vs Pkt Size" --modifier_val false \
        --modifier_key "Capacity" --modifier_val true \
        --rpt_dest $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/ap_auto_capacity
    post_test $RSLTS_DIR/ap_auto_capacity
fi

# Run Stability test (single port resets, voip, tcp, udp)
echo "Checking if we should run Short-AP Stability Reset test."
if [ "_$DO_SHORT_AP_STABILITY_RESET" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "AP-Auto" --tname ap-auto-ben --tconfig $AP_AUTO_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "AP-Auto Port-Reset" \
        --modifier_key "Basic Client Connectivity" --modifier_val false \
        --modifier_key "Stability" --modifier_val true \
        --modifier_key "Band-Steering" --modifier_val false \
        --modifier_key "Multi-Station Throughput vs Pkt Size" --modifier_val false \
        --modifier_key "Stability Duration:" --modifier_val $STABILITY_DURATION \
        --rpt_dest  $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/ap_auto_stability_reset_ports
    post_test $RSLTS_DIR/ap_auto_stability_reset_ports
fi

# Run Stability test (radio resets, voip, tcp, udp)
echo "Checking if we should run Short-AP Stability Radio Reset test."
if [ "_$DO_SHORT_AP_STABILITY_RADIO_RESET" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "AP-Auto" --tname ap-auto-ben --tconfig $AP_AUTO_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "AP-Auto Radio-Reset" \
        --modifier_key "Basic Client Connectivity" --modifier_val false \
        --modifier_key "Stability" --modifier_val true \
        --modifier_key "Band-Steering" --modifier_val false \
        --modifier_key "Stability Duration:" --modifier_val $STABILITY_DURATION \
        --modifier_key "Multi-Station Throughput vs Pkt Size" --modifier_val false \
        --modifier_key "Reset Radios" --modifier_val true \
        --rpt_dest  $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/ap_auto_stability_reset_radios
    post_test $RSLTS_DIR/ap_auto_stability_reset_radios
fi

# Run Stability test (no resets, no voip, tcp, udp)
echo "Checking if we should run Short-AP Stability No-Reset test."
if [ "_$DO_SHORT_AP_STABILITY_NO_RESET" == "_1" ]
then
    pre_test
    ../lf_gui_cmd.pl --manager $GMANAGER --port $GMPORT --ttype "AP-Auto" --tname ap-auto-ben --tconfig $AP_AUTO_CFG \
        --modifier_key "Test Rig ID:" --modifier_val "$TEST_RIG_ID" \
        --modifier_key "DUT_NAME" --modifier_val "$DUT" \
        --modifier_key "KPI_TEST_ID" --modifier_val "AP-Auto No-Reset" \
        --modifier_key "Basic Client Connectivity" --modifier_val false \
        --modifier_key "Band-Steering" --modifier_val false \
        --modifier_key "Stability" --modifier_val true \
        --modifier_key "Stability Duration:" --modifier_val $STABILITY_DURATION \
        --modifier_key "Multi-Station Throughput vs Pkt Size" --modifier_val false \
        --modifier_key "VOIP Call Count:" --modifier_val 0 \
        --modifier_key "Concurrent Ports To Reset:" --modifier_val 0 \
        --rpt_dest  $RPT_TMPDIR > $REGLOG 2>&1
    mv $RPT_TMPDIR/* $RSLTS_DIR/ap_auto_stability_no_reset
    post_test $RSLTS_DIR/ap_auto_stability_no_reset
fi

if [ "_${LFLOG_PID}" != "_" ]
then
    kill $LFLOG_PID
    mv $LF_SER_LOG $RSLTS_DIR/lanforge_console_log.txt
fi
if [ "_${DUTLOG_PID}" != "_" ]
then
    kill $DUTLOG_PID
    mv $$DUT_SER_LOG $RSLTS_DIR/dut_console_log.txt
fi

RPT_ARGS=
if [ "_${NOTES_HTML}" == "_" ]
then
    NOTES_HTML=NA
fi

if [ "_${GITLOG}" == "_" ]
then
    GITLOG=NA
fi

if [ "_${DUTGITLOG}" == "_" ]
then
    DUTGITLOG=NA
fi

echo "./lf_gui_report_summary.pl --title \"$TEST_RIG_ID: $DUT_SW_VER\" --dir $RSLTS_DIR --dutgitlog $DUTGITLOG --gitlog $GITLOG --notes $NOTES_HTML"
./lf_gui_report_summary.pl --title "$TEST_RIG_ID: $DUT_SW_VER" --dir $RSLTS_DIR --dutgitlog $DUTGITLOG --gitlog $GITLOG --notes $NOTES_HTML < index_template.html  > $RSLTS_DIR/index.html

echo "Done with automated regression test."
echo "Results-Dir: $RSLTS_DIR"
