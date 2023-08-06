#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

__author__ = 'East'
__created__ = '2021/11/16 15:07'
__filename__ = 'setup.py'

setuptools.setup(
    name="dm-easy-db",  # Replace with your own username
    version="0.1.1",
    author="miaodongfang",
    author_email="miaodongfang@bluemoon.com.cn",
    description="A easy common db operation package",
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type="text/markdown",
    url="http://gitlab.admin.bluemoon.com.cn/BigData-DataAlgorithm/easy_db.git",
    packages=setuptools.find_packages(exclude=['test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
