#!/bin/bash
OUTPUT_DIR="$1"
TEST_INDEX="$2"
HOST="$3"
curl -XGET http://"$HOST":8080/atten/1/1/3219?fields=module+1,module+2,module+3,module+4 | json_pp > "$OUTPUT_DIR/att_data$TEST_INDEX.json"
