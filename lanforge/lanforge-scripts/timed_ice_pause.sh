#!/bin/bash
# --------------------------------------------------------------------------- #
# timed_ice_pause.sh
#
# use this script to regularly pause traffic on a WANlink by
# dropping all packets for a specified amount of time
#
# -n     name of wanlink
# -r     run for time period
# -p     pause traffic for time period
# -h     show help
# -S     seconds
# -M     minutes
# -H     hours
# -D     days
#
# Time period should be a valid argument to sleep(1):
#  5s    5 seconds
#  6m    6 minutes
#  7h    7 hours
#  8d    8 days
#
# Time ranges have to be valid input to shuf(1), just integers:
#  1-10  => shuf -i 1-10 -n 1
#
# --------------------------------------------------------------------------- #
# scripts
cd /home/lanforge/scripts
trap do_sigint INT

function do_sigint() {
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $link_name-A NA NA NA NA NA 0" &>/dev/null
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $link_name-B NA NA NA NA NA 0" &>/dev/null

   exit 0
}

function stop_cx() {
   [ -z "$1" ] && echo "No connection name, bye." && exit 1
   local name=$1
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd \
      --cmd "set_cx_state all $name QUIESCE" &>/dev/null
}

function start_cx() {
   [ -z "$1" ] && echo "No connection name, bye." && exit 1
   local name=$1
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd \
      --cmd "set_cx_state all $name RUNNING" &>/dev/null
}

function pause_wl() {
   [ -z "$1" ] && echo "No connection name, bye." && exit 1
   [ -z "$2" ] && echo "No sleep time, bye." && exit 1
   local name=$1
   local pause_time=$2

   # read the max-drop-rate
   local formerDrA=-1
   local formerDrB=-1
   local info
   mapfile -t info < <(./lf_firemod.pl --mgr localhost --quiet on --action do_cmd \
      --cmd "show_endpoints $name-A")
   for L in "${info[@]}"; do
      #echo "L: $L"
      if [[ $L == *DropFreq:* ]]; then
         formerDrA=`echo $L | grep -oP 'DropFreq: (\S+)'`
         formerDrA=${formerDrA/DropFreq: /}
         #echo "formerDrA: $formerDrA"
      fi
   done
   if [ $formerDrA -lt 0 ]; then
      echo "DropFreq not found for $name-A"
      exit 1
   fi

   mapfile -t info < <(./lf_firemod.pl --mgr localhost --quiet on --action do_cmd \
      --cmd "show_endpoints $name-B")
   for L in "${info[@]}"; do
      #echo "L: $L"
      if [[ $L == *DropFreq:* ]]; then
         formerDrB=`echo $L | grep -oP 'DropFreq: (\S+)'`
         formerDrB=${formerDrB/DropFreq: /}
         #echo "formerDrB: $formerDrB"
      fi
   done
   if [ $formerDrB -lt 0 ]; then
      echo "DropFreq not found for $name-B"
      exit 1
   fi

   if [ -z "$formerDrA" -o $formerDrA -lt 0 ] ; then
      echo "Unable to read wanlink-A speed, or wanlink already paused."
      exit 1
   fi
   if [ -z "$formerDrB" -o $formerDrB -lt 0 ] ; then
      echo "Unable to read wanlink-B speed, or wanlink already paused."
      exit 1
   fi


   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-A NA NA NA NA NA 1000000" &>/dev/null

   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-B NA NA NA NA NA 1000000" &>/dev/null

   echo -n "Pausing $pause_time"
   sleep $pause_time

   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-A NA NA NA NA NA $formerDrA" &>/dev/null
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-B NA NA NA NA NA $formerDrB" &>/dev/null

   echo -n " go "
}

# provide either a number or a pair of numbers joined by a dash to
# generate a random value in that range
# select_range 1  returns 1
# select_range 1-10 returns
function select_range() {
   [ -z "$1" ] && "echo select_range wants a numeric string, bye" && exit 1

   if [[ $1 = *-* ]]; then
      echo "$(shuf -i $1 -n1)$unit"
   else
      echo "$1"
   fi
}

show_help=0
run_time=0
pause_time_sec=0
link_name=''
unit=s

while getopts "h:n:r:p:SMHD" arg; do
   #echo "ARG[$arg] OPTARG[$OPTARG]"
   case $arg in
   n) link_name=$OPTARG
      ;;
   r) run_time=$OPTARG
      ;;
   p) pause_time=$OPTARG
      ;;
   S) unit=s
      ;;
   M) unit=m
      ;;
   H) unit=h
      ;;
   D) unit=d
      ;;
   h) show_help=1
      ;;
   *)
      echo "Ignoring option $arg $OPTARG"
   esac
done

if [ -z "$link_name" -o -z "$run_time" -o -z "$pause_time_sec" ]; then
   show_help=1
fi

if [ $show_help -gt 0 ]; then
   echo "Usage: $0 -n {CX name} -r {run time} -p {pause time}"
   echo "   Use this on lanforge localhost"
   echo "   time units are assumed to be seconds, or arguments to sleep(1)"
   echo " $0 -n wanlink1 -r 10m -p 1-2s"
   echo "   or time can be set for ranges with these switches: "
   echo "   units: -S seconds, -M minutes, -H hours, -D days"
   echo "   time can be a number or a range eg 1-10"
   echo "   (units cannot be mixed if they are ranges)"
   echo " $0 -n wanlink1 -r 10-20 -p 1-2 -M"
   exit 1
fi


echo "Starting connection $link_name..."
start_cx $link_name
while true; do
   sleep $(select_range $run_time)
   pause_wl "$link_name" $(select_range $pause_time)
done
#
