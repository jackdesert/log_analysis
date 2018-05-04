Generate a Performance Report
=============================


Fetch Data from Server
----------------------
If first argument is "staging", it pulls data from staging.
Otherwise it pulls from production.

    # Production
    ./fetch_and_prepare_data.sh

    # Production
    ./fetch_and_prepare_data.sh --staging

    # Hand-Picked Files
    ./fetch_and_prepare_data.sh <file_1> <file_2> ... <file_n>


Generate Report
---------------

    python3 generate_report.py
