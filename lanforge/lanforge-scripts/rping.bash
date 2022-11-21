#!/bin/bash

## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ##
##  Ping a random ip every second, indefinitely. The ping command
##  has a deadline of *count* seconds and wait time of 1 second.
##  This script is aware of vrf_exec.bash and LF_NO_USE_VRF.
##
##  Example Usage:
##
##  Ping a random ip once from port br0 every second:
##  ./rping.bash -p br0 -c 1
##
##  Default to eth1, ping 4 random IPs, ping each ip 10 times
##  ./rping.bash -r 4 -c 10
##
##  Ping 4 random IPs, ping each ip 10 times, from port br1
##  ./rping.bash -r 4 -c 10 -pbr1
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ##
# set -vux

HL="/home/lanforge"
HL_VX="$HL/vrf_exec.bash"
UV=1
if [ -f $HL/LF_NO_USE_VRF ]; then
    UV=0
fi
if [ ! -x $HL_VX ]; then
    UV=0
fi

usage() {
    echo "Usage: $0 [-p port] [-c count of pings per ip] [-r number random ips] [-d seconds duration]"
}

PORT=eth1
COUNT=1
NUM_IP=0
DURATION=0

while getopts "hi:c:d:p:" OPT; do
    case "${OPT}" in
        c) COUNT="${OPTARG}"
            ;;
        d) DURATION="${OPTARG}"
            if (( $DURATION < 0 )); then
                echo "$0: duration cannot be negative"
                exit 1
            fi
            ;;
        h) usage
            exit 0
            ;;
        i) NUM_IP="${OPTARG}"
            ;;
        p) PORT="${OPTARG}"
            ;;
        *) echo "Unknown option $OPT";
            usage
            exit 1
            ;;
    esac
done

if [[ x$PORT == x ]]; then
    echo "$0: no port" >&2
    return 1
fi

# this is unfiltered and will ping network numbers, broadcast numbers and
# multicast addresses, if you need a specific range, you should add that
# logic near here
rand_ip() {
    printf "%d.%d.%d.%d" \
        "$((RANDOM % 256))" \
        "$((RANDOM % 256))" \
        "$((RANDOM % 256))" \
        "$((RANDOM % 256))"
}

my_ping() {
    if [[ x$1 == x ]]; then
        echo "$0: my_ping: cannot ping empty ip" >&2
        return 1
    fi

    if (($UV == 1)); then
        $HL_VX $PORT ping -c $COUNT  -D -i1 -n -w$COUNT -W1 "$1"
    else
        ping -I$PORT -c $COUNT -D -i1 -n -w$COUNT -W1 "$1"
    fi
}

IP_LIST=()
if (( NUM_IP != 0 )); then
    for n in `seq 1 $NUM_IP`; do
        IP_LIST+=($(rand_ip))
    done
fi

counter=0;
mod=$NUM_IP
while true; do
    if (( $NUM_IP > 0 )); then
        i=$(($counter % $NUM_IP))
        randi="${IP_LIST[$i]}"
        counter=$((counter++))
    else
        randi=$(rand_ip)
    fi
    my_ping "$randi"
    sleep 1
done
#
