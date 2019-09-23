#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wazo-router-calld',
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    description='Wazo Router Server Daemon',
    long_description=readme,
    long_description_content_type="text/markdown",
    license=license,
    url='http://www.wazo-platform.org/',
    install_requires=[
        'Click>=7.0',
        'fastapi>=0.38.0',
        'python-consul>=1.1.0',
        'psycopg2-binary>=2.8.0',
        'requests>=2.22.0',
        'SQLAlchemy>=1.3.0',
        'uvicorn>=0.9.0',
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'wazo-router-calld=wazo_router_calld.main:main',
        ],
    }
)
