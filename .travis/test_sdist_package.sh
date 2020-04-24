#!/usr/bin/env bash
set -ev

echo "... Testing sdist package ..."
cd dist
ls -a
pip install ./gs_api_client-$(python setup.py --version).tar.gz

echo "... Testing sdist package done ..."
