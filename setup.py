#!/usr/bin/env python3

'''
setup.py

Setup configuration file for the pylaunch package.

Date: 05/19/2018
'''

import os
from setuptools import setup, find_packages


_DESCRIPTION = 'A simple package which provides helpful classes and' \
        ' functions for writing API wrappers in python.'


def _readme():
    readme_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(readme_dir, 'README.md')) as readme:
        return readme.read()

setup(
    name='pastebin-api',
    version='0.0',
    description=_DESCRIPTION,
    long_description=_readme(),
    author='moge233',
    license='GNU',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
