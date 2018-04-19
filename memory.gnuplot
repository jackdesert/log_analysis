# Source: http://blog.mague.com/?p=201
#set datafile separator ","
set terminal png size 12000,600
set title "Memory"
set ylabel "MB (Two processes)"
set xlabel "month/day"
set xdata time

# Actual format of incoming data
set timefmt "%Y-%m-%dT%H:%M:%S"

# Display of labels on x-axis
set format x "%m/%d %H:%M"
set key left top
set grid
set xtics "2018-04-05", 6*3600
plot "formatted.log" using 1:2 with lines lw 2 lt 3 title 'hosta'
