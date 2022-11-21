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
# this command is too limited to be useful for creating roaming stations at the moment
#./lf_associate_ap.pl --mgr $mgr --resource $resource $clilog \
# --ssid $ssid --security $encryption --passphrase $passphrase \
# --num_stations $num_stas --first_sta "sta$first_sta" \
# --first_ip DHCP --radio $radio --action add --xsec use-dot1x

#sleep 2

key_mgt="WPA-EAP"
pairwise="CCMP"
group="CCMP"
psk=NA
key=NA
ca_cert="/home/lanforge/apu2-a-ca.pem"
eap="TLS"
identity="lanforge@lanforge.com"
anon_id=NA
phase1=NA
phase2=NA
eap_passwd=NA
pin=NA
pac_file=NA
private_key="/home/lanforge/apu2-a-client.p12"
pk_passwd="lanforge"
hessid=NA
realm=NA
client_cert=NA
imsi=NA
milenage=NA
domain=NA
roaming_consortium=NA
venue_group=NA
venue_type=NA
network_type=NA
ipaddr_type_avail=NA
network_auth_type=NA
anqp_3gpp_cell_net=NA

for n in `seq $first_sta $(($first_sta -1 + $num_stas))` ; do
  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "add_sta 1 8 wiphy0 sta$n 2181039104 'ja2a-8021x' NA [BLANK] DEFAULT NA 00:0e:8e:41:0d:47 8 NA NA NA NA NA 2181039104"

  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "set_port 1 8 sta100 0.0.0.0 255.255.0.0 NA NA 1424969217212417 '00 0e 8e 03 32 47' NA NA BLANK 8548171820 8000 0 65535 4294967295 -1 -1 -1 -1 255 AUTO AUTO AUTO NA 0 192.168.100.1 0 NONE 9007199254740992 NONE"

  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
   "set_wifi_extra 1 $resource sta$n $key_mgt $pairwise $group $psk $key $ca_cert $eap $identity $anon_id $phase1 $phase2 $eap_passwd $pin $pac_file $private_key $pk_passwd $hessid $realm $client_cert"
done

bssid1="00:0e:8e:14:08:da"
bssid2="00:0e:8e:2e:84:19"

#roam commands: see http://ctlocal/lfcli_ug.php#wifi_cli_cmd
for n in `seq $first_sta $(($first_sta -1 + $num_stas))` ; do
  # roam to bssid1
  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "wifi_cli_cmd 1 $resource sta$n 'roam $bssid1'"
  sleep 2 # your sleep interval here should match the report timer you set in the GUI
  # scanning the port before it reports will probably result in stale (previous to roam) data
  # this is the point you do a 'nc_show_port 1 $resource sta$n' and grep for BSSID
  # roam to bssid2
  ./lf_firemod.pl --mgr $mgr --resource $resource $clilog --action do_cmd --cmd \
  "wifi_cli_cmd 1 $resource sta$n 'roam $bssid2'"
  sleep 2 # your sleep interval here should match the report timer you set in the GUI
  # scanning the port before it reports will probably result in stale (previous to roam) data
  # this is the point you do a 'nc_show_port 1 $resource sta$n' and grep for BSSID

done

#
