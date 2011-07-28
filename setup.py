#!/usr/bin/env python

from setuptools import setup

setup(
    name='ogrkit',
    version='0.0.1',
    description='A suite of command-line utilities implementing basic geometric operations. ',
    long_description=open('README.rst').read(),
    author='Christopher Groskopf',
    author_email='staringmonkey@gmail.com',
    url='http://blog.apps.chicagotribune.com/',
    license='MIT',
    packages=[
        'ogrkit',
        'ogrkit.utilities'
    ],
    scripts = [
        'ogrdifference',
    ],
    install_requires = [
        'GDAL==1.6.0']
)
