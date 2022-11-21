#!/bin/bash
usage="$0 <manager> <group-name> <endp-name-prefix>"
if [[ x$1 = x ]]; then
   echo "Please provide lanforge manager hostname or ip"
   echo $usage
   exit 1
fi
if [[ x$2 = x ]]; then
   echo "Please provide a group name"
   echo $usage
   exit 1
fi
if [[ x$3 = x ]]; then
   echo "Please provide an endpoint name prefix"
   echo $usage
   exit 1
fi

# query for endpoints maching prefix
if [ -f /tmp/endp.$$ ]; then
   rm -f /tmp/endp.$$
fi

./lf_firemod.pl --mgr $1 --quiet yes --action list_endp > /tmp/endp.$$
lines=`wc -l < /tmp/endp.$$`
if [ $lines -lt 1 ]; then
   echo "Unable to see any endpoints"
   exit 1
fi

declare -A names
while read line; do
   hunks=($line)
   endp="${hunks[1]}"
   endp=${endp/]/}
   endp=${endp/[/}
   if [[ $endp = D_* ]]; then
      continue
   fi

   # if name lacks a -A/B ending, it is prolly generic and the cx begins with CX_
   if [[ $endp = *-A ]] || [[ $endp = *-B ]]; then
      cxname=${endp%-A}
      cxname=${cxname%-B}
   else
      cxname="CX_${endp}"
   fi
   if [[ $cxname = $3* ]] || [[ $cxname = CX_$3* ]]; then
      names[$cxname]=1
   fi
done < /tmp/endp.$$

if [ ${#names[@]} -lt 1 ]; then
   echo "No connections start with $3"
   exit 1
fi

echo "Creating group $2"
./lf_firemod.pl --mgr $1 --quiet 1 --cmd "add_group '$2'"


for n in ${!names[@]}; do
   echo "adding connection $n to '$2'"
   ./lf_firemod.pl --mgr $1 --quiet 1 --cmd "add_tgcx '$2' '$n'"
done


