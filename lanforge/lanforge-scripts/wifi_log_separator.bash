#!/bin/bash

log_dir=/home/lanforge/wifi
result_dir=/home/lanforge/report-data/wifi-sta-logs

[ ! -d $result_dir ] && mkdir -p $result_dir

now=`date +%Y%m%d-%H%M%S`
cd $log_dir
ls wpa_supplicant_log_wiphy[0-24].txt > /tmp/log.list 2>/dev/null
[ $? -ne 0 ] && echo "No logs found" && exit 1

for logfile in `cat /tmp/log.list`; do
   egrep -o ' sta[0-9]+: ' "$logfile" | sort | uniq > /tmp/sta_names.txt
   [ ! -s /tmp/sta_names.txt ] && continue
   for sta in `cat /tmp/sta_names.txt` ; do
      [[ x$sta = x ]] && continue
      echo "$sta" > /tmp/pattern
      safe_name="${sta/:/}"
      fgrep -f /tmp/pattern ${logfile} > "${result_dir}/${safe_name}_${now}.txt"
   done
   xz -7 < ${logfile} > ${logfile}.${now}.xz
   echo "" > ${logfile}
done
