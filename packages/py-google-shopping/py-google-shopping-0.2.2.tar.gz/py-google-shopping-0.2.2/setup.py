# Copyright (c) 2021 Moat Systems Limited
#
# This software is released under the MIT License.
# https://moatsystems.com/mit/
#
# Author: Moat Systems Limited <hi@moatsystems.com>
# Description: Python client for Google Shopping API

import sys
from setuptools import setup, find_packages
from distutils.core import Extension

version = '0.2.2'

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

macros = []
if sys.platform.startswith('freebsd') or sys.platform == 'darwin':
    macros.append(('PLATFORM_BSD', '1'))
elif 'linux' in sys.platform:
    macros.append(('_GNU_SOURCE', ''))

setup(
    name='py-google-shopping',
    version='0.2.2',
    packages=['py_google_shopping'],
    license='MIT',
    author='Moat Systems Limited',
    author_email='hi@moatsystems.com',
    url='https://moatsystems.com',
    description='Python client for Google Shopping API',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='google shopping content api merchant product python',
    install_requires=['requests'],
    tests_require=['mock'],
)
