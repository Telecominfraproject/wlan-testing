#!/bin/bash
#set -x
set -e
if [ -z "$1" ]; then
   lic_file="/home/lanforge/license.txt"
else
   lic_file="$1"
fi
if [ ! -f "$lic_file" ]; then
   echo "File not found [$lic_file]"
   exit 1
fi
declare -a lic_lines
IFS=$'\n' lic_lines=(`cat $lic_file`)

if [[ ${#lic_lines[@]} -lt 2 ]]; then
   echo "Nothing found in [$lic_file]"
   exit 1
fi
NOW=`date +%s`
num_expired=0
for line in "${lic_lines[@]}"; do
   [[ "$line" = "" ]] && continue;
   IFS=$' ' hunks=($line)
   lastbit=${hunks[4]}
   [[ "$lastbit" = "" ]] && echo "Unable to determine timecode for ${hunks[0]}" && continue
   delta=$(( $lastbit  - $NOW ))
   if [[ $delta -lt 86200 ]] && [[ $delta -gt 0 ]] ; then
      echo "${hunks[0]} expires today!"
   elif [[ $delta -le 0 ]]; then
      echo "${hunks[0]} expired"
      ((num_expired++)) || true
   fi
done
exit $num_expired
#
