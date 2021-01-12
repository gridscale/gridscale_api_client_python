#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gs_api_client',
    version='1.1.4',
    description='Official Python idiomatic client for gridscale services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gridscale/gridscale_api_client_python',
    author='Thomas Wiebe',
    author_email='thomas@gridscale.io',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='API Client',
    package_dir={},
    packages=find_packages(exclude=['dist', 'examples']),
    install_requires=[
        "urllib3 >= 1.15",
        "six >= 1.10",
        "certifi",
        "python-dateutil",
    ],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
    scripts=[]
)
