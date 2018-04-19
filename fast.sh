#! /bin/bash

formatted=formatted.log
recent_formatted=recent_formatted.log
gnuplot_file=memory.gnuplot
output=pretty.png

echo Making Short version of file
tail -n 1000000 $formatted > $recent_formatted
mv $recent_formatted $formatted


echo Generating PNG: $output
/usr/bin/gnuplot < $gnuplot_file > $output
echo ''
