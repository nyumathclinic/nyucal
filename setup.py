#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'lxml',
    'requests>=2.18.1'
]

setup_requirements = [
    'pytest-runner',
    # TODO(leingang): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='nyucal',
    version='0.1.0',
    description="Nyucal is for parsing the NYU Academic Calendar webpage into machine readable calendar formats",
    long_description=readme + '\n\n' + history,
    author="Matthew Leingang",
    author_email='leingang@nyu.edu',
    url='https://github.com/leingang/nyucal',
    packages=find_packages(include=['nyucal']),
    entry_points={
        'console_scripts': [
            'nyucal=nyucal.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='nyucal',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
