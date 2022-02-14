#!/bin/bash
echo "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- "
echo "      This script will issue local arp flushes. "
echo "      Those commands cannot be issued against a remote lanforge."
echo "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- "
sleep 2
mgr=localhost
port=4001
station=wlan0
upstream=eth1
num_mvlans=200
cxlist=()
ports=($station)
saved_gc_stale_time=`cat /proc/sys/net/ipv4/neigh/default/gc_stale_time`
saved_base_reachable_time_ms=`cat /proc/sys/net/ipv4/neigh/default/base_reachable_time_ms`
trap do_sigint ABRT
trap do_sigint INT
trap do_sigint KILL
trap do_sigint PIPE
trap do_sigint QUIT
trap do_sigint SEGV
trap do_sigint TERM

function do_sigint() {
    echo -en "\nDefaulting arp timings "
    for ((i=0; i < num_mvlans; i++)); do
        mvlan="${upstream}#${i}"
        echo $saved_gc_stale_time > /proc/sys/net/ipv4/neigh/$mvlan/gc_stale_time
        echo $saved_base_reachable_time_ms > /proc/sys/net/ipv4/neigh/$mvlan/base_reachable_time_ms
        echo -n "."
    done
    echo ""
    echo -en "\nStopping connections: "
    fire_cmd stop_group udp-arp
    #for cx in "${cxlist[@]}"; do
    #    echo -n ":"
    #    fire_cmd set_cx_state default_tm $cx STOPPED >/dev/null
    #done
    echo ""
    fire_cmd clear_group udp-arp
    echo -n "Removing connections: "
    for cx in "${cxlist[@]}"; do
        echo -n "x"
        fire_cmd rm_cx default_tm $cx STOPPED >/dev/null
    done
    echo ""
    echo -n "Removing endpoints:   "
    for cx in "${cxlist[@]}"; do
        echo -n "-"
        fire_cmd rm_endp ${cx}-A STOPPED >/dev/null
        fire_cmd rm_endp ${cx}-B STOPPED >/dev/null
    done
    echo ""
    set +x
    exit 0
}

function fire_cmd() {
    ./lf_firemod.pl --mgr $mgr --mgr_port $port --quiet yes \
         --action do_cmd --cmd "$*" &>/dev/null
}
function fire_newcx() {
    local cxname=$1; shift
    local sta=$1; shift
    local eth=$1; shift
    ./lf_firemod.pl --mgr $mgr --mgr_port $port --action create_cx --quiet yes \
        --cx_name $cxname --use_ports $sta,$eth --use_speeds 11500,11500 --endp_type udp \
        &>/dev/null
}

# create new set of vlans, this will also recreate them using random mac addresses

#num_vlans=$(( $num_mvlans - 1))
set -e
if (( num_mvlans < 1 )); then
    echo "Too few vlans"
    exit 1
fi

echo -n "Removing old $num_mvlans macvlans: "
for ((i=0; i < num_mvlans; i++)); do
    mvlan="${upstream}#${i}"
    fire_cmd rm_vlan 1 1 $mvlan
    echo -n "-"
    sleep 0.03
done
sleep 1
echo " Checking for $num_mvlans old vlans:"
while (./lf_portmod.pl --mgr localhost --list_port_names | grep -q "$upstream#"); do
    sleep 1
    echo -n ","
done

echo -n "Adding $num_mvlans new macvlans:   "
for ((i=0; i < num_mvlans; i++)); do
    fire_cmd add_mvlan 1 1 $upstream 'xx:xx:xx:*:*:xx' $i
    echo -n ":"
    sleep 0.05
done
# "84033538"
for ((i=0; i < num_mvlans; i++)); do
    mvlan="${upstream}#${i}"
    fire_cmd set_port 1 1 "$mvlan" NA NA NA NA 2147483648 NA NA NA NA 75513858
    echo -n "="
    sleep 0.05
    echo 1 > /proc/sys/net/ipv4/neigh/$mvlan/gc_stale_time
    echo 1 > /proc/sys/net/ipv4/neigh/$mvlan/base_reachable_time
done
echo ""
fire_cmd add_group udp-arp
sleep 2
echo -n "Creating $num_mvlans connections:  "
for ((i=0; i < num_mvlans; i++)); do
    mvlan="${upstream}#${i}"
    fire_newcx "udp-$i" $station $mvlan
    echo -n "+"
    cxlist+=("udp-$i")
    ports+=($mvlan)
    fire_cmd add_tgcx udp-arp "udp-$i"
done

sleep 2
#for ((i=0; i < num_mvlans; i++)); do
    #echo -n "="
    #fire_cmd set_cx_state default_tm "udp-$i" RUNNING
#done
fire_cmd start_group udp-arp
sleep 2
echo ""
echo -n "Starting arp flushing: "
while : ; do
    for p in "${ports[@]}"; do
         ip neigh flush dev $p
    done
    echo -n "!"
    sleep 0.2
done
#
