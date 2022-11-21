#!/bin/bash
tagname=
if [[ x$1 == x ]]; then
   echo "$0: want a tagname, bye"
   exit 1
else
   tagname="$1"
fi

if [[ x$2 == x ]]; then
   echo "No lower duration, when do you want to collect from? Use 'yyyy-mm-dd ii:mm'"
   exit 1
fi

conf="sensorplot.${tagname}.conf"
data="sensordata.${tagname}.data"
ceesv="sensordata.${tagname}.csv"
peeng="sensordata.${tagname}.png"

[ -f $conf ] && rm -f $conf
[ -f $data ] && rm -f $data
[ -f $ceesv ] && rm -f $ceesv
[ -f $peeng ] && rm -f $peeng

#journalctl -t "$tagname" --since "$2" | head

journalctl -t "$tagname" --output short-unix --since "$2" > "$data"

if [ ! -s $data ]; then
   echo "Unable to collect data"
   exit 1
fi

perl -n \
   -e 'next if(/mt/); if (/^(\d+)\.[^:]+: ([0-9.]+), ([0-9.]+), ([0-9.]+)/) { print "$1 $2 $3 $4\n"}' \
   < $data \
   | tee $ceesv \
   | tail -1

if [ ! -s $ceesv ]; then
   echo "Unable to produce data"
   exit 1
fi

#echo "journalctl -t $Q$tagname$Q --output short-unix --since $Q$2$Q"
#while IFS= read -r line; do
#   hunks=($line)
#   echo -n ${hunks[0]}
#   date +' %Y-%m-%d %H:%M' --date @${hunks[0]}
#done < $ceesv | head

# create gnuplot config file
BS='\'
cat > ${conf} <<EOF
set title               "${tagname}: TX 100Mbps multi 10 from $2"
set output              "${peeng}"
set term                png
set datafile separator  " "
set xlabel              "Time"
set timefmt             "%s"
set format x            "%H:%M"
set xdata               time
set ylabel              "DegC"
set grid
set key                 left

plot \
  "${ceesv}" using 1:3 title "coretemp", $BS
  "${ceesv}" using 1:2 title "mtk 1", $BS
  "${ceesv}" using 1:4 title "mtk 2"
EOF

if [ ! -s $conf ]; then
   echo "BAD CONF FILE $conf"
   exit 1
fi
if [ ! -s $ceesv ]; then
   echo "BAD CSV FILE $ceesv"
   exit 1
fi

echo -n "creating [$peeng] using (gnuplot -c $conf $ceesv)"
gnuplot -c $conf $ceesv
echo " created $peeng"

#
