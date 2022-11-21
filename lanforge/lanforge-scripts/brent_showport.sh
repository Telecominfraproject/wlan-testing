#!/bin/bash

mgr="192.168.100.86"

./lf_portmod.pl --manager $mgr --load port-regression > /dev/null
sleep 10s

for x in vap0 sta0 eth1#0 eth1 eth1.1 rddVR0 br0
do
   #Test MAC
   port_output=`./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --show_port MAC`
   answer=${port_output:5}
   #  echo "MAC exists: $x $answer
   if [ -z "$answer" ]; then
      echo "Failed to find MAC address for $x."
      exit 1
   fi

   #Test port UP
   port_output=`./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --show_port Current`
   answer=${port_output:9:2}
   #  echo "DB UP: $x $answer"
   if [ $answer != "UP" ]; then
      echo "Failed, port $x is down after loading DB."
      exit 1
   fi

   #Test port UP after reset
   ./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --cmd reset > /dev/null
   sleep 2s
   port_output=`./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --show_port Current`
   answer=${port_output:9:2}
   #  echo "UP after reset: $x $answer"
   if [ $answer != "UP" ]; then
      echo "Failed, port $x is down after resetting."
      exit 1
   fi

   #Test DOWN after ifdown
   ./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --set_ifstate down
   port_output=`./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --show_port Current`
   answer=${port_output:9:4}
   #  echo "DOWN after ifdown: $x $answer"
   if [ $answer != "DOWN" ]; then
      echo "Failed, port $x is still up after ifdown."
      exit 1
   fi

   #Test UP after ifup
   ./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --set_ifstate up
   sleep 5s
   port_output=`./lf_portmod.pl --quiet 1 --manager $mgr --card 2 --port_name $x --show_port Current`
   answer=${port_output:9:2}
   #  echo "UP after ifup: $x $answer"
   if [ $answer != "UP" ]; then
      echo "Failed, port $x is still down after ifup."
      exit 1
   fi
done

echo "Test passed."
