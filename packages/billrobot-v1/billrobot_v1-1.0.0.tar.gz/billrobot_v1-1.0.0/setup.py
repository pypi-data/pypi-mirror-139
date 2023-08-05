#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: botmain.py
# Author: Bill Ma
# Mail: maboning237103015@163.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup,find_packages

setup(
    name = "billrobot_v1",
    version = "1.0.0",
    keywords = ("pip", "robots","billma", "direct", "1.0.0","shat"),
    description = "A Python robot that you can use it directly",
    long_description = "A Python robot that you can use it directly",
    license = "MIT Licence",
    url = "https://github.com/billma007/billrobot_v1",
    author = "BillMa",
    author_email = "maboning237103015@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pytz","requires","datetime"]
)