#!/bin/bash

# Example script that creates and starts some multicast endpoints using
# the lf_firemod.pl script.  Lots of hard-coded variables in this
# file that could become command-line switches, or could be re-implemented
# in perl or some other favorite scripting language.

xmit_count=200
rcv_count=100  # Could create more of these and only start a subset

lf_mgr=192.168.100.212
resource=3
quiet=no
report_timer=1000

# Create and start transmitters
for ((i=0; i<$xmit_count; i+=1))
do
  port_num=$((10000 + i))
  # Creat transmitter endpoint
  ./lf_firemod.pl --action create_endp --endp_name mcast_xmit_$i --speed 154000 --endp_type mc_udp --mcast_addr 224.9.9.$i --mcast_port $port_num --rcv_mcast NO --port_name eth1 --min_pkt_sz 1472 --max_pkt_sz 1472 --use_csums NO --ttl 32 --mgr $lf_mgr --resource $resource --quiet $quiet --report_timer $report_timer

  # Start transmitter
  ./lf_firemod.pl --endp_name mcast_xmit_$i --action start_endp --mgr $lf_mgr
done

# Create and start receivers.
for ((i=0; i<$rcv_count; i+=1))
do
  port_num=$((10000 + i))
  ./lf_firemod.pl --action create_endp --endp_name mcast_rcv_$i --speed 0 --endp_type mc_udp --mcast_addr 224.9.9.$i --mcast_port $port_num --rcv_mcast YES --port_name sta2 --use_csums NO --mgr $lf_mgr --resource $resource --quiet $quiet --report_timer $report_timer

  # Start receiver
  ./lf_firemod.pl --endp_name mcast_rcv_$i --action start_endp --mgr $lf_mgr
done


# Script could then randomly start and stop the receivers
# to cause multicast join and leave messages.
