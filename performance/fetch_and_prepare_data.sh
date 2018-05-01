#! /bin/bash

subdomain=bip
environment=production


rsync_required=true
grepped=../shared_log_files/grepped_for_performance_report.log

if [ $1 = '--staging' ]; then
  subdomain=staging
  environment=staging
elif [ $1 ]; then

  echo Using passed-in file: $1
  raw=$1
  unset rsync_required
fi




if [ $rsync_required ]; then
  raw=../shared_log_files/$environment.log

  echo Pulling File from $environment
  rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
    ubuntu@$subdomain.elitecare.com:/opt/elitecarerails/log/$environment.log $raw
fi


echo Generating grepped file
# Make sure it has the new "to" key
# Skip lines with an "error" key (They have since been blocked via lograge)
# because the error has spaces in it, which throws off our space-delimited parsing
cat $raw | grep to: | grep -v error: > $grepped

echo Data is ready in $grepped

