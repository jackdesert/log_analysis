#! /bin/bash

subdomain=bip
environment=production


rsync_required=true
grepped=../shared_log_files/grepped_for_performance_report.log

if [ $1 = '--staging' ]; then
  subdomain=staging
  environment=staging
elif [ $1 ]; then
  raw_files=$@
  unset rsync_required
fi




if [ $rsync_required ]; then
  raw_dir=../shared_log_files/$environment
  mkdir -p $raw_dir

  echo Pulling File from $environment
  rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
    ubuntu@$subdomain.elitecare.com:/opt/elitecarerails/log/$environment.log* $raw_dir

  raw_files=$raw_dir/*
fi


echo ''
echo Using files:
for file in $raw_files
  do
    echo "  $file"
  done


echo ''
echo Generating combined, grepped file
# Make sure it has the new "to" key
# Skip lines with an "error" key (They have since been blocked via lograge)
# because the error has spaces in it, which throws off our space-delimited parsing
cat $raw_files | grep to: | grep -v error: > $grepped

line_count=`wc -l $grepped | awk '{ print $1 }'`

echo ''
echo $line_count lines written to $grepped

