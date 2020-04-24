#!/usr/bin/env bash

echo "... Testing sdist package ..."

pip install dist/gs_api_client-$(python setup.py --version).tar.gz

echo "... Testing sdist package done ..."
