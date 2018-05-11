Histogram
=========


Prerequisites
-------------

python3.6 is required because this program uses f-strings (formatted string literals)


### Installing Python 3.6

This link shows how to install python3.6 on Ubuntu 16.04
source: https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get

    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6

### Installing Modules

If python3.6 was already installed on your system, you can

    sudo apt-install python3-pip
    pip3 install --user numpy pandas matplotlib

If you installed python3.6 using the above-mentioned PPA,
you will need to invoke pip like this:

    python3.6 -m pip install numpy pandas matplotlib

source: https://github.com/pypa/pip/issues/4220#issuecomment-271132971


Generate Report
---------------

    python3.6 histogram <processed_log> <output_dir>
