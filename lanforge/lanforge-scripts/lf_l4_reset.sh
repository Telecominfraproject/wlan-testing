#!/bin/bash
# This script will reset any layer 4 connection that reaches 0 Mbps over last minute.
# Run this script from the /home/lanforge/scripts directory.


# Custom variables
# Use DB to set a database to load.
# Use mgr to have this script run on another system (replace localhost with ip or hostname).
# Use rate to change how often the script checks layer 4 endpoints (default is 60s).
DB=""
mgr="localhost"
napTime="30s"
min="0"

### Should not need to change anything below this line! ###

function show_help() {
   echo "$0 -m <manager> -d <delay> -n <minimum-bps> -l <database>"
   echo "  --mgr <manager> --delay <seconds> --min <minimum-bps> --load <database>"
   echo ""
   exit
}

ARGS=`getopt -o d:l:m:n:h --long help,load:,delay:,mgr:,min: -- "$@"`

while :; do
   case "$1" in 
      -l|--load) DB="$2"; shift 2 ;;

      -d|--delay) napTime="$2"; shift 2 ;;

      -m|--mgr) mgr="$2"; shift 2 ;;

      -n|--min) min="$2"; shift 2 ;;

      --) shift; break;;

      -h|--help)
         show_help
         exit 1 ;;
      *) break;;
   esac 
done

echo -n "Options --mgr $mgr --delay $napTime --min $min"
if [[ $DB != "" ]]; then
   echo -n "--db $DB"
fi
echo ""

# Load DB (if provided above)
if [[ ! $DB = "" ]]; then
   echo -n "Loading database $DB..."
   ./lf_portmod.pl --manager $mgr --load $DB > /dev/null
   sleep 10s
   echo "...done"
fi
echo "Press Control-C to stop..."

while : ; do
   # List layer-4 cx
   l4output=`./lf_firemod.pl --mgr $mgr --cmd "show_cx" \
   | grep "type: L4_GENERIC" | awk ' ''{print $3}' | cut -d "_" -f 2- \
   | sort | uniq`
  
   # We get all the statuses we can get because that it a lot faster
   # than querying one status at a time
   allStatuses=`./lf_firemod.pl --mgr $mgr --action show_endp`

   l4list=($l4output)
   for i in "${l4list[@]}"
   do
      # if we call lf_firemod multiple times we have to wait on
      # the manager and it ends up taking longer than our dwell time
      # endp_status=`./lf_firemod.pl --mgr $mgr --action show_endp --endp_name`

      endp_status=`echo "$allStatuses" | awk "/L4Endp \[$i\]/{flag=1}/^\$/{flag=0}flag"`

      #echo '---------------------------------------'
      #echo "$endp_status"
      #echo '---------------------------------------'
      
      l4read=`echo "$endp_status"  | awk  '/Bytes Read:/ {print $8}'`
      l4write=`echo "$endp_status" | awk  '/Bytes Written:/ {print $8}'`
      runChk=`echo "$endp_status"  | grep '^L4Endp '`
      runStat=`echo "$runChk"      | sed  's/L4Endp \[.*\] (\(.*\))/\1/'`

      checkSpeed=0
      doL4Restart=0
      case "$runStat" in
      "RUNNING")
         checkSpeed=1
         ;;
      "RUNNING, ALLOW_REUSE")
         checkSpeed=1
         ;;
      "NOT_RUNNING")
         doL4Restart=1
         ;;
      "NOT_RUNNING, WAIT_RESTART")
         doL4Restart=1
         ;;
      "NOT_RUNNING, ALLOW_REUSE")
         ;;
      *)
         echo "Unknown case ${i}[$runStat]"
         ;;
      esac
      if [[ x$checkSpeed = x1 ]]; then
         #echo "l4read[$l4read] min[$min] l4write[$l4write]"
         if (( $l4read <= $min )) && (( $l4write <= $min )); then
            doL4Restart=1
         fi
      fi

      #echo "restart[${doL4Restart}]   $i   l4read[$l4read] l4write[$l4write] $runChk" 

      if (( $doL4Restart == 1 )); then
         echo "Resetting $i at `date`" 
         ./lf_firemod.pl --mgr $mgr --cmd "set_cx_state all CX_$i STOPPED" > /dev/null
         sleep 3s
         ./lf_firemod.pl --mgr $mgr --cmd "set_cx_state all CX_$i RUNNING" > /dev/null
      fi
   done

   echo -n "."
   sleep $napTime
done
