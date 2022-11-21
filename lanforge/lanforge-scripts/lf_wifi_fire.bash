#!/bin/bash

#  This script is an attempt to simplify the creation of stations and connections for said stations.
#  One UDP connection will be created for each station.
#  The number of stations, station SSID, encryption type and passphrase, number of packets to send, and transmit rates
#  can all be configured with the below options.
#  Required values are SSID, radio, and upstream port.
#  Note: The upstream port will be designated to Endpoint A and station to Endpoint B.
#  -m   Manager IP or hostname.
#  -r   Resource number.
#  -w   Which radio to use i.e. wiphy0 wiphy1 etc.
#  -n   Number of stations to create.
#  -s   SSID for stations.
#  -e   Encryption type: open|wep|wpa|wpa2.
#  -k   Passphrase for when AP is encrypted.
#  -a   The upstream port to which station(s) will connect.
#  -A   Transmit rate from upstream port.
#  -B   Transmit rate from station.
#  -p   Number of default UDP sized packets to send.
#  -h   Help information.

#  Example usage:
#  ./lf_wifi_fire.bash -m lf0350-1234 -r 1 -w wiphy0 -n 40 -s test-SSID -e wpa2 -k hello123 -a eth1 -A 56000 -B 2000000 -p 10000

set -e
#set -u
set -o pipefail

clilog="--log_cli /tmp/clilog.txt"

#default values
mgr=localhost
resource=1
num_stas=40
num_packets=Infinite
encryption=open
passphrase='[BLANK]'
rate_A=1000000
rate_B=1000000

#other variables
first_sta=100
flag_radio=false
flag_ssid=false
flag_port=false

show_help="This script is an attempt to simplify the creation of stations and connections for said stations.
One UDP connection will be created for each station.
The number of stations, station SSID, encryption type and passphrase, number of packets to send, and transmit rates
can all be configured with the below options.
Required values are SSID, radio, and upstream port.
Note: The upstream port will be designated to Endpoint A and station to Endpoint B.
-m   Manager IP or hostname.
-r   Resource number.
-w   Which radio to use i.e. wiphy0 wiphy1 etc.
-n   Number of stations to create.
-s   SSID for stations.
-e   Encryption type: open|wep|wpa|wpa2.
-k   Passphrase for when AP is encrypted.
-a   The upstream port to which station(s) will connect.
-A   Transmit rate from upstream port.
-B   Transmit rate from station.
-p   Number of default UDP sized packets to send.
-h   Help information.

Example usage:
./lf_wifi_fire.bash -m lf0350-1234 -r 1 -w wiphy0 -n 40 -s test-SSID -e wpa2 -k hello123 -a eth1 -A 56000 -B 2000000 -p 10000"

while getopts 'm:r:n:p:a:e:k:w:s:A:B:h' OPTION; do
   case "$OPTION" in
      m)
        #manager
        mgr="$OPTARG"
        ;;
      r)
        #resource
        resource="$OPTARG"
        ;;
      n)
        #num stations
        num_stas="$OPTARG"
        ;;
      p)
        #packets
        num_packets="$OPTARG"
        ;;
      a)
        #upstream port
        flag_port=true
        port_A="$OPTARG"
        ;;
      e)
        #encryption
        encryption="$OPTARG"
        ;;
      k)
        #encryption passphrase
        passphrase="$OPTARG"
        ;;
      w)
        #radio
        flag_radio=true
        radio="$OPTARG"
        ;;
      s)
        #ssid
        flag_ssid=true
        ssid="$OPTARG"
        ;;
      A)
        #transmit rate for endpoint A
        rate_A="$OPTARG"
        ;;
      B)
        #transmit rate for endpoint B
        rate_B="$OPTARG"
        ;;
      h)
        #send help message
        echo "$show_help"
        exit 1
        ;;
esac
done
shift "$(($OPTIND -1))"

#check for required getopts
if [ "$flag_ssid" = false ] || [ "$flag_radio" = false ] || [ "$flag_port" = false ] ;
then
   echo "Please provide at minimum the upstream port (-a), ssid (-s), and radio (-w). Run the script with -h for more information."
   exit 1
fi

echo "Deleting old stations."
./lf_associate_ap.pl --mgr $mgr --resource $resource $clilog --action del_all_phy --port_del $radio

./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes --action do_cmd $clilog \
 --cmd "nc_show_ports 1 $resource all 1" &>/dev/null

sleep 2

echo "Creating new stations."
./lf_associate_ap.pl --mgr $mgr --resource $resource $clilog \
 --ssid $ssid --security $encryption --passphrase $passphrase \
 --num_stations $num_stas --first_sta "sta$first_sta" \
 --first_ip DHCP --radio $radio --action add

sleep 2

function new_cx(){
   local cx=$1
   local portA=$2
   local portB=$3

   ./lf_firemod.pl --mgr $mgr --resource $resource $clilog \
    --action create_endp --endp_name "$cx-A" --port_name $portA \
    --speed $rate_A --endp_type lf_udp --report_timer 1000

   ./lf_firemod.pl --mgr $mgr --resource $resource $clilog \
    --action create_endp --endp_name "$cx-B" --port_name $portB \
    --speed $rate_B --endp_type lf_udp --report_timer 1000

   ./lf_firemod.pl --mgr $mgr $clilog  --action create_cx --cx_name $cx --cx_endps "$cx-A,$cx-B" --report_timer 1000

   ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --quiet yes --action do_cmd \
    --cmd "set_endp_details $cx-A NA NA NA $num_packets" &>/dev/null

   ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --quiet yes --action do_cmd \
    --cmd "set_endp_details $cx-B NA NA NA $num_packets" &>/dev/null
}

# Delete all connections and endpoints that have 'bg' in the name
echo "Deleting old connections."
cx_array=( `./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action list_cx | awk '/bg/ { print $ 2 }' | sed 's/,$//'`  )
for i in "${cx_array[@]}"
   do
      :
       ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action delete_cx --cx_name $i
       ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action delete_endp --endp_name "$i-A"
       ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action delete_endp --endp_name "$i-B"
   done

./lf_firemod.pl --mgr $mgr --resource $resource $clilog --quiet yes --action do_cmd --cmd 'nc_show_endpoints all' &>/dev/null

sleep 5

echo "Creating new connections."
last_sta=$((first_sta + num_stas - 1))
for i in `seq $first_sta $last_sta`; do
   new_cx bg$i $port_A sta$i
done

echo "All stations and connections have been created."

/lf_firemod.pl --mgr $mgr --resource $resource $clilog --quiet yes --action do_cmd --cmd 'nc_show_endpoints all' &>/dev/null

#
