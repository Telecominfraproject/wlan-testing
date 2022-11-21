#!/bin/bash

set -x
java_pid=`pgrep java`
[ -z "$java_pid" ] && echo "no running java process" && exit 1

p_jmap=`which jmap`
[ -z "$p_jmap" ] && echo "jmap not found" && exit 1

now=`date +heap_+%Y-%m-%d_%I-%M-%S`
$p_jmap -dump:live,format=b,file=/home/lanforge/Documents/$now.bin $java_pid

jstack $java_pid
echo done
