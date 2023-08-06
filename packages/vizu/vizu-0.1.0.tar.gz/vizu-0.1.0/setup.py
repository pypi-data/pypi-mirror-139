#!/usr/bin/env python

from setuptools import setup
import pathlib
import os

HERE = pathlib.Path(__file__).parent

setup(
    name='vizu',
    version=os.getenv("VERSION_TAG", "v0.0.2").lstrip("v"),
    description='Visualization of data files',
    author='Jesper Halkjær Jensen',
    author_email='mail@jeshj.com',
    #url='https://www.python.org/sigs/distutils-sig/',
    packages=['vizer', 'vizer.assets'],
    entry_points={
        'console_scripts': [
            'vizu = vizer.main:run',
        ],
    },
    license="MIT",
    python_requires='>=3.6',
    install_requires=[
        "flask==2.0.3"
        "pandas==1.4.1"
        "scipy==1.8.0"
        "dash==2.2.0"
        "dash-extensions==0.0.71"
        "dash-bootstrap-components==1.0.3"
        "dash-table==5.0.0"
    ]
)
