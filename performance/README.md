Generate a Performance Report
=============================


Fetch Data from Server
----------------------
If first argument is "staging", it pulls data from staging.
Otherwise it pulls from production.

    ./fetch_and_prepare_data.sh [--staging]


Generate Report
---------------

    python3 generate_report.py
