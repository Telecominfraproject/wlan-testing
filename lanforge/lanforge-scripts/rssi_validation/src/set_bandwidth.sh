#!/bin/bash
HOST="$1"
AP_NAME="$2"
BANDWIDTH="$3"
case "$BANDWIDTH" in
    20)
	~/lanforge-scripts/py-scripts/modify_vap.py --debug \
	    --mgr "$HOST" --vap "$AP_NAME" \
	    --enable_flag disable_ht80 --enable_flag disable_ht40
	;;
    40)
	~/lanforge-scripts/py-scripts/modify_vap.py --debug \
	    --mgr "$HOST" --vap "$AP_NAME" \
	    --enable_flag disable_ht80 --disable_flag disable_ht40
	;;
    80)
	~/lanforge-scripts/py-scripts/modify_vap.py --debug \
	    --mgr "$HOST" --vap "$AP_NAME" \
	    --disable_flag disable_ht80 --disable_flag disable_ht40
	;;
    *)
	echo "Not a valid bandwidth: $BANDWIDTH"
esac
