#!/usr/bin/env bash
set -ev
echo "Building version $(python setup.py --version)"

python setup.py sdist bdist_wheel
ls -a
echo "Building Done"

echo "... Testing sdist package ..."

pip install dist/gs_api_client-$(python setup.py --version).tar.gz

echo "... Testing sdist package done ..."