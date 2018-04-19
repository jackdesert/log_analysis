#set datafile separator " memory:"
set terminal png size 1200,600
set title "Memory"
set ylabel "MB"
set xlabel "Time"
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set format x "%H:%M:%S"
set key left top
set grid
plot "formatted.log" using 1:2 with lines lw 2 lt 3 title 'hosta'
