#!/usr/bin/env bash

echo "Testing sdist wheel package $(python setup.py --version)"

pip install dist/gs_api_client-$(python setup.py --version)-py3-none-any.whl

echo "Testing sdist wheel package done"
