#!/usr/bin/env python3
# coding=UTF-8

import setuptools

from rains import __version__


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(

    name='rains', 
    version=__version__, 
    author='7cat', 
    author_email='quinn.7@foxmail.com', 
    description='NULL', 
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
            'rains_test = rains.console_rains:main'
        ],
    },
)
