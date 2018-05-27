Log Analysis
============

A generic toolset for analyzing performance bottlenecks by ingesting
your well-formatted log files.


Prerequisites
-------------

python3.6 is required because this program uses f-strings (formatted string literals)

    # If supported by your distribution
    sudo apt install python3.6

Modules:

    python3.6 -m pip install numpy pandas matplotlib



Expected Log Format
-------------------

Your logs must be in the following format:

    <timestamp> <key1>:<value1> <key2>:<value2> <key3>:<value3>

Example:

    2018-05-27T08:12:35 duration:5 to:dashboard#alerts.html pid:5046 memory:670

Required keys in log:

    * timestamp (string, must have no spaces, and must be first)
    * duration (integer, how many milliseconds required to respond to request)
    * memory (integer that means number of megabytes your webserver was using at the end of the request)
    * to (string, which endpoint was accessed)
    * pid (integer, posix PID of process used to field request)

Additional key:value pairs are permitted and will be ignored




Histogram and Duration Scatter
==============================

For each endpoint in your log file, generate a
histogram (shows when traffic is highest)
and a duration scatter (shows each request and how long it took,
so you get a sense of which requests are outliers)


![Histogram]( https://github.com/jackdesert/log_analysis/blob/master/example_plots/alerts-index.json--max-224__primary.png )
![Duration Scatter]( https://github.com/jackdesert/log_analysis/blob/master/example_plots/alerts-index.json__duration-scatter.png )

### Invocation

    python3.6 histogram.py        <log_file> <output_directory>
    python3.6 duration_scatter.py <log_file> <output_directory>


### Example

    mkdir -p /tmp/plots
    python3.6 traffic_histograms.py     example_logs/example.log /tmp/plots
    python3.6 duration_scatter_plots.py example_logs/example.log /tmp/plots

    # View plots
    firefox /tmp/plots


### Naming Convention

Note the naming convention of a pair of plots for a single endpoint:

  * alerts-index.json--max-224__primary.png
  * alerts-index.json__duration-scatter.png

They both start with the name of the endpoint

They both end with a type designation (__primary.png or __duration_scatter.png)

The one marked "primary" also contains a numerical value (224 in this case)
denoting the max value in the plot. This is helpful for displaying all the plots together on a page, sorted by the max amount of traffic received.


Performance Report
==================

Generates a report of your slowest and most trafficked endpoints

Shows a "Top Ten" offenders for each of the following categories:

  * Median duration (aka median response time)
  * 90th percentile duration
  * Total duration
  * Hits
  * Mean memory growth (How much does the resident memory size grow from this endpoint)
  * Total memory growth (total memory growth due to this endpoint)

### Invocation

    python3.6 performance_report.py example_logs/example.log > /tmp/performance.txt

    # View report in browser
    firefox /tmp/performance.txt


### Example

Here's the performance report generated from example.log: [performance.txt](https://raw.githubusercontent.com/jackdesert/log_analysis/master/example_reports/performance.txt)

