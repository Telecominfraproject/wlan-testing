set term pngcairo size 150,100
set output "plot.png"
set datafile separator "\t"
#set ylabel "Data"
#set xlabel "Test#"
set ylabel
set xlabel
#set xdata time
#set grid
#set key outside
set key off
unset xtics
unset ytics
unset border
set title
plot filename using 1:2 with lines

