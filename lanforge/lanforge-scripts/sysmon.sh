#!/bin/bash

# grabs netdev stats and timestamp every second or so, saves
# to logfile.

# Usage:
#
# Monitor every 60 seconds
# ./sysmon.sh 60
#
# Monitor every 5 seconds (default)
# ./sysmon.sh

USAGE="Usage: sysmon.sh [ -s sleep_time ] [ -p ] [ -h ]\n
  -p means show port stats\n
  -s specifies sleep-time between reports.\n
  -h  Show help and exit.\n
"

log="/home/lanforge/sysmon.log"
sleep_time=5
show_port_stats=0

while getopts "s:hp" opt; do
    case "$opt" in
	s)
	  sleep_time=${OPTARG}
	  ;;
        h)
	  echo -e $USAGE
	  exit 0
	  ;;
        p)
	  show_port_stats=1
	  ;;
	*)
	  echo -e $USAGE
	  exit 1
	  ;;
    esac
done

# Reset arguments to $1, $2, etc.
shift $((OPTIND - 1))

echo "Starting sysmon.sh script, sleep-time: $sleep_time."
if [ $show_port_stats == "1" ]
    then
    echo "Gathering interface stats."
else
    echo "NOT gathering interface stats."
fi

echo "Starting sysmon.sh script." > $log;

while true
  do
  echo "Logging system stats to $log..."
  date
  date +"%Y-%m-%d %H:%M:%S" >> $log
  # netdev link stats.
  if [ $show_port_stats == "1" ]
      then
      echo "Link stats:" >> $log
      ip -s link show >> $log
  fi
  date +"%Y-%m-%d %H:%M:%S" >> $log
  echo "Process Listing: " >> $log
  COLUMNS=512 LINES=15000 top -b -n 1 -w512 -c >> $log 2>/dev/null
  echo "Memory Info: " >> $log
  cat /proc/meminfo >> $log
  echo "Disk-Free Info: " >> $log
  df >> $log
  # Show free-memory on console.  Can direct to /dev/null if
  # user does not want to see this.
  grep MemFree /proc/meminfo
  date +"%Y-%m-%d %H:%M:%S" >> $log
  echo "" >> $log
  sleep $sleep_time
done
