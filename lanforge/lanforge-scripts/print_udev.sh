#!/bin/bash

li_show_lines=$(ip -o li show)

while read line ; do
   #echo "* $line"
   line=${line#*: }
   ifname=''
   mac=''
   case $line in
      eth* | enp* | wlan*)
         #echo "LIKE: $line"
         hunks=($line);
         ifname="${hunks[0]}"
         ifname="${ifname%:*}"
         #echo "N: ${#hunks[@]}"
         for i in `seq 1 ${#hunks[@]}`; do
            #echo  "$i ${hunks[$i]}"
            if [ ! -z "${hunks[$i]}" -a "${hunks[$i]}" = "link/ether" ]; then
               mac="${hunks[ $[ $i + 1] ]}"
               break;
            fi
         done
         #echo "Hi! $ifname has [$mac]"
         echo 'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="'$mac'", ATTR{dev_id}=="0x0", ATTR{type}=="1", NAME="'$ifname'" ENV{NM_UNMANAGED}="1"'
         ;;
      *)
         #echo "IGNORING: $line"
         ;;
   esac
done <<< "$li_show_lines"
