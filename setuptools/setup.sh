#!/bin/bash

# create wheel package
./setup.py bdist_wheel # see setup.cfg for options

# install
./setup.py install # see setup.cfg for options

# clean
./setup.py clean # see setup.cfg for options
rm ./dist -rf
rm ./*.egg-info -rf
