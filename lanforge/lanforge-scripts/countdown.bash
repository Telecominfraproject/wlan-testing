#!/bin/bash
ticker_time="$1"
orig_time="$1"
#echo ""
while [[ $ticker_time -gt 0 ]]; do
   sleep 1
   ticker_time=$(( $ticker_time - 1 ))
   countd=$orig_time
   printf "\r"
   for n in `seq 0 $orig_time`; do
      if [[ $n -lt $ticker_time ]]; then
         echo -n '#'
      else
         echo -n '-'
      fi
   done
   echo -n " $ticker_time/$orig_time"
done
echo ""