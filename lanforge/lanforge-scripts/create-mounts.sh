#!/bin/bash
#set -x

CIFS_USERNAME="lanforge"
CIFS_PASSWORD="lanforge"
NFS_SRV="192.168.100.3"
NFS_PATH="/mnt/d2"
CIFS_SRV="192.168.100.3"
CIF_PATH="/mnt/d2"
LOCAL_MOUNT_PATH="/mnt"
NFS_OPTS=""

if [ $# -lt 4 ]; then
  echo "Usage: `basename $0` NFS|CIFS <ethN> <first_mvlan> <last_mvlan> <server server-path local-mnt-path>"
  exit 1
fi


IF=$2
MV_START=$3
MV_STOP=$4
if [ ! -z "$5" ]
then
   NFS_SRV=$5
   CIFS_SRV=$5
fi

if [ ! -z "$6" ]
then
   NFS_PATH=$6
   CIFS_PATH=$6
fi

if [ ! -z "$7" ]
then
   LOCAL_MOUNT_PATH=$7
fi

if [ $1 = "CIFS" ]; then
   LOCAL_PATH="$LOCAL_MOUNT_PATH/cifs_${IF}#"
   CIFS_OPTS="username=$CIFS_USERNAME,password=$CIFS_PASSWORD,$CIFS_OPTS"
else
   LOCAL_PATH="$LOCAL_MOUNT_PATH/nfs_${IF}#"
fi

LIP=clientaddr
if uname -a | grep 2.6.20
then
	LIP=local_ip
fi

for ((m=MV_START; m <= MV_STOP ; m++))
do
  if [ `ifconfig $IF#$m > /dev/null 2>&1; echo $?` -eq "1" ]; then
    echo "*** MISSING INTERFACE: $IF#$m"
    echo
  elif [ `ifconfig $IF#$m | grep "inet addr" > /dev/null; echo $?` -eq "1" ]; then
    echo "*** MISSING IP ADDRESS ON INTERFACE: $IF#$m"
  else
    if [ ! -d "$LOCAL_PATH$m" ]; then
      echo "mkdir -p $LOCAL_PATH$m"
      mkdir -p $LOCAL_PATH$m
    fi
    IPADDR=`ifconfig $IF#$m | grep "inet addr" | awk -F":" '{ print $2}' |\
            awk '{ print $1}'`
    # Ping seems to fail sometimes..probably file-server is under too much load or something
    # so try the ping up to 5 times.
    for ((q=0;q<5;q+=1))
    do
      if [ `ping -c 1 -w 1 -I $IPADDR $NFS_SRV > /dev/null; echo $?` -eq "0" ]; then
	q=10; # done
        if [ $1 = "CIFS" ]; then
           echo "mount -t cifs -o local_ip=$IPADDR,$CIFS_OPTS //$CIFS_SRV$CIFS_PATH $LOCAL_PATH$m"
           if [ `mount -t cifs -o local_ip=$IPADDR,$CIFS_OPTS //$CIFS_SRV$CIFS_PATH $LOCAL_PATH$m >\
                 /dev/null; echo $?` -ne "0" ]; then
             echo
           fi
        else
           echo "mount -t nfs -o $LIP=$IPADDR,$NFS_OPTS $NFS_SRV:$NFS_PATH $LOCAL_PATH$m"
           if [ `mount -t nfs -o $LIP=$IPADDR,$NFS_OPTS $NFS_SRV:$NFS_PATH $LOCAL_PATH$m >\
                 /dev/null; echo $?` -ne "0" ]; then
             echo
           fi
        fi
      else
        echo  "*** UNABLE TO PING: $NFS_SRV FROM: $IF#$m, $IPADDR"
      fi
    done
  fi
done
echo "********************************************"
if [ $1 = "CIFS" ]; then
  echo "Total number of mounts according to 'mount': `mount | grep "$CIFS_SRV$CIFS_PATH" |\
      grep "$LOCAL_PATH" | grep "type cifs" |\
      wc | awk '{ print $1 }'`"
else
   echo "Total number of NFS mounts according to 'mount': `mount | grep "$NFS_SRV:$NFS_PATH" |\
      grep "$LOCAL_PATH" | grep -i "type $1" | grep "$LIP=" | grep "addr=$NFS_SRV" |\
      wc | awk '{ print $1 }'`"
   echo
fi
