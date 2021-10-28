#!/bin/bash
# check for log file
LOCKFILE="/tmp/update-test.lock"
[ -f $LOCKFILE ] && echo "lockfile $LOCKFILE found, bye" && exit 0

export DISPLAY=":1"
[ ! -z "$DEBUG" ] && set -x
IP="192.168.95.239"
HL="/home/lanforge"
HLD="${HL}/Documents"
scripts="${HLD}/lanforge-scripts"
verNum="5.4.3"
GUILog="/home/lanforge/Documents/GUILog.txt"
GUIUpdate="/home/lanforge/Documents/GUIUpdateLog.txt"
CTLGUI="/home/lanforge/Documents/connectTestGUILog.txt"
CTLH="/home/lanforge/Documents/connectTestHLog.txt"
GUIDIR="${HL}/LANforgeGUI_${verNum}"
ST="/tmp/summary.txt"
DM_FLAG="${HL}/LANforgeGUI_${verNum}/DAEMON_MODE"
output=/tmp/gui_update_test
NO_AUTO="${HL}/LANforgeGUI_${verNum}/NO_AUTOSTART"
D_MODE="${HL}/LANforgeGUI_${verNum}/DAEMON_MODE"

trap do_sigint HUP
trap do_sigint ABRT
trap do_sigint INT
# trap do_sigint KILL # cannot be trapped
trap do_sigint PIPE
trap do_sigint QUIT
trap do_sigint SEGV
trap do_sigint TERM

function do_sigint() {
   [ -f $LOCKFILE ] && echo "removing lockfile" && rm -f $LOCKFILE
   for f in $GUILog $GUIUpdate $CTLGUI $CTLH $LOCKFILE $NO_AUTO /tmp/\+.*; do
      rm -f "$f"
   done
}

function start_gui() {
   daemon_mode=""
   [ -f "$D_MODE" ] && daemon_mode="-daemon"
   ( cd $GUIDIR; nohup env RESTARTS=999999 ./lfclient.bash $daemon_mode -s localhost &> $GUILog & )
   connect_fail=0
   wait_8080 || connect_fail=1

   if (( $connect_fail == 1 )); then
     set -x
     echo "" > $output
     [ -s $GUIUpdate ] && cat $GUIUpdate >> $output
     # cat $GUILog >> $output
     echo "------------------------------------------" >> $output
     mail  -q $output -s 'GUI connect failure' "test.notice@candelatech.com" < $GUILog
     [ ! -z "$DEBUG" ] && cat $GUILog
     do_sigint
     exit 1
   else
     echo "start_gui: connection found"
   fi
   return 0
}

function wait_8080() {
   set +x
   local connected=0
   local limit_sec=90
   echo "Testing for 8080 connection "
   lastpid=''
   zpid=''
   while (( connected == 0 )); do
      (( limit_sec <= 0)) && break
      curl -so /dev/null http://localhost:8080/ && connected=1
      (( connected >= 1 )) && break;
      limit_sec=$(( limit_sec - 1 ))
      lastpid=$zpid
      zpid=`pgrep java`
      if [ -z "$zpid" ]; then
          if [[ x"$zpid" = x ]] && [[ "$lastpid" != "" ]]; then
              echo "GUI crashed while starting, bye."
              return 1
          fi
          [ ! -z "$DEBUG" ] && echo -n "-$zpid/$lastpid "
      else
          [ ! -z "$DEBUG" ] && echo -n "+$zpid/$lastpid "
      fi

      sleep 1
   done
   if [[ $connected = 0 ]]; then
      echo "Unable to connect, bye"
      return 1
   else
      echo "Connection established"
   fi
   [ ! -z "$DEBUG" ] && set -x
   return 0
}

touch $LOCKFILE

if [ -f ${GUIDIR}/down-check ]; then
   numFound=`find ${GUIDIR} -name down-check -mmin +59 | grep -c down-check`

   if (( numFound >= 1 )); then
     ping -c2 -i1 -nq -w4 -W8 ${IP}
     if (( 0 == $? )); then
       rm "${GUIDIR}/down-check"
     else
       touch "${GUIDIR}/down-check"
       echo "Could not connect to ${IP}"
       do_sigint
       exit 1
     fi
   else
     ping -c2 -i1 -nq -w4 -W4 ${IP}
     if (( 0 != $? )); then
       touch "${GUIDIR}/down-check"
       echo "Could not connect to ${IP}"
       do_sigint
       exit 1
     fi
   fi
fi

sudo rm -f /tmp/*.txt
sudo rm -f $GUILog $GUIUpdate $CTLGUI $CTLH $ST

touch "$NO_AUTO"
touch $GUIUpdate
touch $ST
if [ ! -z "$SKIP_INSTALL" ] && [ x$SKIP_INSTALL = x1 ]; then
   echo "skipping installation" | tee -a $GUIUpdate
else
   echo "doing installation"
   set -x
   python3 ${scripts}/auto-install-gui.py --versionNumber $verNum &> $GUIUpdate
   if [ -s $GUIUpdate ]; then
       grep -q "Current GUI version up to date, not testing" $GUIUpdate
       do_sigint
       exit 0
   fi
   [ -s $GUIUpdate ] && head $GUIUpdate >> $ST
   if grep -q -i "fail" $GUIUpdate; then
     mail -s 'GUI Update Test Failure' -q $GUILog -a $GUIUpdate "test.notice@candelatech.com" < $ST
     do_sigint
     exit 1
   fi
   set +x
fi
sleep 1
rm -f "$NO_AUTO"
pgrep java &>/dev/null && killall -9 java
start_gui
echo "Doing connectTest.py > $CTLGUI"
python3 ${scripts}/connectTest.py &> $CTLGUI
echo "== GUI =============================================" >> $ST
head $CTLGUI >> $ST
echo "===============================================" >> $ST
pgrep java &>/dev/null && killall -9 java
sleep 1

#-daemon
#touch "$D_MODE"
#start_gui
#python3 ${scripts}/connectTest.py &> $CTLH#

#echo "== HEADLESS =============================================" >> $ST
#head $CTLH >> $ST
#echo "===============================================" >> $ST
#rm -f "$D_MODE"
#pgrep java &>/dev/null && killall -9 java
start_gui
connect_fail=0
wait_8080 || connect_fail=1

cat $ST > $output
echo "=== FULL LOGS ============================================" >> $output
[ -s $GUILog ] && cat $GUILog >> $output
echo "===============================================" >> $output
[ -s $GUIUpdate ] && cat $GUIUpdate >> $output
echo "===============================================" >> $output
[ -s $CTLGUI ] && cat $CTLGUI >> $output
echo "===============================================" >> $output
[ -s $CTLH ] && cat $CTLH >> $output
echo "===============================================" >> $output
echo -e "--\n.\n" >> $output

mail -s 'GUI Update Test' "test.notice@candelatech.com" < $output
#cat $ST | mail -s 'GUI Update Test' -a $GUILog -a $GUIUpdate -a $CTLGUI -a $CTLH  "test.notice@candelatech.com"

do_sigint
#eof
