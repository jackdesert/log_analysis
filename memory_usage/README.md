Memory Usage Report
===================


Full Report (Includes rsync from server)
----------------------------------------


If called with "staging" as the first argument, data is pulled from staging server.
Otherwise data is pulled from production.

    ./run.sh [staging]



Fast Version (Recent Data only, No Rsync)
-----------------------------------------

This assumes that you have already downloaded the log file via `./run.sh`

    ./fast.sh
