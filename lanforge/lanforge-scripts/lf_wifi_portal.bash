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
-h   Help information.

Example usage:
$0 -m lf0350-1234 -r 1 -w wiphy0 -n 40 -s test-SSID"

while getopts 'm:r:n:p:a:w:s:A:B:h' OPTION; do
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
      h)
        #send help message
        echo "$show_help"
        exit 1
        ;;
esac
done
shift "$(($OPTIND -1))"

#check for required getopts
if [ "$flag_ssid" = false ] || [ "$flag_radio" = false ]; then
   echo "Please provide at minimum the ssid (-s), and radio (-w). Run the script with -h for more information."
   exit 1
fi

echo "Deleting old stations."
./lf_associate_ap.pl --mgr $mgr --resource $resource $clilog --action del_all_phy --port_del $radio

./lf_firemod.pl --mgr $mgr --resource $resource --quiet yes  $clilog --action do_cmd \
 --cmd "nc_show_ports 1 $resource all 1" &>/dev/null

sleep 2

echo "Creating new stations."

for n in `seq $first_sta $(($first_sta -1 + $num_stas))` ; do
   # set disable_roam, mac, blank password, default rate, mode abgnAC 
  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "add_sta 1 $resource $radio sta$n 2147483648 $ssid NA [BLANK] NA DEFAULT xx:xx:xx:xx:*:xx 8 DEFAULT NA NA NA NA 2147483648"

  # sets no_dhcp_restart, no_ifup_post, use_dhcp, current_flags, dhcp, dhcp_rls, no_dhcp_conn, skip_ifup_roam
  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "set_port 1 $resource sta$n NA NA NA NA 1407377031036928 NA NA NA NA 5435834370"

   # see http://www.candelatech.com/cookbook.php?vol=cli&book=Changing+Station+POST_IFUP+Script+with+the+CLI+API
   # see http://www.candelatech.com/lfcli_ug.php#set_wifi_extra2
   ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
   "set_wifi_extra2 1 $resource sta$n 0 NA NA NA NA NA NA NA NA NA './portal-bot.pl --bot bp.pm --user username --pass secret --start_url http://www.google.com/  --ap_url http://10.41.3.250/ --login_form login.php --login_action login.php --logout_form logout.php'"
done

echo "Updating stations to portal_bot..."

#
