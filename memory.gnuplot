# Source: http://blog.mague.com/?p=201
#set datafile separator ","
set terminal png size 1200,600
set title "Memory"
set ylabel "MB (Two processes)"
set xlabel "month/day"
set xdata time

# Actual format of incoming data
set timefmt "%Y-%m-%dT%H:%M:%S"

# Display of labels on x-axis
set format x "%m/%d"
set key left top
set grid
plot "formatted.log2" using 1:2 with lines lw 2 lt 3 title 'hosta'
