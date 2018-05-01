#! /bin/bash

subdomain=bip
environment=production

if [ $1 = 'staging' ]; then
  subdomain=staging
  environment=staging
fi




raw=../shared_log_files/$environment.log
grepped=../shared_log_files/grepped_for_performance_report.log


echo Pulling File from $environment
rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
  ubuntu@$subdomain.elitecare.com:/opt/elitecarerails/log/$environment.log $raw

echo Generating grepped file: $grepped
# Make sure it has the new "to" key
# Skip lines with an "error" key (They have since been blocked via lograge)
# because the error has spaces in it, which throws off our space-delimited parsing
cat $raw | grep to: | grep browser: | grep -v error: > $grepped

echo Data is ready in $grepped

