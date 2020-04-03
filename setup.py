#!/usr/bin/python3

from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()

setup(
    name='whatdo',
    version='0.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
