#!/bin/bash
##                                                                   ##
##   Top and Memory Usage Reporter                                   ##
##                                                                   ##
## Use this script to regularly record the                           ##
## free memory and number of processes running                       ##
## on your LANforge server.                                          ##
##                                                                   ##
## This script can be installed into cron by                         ##
## one of two methods:                                               ##
##    a) ln -s `pwd`/topmon.sh /etc/cron.hourly                      ##
##                                                                   ##
## Or more frequently:                                               ##
##    b) crontab -u lanforge -e                                      ##
##    and add the line                                               ##
## * */3 * * * /home/lanforge/scripts/topmon </dev/null &>/dev/null  ##
##                                                                   ##
## Find the results in /home/lanforge/topmon.log                     ##
##                                                                   ##
max_size="100MB"
log="/home/lanforge/topmon.log"
tmp="/home/lanforge/tmp.topmon.log"
now=$( date +"%Y-%m-%d %H:%M:%S")
echo ""     >> $tmp
echo "$now" >> $tmp
echo ""     >> $tmp
COLUMNS=512 LINES=15000 top -b -n 1 -w512 -c >> $tmp
echo ""     >> $tmp
# save the last 1M of the log file
tail -c $max_size $tmp > $log
#eof
