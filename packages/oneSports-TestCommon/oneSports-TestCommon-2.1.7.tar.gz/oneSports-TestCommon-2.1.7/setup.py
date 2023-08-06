#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="oneSports-TestCommon",  # 这里是pip项目发布的名称
    version="2.1.7",  # 版本号，数值大的会优先被pip
    keywords=["pip", "TestCommon", "oneSports"],
    description="An auto test common module",
    long_description="An auto test common module",
    license="MIT Licence",

    url="http://gitlab.onesport.com.cn/auto_test/common.git",  # 项目相关文件地址，一般是github
    author="zsy",
    author_email="501971693@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["cryptography", "pycryptodome", "psycopg2-binary", "paramiko"]  # 这个项目需要的第三方库
)
