
# Orders Script

This is a script to streamline a PDF of medication orders down to one-liners.

## Setup

Currently, this is run as a [python](https://www.python.org/) script. To use:

- Install a recent version of python (developed with 3.10)
- Download this repository (including orders.py and pyproject.toml)
- From the commandline, install dependencies with: `pip install .`

## Running

To run the script and output to the commandline, use `python orders.py PDF_NAME`

To output to file, instead use `python orders.py PDF_NAME > OUTPUT.txt`
