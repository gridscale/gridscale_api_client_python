#!/usr/bin/env bash

echo "Building version $(python setup.py --version)"

pip install dist/gs_api_client-$(python setup.py --version).tar.gz

echo "Building Done"
