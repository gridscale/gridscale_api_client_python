#!/usr/bin/env bash
set -ev
echo "Checking release version $(python setup.py --version)"

#if git tag | grep -qE "^v$(python setup.py --version)$"; then echo "Release already exists"; exit 1; fi
if ! grep -q "v$(python setup.py --version)" CHANGELOG.md; then echo "Version missing in CHANGELOG.md"; exit 1; fi

echo "Checking Done"
