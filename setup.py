#!/usr/bin/env python
# coding=utf-8

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import multiprocessing
except:
    pass

APP_NAME = 'checkmyreqs'
VERSION = '0.1.2'

# Grab requirments.
with open('requirements.txt') as f:
    required = f.readlines()

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

# Build Helper.
if sys.argv[-1] == 'build':
    try:
        import py2exe
    except ImportError:
        print('py2exe is required to continue.')
        sys.exit(1)

    sys.argv.append('py2exe')

    settings.update(
        zipfile = None,
        options = {
            'py2exe': {
                'compressed': 1,
                'optimize': 0,
                'bundle_files': 1}})

settings.update(
    name=APP_NAME,
    version=VERSION,
    author='Dustin Collins',
    author_email='dustinrcollins@gmail.com',
    packages=['tests'],
    scripts=['checkmyreqs.py'],
    url='https://github.com/dustinmm80/checkmyreqs',
    license='LICENSE.txt',
    description='Check your project requirements for Python version compatibility',
    long_description=open('README.rst').read(),
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'checkmyreqs = checkmyreqs:main',
        ],
    }
)

setup(**settings)
