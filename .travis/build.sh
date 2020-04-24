#!/usr/bin/env bash
set -ev
echo "Building version $(python setup.py --version)"

python setup.py sdist bdist_wheel
ls -a
echo "Building Done"
