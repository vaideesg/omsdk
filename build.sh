#!/bin/sh
rm -fr build dist omsdk.egg-info
cp setup-linux.py setup.py
python setup.py sdist --formats=gztar
