#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
from setuptools import setup, find_packages


def get_requirements():
    requirements_txt = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
    with open(requirements_txt) as fd:
        return fd.read().splitlines()

setup(
    name='selinon_worker',
    version='0.1',
    packages=find_packages(),
    package_data={
        'myapp': [
            os.path.join('config', '*.yaml'),
            os.path.join('config', '*.yml'),
            os.path.join('config', 'flows', '*.yaml'),
            os.path.join('config', 'flows', '*.yml')
        ]
    },
    scripts=[],
    install_requires=get_requirements(),
    include_package_data=True,
    author='Fridolin Pokorny',
    author_email='fridolin.pokorny@gmail.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin.pokorny@gmail.com',
    description='Selinon demo example worker application',
    license='MIT',
    keywords='selinon celery',
    url='https://github.com/selinon/demo',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
    ]
)
