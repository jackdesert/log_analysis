#! /bin/bash

$raw=raw.log
$formatted=formatted.log
$gnuplot_file=http.gnuplot
$output=pretty.png

cat $raw | awk '{ print $1, $8 }' | grep memory > $formatted


/usr/bin/gnuplot < $formatted > $output
