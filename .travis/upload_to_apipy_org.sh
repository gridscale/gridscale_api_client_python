#!/usr/bin/env bash
set -ev

echo "Uploading package to pypi.org"
ls -l
#pip install twine
#twine upload -u __token__ -p "$PYPI_ORG_TOKEN" dist/gs_api_client-*

echo "Upload Done"
