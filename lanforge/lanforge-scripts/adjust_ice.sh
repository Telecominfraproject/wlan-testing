#!/bin/bash
#
# adjust_ice.sh
#
# This script takes a csv data file with downlink, uplink and rtt values
# and uses the values to adjust an existing running wanlink.
#
# Each value is checked against the committed information rate (CIR) limits
# and when the limit is exceeded a shuffled value is chosen between a default
# min and max.
#
# Inputs are:
# csv filename
# name of wanlink
# run time between value changes

cd /home/lanforge/scripts

file=$1
name=$2
run_time=$3


print_help() {
   echo "Usage: $0 {csv filename} {wanlink name} {run time}"
   echo "   Use this on lanforge localhost"
   echo "   Run time units are seconds"
   echo " $0 values.csv wanlink-01 60"
   echo ""
}

if [ $# -eq 0 ]; then
   print_help
   exit 1
fi
slices=10
cir_dn=3500000
cir_up=2000000
min=20000
max=200000
dates=()
downlink=()
uplink=()
delay=()
declare -A months
months=([Jan]=1 [Feb]=2 [Mar]=3 [Apr]=4 [May]=5 [Jun]=6 [Jul]=7 [Aug]=8 [Sep]=9 [Oct]=10 [Nov]=11 [Dec]=12)

# expects a "d-m-y hours:minutes meridian" format
function date_to_ts() {
   local year
   local hourmin
   local meridian
   [ -z "$1" ] && echo "date_to_ts: wants \$1 date string" && exit 1
   local hunks=($1);
   local datehunks=()

   IFS=- read -r -a datehunks < <(echo "${hunks[0]}")
   
   local month=${datehunks[1]}
   local monthno=${months[$month]}

   #echo "${monthno}/${datehunks[0]}/${datehunks[2]} ${hunks[1]} ${hunks[2]}"
   date --date "${monthno}/${datehunks[0]}/${datehunks[2]} ${hunks[1]} ${hunks[2]}" +"%s"
}

function get_values() {
   while read -r line
   do
       if [[ $line != "" ]]; then
         if [[ $line == *DATE* ]]; then
           continue;
         fi
         if [[ $line != *-* ]]; then
           continue;
         fi

         local datestr=`echo $line |cut -d '"' -f1 |sed 's/,/ /g'`
         local timest=$(date_to_ts "$datestr")
         dates+=($timest)
         local dl=`echo $line |cut -d '"' -f2 |sed 's/,//g'`
         if [[ $dl < $cir_dn ]]; then
           let dl=$(( $cir_dn - $dl ))
           downlink+=( $dl )
         else
           let bas=$(shuf -i "$min-$max" -n1)
           downlink+=( $bas )
         fi

         local ul=`echo $line |cut -d '"' -f6 |sed 's/,//g'`
         if [[ $ul < $cir_up ]]; then
           let ul=$(( $cir_up - $ul ))
           uplink+=( $ul )
         else
           let bas=$(shuf -i "$min-$max" -n1)
           uplink+=( $bas )
         fi

         local lat=`echo $line |cut -d '"' -f9 |sed 's/,//g' |cut -d '.' -f1`
         let lat=$(( $lat/2 ))
         delay+=( $lat )

       fi
   done < $file
}


function modify_values {
   [ -z "$1" ] && echo "modify_values wants row index \$1, bye" && exit 1
   local row_idx=$1
   local dl_now=0
   local ul_now=0
   local lt_now=0
   local ts_now=${dates[$row_idx]}
   local ts_next=${dates[ $(( $row_idx +1 )) ]}
   local delta=$(( $ts_next - $ts_now ))
   local pause=$(( $delta / $slices ))
   #echo "now: $ts_now, next: $ts_next, delta: $delta pause: $pause"
   local downlink_now="${downlink[$row_idx]}"
   local downlink_next="${downlink[ $(( $row_idx +1 )) ]}"
   local downlink_delta=$(( $downlink_next - $downlink_now ))
   local uplink_now="${uplink[$row_idx]}"
   local uplink_next="${uplink[ $(( $row_idx +1 )) ]}"
   local uplink_delta=$(( $uplink_next - $uplink_now ))
   local delay_now="${delay[ $row_idx ]}"
   local delay_next="${delay[ $(( $row_idx +1 )) ]}"
   local delay_delta=$(( $delay_next - $delay_now ))
   local dl_series=()
   local ul_series=()
   local delay_series=()
   local j;

   #echo "Deltas: $downlink_delta $uplink_delta $delay_delta"
   echo "Now:    $downlink_now $uplink_now $delay_now"
   for ((j=1; j < $slices; ++j)); do 
      
      local d_j=$(( $downlink_delta / $slices ))
      local u_j=$(( $uplink_delta / $slices ))
      local l_j=$(( $delay_delta / $slices ))
      
      local d_a=$d_j
      local u_a=$u_j

      if [[ $l_j != 0 ]]; then
        local l_a=$l_j
      else
        local l_a=1
      fi
      
      [[ $d_j -lt 0 ]] && d_a=$(( -1 * $d_j ))
      [[ $u_j -lt 0 ]] && u_a=$(( -1 * $u_j ))
      [[ $l_j -lt 0 ]] && l_a=$(( -1 * $l_j ))
      local d_i=$(( ($j * $d_j) + `shuf -i 1-$d_a -n1` ))
      local u_i=$(( ($j * $u_j) + `shuf -i 1-$u_a -n1` ))
      local l_i=$(( ($j * $l_j) + `shuf -i 1-$l_a -n1` ))
      #echo "$j:     $d_i $u_i $l_i"
      echo "$j:      $(($downlink_now + $d_i)) $(($uplink_now + $u_i)) $(($delay_now + $l_i))"
      dl_series+=( $(($downlink_now + $d_i)) )
      ul_series+=( $(($uplink_now + $u_i)) )
      delay_series+=( $(($delay_now + $l_i)) )
   done
   echo "Next:   $downlink_next $uplink_next $delay_next"
   
   for ((j=0; j < 9; ++j)); do 
   
      dl_now=${dl_series[$j]}
      ul_now=${ul_series[$j]}
      lt_now=${delay_series[$j]}

      echo "set wanlink $name: $dl_now $ul_now $lt_now"
      echo "set wanlink $name-A: Downlink $dl_now, Delay $lt_now"
      ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
         "set_wanlink_info $name-A $dl_now $lt_now NA NA NA NA" &>/dev/null
      echo "set wanlink $name-B: Uplink $ul_now, Delay $lt_now"
      ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
         "set_wanlink_info $name-B $ul_now $lt_now NA NA NA NA" &>/dev/null

      echo "B-LOOP Waiting for $pause seconds."
      sleep $pause
   done
}


get_values

stop_at="$(( ${#downlink[@]} - 1 ))"

for ((i=0; i < $stop_at; ++i)); do
   
   #echo "set wanlink $name: ${downlink[i]} ${uplink[i]} ${delay[i]}"
   echo "set wanlink $name-A: Downlink ${downlink[i]}, Delay ${delay[i]}"
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-A ${downlink[i]} ${delay[i]} NA NA NA NA" &>/dev/null
   echo "set wanlink $name-B: Uplink ${uplink[i]}, Delay ${delay[i]}"
   ./lf_firemod.pl --mgr localhost --quiet on --action do_cmd --cmd \
      "set_wanlink_info $name-B ${uplink[i]} ${delay[i]} NA NA NA NA" &>/dev/null

   echo "A-LOOP Waiting for $run_time seconds."
   sleep $run_time

   [[ $i -ge $stop_at ]] && break
   modify_values $i
done

