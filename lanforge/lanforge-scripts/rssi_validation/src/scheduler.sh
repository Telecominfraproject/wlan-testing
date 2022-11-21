#!/bin/bash
# This script requires the dependencies of ~/lanforge-scripts. To install, run:
# python3 ~/lanforge-scripts/py-scripts/update_dependencies.py
NUMTESTS="$1"
HOST="$2"
AP_RADIO="$3"
AP_NAME="$4"
STA_NAMES="sta0000,sta0001,sta0002,sta0003,sta0004,sta0005,sta0006"
ATTEN_START=200 #ddB
ATTEN_STEP=10 #ddB

# Minimal Test
# -----
BANDWIDTH_OPTIONS=( 20 )
CHANNEL_OPTIONS=( 36 )
ANTENNA_OPTIONS=( 0 )

# Full Test
# -----
# BANDWIDTH_OPTIONS=( 20 40 80 )
# CHANNEL_OPTIONS=( 6 36 )
# ANTENNA_OPTIONS=( 0 1 4 7 8 )

MAIN_DIR=$(dirname $PWD)
SRC_DIR="$MAIN_DIR/src"
JSON_DIR="$MAIN_DIR/json"

request_data () {
    OUTPUT_DIR="$1"
    ATTENUATION="$2"
    mkdir -p "$OUTPUT_DIR"
    $SRC_DIR/sta_requester.sh "$OUTPUT_DIR" "$ATTENUATION" "$HOST" "$STA_NAMES"
    $SRC_DIR/att_requester.sh "$OUTPUT_DIR" "$ATTENUATION" "$HOST"
}

vary_attenuation () {
    # calls request_data()
    for test_index in $(seq 0 $NUMTESTS)
    do
	THIS_DIR="$1"
	ATTENUATION=$(($ATTEN_START + $ATTEN_STEP * $test_index))
	ATTENUATION_DIR="$THIS_DIR/Attenuation$ATTENUATION"
	python3 ~/lanforge-scripts/py-scripts/lf_atten_mod_test.py \
		-hst $HOST -atten_serno all --atten_idx all \
		--atten_val $ATTENUATION
	sleep 5 #allow time for new RSSI to take effect
	echo "$ATTENUATION_DIR"
	request_data "$ATTENUATION_DIR" "$ATTENUATION"
    done    
}

vary_antenna () {
    # calls vary_attenuation()
    for antenna in "${ANTENNA_OPTIONS[@]}"
    do
	THIS_DIR="$1"
        ANTENNA_DIR="$THIS_DIR/Antenna$antenna"
	python3 ~/lanforge-scripts/py-scripts/lf_modify_radio.py \
		--host "$HOST" --radio "$AP_RADIO" \
		--antenna "$antenna" --debug
	sleep 120 #allow time for stations to reassociate
        vary_attenuation "$ANTENNA_DIR"
    done
}

vary_channel () {
    # calls vary_antenna()
    for channel in "${CHANNEL_OPTIONS[@]}"
    do
	THIS_DIR="$1"
        CHANNEL_DIR="$THIS_DIR/Channel$channel"
	python3 ~/lanforge-scripts/py-scripts/lf_modify_radio.py \
		--host "$HOST" --radio "$AP_RADIO" \
		--channel "$channel" --debug
	sleep 120 #allow time for stations to reassociate
        vary_antenna "$CHANNEL_DIR"
    done
}

vary_bandwidth () {
    # calls vary_channel()
    for bandwidth in "${BANDWIDTH_OPTIONS[@]}"
    do
	THIS_DIR="$1"
        BANDWIDTH_DIR="$THIS_DIR/Bandwidth$bandwidth"
	./set_bandwidth.sh "$HOST" "$AP_NAME" "$bandwidth"
	sleep 60 #allow time for stations to reassociate
        vary_channel "$BANDWIDTH_DIR"
    done
}

vary_bandwidth "$JSON_DIR"
