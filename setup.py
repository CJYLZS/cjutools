#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: cjylzs(691086891@qq.com)
# Description: utils and cmd framework

from setuptools import setup, find_packages

setup(
    name='cjutools',
    version='0.0.3',
    keywords='cjutools',
    description='tools depend cjutils',
    license='MIT License',
    url='https://github.com/CJYLZS/cjtools.git',
    author='cjylzs',
    author_email='691086891@qq.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['cjutils>=0.0.10']
)
