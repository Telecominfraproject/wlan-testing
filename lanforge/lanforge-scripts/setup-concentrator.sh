#!/bin/bash
set -x
set -e
[ -f /root/strongswan-config ] && . /root/strongswan-config ||:
ETC=${ETC:=/etc/strongswan}
SWAND="$ETC/strongswan.d"
IPSECD="$ETC/ipsec.d"
SWANC="$ETC/swanctl"
NOWSEC=`date +%s`
SWAN_LIBX=${SWAN_LIBX:=/usr/libexec/strongswan}
[ -d $SWAN_LIBX ] || {
  echo "SWAN_LIBX $SWAN_LIBX not found. Plese set SWAN_LIBX in /root/strongswan-config"
  exit 1
}
export LD_LIBRARY_PATH="$SWAN_LIBX:$LD_LIBRARY_PATH"
WAN_IF=${WAN_IF:=eth1}
WAN_IP=${WAN_IP:=10.1.99.1}
WAN_CONCENTRATOR_IP=${WAN_CONCENTRATOR_IP:=10.1.99.1}
XIF_IP=${XIF_IP:=10.9.99.1}

function initialize_vrf() {
  local WANDEV=$WAN_IF
  local VRFID=$1
  local VRFDEV=vrf$VRFID
  local XFRMDEV=xfrm$VRFID

  # do you need this?
  #sysctl -w net.ipv4.ip_forward=1
  #sysctl -w net.ipv4.conf.all.rp_filter=0

  # setup vrf
  ip link add $VRFDEV type vrf table $VRFID
  ip link set dev $VRFDEV up
  ip route add unreachable default metric 4278198272 vrf $VRFDEV

  # create tunnel device
  ip li del $XFRMDEV >/dev/null 2>&1
  $SWAN_LIBX/xfrmi -n $XFRMDEV -i $VRFID -d $WANDEV
  ip li set dev $XFRMDEV up
  ip li set dev $XFRMDEV master $VRFDEV
  ip add add 169.254.24.201/32 dev $XFRMDEV scope link
  ip ro add default dev $XFRMDEV vrf $VRFDEV
  ip -6 ro add default dev $XFRMDEV vrf $VRFDEV
}

function initialize_fake_client_netns() {
  local VRFID=$1
  sysctl  net.ipv4.conf.all.rp_filter=0
  sysctl  net.ipv4.conf.default.rp_filter=0
  ip netns add ts-vrf-${VRFID}
  ip netns exec ts-vrf-${VRFID} ip li set dev lo up
  ip li del ts-vrf-${VRFID}a
  ip link add ts-vrf-${VRFID}a type veth peer name ts-vrf-${VRFID}b netns ts-vrf-${VRFID}
  ip netns exec ts-vrf-${VRFID} ip link set dev ts-vrf-${VRFID}b up
  ip netns exec ts-vrf-${VRFID} ip add add dev ts-vrf-${VRFID}b 10.0.201.2/24
  ip netns exec ts-vrf-${VRFID} ip ro add default via 10.0.201.1
  ip li set dev ts-vrf-${VRFID}a up
  ip li set dev ts-vrf-${VRFID}a master vrf${VRFID}
  ip add add 10.0.201.1/24 dev ts-vrf-${VRFID}a
}

function initialize() {
  [ -d "$SWANC/peers-available" ] || mkdir "$SWANC/peers-available"
  [ -d "$SWANC/peers-enabled" ] || mkdir "$SWANC/peers-enabled"
  [ -f "$SWANC/secrets.conf" ] || touch "$SWANC/secrets.conf"

  systemctl enable strongswan
  systemctl daemon-reload
  systemct  start strongswan || {
    journalctl -xe
  }
}

function vrf_ping() {
  local vrfid=$1
  ip netns exec ts-vrf-$vrfid ping 10.0.201.2 
}


function backup_keys() {
  if  [ -f $SWANC/secrets.conf ]; then
    cp $SWANC/secrets.conf $SWANC/.secrets.conf.$NOWSEC
  fi
}

function deactivate_peer() {
  [ -e "$SWANC/peers-enabled/${1}.conf" ] || {
    if [ -e "$SWANC/peers-available/${1}.conf" ]; then
      echo "Peer $1 deactivated."
    else
      echo "No peer config at $SWANC/peers-available/${1}.conf"
    fi
    exit 0
  }

  echo -n "Deactivating $1..."
  rm "$SWANC/peers-enabled/${1}.conf"
  swanctl --load-all
  echo "done"
}


function activate_peer() {
  [ -f "$SWANC/peers-available/${1}.conf" ] || {
    echo "No peer config at $SWANC/peers-available/${1}.conf"
    exit 1
  }

  if [ -e "$SWANC/peers-enabled/${1}.conf" ]; then
    echo "Peer $1 actiated."
  else
    echo -n "Activating $1..."
    ln -s" $SWANC/peers-available/${1}.conf" "$SWANC/peers-enabled/"
    swanctl --load-all
    echo "done"
  fi
}

function create_concentrator_peer() {
  if [ -f "$SWANC/peers-available/${1}.conf" ]; then
    echo "Peer $1 config already exists."
    return;
  fi

  cat > "$SWANC/peers-available/${1}.conf" <<EOF
$1 {
  local_addrs = %any
  remote_addrs = %any
  unique = replace
  local {
    auth = psk
    id = @${1}-slave.loc # identifier, use VRF ID
  }
  remote {
    auth = psk
    id = @${1}-master.loc # remote id, use VRF ID
  }
  children {
    ${1}_sa {
      local_ts = 0.0.0.0/0, ::/0
      remote_ts = 0.0.0.0/0, ::/0
      if_id_out = 1 # xfrm interface id, use VRF ID
      if_id_in = 1  # xfrm interface id, use VRF ID
      start_action = trap
      life_time = 1h
      rekey_time = 55m
      esp_proposals = aes256gcm128-modp3072 # good for Intel HW
      dpd_action = trap
    }
  }
  keyingtries = 0
  dpd_delay = 30
  version = 2
  mobike = yes
  rekey_time = 23h
  over_time = 1h
  proposals = aes256-sha256-modp3072
}
EOF
}

function create_station_peer() {
  if [ -f "$SWANC/peers-available/${1}.conf-remote" ]; then
    echo "Peer $1 remote config already exists."
    echo "Remove $SWANC/peers-available/${1}.conf-remote to continue."
    exit 1;
  fi

  cat > "$SWANC/peers-available/${1}.conf-remote" <<EOF
$1 {
  local_addrs = %any # use any local ip to connect to remote
  remote_addrs = $WAN_CONCENTRATOR_IP
  unique = replace
  local {
    auth = psk
    id = @${1}-master.loc # identifier, use VRF ID
  }
  remote {
    auth = psk
    id = @${1}-slave.loc # remote id, use VRF ID
  }
  children {
    ${1}_sa {
      local_ts = 0.0.0.0/0, ::/0
      remote_ts = 0.0.0.0/0, ::/0
      if_id_out = 1 # xfrm interface id, use VRF ID
      if_id_in = 1  # xfrm interface id, use VRF ID
      start_action = trap
      life_time = 1h
      rekey_time = 55m
      esp_proposals = aes256gcm128-modp3072 # good for Intel HW
      dpd_action = trap
    }
  }
  keyingtries = 0
  dpd_delay = 30
  version = 2
  mobike = yes
  rekey_time = 23h
  over_time = 1h
  proposals = aes256-sha256-modp3072
}
EOF
}

function create_concentrator_key() {
  [ -f "$SWANC/secrets.conf" ] || {
    echo "$SWANC/secrets.conf not found!"
    exit 1
  }
  backup_keys
  k=`dd if=/dev/urandom bs=20 count=1 | base64`
  cat >> "$SWANC/secrets.conf" <<EOF
ike-${1}-master {
  id = ${1}-master.loc # use remote id specified in tunnel config
  secret = "$k"
}
EOF
  echo "created $1 key"
}

function create_station_key() {
  [ -f "$SWANC/secrets.conf" ] || {
    echo "$SWANC/secrets.conf not found!"
    exit 1
  }
  backup_keys
  local conc_keys=(`egrep -B4 "^ike-${1}-master \{" $SWANC/secrets.conf`)
  local lines=()
  local foundit=0
  local line
  for line in "${conc_keys[@]}"; do
    echo "LINE $line"
    [[ $line = *-master.loc ]] && {
      line=${line/master.loc/slave.loc}
    } ||:
    lines+=($line)
  done
  for line in "${lines}"; do
    echo "$line"
  done > $SWANC/${1}-secrets.conf-remote
  echo "created $SWANC/${1}-secrets.conf-remote"
}

function get_vrf_for_if() {
  local ifmaster=`ip -o li show $1 | egrep -o '(master \S+)'`
  [[ x$ifmaster = x ]] && echo "No master found for $1"
  echo ${ifmaster#master }
}

function enable_ipsec_if() {
  vrfnum=$(get_vrf_for_if $WAN_IF)
  xif="xfrm${vrfnum}"
  $SWAN_LIBX/xfrmi -n $xif  -i ${vrfnum} -d $WAN_IF ||:

  ip link set dev $xif up ||:
  ip link set dev $xif master vrf${vrfnum} ||:
  ip address add $XIF_IP/32 dev $xif scope link ||:
  ip route add default dev $xif vrf $vrfnum ||:
  ip route add 10.0.0.0/8 dev $xif vrf $vrfnum ||:
}

function check_arg() {
  if [ ! -f "$SWANC/secrets.conf" ] ; then
    echo "$SWANC/secrets.conf not found. Suggest running $0 -i, bye."
    exit 1
  fi
  [[ z$1 != z ]] || {
    echo "Please give me a peer name, bye."
    exit 1
  }
}

function activate_all() {
  local f
  for f in $SWANC/*.conf; do
    echo "CONF $f"
    f=`basename $f`
    [[ $f = secrets.conf ]] && continue ||:
    [[ $f = swanctl.conf ]] && continue ||:
    [[ $f = *.conf ]] && f=${f%.conf}
    echo "f now $f"
    activate_peer $f
  done
}

function copy_config() {
  local vrf=`get_vrf_for_if $WAN_IF`
  ip vrf exec $vrf scp $WAN_IP:$SWANC/${1}-secrets.conf-remote $SWANC/${1}-secrets.conf
  ip vrf exec $vrf scp $WAN_IP:$SWANC/peers-available/${1}.conf-remote $SWANC/peers-available/${1}.conf
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#     M   A   I   N
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


while getopts "a:c:d:f:p:v:behi" arg; do
  case $arg in
    a)
      check_arg $OPTARG
      echo "Activating $OPTARG"
      activate_peer $OPTARG
      ;;
    b)
      enable_ipsec_if $WAN_IF
      ;;
    c)
      check_arg $OPTARG
      echo "Creating $OPTARG"
      create_concentrator_peer $OPTARG
      create_station_peer $OPTARG
      create_concentrator_key $OPTARG
      create_station_key $OPTARG
      ;;
    d)
      check_arg $OPTARG
      echo "Deactivating $OPTARG"
      deactivate_peer $OPTARG
      ;;
    e)
      activate_all
      ;;
    f)
      check_arg $OPTARG
      copy_config $OPTARG
      ;;
    h)
      cat <<EOF
$0 -i       : initialize /etc/strongswan directories
  -b        : enable ipsec transform interface on [$WAN_IF]
  -c peer   : create_station_peer then create_station_key
  -a peer   : activate peer
  -d peer   : deactivate peer
  -e        : activate all peers
  -f peer   : copy config files from $WAN_IF:/etc/strongswan/swanctl/\$peer.conf-remote
  -p        : print peers
  -v intf   : get vrf for interface
  -h        : help
EOF
      ;;
    i)
      initialize
      echo "Initialized."
      exit 0;
      ;;
    p)
      #echo " print peers"
      strongswan list
      ;;
    v)
      check_arg $OPTARG
      get_vrf_for_if $OPTARG
      ;;

    *) echo "Unknown option: $arg"
  esac
done
