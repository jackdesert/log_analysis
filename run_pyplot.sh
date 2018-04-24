#! /bin/bash

subdomain=bip
environment=production

if [ $1 = 'staging' ]; then
  subdomain=staging
  environment=staging
fi




raw=$environment.log
kept=kept.log
output=stats.dataframe


echo Pulling File from $environment
rsync -av -e "ssh -i ~/.ssh/bip-a.pem" \
  ubuntu@$subdomain.elitecare.com:/opt/elitecarerails/log/$environment.log $raw

echo Keeping lines with new "to" key
cat $raw | grep method: | grep path: | grep status: | grep duration: | grep to:  > $kept


echo Running Python Stats

python3 pyplot.py

cat $output

