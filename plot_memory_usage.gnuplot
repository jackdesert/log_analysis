# Plot memory consumption from production rails process
#
# Source: http://blog.mague.com/?p=201
#set datafile separator ","
set terminal png size 6000,400
set title "Memory Usage of Puma Worker Processes"
set ylabel "Memory (MB) for each process"
set xlabel "month/day"
set xdata time

# Actual format of incoming data
set timefmt "%Y-%m-%dT%H:%M:%S"

# Display of labels on x-axis
set format x "%m/%d %H:%M"

set key left top
set grid
set xtics "2018-04-05", 6*3600


# https://stackoverflow.com/questions/16736861/pointtype-command-for-gnuplot
# "with points pointtype 5" sets the point style

plot "formatted.log" using 1:2 with points pointtype 5  title 'production'
