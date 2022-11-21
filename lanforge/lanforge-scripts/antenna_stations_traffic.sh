#!/bin/bash
. ~lanforge/lanforge.profile

# We can set channel and number of antennas when creating one station or many stations
# Example 1
./lf_associate_ap.pl --mgr idtest \
  --resource 7 \
  --action add \
  --radio wiphy0 \
  --antenna ALL \
  --channel 153 \
  --first_ip DHCP \
  --num_sta 5 \
  --ssid hedtest-wpa2-153 \
  --security wpa2 \
  --passphrase hedtest-wpa2-153


# Example 2
# we can also start traffic with this example
# create layer 3 connections between those stations and upstream bridge port
# action step1 make the layer 3 connections and runs them for duration
./lf_associate_ap.pl --mgr idtest \
  --resource 7 \
  --radio wiphy0 \
  --antenna ALL \
  --channel 153 \
  --first_ip DHCP \
  --num_sta 5 \
  --ssid hedtest-wpa2-153 \
  --security wpa2 \
  --passphrase hedtest-wpa2-153 \
  --duration 5min \
  --upstream br0 \
  --bps_min 1000000 \
  --cxtype tcp \
  --poll_time 5 \
  --action step1

# Example 3
# if we wanted to create the connections independently, we can do it like this:
pkt_size=720
for n in `seq 100 105`; do
  station="sta$n"
  endpa="tcp$n-A"
  endpb="tcp$n-B"
  cxname="tcp$n"

  ./lf_firemod.pl --mgr idtest --resource 7 --action create_endp --endp_type lf_tcp \
      --endp_name "$endpa" --port_name "br0" --speed 1000000 --min_pkt_sz $pkt_size

  ./lf_firemod.pl --mgr idtest --resource 7 --action create_endp --endp_type lf_tcp \
      --endp_name "$endpb" --port_name "sta$n" --speed 1000000 --min_pkt_sz $pkt_size

  ./lf_firemod.pl --mgr idtest --resource 7 --action create_cx --cx_name $cxname --cx_endps $endpa,$endpb
done

for n in  `seq 100 105`; do
  cxname="tcp$n"
  ./lf_firemod.pl --mgr idtest --resource 7 --action do_cmd --cli_cmd "set_cx_state all $cxname RUNNING"
done

# poll every two seconds
for i in `seq 1 $((5 * 30))` ; do
  for n in  `seq 100 105`; do
    ./lf_firemod.pl --mgr idtest --resource 7 --action show_endp --endp_name "tcp$n-A" --endp_vals rx_bps
    ./lf_firemod.pl --mgr idtest --resource 7 --action show_endp --endp_name "tcp$n-B" --endp_vals rx_bps
  done
  sleep 2
done

for n in  `seq 100 105`; do
  cxname="tcp$1"
  ./lf_firemod.pl --mgr idtest --resource 7 --action do_cmd --cli_cmd "set_cx_state all $cxname QUIESCE"
done

# print out all connections:
for n in  `seq 100 105`; do
  ./lf_firemod.pl --mgr idtest --resource 7 --action show_cx --endp_name "tcp$n" --endp_vals rx_bps
done



