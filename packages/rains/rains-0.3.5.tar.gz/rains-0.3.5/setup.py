#!/usr/bin/env python3
# coding=UTF-8

import setuptools

from rains import __version__
from rains import __author__
from rains import __email__


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(

    name='rains', 
    version=__version__, 
    author=__author__, 
    author_email=__email__, 
    description='这是一个开箱即用、稳定且高效的工程化全栈自动化测试框架。', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://gitee.com/catcat7/rains', 
    packages=setuptools.find_packages(), 

    install_requires=[
        'Selenium == 3.14.1', 
        'requests', 
        'flask', 
    ], 

    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent', 
    ],

    entry_points={
        'console_scripts':[
            'rains = rains.console_rains:main'
        ],
    },
)
