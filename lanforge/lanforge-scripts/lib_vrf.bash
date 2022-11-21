#!/bin/bash

# create an associative array of vrf interfaces and their ports

IFLINES=()
declare -A IFNAMES
export IFNAMES
declare -A VRFNAMES
export VRFNAMES

while read line; do
   IFLINES+=("$line")
done < <(ip -o link show)

RE_MASTER=' master ([^ ]+) state '
for item in "${IFLINES[@]}"; do
   #echo -e "\t$item"
   [[ x$item = x ]] && continue

   IFS=': ' hunks=($item)
   [[ "${hunks[1]}" = "" ]] && continue

   ifname="${hunks[1]}"
   [[ "$ifname" = *NOARP,MASTER* ]] && continue

   IFNAMES["$ifname"]="unknown"

   if [[ $item = *master* ]] && [[ $item = *vrf* ]]; then
      #echo "Looking for vrf in $ifname"
      if [[ $item =~ $RE_MASTER ]]; then
         [[ x${BASH_REMATCH[1]} = x ]] && continue;
         vrfname=${BASH_REMATCH[1]};
         #echo "[[[$ifname]]]  [[[$vrfname]]]"
         IFNAMES["$ifname"]="$vrfname"
         VRFNAMES["$vrfname"]="$ifname"
      fi
   fi
done

if [[ x$VRF_DEBUG = x1 ]]; then
   echo "Interfaces: "
   for ifname in "${!IFNAMES[@]}"; do
      echo "IFN   $ifname => ${IFNAMES[$ifname]}"
   done

   echo "virtual routers: "
   for vrfname in "${!VRFNAMES[@]}"; do
      echo "VRF   $vrfname => ${VRFNAMES[$vrfname]}"
   done
fi
#
