#!/bin/bash
PNG_DIR=$1
REPORT_NAME=$2
REPORT="$REPORT_NAME"

# Minimal Test
# -----
# BANDWIDTH_OPTIONS=( 20 )
# CHANNEL_OPTIONS=( 36 )
# ANTENNA_OPTIONS=( 0 )

# Full Test
# -----
ANTENNA_OPTIONS=( 0 1 4 7 8 )
CHANNEL_OPTIONS=( 6 36 )
BANDWIDTH_OPTIONS=( 20 40 80 )

ANTENNA_TITLE=( [0]="Diversity (All)" [1]="Fixed-A (1x1)" [4]="AB (2x2)" [7]="ABC (3x3)" [8]="ABCD (4x4)" [9]="(8x8)" )

add_signal_section () {
    channel=$1
    antenna=$2
    bandwidth=$3
    deviation=$4
    echo "<h3>Channel=$channel, Antenna=${ANTENNA_TITLE[$antenna]}, Bandwidth=$bandwidth</h3>" >> "$REPORT"
    echo "<div class=\"img-container\"><div class=\"ele\"><img src=\"" >> "$REPORT"
    echo $PNG_DIR/$channel\_$antenna\_$bandwidth\_signal\_atten.png >> "$REPORT"
    echo "\"/><img src=\"" >> "$REPORT"
    echo $PNG_DIR/$channel\_$antenna\_$bandwidth\_signal\_deviation\_atten.png >> "$REPORT"
    echo "\"/></div></div>" >> "$REPORT"
}
add_sections (){
    deviation=$1
    for channel in "${CHANNEL_OPTIONS[@]}"
    do
	for antenna in "${ANTENNA_OPTIONS[@]}"
	do
	    for bandwidth in "${BANDWIDTH_OPTIONS[@]}"
	    do
		if ! [[ "$bandwidth" == "80" ]] || ! [[ "$channel" == "6" ]]; then #check for bandwidth incompatibility
		    add_signal_section "$channel" "$antenna" "$bandwidth" "$deviation"
		fi
	    done
	done
    done
}
echo "<head><style>.img-container img {display:inline-block;width:49%;}.ele {aspect-ratio: 1 / 1;}</style></head>" > "$REPORT"
echo "<h2>RSSI Test Report </h2>" >> "$REPORT"
echo "<h3>Attenuation vs. Signal:<br>" >> "$REPORT"
add_sections
