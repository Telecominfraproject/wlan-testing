#!/bin/bash

if [ -z "$1" -o -z "$2" -o -z "$3" ]; then
   echo "Usage: $0 <Layer-3 Name> <Run seconds> <Sleep seconds>"
   echo "   Layer-3 Name: preface with cx: for cross connect"
   echo "                 preface with group: for test group"
   exit 1
fi

MANAGER=${MANAGER:-localhost}
RESOURCE=${RESOURCE:-1}

TRAFFIC_NAME="$1"
USING=wrong
if [[ $1 = cx:* ]]; then
   USING=cx
   TRAFFIC_NAME=${TRAFFIC_NAME#cx:}
elif [[ $1 = group:* ]]; then
   USING=tg
   TRAFFIC_NAME=${TRAFFIC_NAME#group:}
fi

if [[ $USING = wrong ]]; then
   echo "Please specify group using 'group:$TRAFFIC_NAME' or single connection using 'cx:$TRAFFIC_NAME'"
   exit 1
fi

case $USING in
cx)
   START="op_cx run"
   STOP="op_cx stop"
   ;;
tg)
   START="op_group run"
   STOP="op_group stop"
   ;;
esac

RUN_SEC="$2"
SLEEP_SEC="$3"
ACTION="STOPPED"

function op_cx() {
   ACTION="STOPPED"
   if [[ $1 = run ]]; then
      ACTION="RUNNING"
   elif [[ $1 = quiesce ]]; then
      ACTION="QUIESCE"
   fi
   ./lf_firemod.pl --mgr $MANAGER --resource $RESOURCE --quiet yes --action do_cmd --cmd "set_cx_state default_tm $TRAFFIC_NAME $ACTION"
}

function op_group() {
   ACTION="stop_group"
   if [[ $1 = run ]]; then
      ACTION="start_group"
   elif [[ $1 = quiesce ]]; then
      ACTION="quiesce_group"
   fi
   ./lf_firemod.pl --mgr $MANAGER --resource $RESOURCE --quiet yes --action do_cmd --cmd "$ACTION $TRAFFIC_NAME"
}


cd /home/lanforge/scripts
while :; do
   $START
   sleep $RUN_SEC
   $STOP
   sleep $SLEEP_SEC
done
