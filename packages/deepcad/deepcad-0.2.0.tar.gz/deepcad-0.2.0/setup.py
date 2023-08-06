# -*- coding: utf-8 -*-
#############################################
# File Name: setup.py
# Author: bbnclyx
# Mail: 20185414@stu.neu.edu.cn
# Created Time:  2021-12-11
#############################################
from setuptools import setup, find_packages


setup(
    name="deepcad",
    version="0.2.0",
    description=("implemenent deepcad to denoise data by "
                 "removing independent noise"),
    author="bbnclyx and bbnclyx",
    author_email="20185414@stu.neu.edu.cn",
    url="https://github.com/cabooster/DeepCAD-RT",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=['matplotlib','pyyaml','tifffile','scikit-image','opencv-python','csbdeep','gdown==4.2.0'],
)
