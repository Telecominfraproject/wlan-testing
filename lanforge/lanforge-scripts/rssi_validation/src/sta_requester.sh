#!/bin/bash
OUTPUT_DIR="$1"
TEST_INDEX="$2"
HOST="$3"
STA_NAMES="$4"
curl -XGET http://"$HOST":8080/port/1/2/"$STA_NAMES"?fields=rx-rate,signal,channel,ssid,ap,chain+rssi,avg+chain+rssi,mode | json_pp > "$OUTPUT_DIR/sta_data$TEST_INDEX.json"
