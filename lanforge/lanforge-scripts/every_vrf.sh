#!/bin/bash

[[ $# < 2 ]] && {
  echo "Usage: $0 'a command' eth1 eth2 sta2 st3"
  echo "Runs 'a command' in a vrf environment for all following stations"
  exit 1
}

[[ -f lib_vrf.bash ]] || {
  echo "missing lib_vrf.bash, cannot continue"
  exit 1
}
. lib_vrf.bash

execthis="$1"
shift

for eth in "$@"; do
  [[ $execthis = $eth ]] && continue
  vrf=${IFNAMES[$eth]}
  if [[ x$vrf = x ]] || [[ $vrf = unknown ]]; then
    echo "Skipping interface $eth"
    continue
  fi
  echo "[$execthis] $vrf"
  ip vrf exec $vrf $execthis &
done
