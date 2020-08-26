#!/usr/bin/env bash
set -ev

echo "Uploading package to pypi.org"
ls -l

python setup.py sdist bdist_wheel
pip install twine
twine upload -u __token__ -p "$PYPI_ORG_TOKEN" dist/gs_api_client-*

echo "Upload Done"
