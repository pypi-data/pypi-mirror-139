#!/usr/bin/env python3
# coding=UTF-8

import setuptools

from rains import __name__
from rains import __version__
from rains import __author__
from rains import __email__
from rains import __description__
from rains import __url__


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(

    name=__name__, 
    version=__version__, 
    author=__author__, 
    author_email=__email__, 
    description=__description__, 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url=__url__, 
    keywords=['rains', 'test', 'web', 'api'],
    packages=setuptools.find_packages(), 

    install_requires=[
        'Selenium == 3.14.1', 
        'requests', 
        'flask', 
    ], 

    classifiers=[
        'Programming Language :: Python :: 3', 
    ],

    # 打包文件
    data_files=[],

    # 安装执行脚本
    scripts=[],

    # 命令行工具
    entry_points={
        'console_scripts':[
            'rains = rains.console_rains:main',
        ],
    },
)
