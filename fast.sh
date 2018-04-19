#! /bin/bash

gnuplot_file=memory.gnuplot
output=pretty.png

echo Generating PNG: $output
/usr/bin/gnuplot < $gnuplot_file > $output
echo ''
