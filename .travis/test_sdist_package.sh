#!/usr/bin/env bash
set -ev

echo "... Testing sdist package ..."

pip install /home/travis/build/gridscale/gridscale_api_client_python/gs_api_client-$(python setup.py --version).tar.gz

echo "... Testing sdist package done ..."
