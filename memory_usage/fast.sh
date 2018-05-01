#! /bin/bash

formatted=../shared_log_files/formatted_for_memory_usage_report.log
recent_formatted=../shared_log_files/recent_formatted_for_memory_usage.log
gnuplot_file=memory_usage.gnuplot
output=/tmp/memory_usage.png


echo Making Short version of file
tail -n 1000000 $formatted > $recent_formatted
mv $recent_formatted $formatted


echo Generating PNG: $output
/usr/bin/gnuplot < $gnuplot_file > $output
echo ''
