#! /usr/bin/env python
# coding=utf-8

"""
CheckMyReqs

Uses xmlrpc pypi methods as defined here: http://wiki.python.org/moin/PyPIXmlRpc
"""

from __future__ import print_function

import argparse
import os
import sys

try:
    # Different location in Python 3
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

from colorama import init as colorama_init, Fore

colorama_init()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT = ServerProxy('http://pypi.python.org/pypi')

IGNORED_PREFIXES = [
    '#', 'git+', 'hg+', 'svn+', 'bzr+', '\n', '\r\n'
]

def reset_styles():
    """
    Reset the foreground styles of the console text
    """
    try:
        print(Fore.RESET, end='')
    except:
        pass


def parse_requirements_file(req_file):
    """
    Parse a requirements file, returning packages with versions in a dictionary
    :param req_file: requirements file to parse

    :return dict of package names and versions
    """
    print(''.join([
        Fore.CYAN,
        req_file.name,
        '\r\n',
        '----------------------------------------------------------'
    ])
    )

    reset_styles()

    packages = {}

    for line in req_file:
        line = line.strip()
        for prefix in IGNORED_PREFIXES:
            if not line or line.startswith(prefix):
                line = None
                break
        if line:
            line = line.strip()

            if '==' in line:
                package_name, version = line.split('==')
            else:
                package_name, version = (line, '')

            packages[package_name] = version

    return packages


def check_packages(packages, python_version):
    """
    Check the packages from the requirements file against pypi.python.org
    :param packages: dict of packages names and versions
    :param python_version: version of python to check packages against
    """
    for package_name, version in packages.items():
        check_package(package_name, version, python_version)


def check_package(package_name, package_version, python_version):
    """
    Checks a package for compatibility with the given Python version
    Prints warning line if the package is not supported for the given Python version
    If upgrading the package will allow compatibility, the version to upgrade is printed
    If the package is not listed on pypi.python.org, error line is printed

    :param package_name: name of the package to check
    :param package_version: version of the package to check
    :param python_version: version of Python to check compatibility for
    """
    package_info = CLIENT.release_data(package_name, package_version)
    package_releases = CLIENT.package_releases(package_name)

    if package_releases:
        supported_pythons = get_supported_pythons(package_info)

        if python_version not in supported_pythons:
            print(
                '{0.YELLOW}{1} {2} is not listed as compatible with Python {3}{0.RESET}'.format(
                    Fore, package_name, package_version, python_version
                )
            )
            latest_version = package_releases[0]
            latest_package_info = CLIENT.release_data(package_name, latest_version)
            latest_supported_pythons = get_supported_pythons(latest_package_info)
            if python_version in latest_supported_pythons:
                print(
                    '{0.GREEN}upgrade to {1} {2} for Python {3} support{0.RESET}'.format(
                        Fore, package_name, latest_version, python_version
                    )
                )
    else:
        print('{0.RED}{1} is not listed on pypi.python.org{0.RESET}'.format(Fore, package_name))


def get_supported_pythons(package_info):
    """
    Returns a list of supported python versions for a specific package version
    :param package_info: package info dictionary, retrieved from pypi.python.org
    :return: Versions of Python supported, may be empty
    """
    versions = []
    classifiers = package_info.get('classifiers')

    for c in classifiers:
        if c.startswith('Programming Language :: Python ::'):
            version = c.split(' ')[-1].strip()
            versions.append(version)

    return versions


def main():
    """
    Parses user input for requirements files and python version to check compatibility for
    :return:
    """
    parser = argparse.ArgumentParser('Checks a requirements file for Python version compatibility')

    parser.add_argument(
        '-f', '--files', default='requirements.txt', required=False,
        help='requirements file(s) to check',
        type=argparse.FileType('r'), nargs="+"
    )
    parser.add_argument(
        '-p', '--python', required=False,
        help='Version of Python to check against. E.g. 2.5',
        default='.'.join(map(str, sys.version_info))
    )

    args = parser.parse_args()

    for filepath in args.files:
        packages = parse_requirements_file(filepath)
        check_packages(packages, args.python)
        print('\n')

    reset_styles()


if __name__ == '__main__':
    main()
