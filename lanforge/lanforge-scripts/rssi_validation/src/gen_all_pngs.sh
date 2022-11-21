#!/bin/bash
TEST_DIR=$1
PNG_DIR=$2

# Depends on test scenario:
# Theoretically, 1*(number_of_cables) + 12*(number_of_programmable_attenuators) + 12*(number_of_splitter_combiners) + 1*(number_of_pigtails)
PATH_LOSS_2=28.74
PATH_LOSS_5=33.87

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

mkdir -p "$PNG_DIR"
for bandwidth in "${BANDWIDTH_OPTIONS[@]}"
do
    for channel in "${CHANNEL_OPTIONS[@]}"
    do
	for antenna in "${ANTENNA_OPTIONS[@]}"
	do
	    ./generate_png.sh "$TEST_DIR" ../output.csv "$PNG_DIR" "$bandwidth" "$channel" "$antenna" "$PATH_LOSS_2" "$PATH_LOSS_5"
	done
    done
done


