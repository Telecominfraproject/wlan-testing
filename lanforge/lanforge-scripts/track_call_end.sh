#!/bin/bash
#
#------------------------------------------------------------
# Use this script to track traffic on a voip call and end it 
# if the call does not connect.
#------------------------------------------------------------

RtpPktsTx="RTP Pkts Tx"
RtpPktsRx="RTP Pkts Rx"
declare -A call_states=([ON_HOOK]=0 
   [REQUESTED_START_CALL]=1 
   [CALL_STARTUP_IN_PROGRESS]=2 
   [CALL_REMOTE_RINGING]=3
   [CALL_IN_PROGRESS]=4)
   
declare -A highest_call_state=()

# pass this the file name
function study_call() {
   [ ! -r "$1" ] && echo "Unable to find Endpoint record: $1" && exit 1
   local call_state="unknown"
   local actual_state="unknown"
   local running_for=0
   local idx=0
   local line
   if [[ $endp = *-B ]]; then
      idx=1
   fi

   while IFS= read -r line ; do
      local chunks
      local shunks=($line)
      IFS=: read -r -a chunks <<< "$line"
      #for h in "${hunks[@]}"; do 
      #   echo -n "$h,"
      #done
      #echo ""
      local lasthunk="${line:63}"
      local lr=($lasthunk)
      local fields=($(echo "${line:34:+12}") "${lr[0]}" "${lr[1]}")

      first=`echo ${chunks[0]}`;
      #echo "first[$first]"
      case $first in
         RegisterState)
            call_state=${shunks[3]}
            #echo "call_state ${call_state} = ${call_states[$call_state]}"
            ;;
         RptTimer)
            running_for=${shunks[3]}
            running_for=${running_for:0:-1} # chop 's' off 
            ;;
      esac
   done < "$1"
   # this is a work around for voip cli bugs in 5.3.7
   if [[ $call_state = ON_HOOK ]]; then
      actual_state=$call_state
   elif [[ $running_for -gt 65535 ]]; then
      actual_state="ON_HOOK"
   elif [[ $running_for -le 65535 ]]; then
      actual_state=$call_state
   fi
   if [[ ${call_states[$actual_state]} -gt ${highest_call_state[$endp]} ]]; then
      highest_call_state[$endp]=${call_states[$actual_state]}
      [[ $verbose -eq 1 ]] && echo -n "$actual_state "
   fi
} # ~study_call

function usage() {
   echo "$0 -m {manager} -r {resource} -c {CX name} -a {sec} -b {sec} -s -t -u -v"
   echo "   -a <sec> # disconnect A-side after this many seconds"
   echo "   -b <sec> # disconnect B-side after this many seconds"
   echo "   -s # start the connection"
   echo "   -t # stop the cx before starting connection"
   echo "   -u # stop cx upon successfull call"
   echo "   -v # verbose"
   echo "   -h # help"
}

poll_sec=0.25
start=0
stop=0
end_cx=0
verbose=0
disconnect_a=120
disconnect_b=2

while getopts "a:b:c:hm:r:stuv" arg; do
   #echo "ARG[$arg] OPTARG[$OPTARG]"
   case $arg in
   a)
      disconnect_a=$OPTARG
      ;;
   b)
      disconnect_b=$OPTARG
      ;;
   c)
      cx_name=$OPTARG
      ;;
   h)
      usage
      exit 0;;
   m)
      mgr=$OPTARG
      ;;
   r)
      resource=$OPTARG
      ;;
   s)
      start=1
      ;;
   t)
      stop=1
      ;;
   u)
      end_cx=1
      ;;
   v)
      verbose=1
      ;;
   *)
      echo "Ignoring option [$arg]($OPTARG)"
      ;;
   esac
done

[ -z "$mgr" ] && usage && exit 1
[ -z "$resource" ] && usage && exit 1
[ -z "$cx_name" ] && usage && exit 1
[ -z "$disconnect_a" ] && usage && exit 1
[ -z "$disconnect_b" ] && usage && exit 1

cd /home/lanforge/scripts
m="--mgr $mgr"
q="--quiet yes"
r="--resource $resource"

fire=$( echo ./lf_firemod.pl $m $q $r )
# find endpoint name
$fire --action list_endp > /tmp/list_endp.$$

# example:
# ./lf_firemod.pl --mgr idtest --quiet yes --action list_endp | grep VoipEndp \
# | while read -r line ; do hunks=($line); echo "${hunks[1]}"; done
#   [v3v2-30000-B]
#   [v3v2-30000-A]
start_sec=`date +%s`
declare -A results_tx
declare -A results_rx
declare -A results_attempted
declare -A results_completed

declare -A cx_names=()
voip_endp_names=()
while IFS= read -r line ; do
   jhunks=($line)
   [[ "${jhunks[0]}" != "VoipEndp" ]] && continue
   name=${jhunks[1]:1:-1} # that trims the brackets
   [[ $name != ${3}-* ]] && continue
   voip_endp_names+=($name)
   cx_n="${name%-[AB]}"
   [[ -z "${cx_names[$cx_n]+unset}" ]] && cx_names+=(["$cx_name"]=1)
done < /tmp/list_endp.$$

if [ $stop -eq 1 ]; then
   [[ $verbose -eq 1 ]] && echo -n "Stopping ${cx_name}..."
   $fire --action do_cmd --cmd "set_cx_state all '${cx_name}' STOPPED"  &>/dev/null
   sleep 3
   [[ $verbose -eq 1 ]] && echo "done"
fi

if [ $start -eq 1 ]; then
   [[ $verbose -eq 1 ]] && echo -n "Starting ${cx_name}..."
   $fire --action do_cmd --cmd "set_cx_state all '${cx_name}' RUNNING"  &>/dev/null
   [[ $verbose -eq 1 ]] && echo "done"
fi

##
## Wait for A side to connect
##
duration=$(( `date +"%s"` + $disconnect_a ))
endp="${cx_name}-A"
[[ $verbose -eq 1 ]] && echo -n "Endpoint $endp..."
highest_call_state[$endp]=0
while [[ `date +"%s"` -le $duration ]]; do
   $fire --action show_endp --endp_name $endp > /tmp/endp_$$
   study_call /tmp/endp_$$
   rm -f /tmp/endp_$$
   
   [[ $verbose -eq 1 ]] && echo -n "(${highest_call_state[$endp]}) "
   if [[ ${highest_call_state[$endp]} -ge ${call_states[CALL_IN_PROGRESS]} ]]; then
      echo "$endp connected"
      break;
   fi
   sleep $poll_sec
done

##
## Wait for B side to connect
##
duration=$(( `date +"%s"` + $disconnect_b ))
endp="${cx_name}-B"
highest_call_state[$endp]=0
[[ $verbose -eq 1 ]] && echo -n "Endpoint $endp..."
while [[ `date +"%s"` -le $duration ]]; do
   $fire --action show_endp --endp_name $endp > /tmp/endp_$$
   study_call /tmp/endp_$$
   rm -f /tmp/endp_$$
   [[ $verbose -eq 1 ]] && echo -n "(${highest_call_state[$endp]}) "
   if [[ ${highest_call_state[$endp]} -ge ${call_states[CALL_IN_PROGRESS]} ]]; then
      echo "$endp connected"
      break;
   fi
   sleep $poll_sec
done

if [[ ${highest_call_state[$endp]} -lt ${call_states[CALL_IN_PROGRESS]} ]]; then
   echo -n "call not connected, cancelling..."
   $fire --action do_cmd --cmd "set_cx_state all '${cx_name}' STOPPED" &>/dev/null
   echo "done"
elif [[ $end_cx -eq 1 ]]; then
   echo -n "ending connected call..."
   $fire --action do_cmd --cmd "set_cx_state all '${cx_name}' STOPPED" &>/dev/null
   echo "done"
fi
stop_sec=`date +%s`
delta=$(( $stop_sec - $start_sec ))
[[ $verbose -eq 1 ]] && echo "Test duration: $delta seconds"

# eof
