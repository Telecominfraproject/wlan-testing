#!/bin/bash
# set -veux
q="'"
Q='"'
cxname=${1:-}
if [[ x$cxname == x ]] ; then
   echo "$0: please specify CX to start and monitor"
   exit 1
fi

quit_now=0
tagname="$cxname"
temps_flag=/tmp/monitor_temps
chart_flag=/tmp/monitor_chart
run_flag=/tmp/monitor_run
begintime=`date "+%Y-%m-%d %H:%M"`

checkon() {
   local interval=$1
   local flag=$2
   if [[ x$1 == x ]]; then
      echo "checkon: no interval, bye"
      ctrl_c
      exit 1
   fi
   if [[ x$2 == x ]]; then
      echo "checkon: no flag file name, bye"
      ctrl_c
      exit 1
   fi
   while (( interval >= 0 )); do
      sleep 1
      [ ! -f $flag ] && return
      [ ! -f $run_flag ] && return
      interval=$((interval- 1))
   done
}

countdown() {
   local left=$1
   while (( left >= 0 )); do
      if (( quit_now == 1 )) || [ ! -f $run_flag ]; then
         break
      fi
      printf "\r%d..." $left
      sleep 1
      left=$((left - 1))
   done
}

start_cx() {
   if [[ x$1 == x ]]; then
      echo "start_cx: no CX name, bye"
      ctrl_c
      exit 1
   fi
   for cx in "$@"; do
      echo "Starting $cx..."
      /home/lanforge/scripts/lf_firemod.pl --mgr localhost --quiet yes --action do_cmd --cmd \
         "set_cx_state default_tm $cx RUNNING"
   done
}

stop_cx() {
   /home/lanforge/scripts/lf_firemod.pl --mgr localhost --quiet yes --action do_cmd --cmd \
      "set_cx_state ALL ALL STOPPED"
}

ctrl_c () {
   quit_now=1
   [ ! -f $run_flag ] && return
   echo -n "cleaning up..."
   stop_cx
   rm -f $temps_flag
   rm -f $chart_flag
   rm -f $run_flag
   echo "done"
}
trap ctrl_c INT

monitor_temps() {
   if [[ x$1 == x ]]; then
      echo "monitoring_temps: no monitoring duration"
      exit 1
   fi
   echo "monitoring temps every $1"
   if [ ! -x /home/lanforge/scripts/sensorz.pl ]; then
      echo "no sensorz.pl, bye"
      ctrl_c
      exit 1
   fi
   touch $temps_flag
   while [ -f $temps_flag ] && [ -f $run_flag ]; do
      if (( quit_now == 1 )); then
         echo "monitoring_temps ending"
         break;
      fi
      /home/lanforge/scripts/sensorz.pl | logger -t "$tagname"
      checkon $1 $temps_flag
   done
   echo "done monitoring temps"
}

monitoring_chart() {
   if [[ x$1 == x ]]; then
      echo "monitoring_chart: no monitoring duration"
      ctrl_c
      exit 1
   fi
   if [ ! -x /home/lanforge/sensor_chart.bash ]; then
      echo "no sensor_chart.bash, bye"
      ctrl_c
      exit 1
   fi
   echo "charting temps every $1"
   touch $chart_flag
   while [ -f $chart_flag ] && [ -f $run_flag ]; do
      checkon $1 $chart_flag
      if (( quit_now == 1 )) || [ ! -f $run_flag ]; then
         echo "monitoring_chart ending"
         break
      fi
      echo "   sensor_chart.bash $tagname $q${begintime}$q"
      /home/lanforge/sensor_chart.bash "$tagname" "${begintime}" || {
         echo "FAILED TO GENERATE CHART"
         ctrl_c
         exit 1
      }
   done
   now=`date +%Y-%m-%d_%H.%M.%S`
   mv ~/Documents/sensordata.${tagname}.png ~/Documents/sensordata.${tagname}.${now}.png
   echo "done charting temps see `pwd`/sensordata.${tagname}.${now}.png"
}

cd ~/Documents/
# stop all existing connections
stop_cx
touch $run_flag
monitor_temps ${SENS_INTERVAL_SEC:-30} & # usually 30s
# countdown $(( 60 * 1 )) # realistic cooldown time is about 10m
countdown ${PRECOOL_SEC:-60}  # realistic cooldown time is about 10m

start_cx $@

default_chart_interval_sec=$((60 * 2))
monitoring_chart ${CHART_INTERVAL_SEC:-$default_chart_interval_sec} & # usually 2m
default_dur_sec=$(( 60 * 60 * 45 ))
countdown ${TEST_DUR_SEC:-$default_dur_sec} # usually 45m

stop_cx

echo "cooling off..."
countdown ${CHART_INTERVAL_SEC:-$default_chart_interval_sec} # needs to be as long as charting interval
echo "stopping monitoring..."
rm -f $temps_flag $chart_flag $run_flag
#countdown ${CHART_INTERVAL_SEC:-$default_chart_interval_sec} # needs to be as long as charting interval

echo done

#
