#!/bin/bash
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  wait_for_8080.bash
#
#  Use as a trigger for starting a script that connects to the GUI
#  Usage: ./wait_for_8080.bash SECONDS URL NEXT_PROGRAM
#  Example:
#   ./wait_for_8080.bash $((60 * 2)) http://localhost:8080/ "/home/lanforge/scripts/scenario.py"
#  The URL must be exact and include the http port in the URL.
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# set -vux

DEFAULT_WAIT_SECS=$(( 60 * 5 )) # 5 minutes
WAIT_SECS=${1:-$DEFAULT_WAIT_SECS}
URL=${2:-http://localhost:8080/}
NEXT_PROGRAM=${3:-}
if [[ x$WAIT_SECS = x ]] || (( $WAIT_SECS < 1 )); then
  echo "Usage: $0 SECONDS URL NEXT_PROGRAM"
  echo "The URL must be exact and include the http port in the URL."
  echo "Example:"
  echo "    $0 600 http://localhost:8080/ '/usr/bin/xterm -e top'"
  exit 1
fi

SECS_WAITED=0
CONNECTED=0
echo "Waiting up to $WAIT_SECS for $URL" | tee >( logger -t lfclient)
while (( $SECS_WAITED <= $WAIT_SECS )); do
  curl -o /dev/null -sq $URL
  if (( $? == 0 )); then
    echo "Connected to $URL in $SECS_WAITED" | tee >( logger -t lfclient)
    if [[ x$NEXT_PROGRAM == x ]]; then
      exit 0
    fi
    exec $NEXT_PROGRAM
  fi
  sleep 1
  SECS_WAITED=$(( SECS_WAITED+=1 ))
done
echo "Did not connect to $URL within $WAIT_SEC" | tee >( logger -t lfclient)
exit 1
