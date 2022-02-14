#!/bin/bash
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
##                                                             ##
##  Use this script to toggle a set of stations on or off      ##
##                                                             ##
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

function usage() {
   echo "$0 -a up -s staX,staY,staZ..."
   echo "      to turn stations on"
   echo "$0 -a down -s staX,staY,staZ..."
   echo "      to turn stations off"
}

action=none
stations=""
while getopts ":a:s:" opt ; do
   case "${opt}" in 
      a) action="${OPTARG}";;
      s) stations="${OPTARG}";;
      *) exit 1;;
   esac
done
shift $(( OPTIND - 1 ));

[ -z "$stations" ] && echo "No stations specified." && usage  && exit 1

[[ $action = none ]] && echo "No action specified." && usage && exit 1

scriptdir="/home/lanforge/scripts"
portmod="$scriptdir/lf_portmod.pl"
cd $scriptdir
IFS=',' sta_list=($stations)
if [[ $action = up ]] || [[ $action = down ]] ; then
   for sta in "${sta_list[@]}"; do
      echo "station $sta $action"
      $portmod --port_name $sta --set_ifstate $action --quiet 1
   done
   exit 0
else 
   echo "What does action $action mean?"
   usage
   exit 1
fi

#
