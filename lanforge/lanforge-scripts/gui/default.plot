set term pngcairo size 1280,768
set output "plot.png"
set datafile separator "\t"
set ylabel "Data"
set xlabel "Test#"
#set xdata time
set grid
#set key outside
set key off
plot filename using 1:2 with lines

