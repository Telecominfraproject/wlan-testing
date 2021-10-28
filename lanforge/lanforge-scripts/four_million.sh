#!/bin/bash
export PATH=".:$PATH"
FM="./lf_firemod.pl"
mgr=idtest
rsrc=3
max=1000
numvlan=199
connections=()
for c in `seq 1 $max`; do
  n=$(( (10 * $max) + $c ))
  connections[$c]="con${n:1:${#max}}"
done

index=0
portnum=0
for c in "${connections[@]}"; do
   echo -n .
  $FM --mgr $mgr --resource $rsrc --action create_endp --endp_name ${c}-A --speed 25000 --endp_type lf_tcp --port_name "eth1#$portnum"

  $FM --mgr $mgr --resource $rsrc --action create_endp --endp_name ${c}-B --speed 25000 --endp_type lf_tcp --port_name "eth2"
  
  $FM --mgr $mgr --resource $rsrc --action create_cx --cx_name ${c} --cx_endps ${c}-A,${c}-B --report_timer 8000
   echo -n o

  index=$((index + 1))
  portnum=$((index % $numvlan))
done
echo " done"


#
