#!/bin/bash
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# vUE operations script actions:
#   create a station
#   print out stations attributes
#   print list of station names
#   print list of connections
#   bring a station up/down
#   create L3/L4 connection
#   start/stop connection
#   print packets rx/tx for station
#   print packets rx/tx for connection
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
Q='"'
A="'"
SCRIPTDIR="/home/lanforge/scripts"

function usage() {
  echo "$0:
    --create_sta --name <name> --radio <wiphyX> --security <open|wpa2> --ssid <ssid> --passphrase <wpa2 pass> --ip <DHCP | IP-address>
    --delete_sta --name <name>
    --show_port  --name <name>
    --list_ports
    --list_cx
    --list_l4
    --log_cli   <filename>
    --poll_endp --name <name> [--endp_vals tx_bytes,tx_pkts,rx_bytes,rx_pkts]
    --up        --name <name>
    --down      --name <name>
    --create_cx --name <name> --sta <name> --port <name> --tcp|--udp --bps <speed-a>,<speed-b>
    --create_l4 --name <name> --sta <name> --url <name> --utm <urls/10 min> --l4bps <speed>
    --start_cx  --name <cx name>
    --start_l4  --name <l4 name>
    --stop_cx   --name <cx name>
    --stop_l4   --name <l4 name>
    --mgr       <localhost or ip>
    --resource  <1=manager, 2+:resource>

Examples:
  $0 --list_ports --mgr 192.168.1.102 --resource 2
  $0 --create_sta --resource 2 --name sta100  --radio wiphy0 --security wpa2 --ssid jedtest --passphrase jedtest1 --ip DHCP
  $0 --create_sta --resource 2 --name sta100  --radio wiphy0 --security wpa2 --ssid jedtest --passphrase jedtest1 --ip 10.1.1.10 --netmask 255.255.255.0
  $0 --delete_sta --resource 2 --name sta100
  $0 --up --name sta100
  $0 --create_cx  --name tcp10 --sta sta100 --port eth1 --tcp --bps 1000000
  $0 --create_l4  --name web10 --sta sta100 --url http://www.example.com --utm 2400 --l4bps 1000000
  $0 --poll_endp  --name tcp10 --endp_vals tx_pkts,rx_pkts
  Use --log_cli to print out CLI commands
  Use --log_cli /tmp/clilog.txt to log CLI commands to /tmp/clilog.txt
* Stations created with WPA2 and DHCP by default
"
}
##  M A I N
OPTS="`getopt -o hm:r:n:ud -l help,mgr:,resource:,quiet:,\
create_sta,delete_sta,ip:,radio:,name:,ssid:,passphrase:,security:,ip:,netmask:,\
list_ports,list_cx,list_l4,\
show_port,endp_vals:,poll_endp,log_cli:,\
create_cx,port:,sta:,tcp,udp,bps:,\
create_l4,url:,utm:,l4bps:,\
up,down,start_cx,start_l4,stop_cx,stop_l4 \
--name \"$0\" -- \"$@\"`"
if [ $? != 0 ]; then
    usage
    exit 1
fi
#echo "OPTS: $OPTS"
eval set -- "$OPTS"

# defualts
netmask="255.255.0.0"
resource="1"
mgr="localhost"
action="list"
ip="DHCP"
security="wpa2"
proto="lf_udp"
bps=2000000
l4bps=0
utm=2400
clilog=''
quiet="--quiet yes"

function do_firemod() {
  echo "./lf_firemod.pl --mgr \"$manager\" --resource \"$resource\" $clilog $quiet $@"
  ./lf_firemod.pl --mgr "$manager" --resource "$resource" $clilog $quiet $@
}

function do_portmod() {
  echo "./lf_portmod.pl --manager \"$manager\" --card \"$resource\" $clilog $quiet $@"
  ./lf_portmod.pl --manager "$manager" --card "$resource" $clilog $quiet $@
}

function do_associate() {
  echo "./lf_associate_ap.pl --mgr \"$manager\" --resource \"$resource\" $clilog $quiet $@"
  ./lf_associate_ap.pl --mgr "$manager" --resource "$resource" $clilog $quiet $@
}

function do_cmd() {
  newcmd=""
  for c in "$@"; do
    newcmd="$newcmd '$c'"
  done
  ./lf_firemod.pl --mgr "$manager" --resource "$resource" $quiet $clilog --action do_cmd --cmd "$newcmd"
}

while true; do
  case "$1" in
    --name)
      name="$2"
      shift 2;;
    --ssid)
      ssid="$2"
      shift 2;;
    --passphrase)
      passphrase="$2"
      shift 2;;
    --security)
      security="$2"
      shift 2;;
    --radio)
      radio="$2"
      shift 2;;
    --ip)
      ip="$2"
      shift 2;;
    --show_port)
      action="show_port"
      shift;;
    --list_ports)
      action="list_ports"
      shift;;
    --list_cx)
      action="list_cx"
      shift;;
    --poll_endp)
      action="poll_endp"
      shift;;
    --endp_vals)
      endp_vals="$2"
      shift 2;;
    --list_l4)
      action="list_l4"
      shift;;
    --create_sta)
      action="create_sta"
      shift;;
    --delete_sta)
      action="delete_sta"
      shift;;
    --sta)
      sta="$2"
      shift 2;;
    --ip)
      ip="$2"
      shift 2;;
    --netmask)
      netmask="$2"
      shift 2;;
    --port)
      port="$2"
      shift 2;;
    --up)
      action="up"
      shift;;
    --down)
      action="down"
      shift;;
    --create_cx)
      action="create_cx"
      shift;;
    --tcp)
      proto="lf_tcp"
      shift;;
    --udp)
      proto="lf_udp"
      shift;;
    --bps)
      IFS=',' read -a speeds <<< "$2"
      #if [ ${#speeds} -gt 1 ] ; then
      #  echo "found TWO speeds: ${speeds[0]}, ${speeds[1]}"
      #fi
      shift 2;;
    --l4bps)
      l4bps="$2"
      shift 2;;
    --create_l4)
      action="create_l4"
      shift;;
    --url)
      url="$2"
      shift 2;;
    --utm)
      utm="$2"
      shift 2;;
    --start_cx)
      action="start_cx"
      shift;;
    --stop_cx)
      action="stop_cx"
      shift;;
    --start_l4)
      action="start_l4"
      shift;;
    --stop_l4)
      action="stop_l4"
      shift;;
    --mgr)
      manager="$2"
      shift 2;;
    --resource)
      resource="$2"
      shift 2;;
    --log_cli)
      if [[ $2 != --* ]]; then
        clilog="--log_cli ${2}"
        shift 2;
      else
        clilog="--log_cli"
        shift;
      fi
      ;;
    --quiet)
      quiet="--quiet $2"
      shift 2;;
    --help)
      usage; exit 0;;
    -h)
      usage; exit 0;;
    --) shift;
      break;;
      *) echo "Unknown Option [$1]"
      exit 1;;
  esac
done
#echo "Action: $action Mgr $manager Resource $resource Name $name IP $ip SSID $ssid"

if [ -z "$action" ]; then
  usage
  echo "No action specified."
  exit 1
fi

if [ -z "$manager" ]; then
  usage
  echo "No LANforge Manager specified."
  exit 1
fi

if [ -z "$resource" ]; then
  usage
  echo "No resource specified."
  exit 1
fi

# Assume we are already in the right directory...doing a cd here breaks
# running scripts from any other directory. --Ben
#cd $SCRIPTDIR
case "$action" in
  list_ports)
    do_firemod --action list_ports
    ;;

  list_cx)
    do_firemod --action list_cx
    ;;

  list_l4)
    do_firemod --action list_endp  | grep -v UN-MANAGED
    ;;

  show_port)
    [ -z "$name" ] && usage && echo "No station name specified." && exit 1
    do_portmod --port_name "$name" --show_port
    ;;

  poll_endp)
    [ -z "$name" ] && usage && echo "No station name specified." && exit 1
    do_firemod --action list_endp | egrep -q " \[${name}\] "
    if [ $? -ne 0 ]; then
      do_firemod --action list_endp
      echo "Endpoint $name not found."
      exit 1
    fi
    echo "Press <control-c> to stop."
    while true; do
      if [ ! -z "$endp_vals" ]; then
        do_firemod --action show_endp --endp_name "$name" --endp_vals "$endp_vals"
      else
        do_firemod --action show_endp --endp_name "$name" | egrep -v '>>'
      fi
      sleep 3
    done
    ;;

  create_sta)
    [ -z "$name"      ] && usage && echo "No station name specified." && exit 1
    [ -z "$ssid"      ] && usage && echo "No SSID specified." && exit 1
    [ -z "$security"  ] && usage && echo "No WiFi security specified." && exit 1
    [ -z "$radio"     ] && usage && echo "No radio specified." && exit 1
    do_associate --action add \
      --radio "$radio" --security "$security" --ssid "$ssid" --passphrase "$passphrase" \
      --first_sta "$name" --first_ip "$ip" --netmask "$netmask" --num_stations 1
    ;;
   
  delete_sta)
    [ -z "$name"      ] && usage && echo "No station name specified." && exit 1
    do_associate --action del --port_del "$name"
    ;;

  create_cx)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    [ -z "$sta"   ] && usage && echo "No station name specified." && exit 1
    [ -z "$port"  ] && usage && echo "No upstream port name specified." && exit 1
    [ -z "$proto" ] && usage && echo "No connection protocol (tcp|udp) specified" && exit 1
    [ -z "${speeds[0]}" ] && usage && echo "No bitrate provided for L3 connection" && exit 1
    if [ -z "${speeds[1]}" ]; then
      speeds+=(${speeds[0]})
    fi
    #echo "Speed-a: ${speeds[0]} Speed-b: ${speeds[1]}"

    do_firemod \
      --action create_endp --endp_name "${name}-A" --speed "${speeds[0]}" \
      --endp_type "$proto" --port_name "$sta" || exit 1

    do_firemod \
      --action create_endp --endp_name "${name}-B" --speed "${speeds[1]}" \
      --endp_type "$proto" --port_name "$port" || exit 1

    do_firemod --action create_cx --cx_name "$name" --cx_endps "${name}-A,${name}-B"
    ;;

  create_l4)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    [ -z "$url"   ] && usage && echo "No URL specified." && exit 1
    [ -z "$utm"   ] && usage && echo "No requests/10min rate define (--utm)." && exit 1

    # remember do_cmd is alias for ./lf_firemod --action do_cmd --cmd
    url2="dl $url /dev/null"
    do_cmd add_l4_endp "$name" 1 "$resource" "$sta" l4_generic 0 10000 "$utm" "$url2" NA NA 'ca-bundle.crt' NA 0 0 60 "$l4bps" 512 ' ' 0.0.0.0
    do_cmd set_endp_tos "$name" DONT-SET 0
    do_cmd set_endp_flag "$name" L4Enable404 0
    do_cmd set_endp_report_timer "$name" 5000
    do_cmd set_endp_flag "$name" ClearPortOnStart 0
    do_cmd set_endp_quiesce "$name" 3
    do_cmd add_cx "CX_$name" default_tm "$name"
    ;;

  start_cx)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    do_cmd set_cx_state default_tm $name RUNNING
    ;;

  stop_cx)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    do_cmd set_cx_state default_tm $name STOPPED
    ;;

  start_l4)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    do_cmd set_cx_state default_tm CX_$name RUNNING
    ;;

  stop_l4)
    [ -z "$name"  ] && usage && echo "No connection name specified." && exit 1
    do_cmd set_cx_state default_tm CX_$name STOPPED
    ;;

  down)
    [ -z "$name"  ] && usage && echo "No port name specified." && exit 1
    do_portmod --port_name $name --set_ifstate down --quiet 1
    ;;

  up)
    [ -z "$name"  ] && usage && echo "No port name specified." && exit 1
    do_portmod --port_name $name --set_ifstate up --quiet 1
    ;;

  *)
    echo "Unimplemented Action. Please contact support@candelatech.com"
    exit 1
    ;;
esac
# eof
