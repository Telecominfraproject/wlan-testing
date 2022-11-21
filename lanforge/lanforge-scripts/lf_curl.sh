#!/bin/bash
if [ -f /home/lanforge/lanforge.profile ]; then
   . /home/lanforge/lanforge.profile
else
   echo "/home/lanforge/lanforge.profile not found, bye."
   exit 1
fi
CURL=`which curl`
IP=`which ip`
#echo $CURL;
[ -f lib_vrf.bash ] && . ./lib_vrf.bash

SOURCE_IP=""
SOURCE_PORT=""
DEST_HOST=""
OUT_FILE=/dev/null
NUM_LOOPS=1

help="$0 options:
      -d {destination_url}
      -h # this help
      -i {source ip}
      -n {number of times, 0 = infinite}
      -o {output file prefix, /dev/null is default}
      -p {source port}
      -v # verbose curl option -#
E.G.:
   $0 -i 10.0.0.1 -p eth1 -o /tmp/output -d http://example.com/
becomes
   curl -sq. ~Lk --interface 10.0.0.1 -o /tmp/output_eth1 http://example.com/

Best if used from lf_generic_ping.pl to construct commands referencing this script:
   ./lf_generic_ping.pl --mgr cholla-f19 -r 2 -n curl_ex_ --match 'eth2#' --cmd 'lf_curl.sh -o /tmp/curl_%p.out -i %i -d %d -p %p' --dest http://localhost/
"
LFCURL=''
while getopts ":d:vhi:n:o:p:" OPT ; do
   #echo "OPT[$OPT] OPTARG[$OPTARG]"
   case $OPT in
   h)
      echo $help
      exit 0
      ;;
   d)
      DEST_HOST="$OPTARG"
      ;;
   i)
      PORT_IP="$OPTARG"
      if [[ $CURL = ~/local/bin/curl ]] || [[ $CURL = /home/lanforge/local/bin/curl ]]; then
         LFCURL=1
      fi
      ;;
   n)
      NUM_LOOPS=$OPTARG
      ;;
   o)
      OUT_FILE="$OPTARG"
      ;;
   p)
      PORT="$OPTARG"
      SOURCE_PORT="--interface $OPTARG"
      ;;
   v)
      PROGRESS='-#'
      ;;
   *)
      echo "Unknown option [$OPT] [$OPTARG]"
      ;;
   esac
done

if [[ -z "$DEST_HOST" ]]; then
   echo "$help"
   exit 1
fi

if [[ x$OUT_FILE != x/dev/null ]] && [[ x$SOURCE_PORT != x ]] ; then
   OUT_FILE="-o ${OUT_FILE}_${SOURCE_PORT}"
elif [[ $OUT_FILE = /dev/null ]]; then
   OUT_FILE="-o ${OUT_FILE}"
fi

VRF=''
NUM_GOOD=0
LB='#'
L_SOURCE_PORT="$PORT"
if [[ $PORT = *$LB* ]] && [[ $PORT != *@* ]]; then
   L_SOURCE_PORT="${PORT}@${PORT//#*/}"
fi
if [[ ${#IFNAMES[@]} -lt 1 ]]; then
   [[ x$PROGRESS != x ]] && echo "NO VRF PORTS: ${#IFNAMES[@]}"
else
   [[ x$PROGRESS != x ]] && echo "SOME VRF PORTS: ${#IFNAMES[@]}"
   if [[ x${IFNAMES[$L_SOURCE_PORT]} = x ]]; then
      [[ x$PROGRESS != x ]] && echo "No vrf port detected for $L_SOURCE_PORT"
   else
      [[ x$PROGRESS != x ]] && echo "VRF port: ${IFNAMES[$L_SOURCE_PORT]}"
      VRF=1
   fi
fi

if [[ $VRF = 1 ]]; then
   SOURCE_IP=''
elif [[ $LFCURL = 1 ]]; then
   SOURCE_IP="--dns-ipv4-addr $OPTARG --interface $OPTARG"
else
   SOURCE_IP="--interface $OPTARG"
fi


STD_O="/tmp/lf_curl_so.$$"
if [[ x$PROGRESS = x ]]; then
   VERB="-s"
   STD_E="/tmp/lf_curl_se.$$"
else
   VERB=""
   STD_E=""
fi
CCMD="$CURL $VERB -Lk --connect-timeout 2 --max-time 10 $PROGRESS \
-D /tmp/lf_curl_h.$$ $OUT_FILE $SOURCE_IP $DEST_HOST"

if [[ x$VRF != x ]]; then
   CCMD="$IP vrf exec ${IFNAMES[$L_SOURCE_PORT]} $CCMD"
fi

for N in `seq 1 $NUM_LOOPS`; do
   if [[ x$PROGRESS = x ]]; then
      $CCMD > $STD_O &> $STD_E
   else
      echo "Running $CCMD"
      $CCMD
   fi
   if [[ $? > 0 ]]; then
      echo "Failed $DEST_HOST"
      [ -f /tmp/lf_curl_se.$$ ] && head -1 /tmp/lf_curl_se.$$
   else
      NUM_GOOD=$(( $NUM_GOOD +1))
      [ -f /tmp/lf_curl_so.$$ ] && head -1 /tmp/lf_curl_so.$$
      [ -f /tmp/lf_curl_h.$$ ] && head -1 /tmp/lf_curl_h.$$
   fi
   sleep 1
done
echo "Finished $NUM_LOOPS, $NUM_GOOD successful"
#
