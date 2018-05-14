Histogram
=========


Prerequisites
-------------

python3.6 is required because this program uses f-strings (formatted string literals)


### Installing Python 3.6 From Source

On one installation, python3.6 would not run pip, so I ended up installing from source.

    sudo apt-get install libbz2-dev

    wget /path/to/source
    cd <dir>
    ./configure
    make
    make test
    sudo make install

    python3.6 -m pip install --user numpy pandas matplotlib


### Installing Python 3.6 Using PPA

This link shows how to install python3.6 on Ubuntu 16.04
source: https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get

    # Use the DeadSnakes ppa!
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.6

    python3.6 -m pip install --user numpy pandas matplotlib

source: https://github.com/pypa/pip/issues/4220#issuecomment-271132971


Generate Report
---------------

    python3.6 histogram <processed_log> <output_dir>
