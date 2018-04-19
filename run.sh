#! /bin/bash

raw=production.log
formatted=formatted.log
gnuplot_file=plot_memory_usage.gnuplot
output=memory_usage.png

echo Pulling File from Production
rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
  ubuntu@bip.elitecare.com:/opt/elitecarerails/log/production.log $raw

echo Generating formatted file: $formatted
cat $raw | awk '{ print $1, $8 }' | grep memory > $formatted

echo Calling rpl to remove 'memory'
rpl ' memory:' ' ' $formatted
echo ''

echo Generating PNG: $output
/usr/bin/gnuplot < $gnuplot_file > $output
echo ''
