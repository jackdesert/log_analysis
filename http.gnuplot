set datafile separator ","
set terminal png size 900,400
set title "Memory"
set ylabel "MB"
set xlabel "Time"
set xdata time
set timefmt "%s"
set format x "%m/%d"
set key left top
set grid
plot "httpa.reqs" using 1:2 with lines lw 2 lt 3 title 'hosta'
