#!/bin/bash
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
##                                                                         ##
## Use this script to associate stations between SSIDs A and B             ##
##                                                                         ##
## Install this script in /home/lanforge                                   ##
## Usage: ./associate_loop -m localhost -r 1 -a SSIDA -b SSIDB -n 10 -i 5  ##
##   -w wiphy0 -s sta1,sta2,sta3,sta4,sta5,sta6,sta7,sta8,sta9,sta10       ##
##                                                                         ##
##                                                                         ##
##                                                                         ##
##                                                                         ##
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
Q='"'
A="'"
#set -e
#set -x
usage="$0 -m localhost -r 1 -w wiphy0 -s sta1,sta2...<max> -a SSIDA -b SSIDB -n <seconds> -i <iterations>
 -m: manager ip address
 -r: resourse id
 -w: radio name for stations
 -s: station list, comma separated (no spaces)
 -a: first ssid
 -b: second ssid
 -n: naptime in seconds
 -i: iteration to loop

Associate one station (sta1) for 1 second, 10 iterations:
   $0 -m localhost -r 1 -w wiphy0 -s sta1,wlan1 -a testap1 -b testap2 -n 1 -i 10

Associate ten stations (sta105..sta109) for 5 seconds, indefinitely:
   stations=\`seq -f 'sta%g' -s, 105 109\`
   $0 -m 192.168.101.1 -r 2 -w wiphy1 -s \$stations -a testap1 -b testab2 -n 5 -i 0

Hit control-c to stop.
"
modscript=""
if [ -f "lf_firemod" ]; then
   modscript="./lf_firemod.pl"
elif [ -f "/home/lanforge/scripts/lf_firemod.pl" ]; then
   modscript="/home/lanforge/scripts/lf_firemod.pl"
fi
cd /home/lanforge/scripts

[ -z "$modscript" ] && {
   echo "script [$modscript] not present, please use this script from /home/lanforge or /home/lanforge/scripts"
   exit 1
}

infinite=0
while getopts ":a:b:i:m:n:r:s:w:" opt ; do
   case $opt in
      a) SSIDA="$OPTARG"      ;;
      b) SSIDB="$OPTARG"      ;;
      i) iterations="$OPTARG" ;;
      m) manager="$OPTARG"    ;;
      n) naptime="$OPTARG"    ;;
      r) resource="$OPTARG"   ;;
      s) stations="$OPTARG"   ;;
      w) wiphy="$OPTARG"      ;;
   esac
done
[ -z "$stations" ] && {
   echo "-s: stations, requires {begin,...end} for stations;"
   echo "$usage"
   exit 1
}

sta_start=0
sta_end=0;
IFS="," sta_hunks=($stations);
unset IFS
#if [ ${#sta_hunks[@]} -gt 1 ] ; then
#   sta_start=${sta_hunks[0]}
#   sta_end=${sta_hunks[1]}
#else
#   sta_start=${sta_hunks[0]}
#   sta_end=${sta_hunks[0]}
#fi

[ -z "$naptime" ] && {
   echo "-n: naptime required: seconds between changing ssids"
   echo "$usage"
   exit 1
}

[ -z "$iterations" ] && {
   echo "-i: iterations to switch ssids"
   echo "$usage"
   exit 1
}

[ $iterations -lt 0 ] && {
   echo "-i: positive number of iterations only, please"
   exit 1;
}

[ $iterations -eq 0 ] && {
   echo "Infinite iterations selected."
   infinite=1;
}

[ -z "$SSIDB" ] && {
   echo "-b: SSID B required"
   echo "$usage"
   exit 1
}

[ -z "$SSIDA" ] && {
   echo "-a: SSID A required"
   echo "$usage"
   exit 1
}

[ -z "$resource" ] && {
   echo "-r: resource number for radio owning the station to modify"
   echo "$usage"
   exit 1
}

[ -z "$wiphy" ] && {
   echo "-w: wiphy radio owning the station"
   echo "$usage"
   exit 1;
}

[ -z "$manager" ] && {
   echo "-m: ip address of LANforge manager "
   echo "$usage"
   exit 1;
}
use_ssid=0 # 0 := a, 1 := b
while [ $infinite == 1 -o $iterations -ge 0 ] ; do
   for sta in "${sta_hunks[@]}"; do
      if [ $use_ssid == 0 ]; then
         newssid=$SSIDA
      else
         newssid=$SSIDB
      fi
      [ -z "$wiphy" ] && {
         echo "radio unconfigured, error."
         exit 1
      }
      clicmd="add_sta 1 $resource $wiphy $sta NA $newssid"
      $modscript --quiet yes --mgr $manager --resource $resource --action do_cmd --cmd "$clicmd"
      sleep 0.05
   done

   if [ $use_ssid = 1 ]; then
      use_ssid=0;
   else
      use_ssid=1;
   fi
   iterations=$(($iterations - 1))
   sleep $naptime
done

#eof
