#!/usr/bin/env bash
set -ev
echo "Running unittests"

python -m venv .venv
source .venv/bin/activate
python -m pip install -r dev-requirements.txt
pytest

echo "Running unittests Done"

