#!/usr/bin/env bash
set -ev

echo "... Testing sdist package ..."

pip install $HOME/buildout-cache/gs_api_client-$(python setup.py --version).tar.gz

echo "... Testing sdist package done ..."
