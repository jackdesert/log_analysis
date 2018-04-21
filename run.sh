#! /bin/bash

subdomain=bip
environment=production

if [ $1 = 'staging' ]; then
  subdomain=staging
  environment=staging
fi




raw=$environment.log
formatted=formatted.log
gnuplot_file=plot_memory_usage.gnuplot
output=memory_usage.png


echo Pulling File from $environment
rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
  ubuntu@$subdomain.elitecare.com:/opt/elitecarerails/log/$environment.log $raw

echo Generating formatted file: $formatted
cat $raw | awk '{ print $1, $8 }' | grep memory > $formatted

echo Calling rpl to remove 'memory'
rpl ' memory:' ' ' $formatted
echo ''

echo Generating PNG: $output
/usr/bin/gnuplot < $gnuplot_file > $output
echo ''
