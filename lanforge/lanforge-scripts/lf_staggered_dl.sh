#!/bin/bash
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----  #
# This script starts a series of Layer-3 connections across a series of stations #
# each station will wait $nap seconds, download $quantity KB and then remove     #
# its old CX.                                                                    #
#                                                                                #
#  INSTALL                                                                       #
# Copy this script to to /home/lanforge/scripts/lf_staggered_dl.sh               #
# If you are copying this via DOS/Windows, follow these steps:                   #
# 1) copy using samba or pscp or winscp or whatever this script to               #
#     /home/lanforge/scripts/lf_staggered_dl.sh                                  #
# 2) in a terminal on the LANforge, run dos2unix and                             #
#     $ cd /home/lanforge/sripts                                                 #
#     $ dos2unix lf_staggered_dl.sh                                              #
# 3) make the script executable:                                                 #
#     $ chmod a+x lf_staggered_dl.sh                                             #
#                                                                                #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----  #
# . lanforge.profile
[ ! -f lf_firemod.pl ] && echo "Unable to find lf_firemod.pl." && exit 1

#set -e
q="'"
Q='"'
manager=localhost    # :m
resource=1           # :m
first_sta=           # :f
upstream=x           # :u
last_sta=x           # :l
num_sta=x            # :n
naptime=x            # :z
payload_kb=x         # :s
tx_rate=x            # :t
check_naptime=1.0    # seconds between lf_firemod check on endpoint stats
timer=1000           # report timer


function term_procs() {
   echo -en "\nCleaning up background tasks: "; 
   for pid in "${childprocs[@]}"; do
      echo -n "$pid, "
      kill -9 $pid &>/dev/null || true
   done
   echo " done"
}
trap term_procs EXIT

function usage() {
   cat <<__EOF__
${0}: starts a series of layer-3 connections and makes each start
downloading a fixed amount of data after a naptime.
   -m       # lanforge manager (defaults to localhost)
   -r       # lanforge resource (defaults to 1)
   -f       # first station/port
   -n       # number of stations/ports
   -z       # naptime before beginning download
   -u       # upstream port that will transmit
   -t       # transmit bps
   -p       # payload size in KB

Example:    # 20 stations (sta100-sta120) nap 3 seconds before downloading 200KB
   ${0} -m 192.168.1.101 -r 1 -f sta100 -n 20 -z 3 -u eth1 -p 250 -t 1500000

__EOF__
}

while getopts ":f:m:n:p:r:t:u:z:" opt; do
   case "${opt}" in
      f)
         first_sta="${OPTARG}"
         ;;
      m) 
         manager="${OPTARG}"
         ;;
      n) 
         num_sta="${OPTARG}"
         ;;
      p)
         payload_kb="${OPTARG}"
         ;;
      r)
         resource="${OPTARG}"
         ;;
      t)
         tx_rate="${OPTARG}"
         ;;
      u)
         upstream="${OPTARG}"
         ;;
      z)
         naptime="${OPTARG}"
         ;;
      *)
         usage
         exit 1
         ;;
   esac
done
shift $(( OPTIND - 1 ));

[ -z "$manager"     -o "$manager"   == x ] \
   && echo "Please specify LANforge manager ip or hostname." && usage && exit 1

[ -z "$resource"     -o "$resource"   == x ] \
   && echo "Please specify LANforge resource for stations." && usage && exit 1

[ -z "$first_sta"    -o "$first_sta"   == x ] \
   && echo "Please specify first station or port in series to download " && usage && exit 1

[ -z "$num_sta"      -o "$num_sta"     == x ] \
   && echo "Please specify number of stations to put connections on." && usage && exit 1

[ -z "$naptime"      -o "$naptime"     == x ] \
   && echo "Please specify number of seconds to wait before transmitting." && usage && exit 1

[ -z "$payload_kb"   -o "$payload_kb"  == x ] \
   && echo "Please specify kilobytes to transfer per connection." && usage && exit 1

[ -z "$upstream"     -o "$upstream"    == x ] \
   && echo "Please specify upstream port to transmit from" && usage && exit 1

[ -z "$tx_rate"      -o "$tx_rate"     == x ] \
   && echo "Please specify transmit rate in bps" && usage && exit 1

declare -a childprocs
declare -a stations
declare -a cx_names
declare -a cx_create_endp
declare -a cx_create_cx
declare -a cx_mod_endp
declare -a cx_start_cx
declare -a cx_started
declare -a cx_finished
declare -a cx_destroy_cx
declare -A map_destroy_cx

sta_pref=${first_sta//[0-9]/}
sta_start=${first_sta//[A-Za-z]/}
[ -z "$sta_pref"                       ]  && echo "Unable to determine beginning station prefix"      && exit 1
[ -z "$sta_start" -o $sta_start -lt 0  ]  && echo "Unable to determine beginning station number."     && exit 1
[ $num_sta -lt 1 ]                        && echo "Unable to deterine number of stations to create."  && exit 1

packets=$(( 1 + $(( $payload_kb * 1000 / 1460 )) ))
[ -z "$packets" -o $packets -lt 2 ]       && echo "Unable to calculate packets for transfer."         && exit 1
# 111 is a trick number that we'll truncate to three digits later

expon=`echo "111 * 10^${#sta_start}" | bc -l`
counter=$(( expon + $sta_start ))
limit=$(( expon + $sta_start + $num_sta -1 ))
for i in `seq $counter $limit` ; do
   stations+=("${sta_pref}${counter#111}")
   cx_names+=("c-${upstream}-${sta_pref}${counter#111}");
   counter=$(( counter + 1 ))
done
_act="./lf_firemod.pl --mgr $manager --resource $resource --quiet yes --action"
_cmd="./lf_firemod.pl --mgr $manager --resource $resource --quiet yes --cmd"
counter=0
for cx in "${cx_names[@]}"; do
   cx_create_endp+=("$_act create_endp --endp_name ${cx}-A --speed $tx_rate --endp_type lf_tcp --port_name ${upstream} --report_timer $timer")
   cx_create_endp+=("sleep 0.1")
   cx_create_endp+=("$_act create_endp --endp_name ${cx}-B --speed 0 --endp_type lf_tcp --port_name ${stations[$counter]} --report_timer $timer")
   cx_create_endp+=("sleep 0.1")

   cx_create_cx+=("$_act create_cx --cx_name ${cx} --cx_endps ${cx}-A,${cx}-B --report_timer $timer")
   cx_create_cx+=("sleep 0.2")

   cx_mod_endp+=("${cx}-A NA NA NA ${packets}")

   nap=$(( $naptime * $counter ))

   cx_start_cx+=("sleep $nap; $_cmd ${Q}set_cx_state all ${cx} RUNNING${Q} &>/dev/null")

   cx_destroy_cx+=("$_act delete_cx --cx_name ${cx}")
   cx_destroy_cx+=("sleep 0.1")
   cx_destroy_cx+=("$_act delete_endp --endp_name ${cx}-A")
   cx_destroy_cx+=("$_act delete_endp --endp_name ${cx}-B")
   cx_destroy_cx+=("sleep 0.1")

   map_destroy_cx[${cx}]="$_act delete_cx --cx_name ${cx}; sleep 0.1; $_act delete_endp --endp_name ${cx}-A; $_act delete_endp --endp_name ${cx}-B";
   counter=$(( counter + 1 ))
done
echo -n "Removing previous connections..."
for command in "${cx_destroy_cx[@]}" ; do
   $command
done
sleep 1

echo "done"

echo -n "Creating new endpoints..."
for command in "${cx_create_endp[@]}" ; do
   $command
done
echo "done"

echo -n "Creating new cross connects..."
sleep $(( 2 + $(( $counter /2 )) ))
for command in "${cx_create_cx[@]}" ; do
   $command
done
./lf_firemod.pl --mgr $manager --quiet yes --cmd "nc_show_endp all" >  /tmp/ep_count.txt
echo "done"

echo -n "Configuring payload sizes..."
outf="/tmp/cmd.$$.txt"
for command in "${cx_mod_endp[@]}" ; do
   result=1
   rm -f $outf
   while [ $result -ne 0 ]; do
      ep=${command%% *}
      #$_cmd "nc_show_endp $ep"
      $_cmd "set_endp_details $command" > $outf
      result=$(awk '/RSLT:/{print $2}' $outf)
      if [ $result -ne 0 ]; then
         cat $outf
         sleep 5
      fi
   done
   #sleep 0.1
done
echo "done"

echo -n "Starting staggered transmissions..."
sleep $(( 2 + $(( $counter /2 )) ))
for command in "${cx_start_cx[@]}" ; do
   bash -c "$command" &
   childprocs+=($!)
   sleep 0.1
done
echo "done"

echo "Monitoring staggered downloads for ports:"
echo -e "\t${cx_names[@]}"
echo "_R_unning _Q_uiesce _N_ot Running (Tx Packets/Requested Packets)"
echo "--------------------------------------------------------------"
counter=1
while [ $counter -ne 0 ]; do
   messages=()
   #echo -en ""
   for cx in "${cx_names[@]}"; do
      while read L ; do
         endp_report+=("$L")
      done < <($_act show_endp --endp_name ${cx}-A)

      state="?"
      for i in `seq 0 $((${#endp_report[@]}-1))`; do
         ine="${endp_report[$i]}";
         h=($ine);
         case "${ine}" in 
            "Endpoint "*)
               state="${h[2]:1:-1}"
               ;;
            "Tx Pkts: "*)
               txpkts="${h[3]}";
               ;;
         esac
      done
      
      if [[ " ${cx_started[@]} " =~ " ${cx} " ]]; then # can inspect for finishing
         if [[ ! " ${cx_finished[@]} " =~ " ${cx} " ]]; then
            if [ ${txpkts} -ge ${packets} -a ${state} = "NOT_RUNNING" ] ; then
               cx_finished+=(${cx})
               messages+=("$cx: finished running")
               cmd=${map_destroy_cx[${cx}]};
               #messages+=(" CMD[ $cmd ]");
               bash -c "$cmd"
               cx_started=(${cx_started[@]/$cx})
            fi
         fi
      elif [[ " ${cx_finished[@]} " =~ " ${cx} " ]]; then
         :
      else
         if [ ${txpkts} -gt 0 ]; then
            messages+=("$cx: started running")
            cx_started+=(${cx})
         fi
      fi
      case $state in 
         "RUNNING")        st="R";;
         "NOT_RUNNING")    st="N";;
         "QUIESCE")        st="Q";;
         *)
      esac
      echo -en "${cx}: ${st} ${txpkts}/${packets} "
   done
   echo ""
   for m in "${messages[@]}"; do
      echo -e "\t${m}"
   done
 
   # compare the number of finished stations to total number of stations
   [ ${#cx_finished[@]} -eq ${#cx_names[@]} ] && break;
  
   sleep $check_naptime
done
echo "Waiting for background jobs to finish..."
wait

#eof
