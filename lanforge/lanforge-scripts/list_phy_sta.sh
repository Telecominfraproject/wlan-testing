#!/bin/bash
# this script lists wiphy stations per radio

[ -z "$MGR"    ] && echo "$0 wants MGR set, bye"   && exit 1
[ -z "$RESRC"   ] && echo "$0 wants RESRC set, bye"  && exit 1
[ -z "$RADIO"  ] && echo "$0 wants RADIO set, bye" && exit 1

. ~/scripts/common.bash

LINKUP="link=UP"
LINKDOWN="link=DOWN"
LINKANY=""
DEF_OUTFILE="${DEF_OUTFILE:-/tmp/wiphyNN-names.txt}"

OUTFILE="${DEF_OUTFILE/NN/$RADIO}"

[ -z "$OUTFILE" ] && echo "$0 wants OUTFILE set, use 'stdout' for stdout, bye" && exit 1

function helpquit() {
   echo "${D}MGR=localhost ${D}RESRC=1 ${D}RADIO=0 ${D}DEF_OUTFILE=$DEF_OUTFILE $0 --up|--down|--all\n"
   exit 1
}

function firemod_list() {
   ./lf_firemod.pl --mgr $MGR --resource $RESRC --action list_ports \
      | /usr/bin/perl -ne "/^((sta${RESRC}${RADIO}|wlan${RADIO})\d*) ${STATUS}/ && print ${Q}${D}1${N}${Q}"
}

case "$1" in
  *up|*UP)
      STATUS=$LINKUP
      ;;
  *down|*DOWN)
      STATUS=$LINKDOWN
      ;;
  *all|*any|*ALL|*ANY)
      STATUS=$LINKANY
      ;;
  *)
     helpquit
     ;;
esac

cd `dirname $0`

if [ "$OUTFILE" = "stdout" ]; then
   firemod_list | sort
else
   firemod_list | sort > "$OUTFILE"
fi

#
