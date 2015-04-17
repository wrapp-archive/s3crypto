#!/usr/bin/env python

from distutils.core import setup

setup(
    name='s3crypto',
    version='0.1',
    py_modules=['s3crypto'],
    install_requires=[
        "boto",
        "pynacl"
    ],
    zip_safe=False,
)
